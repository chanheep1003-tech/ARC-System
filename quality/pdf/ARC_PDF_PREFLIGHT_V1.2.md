# ARC PDF PREFLIGHT V1.2
VERSION: 1.2
DATE: 2026-09-19
STATUS: ACTIVE-DEV

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
- raw <br>/<b>/<span> 등 markup token 노출 = FAIL
- CONTENT_LOCK/BATCH_ID/SOURCE_ID/Drive 상태 같은 production metadata 노출 = FAIL

## COLUMN DETECTION PRINCIPLE
표의 셀 여러 개를 '2단 본문'으로 오인하지 않도록:
- 긴 paragraph-like block만 사용
- 좌/우 lane 각각 충분한 문자량과 복수 block이 있어야 함
- 두 lane의 vertical coverage가 실제로 겹치는 경우에만 CORE_TWO_COLUMN_FLOW로 판정

## OCCUPANCY
단순 bounding box 높이가 아니라 body content의 vertical interval union을 사용한다.
footer/page number가 페이지 하단에 있다는 이유만으로 sparse page를 정상으로 오판하지 않는다.

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

## LIMIT
PDF bbox 분석은 원본 DOM semantic class를 직접 알 수 없다.
heading/column detection은 conservative heuristic이며 WARN은 human visual review로 확인한다.
자동 preflight는 최종 육안 검수를 대체하지 않는다.

## RELEASE
PDF_PREFLIGHT_STATUS와 PDF_PREFLIGHT_REPORT가 없으면 FINAL_RELEASE 금지.
FAIL은 human approval로 덮을 수 없다.

END ARC PDF PREFLIGHT V1.2
