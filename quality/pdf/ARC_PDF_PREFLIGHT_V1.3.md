# ARC PDF PREFLIGHT V1.3
VERSION: 1.3
DATE: 2026-11-19
STATUS: ACTIVE
SUPERSEDES: archive/quality/pdf/ARC_PDF_PREFLIGHT_V1.2.md (archived)
CHANGE: 코드에 이미 있던 ARC_N 검사를 문서화하고, ARC_FINAL 검사·N° 표지 누출·양면 홀짝 보고를 추가

## PURPOSE
육안 검수 전에 PyMuPDF 기반 deterministic 1차 QC를 수행한다.
V1.2는 실제 사용자 발견 조판 결함을 직접 차단한다: CORE 2단 오염, 의미 블록 절단, 낮은 본문 가독성, heading orphan, raw markup/metadata leak, sparse carry-over.

## TOOL
`tooling/pdf_qc/pdf_preflight.py`

## REQUIRED INVOCATION
제품 모드를 전달한다.
- ARC_CORE: `--product ARC_CORE`
- ARC_N: `--product ARC_N`
- ARC_FINAL: `--product ARC_FINAL`

## COMMON CHECKS
- A4 page-size tolerance
- page boundary overflow
- configured margin 침범
- suspicious text-text bbox overlap
- image/drawing bbox outside page
- broken/replacement glyph 후보
- visible raw HTML token
- student-facing production metadata leak
- render failure
- optional pdftoppm/PyMuPDF raster export

## ARC CORE HARD CHECKS
- physical page 1 cover를 제외한 unregistered near-empty page <25% vertical content coverage = FAIL
- sparse page <45% = WARN/REFLOW
- substantial two-column body-flow signal = FAIL (CORE_TWO_COLUMN_FLOW)
- body text가 Thin/ExtraLight/Light 계열에 유의미하게 의존 = FAIL
- body average size가 print floor 아래로 내려감 = FAIL
- page bottom의 isolated large/heading-like text = FAIL/WARN
- A/B/C major part title가 본문 페이지 상단에서 시작하지 않음 = FAIL
- raw <br>/<b>/<span> 등 markup token 노출 = FAIL
- CONTENT_LOCK/BATCH_ID/SOURCE_ID/Drive 상태 같은 production metadata 노출 = FAIL

## ARC N° HARD CHECKS (code since V1.2, documented V1.3)
- `ARC_N_COVER_VERSO_NOT_BLANK`: 2쪽이 완전 백지(텍스트·이미지·그림 객체 0)가 아님
- `ARC_N_ANSWER_KEY_MISSING`: `정답`/`ANSWER KEY` 머리가 없음
- `ARC_N_SEPARATOR_NOT_BLANK`: 정답표 바로 앞 쪽이 완전 백지가 아님
- `ARC_N_QUESTION_COUNT_MISMATCH` / `ARC_N_ANSWER_COUNT_MISMATCH`: 문항 번호·정답 줄이 1~N과 다름 (`--expected-item-count`)
- `COLUMN_GUTTER_CROSSING`: 문제 쪽 본문 줄이 단 경계를 넘음 (N°·FINAL 공통)
- `ARC_N_STUDENT_TAG_LEAK` (V1.3): 문제 쪽에 `(n점)` 또는 발문 끝 `[1-5]` 난도 표지
- `ARC_N_ANSWER_KEY_ON_VERSO` (V1.3, INFO): 정답표가 짝수 물리 쪽(뒷면)에서 시작. 오프셋 규칙 변경은 사용자 결정 사항

## ARC FINAL HARD CHECKS (V1.3)
호출: `--product ARC_FINAL --expected-item-count <선택형 수> --expected-cr-count <서술형 수> --answer-key-pdf <정답지 PDF>`
- `FINAL_COVER_VERSO_NOT_BLANK`: 표지 뒤 2쪽이 완전 백지가 아님 (사용자 지시 2026-11-19: 백지 유지)
- `FINAL_ANSWER_ON_PROBLEM_SHEET`: 문제지에 정답 머리나 `번호 ①` 형태의 정답 줄. 지문 행 번호(15, 25…)는 정답 줄로 보지 않는다
- `FINAL_QUESTION_COUNT_MISMATCH`: `1.`~`N.` 번호 누락
- `FINAL_CR_COUNT_MISMATCH`: `[서술형 1]`~`[서술형 M]` 불일치
- `FINAL_POINTS_NOT_PRINTED`: `(n점)` 표기 수 < 선택형 + 서술형 수
- `FINAL_ANSWER_KEY_PDF_MISSING` / `FINAL_ANSWER_KEY_COUNT_MISMATCH` / `FINAL_ANSWER_KEY_CR_MISSING`: 별도 정답지 PDF 누락·불일치
생산 파이프라인은 위 인자를 자동으로 넘긴다.

## COLUMN DETECTION PRINCIPLE
표의 셀 여러 개를 '2단 본문'으로 오인하지 않도록:
- PDF의 visual text line을 lane 후보로 사용
- 충분한 길이/폭의 body line만 후보로 남김
- 각 lane의 반복되는 left-edge anchor를 찾아 표 내부의 여러 셀 시작점을 제거
- 좌/우 lane 각각 충분한 line 수와 문자량이 있어야 함
- 두 lane의 vertical coverage가 실제로 겹치는 경우에만 CORE_TWO_COLUMN_FLOW로 판정

## OCCUPANCY
단순 bounding box 높이가 아니라 body content의 vertical interval union을 사용한다.
footer/page number가 페이지 하단에 있다는 이유만으로 sparse page를 정상으로 오판하지 않는다.
단, 다음 페이지가 상단에서 명시적 A/B/C 대경계를 시작하고 직전 페이지 점유율이
25~45%이면 CORE_REGISTERED_BOUNDARY_REMAINDER로 등록한다. 25% 미만 near-empty는
대경계가 뒤따라도 FAIL이며 같은 파트 내부에서 재조판한다.

## TYPOGRAPHY
CORE 기본:
- Pretendard/Noto Sans KR Regular(400) 이상
- target body 9.9pt
- allowed body 9.6~10.2pt
- Light 계열 장문 사용 금지
- heading hierarchy는 rendered size/weight 차이로 확인

## SOURCE-LEVEL OVERFLOW
HTML source가 있는 Typesetter는 PDF export 전에 scrollHeight/clientHeight 검사도 수행한다.
PDF preflight는 이미 잘려 사라진 DOM content를 복원할 수 없으므로 source overflow audit와 PDF render audit를 모두 사용한다.

## RESULT
PASS: hard issue 없음
WARN: reflow 또는 육안 확인 필요
FAIL: reading/solving/brand/product-mode integrity에 영향을 주는 hard issue

## BOUNDED AUTO-FIX CONNECTION
`tooling/pdf_qc/autofix_controller.py`가 FAIL/WARN 코드를 분류한다.

- AUTO_FIX: Typesetter 소유의 allowlisted layout profile만 변경 후 재렌더·동일 preflight 재실행
- CONTENT_RETURN: 정답, 문항 수, 원문, glyph, raw markup, 학생 metadata 등 locked-content 계층으로 반환
- HOLD: 미등록 오류, 제품 규칙 누출, 2회 초과 또는 동일 fingerprint 반복

AUTO_FIX는 CORE 1단, 9.9pt/Regular, 의미 단위 reflow, heading keep,
A4/safe margin, ARC_N 필수 공백 페이지 같은 조판 상태만 복구한다.
학생 원문·문항·선지·정답은 절대 변경하지 않는다.

## LIMIT
PDF bbox 분석은 원본 DOM semantic class를 직접 알 수 없다.
heading/column detection은 conservative heuristic이며 WARN은 human visual review로 확인한다.
자동 preflight는 최종 육안 검수를 대체하지 않는다.

## RELEASE
PDF_PREFLIGHT_STATUS와 PDF_PREFLIGHT_REPORT가 없으면 FINAL_RELEASE 금지.
FAIL은 human approval로 덮을 수 없다.

END ARC PDF PREFLIGHT V1.3
