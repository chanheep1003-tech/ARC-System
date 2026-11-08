# ARC_FINAL_QUALITY_GATE_V1.1
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

ARC FINAL에는 전 과목 공통 고정 난도곡선을 강제하지 않는다.

기본 원칙:
FINAL = 실제 동북고 해당 과목 시험 난도대의 모의고사

실제 기출 코퍼스:
quality/anchors/DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0.yaml

과목별 ACTIVE anchor:
- KOR → KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0
- SOC → SOC_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0
- SCI-REDOX → SCI_REDOX_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0
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

### 2D-0. 기말 범위와 앵커 (2026-11-08)
위 SCI-REDOX 앵커는 중간고사 산화·환원 범위용이다. 기말 과학 범위(전체 학기−중간)에는 직접 범위 앵커가 없으므로
동북고 과학 실제 시험 코퍼스 전체 앙상블만 사용하고 FINAL_ANCHOR_PROVENANCE.CONFIDENCE=LOW로 기록한다(후속 과제: 과학 기말용 앙상블 앵커 파일 신설).
목표 평균은 각 앵커 평균에 +0.1~+0.3(PROVISIONAL)을 더한다.

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
기본은 실제 시험과 비슷한 난도 곡선이며, 사용자 결정(2026-11-08)에 따라 평균 난도만 앵커 평균 +0.1~+0.3 범위로 소폭 높인다.

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
