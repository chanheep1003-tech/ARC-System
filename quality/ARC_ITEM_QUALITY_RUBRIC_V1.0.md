# ARC_ITEM_QUALITY_RUBRIC_V1.0
VERSION: 1.0
DATE: 2026-09-17
ROLE: 문항 자체의 교육적·평가적 품질 검수
STATUS: ACTIVE

## 0. PURPOSE
정답이 맞고 범위 안이라는 이유만으로 좋은 문항으로 인정하지 않는다.
BANK_PASS 후보는 오류 검증 후 별도의 ITEM QUALITY GATE를 통과해야 한다.

## 1. HARD QUALITY FAIL
다음은 정답 오류가 없어도 폐기한다.
- 발문이 모호해 두 해석이 가능함
- 지엽 암기나 말장난만으로 난도를 높임
- 단순 계산노동/읽기노동이 사고력보다 큼
- 정답만 유독 길거나 구체적이라 힌트가 됨
- 오답이 너무 허술해 실질적으로 2~3지선다임
- 선지 간 판단 기준이 제각각이라 평가축이 흐림
- 자료가 문제 해결에 사실상 필요 없음
- 같은 CONCEPT_ID/QUESTION_FORM의 기존 BANK 문항과 과도하게 유사
- 학교 시험 스타일과 명백히 동떨어진 구조
- 고난도인데 어려움의 원인이 범위 밖 지식·조건 부족·표현 난삽함임

## 2. ITEM QUALITY SCORE — 100
A. EVALUATION_VALIDITY /20
B. STEM_CLARITY /15
C. DISTRACTOR_QUALITY /20
D. REASONING_QUALITY /15
E. SCHOOL_STYLE_MATCH /10
F. ORIGINALITY /10
G. EFFICIENCY /5
H. ASSET_FUNCTION /5

TOTAL = 100

## 3. PASS RULE
- 90~100: BANK_A — 매우 우수, N°/FINAL 우선 후보
- 84~89: BANK_B — 사용 가능
- 78~83: REVISE — 수정 후 처음부터 재검증
- 77 이하: DISCARD
- HARD QUALITY FAIL 1개 이상: 점수와 무관하게 DISCARD

검증문항은행에는 BANK_A/B만 저장한다.

## 4. HIGH-DIFFICULTY QUALITY
D4/D5는 추가 검사:
- 어려움의 주원인이 REASONING_DEPTH / DATA_LOAD / DISTRACTOR_STRENGTH인가
- 조건이 충분한가
- 풀이 후 정답이 납득 가능한가
- 풀이 시간이 길어지는 이유가 반복 계산/장문 독해 때문이 아닌가
- 핵심 원리를 파악하면 명확히 풀리는가

하나라도 아니면 D4/D5로 인정하지 않고 수정 또는 폐기한다.

## 5. SET-LEVEL QUALITY
20문항 세트도 별도 검사한다.
- 동일 발문/구조 반복
- 같은 함정 반복
- 초반 암기형 과밀
- 특정 CONCEPT_ID 과밀
- 자료형의 장식화
- 정답 번호 비정상 쏠림
- D등급 분포의 과도한 편향
- 학교시험과 다른 난도 흐름

SET_QUALITY:
PASS / REVIEW / FAIL

## 6. BANK METADATA ADDITIONS
각 BANK 문항에:
ITEM_QUALITY_SCORE:
QUALITY_TIER: A / B
QUALITY_COMPONENTS:
  evaluation_validity:
  stem_clarity:
  distractor_quality:
  reasoning_quality:
  school_style_match:
  originality:
  efficiency:
  asset_function:
QUALITY_FLAGS: []
QUALITY_RUBRIC_VERSION: ARC-IQR-V1.0

## 7. FEEDBACK LOOP
반복적으로 낮은 점수를 받는 원인을 집계한다.

예:
- DISTRACTOR_WEAK 반복
- STEM_AMBIGUOUS 반복
- SCHOOL_STYLE_LOW 반복
- TOO_SIMILAR 반복
- FAKE_DIFFICULTY 반복

같은 품질 결함이 같은 과목에서 3회 이상 반복되면
과목 MASTER 또는 COMMON ENGINE 수정 후보로 올리고 QA BENCH로 회귀검사한다.

END ARC ITEM QUALITY RUBRIC V1.0
