# ARC_FINAL_QUALITY_GATE_V1.2
VERSION: 1.1
DATE: 2026-09-26
STATUS: ACTIVE
VALIDATION_MARKER: DONGBUK_MULTI_EXAM_FINAL_CALIBRATION_20260926
ROLE: ARC FINAL 전용 난이도·문항질·세트실전성 승인 게이트
ACTUAL_EXAM_CORPUS_SIZE: 16
SCHOOL_DEFAULT: 동북고등학교

## 0. PURPOSE
ARC FINAL은 단순히 ARC_N에서 어려운 문제를 모은 제품이 아니다.
실제 시험 직전 1회분 실전 세트로서 범위 충실도, 난도 곡선, 변별력, 오답 경쟁력, 시간 압박 현실성을 동시에 만족해야 한다.

FINAL은 아래 두 프로필이 모두 PASS여야 CONTENT_LOCK 가능:
- DIFFICULTY_PROFILE
- ITEM_QUALITY_PROFILE

## 1. HARD FAIL
다음 중 하나면 FINAL_RELEASE 금지:
- 정답이 유일 최장/최상세 선지인 패턴이 반복되어 길이로 답 추측 가능
- 5지선다인데 즉시 제거 가능한 선지 3개 이상인 문항이 세트에 반복
- D3+ 문항인데 strong distractor 2개 미만
- D4/D5 표방 문항이 실제로 1단계 직접확인
- 범위 밖 지식, 지엽 암기, 말장난, 조건 부족으로 어렵게 만듦
- 동일 판단축/풀이경로가 세트에서 반복되어 체감 난도만 부풀림
- 정답 단서가 stem/보기/선지 길이·문체에서 과도하게 노출
- 자료가 장식이고 정답 결정에 쓰이지 않음
- SCHOOL_RELATIVE=BELOW_SCHOOL 문항이 이유 없이 포함
- 학교자료/교과서 근거 추적 불가
- ANSWER_KEY 불완전, 복수정답, 근거 오류
- 시간 소모가 추론이 아니라 불필요한 독해/계산노동에서 발생

## 2. DIFFICULTY PROFILE — SUBJECT SCHOOL ANCHOR

ARC FINAL에는 전 과목 공통 고정 난도곡선을 강제하지 않는다. (V1.2: 아래 §11의 두 판 가운데 학교 수준(STANDARD)이 이 절의 기준이다.)

기본 원칙:
FINAL = 실제 동북고 해당 과목 시험 난도대의 모의고사

실제 기출 코퍼스:
quality/anchors/DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0.yaml

과목별 ACTIVE anchor:
- KOR → KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0
- SOC → SOC_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0
- SCI → SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0 (2026-2 기말 A~D 범위. 산화·환원 전용 anchor는 중간고사 범위용)
- SCI-REDOX → SCI_REDOX_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0 (산화·환원 범위 FINAL에만)
- ENG → ENG_DONGBUK_POINTS_PROXY_DIFFICULTY_ANCHOR_V1.0 (잠정, 신뢰도 LOW — §14)
- HIS → 현재 FINAL 비활성

FINAL은 다음 네 값이 subject anchor tolerance 내에 있어야 한다.
- D1+D2 share
- D3 share
- D4+D5 share
- mean difficulty level

추가:
- 후반부 변별 문항 수가 anchor 최소값 이상
- LONG 문항이 3개 이상 연속하지 않음
- 고난도가 단순 장문노동/계산노동/범위 밖 지식에서 발생하지 않음

SCHOOL_MULTI_EXAM_ANCHOR 모드에서 anchor가 없으면
FINAL_SCHOOL_ANCHOR_MISSING = HARD FAIL.

### 2A. KOR TARGET
center:
- D1+D2 ≈ 0.343
- D3 ≈ 0.400
- D4+D5 ≈ 0.257
- mean ≈ 2.89

허용 tolerance는 anchor 파일을 따른다.
이는 2025-2 중간/기말 + 2026-1 중간/기말 실제 4회 시험을 앙상블한 값이다.

### 2B. SOC TARGET
center:
- D1+D2 ≈ 0.310
- D3 ≈ 0.472
- D4+D5 ≈ 0.218
- mean ≈ 2.87

사회는 '있는 대로 고르기', 사상가/원칙 비교, 지도·통계·그래프 적용이 SCHOOL_STANDARD 층에도 자주 포함된다.
D4 비율만 기계적으로 늘리지 않는다.

### 2C. SCI-REDOX TARGET
center:
- D1+D2 ≈ 0.301
- D3 ≈ 0.391
- D4+D5 ≈ 0.308
- mean ≈ 2.97

가장 높은 관련성:
2025-2 통합과학2 중간고사 산화·환원 실제 8~12번.

직접 범위 문항군의 구조 난도:
- Q8 D3
- Q9 D2
- Q10 D4
- Q11 D3
- Q12 D4

이 5문항은 current scope direct anchor이므로 65% 가중.
동북고 통합과학 4회 전체 난도 코퍼스를 35% 혼합해 소표본 과적합을 줄인다.

### 2D. CALIBRATION BEHAVIOR
학교보다 쉬우면:
- 빈출 학교형 문제에서 distractor와 reasoning depth를 강화
- 기본문항을 모두 제거하지 않음
- 범위 밖 개념으로 올리지 않음

학교보다 어려우면:
- 낯선 형식/과도한 조건/자료량을 줄임
- strong distractor는 유지
- 학교 실제 난도대로 되돌림

FINAL은 더 어려울수록 좋은 제품이 아니다.
실제 시험과 비슷한 난도 곡선이어야 좋은 FINAL이다.

## 3. ITEM QUALITY PROFILE
각 문항 최소 기록:
ITEM_ID
ACTUAL_DIFFICULTY
REASONING_STEPS
STRONG_DISTRACTOR_COUNT
EFFECTIVE_CHOICE_COUNT
FIRST_PASS_PLAUSIBLE_CANDIDATES
SECOND_BEST_OPTION
SECOND_BEST_REFUTATION
IMMEDIATE_ELIMINATION_COUNT
CORRECT_IS_LONGEST
LONGEST_TO_MEDIAN_RATIO
CORRECT_DETAIL_OUTLIER
ANSWER_EVIDENCE
SCOPE_TRACE
EXPECTED_TIME_CLASS

FINAL 문항 합격:
- D3+: strong distractor >=2
- D3+: plausible candidates >=3
- D4/D5: effective choices >=4
- second-best가 실제로 매력적이지만 한 근거로 명확히 탈락
- 길이/문체/절대어가 정답 단서가 아님
- 실제 사고단계가 난도표기와 일치

## 4. ANSWER-LENGTH SET AUDIT
ITEM_COUNT >= 10:
- LONGEST_OPTION_IS_KEY_RATE <= 0.30 권장
- 0.30 초과: REVISE
- 0.40 초과: FAIL

추가:
- 정답 선지 평균 길이가 오답 선지 평균보다 일관되게 길면 재작성
- 특정 정답번호 위치에서 유독 긴 선지가 반복되면 POSITION_LENGTH_BIAS
- 정답만 교과서형 완결설명이고 오답은 짧은 파편이면 FAIL

## 5. DISTRACTOR ADVERSARIAL REVIEW
각 D3+ 문항에서 독립 검수자는 정답을 숨긴 상태로:
1. first-pass 후보 2~3개를 고름
2. 가장 매력적인 오답 SECOND_BEST를 지정
3. 왜 학생이 고를 수 있는지 오개념/부분진실 근거 기록
4. 왜 최종적으로 틀렸는지 정확한 한 축으로 반박
5. 정답을 제거해도 다른 오답끼리 품질이 무너지지 않는지 확인

SECOND_BEST가 지정 불가능하면 문항은 너무 쉬운 것으로 본다.

## 6. DONGBOOK REALISM
FINAL은 다음 학교 대비 특성을 우선한다.
- 학교자료/보충자료의 핵심 판단축
- 실제 기출에서 반복되는 자료 처리 방식과 난도 흐름
- 보기/자료/조건을 읽고 구분하는 부담
- 단순 암기보다 적용·비교·복합판단
- 과목별 MASTER가 정의한 학교형 문항 DNA

'동북고스럽다'는 막연한 문체 모사가 아니라 검증된 자료/기출 구조 근거로만 판정한다.

## 7. TIME-PRESSURE REALISM
문항마다 EXPECTED_TIME_CLASS:
SHORT / STANDARD / LONG

세트 FAIL:
- LONG 문항이 연속 3개 이상
- 난도 대부분이 읽기량에서 발생
- 후반부에 LONG + D5가 과도하게 몰려 실제 시험시간을 비현실적으로 초과
- 계산노동/문장해독 노동이 개념 추론보다 큼

## 8. FINAL RELEASE GATE
FINAL_DIFFICULTY=PASS
FINAL_ITEM_QUALITY=PASS
ANSWER_LENGTH_BIAS=PASS
DISTRACTOR_COMPETITIVENESS=PASS
SCOPE_FIDELITY=PASS
UNIQUE_ANSWER=PASS
ANSWER_KEY_COMPLETE=PASS
PRODUCT_ISOLATION=PASS
PDF_QC=PASS

하나라도 FAIL이면 FINAL_RELEASE=BLOCKED.

## 9. CANARY FAULT INJECTION
FINAL CANARY에 의도적으로 다음 결함을 주입하고 차단 여부를 확인:
- 정답만 30% 이상 긴 문항
- 즉시 제거 오답 3개
- D4 라벨이지만 1단계 풀이
- 동일 판단축 3문항 반복
- 정답 절대어 힌트
- 근거 없는 고난도 선지
- 후반 LONG 문항 과밀

모든 결함이 gate에서 차단되어야 FINAL_CANARY_PASS.




## 10. MULTI-EXAM ANCHOR PROVENANCE
FINAL_DIFFICULTY PASS에는 다음이 내부적으로 확인되어야 한다.

FINAL_ANCHOR_PROVENANCE:
  MODE: SCHOOL_MULTI_EXAM_ANCHOR
  SUBJECT:
  ANCHOR_ID:
  SOURCE_EXAM_COUNT:
  CORPUS:
  CONFIDENCE:

KOR/SOC는 source_exam_count >= 4를 기대한다.
SCI-REDOX는 direct-scope actual item group + broader science ensemble을 사용한다.

실제 학생 정답률이 없는 한 이 난도는 STRUCTURAL_CALIBRATION이다.
이를 실측 정답률 기반 난도로 표현하지 않는다.

END ARC FINAL QUALITY GATE V1.1


---
# V1.2 추가 (2026-11-15, 사용자 지시: "ARC FINAL 출제 규칙도 손봐야 할 것 같다, 곧 실전모의고사")
번들 최상위에 `final_gate: V1.2`를 적으면 아래가 모두 적용된다. `arc.py scaffold --product ARC_FINAL`이 기본으로 적는다. 선언하지 않은 옛 FINAL 번들·카나리는 V1.1 규칙만 받는다.

## 11. 두 판 — 학교 수준(STANDARD) · 심화판(ADVANCED)
사용자 결정(2026-11-15): "학교 수준 + 심화판". 2026-10-08 요청(평균 3.0~3.5)은 심화판으로 보존한다.
| 판 | `final_edition` | 난도 기준 |
|---|---|---|
| 학교 수준 (기본) | `STANDARD` | 과목 anchor ± tolerance (§2). 더 쉬워도 더 어려워도 FAIL |
| 심화판 | `ADVANCED` | 평균 3.0~3.5, D4+D5 ≥ anchor D4+D5 + 0.05, 후반부 D4+ ≥ anchor 최소 + 1 |
- 두 판 모두 **학교 시험 구조(§12)는 똑같다.** 심화판은 문항 수·배점·영역을 바꾸지 않고 난도만 올린다.
- 심화판도 범위 밖 지식·장문 노동·계산 노동으로 어렵게 만들지 않는다(§2D). 어려움은 새 자료 추론·조건 결합·예외 검토에서 나온다(§13).
- 계획: `python tooling/arc.py plan --subject KOR --product ARC_FINAL --scope "…" --edition 학교수준|심화판`
- 게이트 코드: FINAL_EDITION_INVALID, FINAL_ADVANCED_MEAN_OUT_OF_RANGE, FINAL_ADVANCED_NOT_HARDER.

## 12. 학교 시험 구조 고정
기준: 현재 시험 설정(`ops/exams/EXAM_CONTEXTS_V1.yaml`)의 과목별 `exam_structure` — 학교 공지 `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml`을 옮긴 값.
| 과목 | 선택형 | 서술형 | 영역 배분 |
|---|---|---|---|
| 국어 | 22문항 80점 | 4문항 20점 | — |
| 영어 | 34문항 80점 (1~10번 어휘 각 1점) | 4문항 20점 | 번호·유형·배점은 `quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml`의 `arc_final_blueprint` |
| 사회 | 22문항 90점 | 2문항 10점 | A 7+1, B 7+1, C 8+0 (문항마다 `part: A/B/C`) |
| 과학 | 24문항 80점 | 4문항 20점 | A~D (문항마다 `part`; 영역별 문항 수는 공지에 없음 → 범위 쪽수 비율로 계획) |
- 번들: 선택형 `format: MCQ`, 서술형 `format: CR`, 문항마다 `points`. 사회·과학은 `part`.
- 게이트 코드: FINAL_STRUCTURE_MISMATCH(문항 수), FINAL_POINTS_MISMATCH(배점 합), FINAL_PART_ALLOCATION_MISMATCH(영역별 수), FINAL_STRUCTURE_MISSING(시험 설정에 구조 없음).
- 시험 시간·문항 배치(쉬운 문항 앞, 변별 문항 후반)는 §7·§2의 후반부 규칙을 따른다.

## 13. 출제자 시선을 FINAL에도 (quality/ARC_EXAMINER_LENS_V1.3.md)
- FINAL 번들도 `examiner_lens: V1.3`을 선언한다. 생산 파이프라인과 draft_preview가 출제자 시선 게이트를 함께 돌린다(게이트 이름 `EXAMINER_LENS`, 실패 코드 앞에 `LENS_`).
- 내신 출제 순서(출제 계획표 → 수업 근거 → 오개념별 오답 → 이의 제기 검토 → 동료 교사 블라인드 검토)를 그대로 따른다. FINAL은 실제 시험지이므로 **이의 제기 검토(§3)와 동료 교사 검토를 생략하지 않는다.**
- 난도↔유형 연결: D2 확인·적용 / D3 적용·추론·심화 / D4 추론·심화 / D5 심화. 그래서 학교 수준 FINAL은 확인·적용이 많고, 심화판은 추론·심화가 자연히 많아진다.
- 학교 실제 시험처럼: 교과서·학습지 지문을 쓰는 문항이 기본이고, 새 자료(INFER/EXTEND)는 학교 기출에서 확인된 형식(국어: 교과서 지문 + 외부 작품 비교, 새 <보기> 조항 등)으로만 쓴다. 학생용 안내(§11 of lens)와 <보기> 조판(§12 of lens)도 그대로.

## 14. 과목별 난도 기준(anchor) 등록 상태 (2026-11-15)
시험 설정 `DONGBUK_2026_2_FINAL`의 각 과목 `difficulty_anchor`에 경로·sha256·단원을 등록했다(이전에는 모두 null이라 FINAL이 BLOCKED였다).
| 과목 | anchor | 근거 | 학교 수준 평균 | 신뢰도 |
|---|---|---|---|---|
| 국어 | KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0 | 실제 시험 4회 앙상블 | 2.89 ± 0.20 | HIGH |
| 영어 | ENG_DONGBUK_POINTS_PROXY_DIFFICULTY_ANCHOR_V1.0 | 2026 체제 실제 시험 3회의 **문항별 학교 배점**을 난도 대리 지표로 변환(2026-11-15 교체, 이전 추정치는 archive) | 2.75 ± 0.22 | MEDIUM_LOW |
| 사회 | SOC_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0 | 실제 시험 4회 앙상블 | 2.87 ± 0.22 | MEDIUM_HIGH |
| 과학 | SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0 | 통합과학 실제 4회 앙상블(SCI_ALL). 이번 A~D 범위 직접 기출은 아님 | 2.53 ± 0.22 | MEDIUM |
- 영어 기준은 정답률이 아니라 교사 배점에 근거한 근사다. 문항 분석·정답률 자료가 오면 교체한다.
- anchor 파일을 고치면 시험 설정의 sha256도 갱신해야 한다(FINAL_ANCHOR_CHECKSUM_MISMATCH).

## 15. 실전 모의고사 제작 순서 (과목 순서: 국어 → 영어 → 사회 → 과학, 사용자 지정)
```bash
python tooling/arc.py plan --subject KOR --product ARC_FINAL --scope "기말 전범위" [--edition 심화판]
python tooling/arc.py scaffold --subject KOR --product ARC_FINAL --scope "기말 전범위" --actor CLAUDE --out quality/production/<번들>
# 자료 열람(Drive) → items.yaml 작성 (format/points/part, examiner_lens 필드)
python tooling/production/draft_preview.py quality/production/<번들> --output-dir <scratch>
# 동료 교사 블라인드 검토(별도 컨텍스트) → production_pipeline → 사용자 검수 1회 → 통과 시 Drive 저장
```

## 16. 과목별 출제 스타일 프롬프트 (2026-11-15) — FINAL 출제 전 반드시 읽는다
"실제 동북고 시험지와 최대한 비슷하게"를 위한 과목별 규칙. 번호별 배치, 표준 발문, 유형별 변형 공식, 오답 함정, 자료 제시 방식, 서술형 조건·채점, 난도(학교 수준/심화판), 금지 목록, 자체 점검을 담았다.
| 과목 | 파일 | 근거 |
|---|---|---|
| 국어 | `quality/style/ARC_STYLE_PROMPT_KOR_V1.0.md` | 동북고 5개 학기 분석 + 선생님 기말 보충자료1 |
| 영어 | `quality/style/ARC_STYLE_PROMPT_ENG_V1.0.md` | 동북고 5개 정기고사 178문항 전수 분석 |
| 사회 | `quality/style/ARC_STYLE_PROMPT_SOC_V1.0.md` | 동북고 통합사회 5개 학기 분석 |
| 과학 | `quality/style/ARC_STYLE_PROMPT_SCI_V1.0.md` | 동북고 통합과학 5개 학기 분석 |
- manifest `active.quality.style_prompts`, `arc.py plan`의 읽기 순서, FINAL 뼈대의 `style_prompt` 필드에 연결.
- 근거는 Drive 분석 문서(evidence D2). 원안지 문항별 재대조 전이므로, 원안지와 다르면 **원안지가 이긴다**.
