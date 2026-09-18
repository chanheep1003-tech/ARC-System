# ARC_ITEM_QUALITY_RUBRIC_V1.1
VERSION: 1.1
DATE: 2026-09-18
ROLE: 문항 자체의 교육적·평가적 품질 검수
STATUS: ACTIVE

## 0. PURPOSE
정답이 맞고 범위 안이라는 이유만으로 좋은 문항으로 인정하지 않는다.
특히 자동 QA의 점수 인플레이션을 막고, 실제 문항 근거에 기반해 BANK_PASS를 결정한다.

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
- 학교 시험 구조와 명백히 동떨어짐
- 고난도인데 어려움의 원인이 범위 밖 지식·조건 부족·표현 난삽함임
- ITEM/COMMERCIAL 점수가 문항 근거 없이 반복 패턴으로 부여됨

## 2. ITEM QUALITY SCORE — 100
A. EVALUATION_VALIDITY /20
B. STEM_CLARITY /15
C. DISTRACTOR_QUALITY /20
D. REASONING_QUALITY /15
E. SCHOOL_STYLE_MATCH /10
F. ORIGINALITY /10
G. EFFICIENCY /5
H. ASSET_FUNCTION /5

각 항목은 반드시 '점수 + 한 줄 근거'를 남긴다.
총점만 적거나 'independently checked' 같은 추상 문구만 쓰면 QA 미완료로 본다.

## 3. ANTI-INFLATION SCORE CEILINGS
다음 상한은 자동 적용한다.

### DIRECT_RECALL_CEILING
자료·조건·전이 없이 단순 개념 확인/정의 매칭만 요구:
- REASONING_QUALITY <= 8/15
- ORIGINALITY <= 6/10
- TOTAL <= 83
- PREMIUM_BANK_A 금지

### WEAK_DISTRACTOR_CEILING
5지선다에서 3개 이상이 즉시 제거 가능한 허술한 오답:
- DISTRACTOR_QUALITY <= 10/20
- TOTAL <= 83
- BANK_A 금지

### GENERIC_CONTEXT_CEILING
상황·숫자·대상을 다른 단원으로 쉽게 치환해도 골격이 동일:
- ORIGINALITY <= 5/10
- SCHOOL_STYLE_MATCH <= 7/10

### UNGROUNDED_STYLE_CEILING
현재 교과서/학습지/학교자료/검증 문제집과 구조 비교 근거가 없음:
- SCHOOL_STYLE_MATCH <= 6/10
- COMMERCIAL 등급 A 금지

### FAKE_D3_PLUS
D3 이상으로 표기했지만 실제 해결이 1단계 직접개념 확인이면:
- DIFFICULTY_MISCLASSIFIED
- REVISE
- 난도 재산정 전 BANK_PASS 금지

## 4. PREMIUM RULE
PREMIUM_BANK_A는 다음을 모두 만족해야 한다.
- ITEM >= 92
- COMMERCIAL >= 92
- HARD FAIL 0
- DIRECT_RECALL_CEILING 없음
- WEAK_DISTRACTOR_CEILING 없음
- GENERIC_CONTEXT_CEILING 없음
- 최소 하나의 실질적 평가요소 존재: 자료 해석 / 조건 결합 / 개념 전이 / 사료·제시문 분석 / 다단계 추론
- 정답뿐 아니라 핵심 오답 2개 이상이 실제 오개념·조건오류·HALF_TRUE에 기반

## 5. PASS RULE
- 92~100: BANK_A 후보
- 86~91: BANK_B
- 80~85: REVISE
- 79 이하: DISCARD
- HARD QUALITY FAIL 1개 이상: DISCARD
- 점수 상한 규칙이 적용되면 상한을 넘겨 기록할 수 없음

## 6. COMMERCIAL REALISM CHECK
상업 문제집 수준 판정 시 다음을 별도로 확인한다.
- 실제 교과 개념어를 사용하고 추상적 AI 문체가 적은가
- 오답이 학습자가 실제로 고를 법한가
- 조건·자료가 정답 경로에 기능적으로 쓰이는가
- 발문·선지 길이가 기계적으로 균일하지 않은가
- 정답만 안전하고 구체적인 설명문이 되지 않는가
- '모두/항상/반드시/전혀'만으로 오답을 만드는 패턴이 반복되지 않는가

COMMERCIAL 92+는 실제 참고자료의 구조적 근거 또는 명확한 편집 근거가 있어야 한다.

## 7. SCORE PATTERN SANITY
20문항 세트에서 다음이면 점수 인플레이션 의심으로 세트 전체 재검토한다.
- 70% 이상이 88~92 구간에 몰림
- 3개 이하의 총점 값이 기계적으로 반복
- QUALITY_FLAGS가 전부 빈 배열
- 서로 다른 문항인데 QUALITY_COMPONENTS가 같은 문구로 복사됨
- PREMIUM_BANK_A 비율이 40% 초과하면서 고난도/자료형 근거가 부족함

## 8. HIGH-DIFFICULTY QUALITY
D4/D5는 추가 검사:
- 어려움의 주원인이 REASONING_DEPTH / DATA_LOAD / DISTRACTOR_STRENGTH인가
- 조건이 충분한가
- 풀이 후 정답이 납득 가능한가
- 반복 계산/장문 독해 때문이 아닌가
- 핵심 원리를 파악하면 명확히 풀리는가
하나라도 아니면 D4/D5로 인정하지 않는다.

## 9. BANK METADATA
각 BANK 문항:
ITEM_QUALITY_SCORE:
QUALITY_TIER:
QUALITY_COMPONENTS:
  evaluation_validity: {score, evidence}
  stem_clarity: {score, evidence}
  distractor_quality: {score, evidence}
  reasoning_quality: {score, evidence}
  school_style_match: {score, evidence}
  originality: {score, evidence}
  efficiency: {score, evidence}
  asset_function: {score, evidence}
QUALITY_FLAGS: []
SCORE_CEILINGS_APPLIED: []
QUALITY_RUBRIC_VERSION: ARC-IQR-V1.1

END ARC ITEM QUALITY RUBRIC V1.1
