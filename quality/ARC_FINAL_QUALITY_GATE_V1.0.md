# ARC_FINAL_QUALITY_GATE_V1.0
VERSION: 1.0
DATE: 2026-09-24
STATUS: ACTIVE
VALIDATION_MARKER: NFINAL_HARDENING_20260924
ROLE: ARC FINAL 전용 난이도·문항질·세트실전성 승인 게이트
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

## 2. DIFFICULTY PROFILE
20문항 기본 시작 곡선:
D1 0~5%
D2 10~20%
D3 40~50%
D4 25~35%
D5 5~10%

학교 실제 기출의 검증된 난도 곡선이 있으면 보정 가능.
단, 동북고 대비력이 낮아지는 방향의 근거 없는 하향은 금지.

필수:
- D4+D5 >= 30% 또는 학교 앵커가 명확히 다른 구조를 증명
- D1+D2 <= 25%
- 후반 30% 구간 D4+ 최소 2문항 권장
- 초반 4문항 직접회상 연속 금지
- D5는 억지 함정/장문노동 금지

내부 출력:
DIFFICULTY_PROFILE:
  D1:
  D2:
  D3:
  D4:
  D5:
  SCHOOL_RELATIVE_COUNTS:
  D4_D5_RATE:
  D1_D2_RATE:
  LATE_SECTION_D4_PLUS:
  RESULT: PASS/WARN/FAIL

## 2A. SCHOOL ANCHOR MODE (FINAL 기본값, 2026-09-25 사용자 지시)
"final은 무조건 동북고 시험 난이도에 맞춰서 출제한다."

- `runtime.arc_final_difficulty_mode: SCHOOL_ANCHOR`이면 위 2절의 고정 곡선 대신 학교 기준치와 비교한다.
- KOR 기준치: `quality/anchors/KOR_DONGBUK_2025_2_MID_DIFFICULTY_ANCHOR_V1.0.yaml`
  (2025-2 동북고 1학년 중간 공통국어2, 선택형 21문항을 같은 D1~D5 척도로 1회 블라인드 평정: D1 1 · D2 7 · D3 9 · D4 4 · D5 0, 평균 2.76).
- 판정은 세트의 블라인드 난이도를 기준으로 한다.
  - D1+D2, D3, D4+D5 비율이 각각 기준치 ±0.15 이내여야 한다.
  - 평균 난도(D1=1 … D5=5)가 기준치 ±0.30 이내여야 한다.
  - 후반 30% 구간의 D4+ 문항은 기준치 −1 이상이어야 한다.
- 실패 코드:
  - 기준보다 쉬우면 `FINAL_SCHOOL_ANCHOR_EASIER`
  - 기준보다 어려우면 `FINAL_SCHOOL_ANCHOR_HARDER`
  - 비율만 벗어나면 `FINAL_SCHOOL_ANCHOR_SHARE_OFF`
- 학교 시험보다 어렵게 만드는 것도 불합격이다. FINAL은 실제 시험과 같은 체감 난도를 목표로 한다.
- 기출 문구·선지는 재사용하지 않는다. 기준치는 구조와 난도 보정에만 쓴다.

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

END ARC FINAL QUALITY GATE V1.0
