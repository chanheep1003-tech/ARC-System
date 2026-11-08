# ARC_DIFFICULTY_ENGINE_V1.5
VERSION: 1.5
DATE: 2026-09-26
ROLE: 문항 난이도 추정·비교·보정 엔진
STATUS: ACTIVE
SCOPE: 공통국어2 / 통합과학2 / 통합사회2 / 한국사2 / 인공지능기초
EXCLUDED: 공통수학

## 0. PURPOSE
ARC의 난이도는 AI가 단독으로 “쉬움/어려움”을 감으로 판정하지 않는다.

난이도는 다음 4단계로 추정·보정한다.

1) STRUCTURAL ESTIMATE
   문항 자체의 개념부담·추론단계·자료부담·오답매력도·조건부담·낯선 적용을 수치화

2) REFERENCE COMPARISON
   동일 과목의 학교 실제 기출, 학교자료, 문제집/고난도 자료와 비교

3) BANK CALIBRATION
   검증문항은행에 축적된 기존 문항들과 상대 비교

4) OUTCOME CALIBRATION
   실제 사용자 풀이결과, 학교시험 결과, 정답률 자료가 생기면 사후 보정

모든 ARC_N / ARC_FINAL 문항은 STRUCTURAL ESTIMATE 뒤 blind PASS B에서 실제 해결 부담을 다시 측정한다.
TARGET_DIFFICULTY는 PASS B의 ACTUAL_DIFFICULTY와 일치하도록 수정 또는 재분류한 뒤 CONTENT_LOCK한다.

난이도는 학생용 문제 본문(발문·자료·선지)에 표시하지 않는다.
예외(사용자 결정 2026-11-08): ARC_N 문항 메타 스트립에는 D1~D5 등급을 그대로 표시한다. ARC_FINAL에는 어떤 형태로도 표시하지 않는다.
그 밖에는 ARC N°/FINAL의 내부 설계와 문제은행 메타데이터에만 사용한다.

## 1. ARC DIFFICULTY LEVEL

|등급|점수|정의|
|---|---:|---|
|D1|0–24|개념 직접확인·단일 판단|
|D2|25–44|기본 적용·단순 자료해석|
|D3|45–64|복수조건·2단계 추론·중간 자료부담|
|D4|65–79|복합자료·고매력 오답·3단계 이상 추론|
|D5|80–100|최상위 변별형·복수 자료/조건 통합|

주의:
- 범위 밖 지식 필요
- 조건 부족
- 복수정답
- 지나친 계산노동
- 애매한 표현
은 난도가 아니라 품질 오류다.
HARD FAIL 문항은 난이도 산정 대상에서 제외한다.

## 2. STRUCTURAL SCORE — 100

### A. CONCEPT_LOAD /20
0–5   단일 개념 직접 확인
6–10  개념 1~2개 연결
11–15 개념 2개 이상 통합
16–20 여러 개념을 동시에 구분·적용

### B. REASONING_DEPTH /25
0–5   1단계 판단
6–10  2단계
11–17 2~3단계
18–22 3단계 이상
23–25 복수 경로를 통합해야 정답 결정

### C. DATA_LOAD /20
0–4   자료 없음/단순 제시
5–9   표·지문·그림 1개 단순 해석
10–14 자료 내 복수 요소 비교
15–17 2개 이상 자료 연결
18–20 복합자료·추세·변화량·조건 동시 해석

### D. DISTRACTOR_STRENGTH /15
0–3   즉시 배제 가능한 오답
4–7   개념 혼동형
8–11  HALF_TRUE / 조건 일부 참
12–15 판단축 2개 이상을 구분해야 배제

### E. CONDITION_LOAD /10
0–2   조건 0~1개
3–5   조건 2개
6–8   조건 3개 이상
9–10  조건 우선순위·예외·순서까지 관리

### F. TRANSFER_NOVELTY /10
0–2   교과서와 거의 동일한 맥락
3–5   익숙한 변형
6–8   낯선 사례/표현
9–10  처음 보는 맥락에서 개념을 재구성해 적용

BASE_DIFFICULTY_SCORE =
A + B + C + D + E + F

## 3. REFERENCE HIERARCHY

난이도 비교 우선순위:

### R0 — SAME SCHOOL ACTUAL EXAM
동북고 실제 기출.
가장 중요한 기준.

목적:
- “동북고 보통 문항”
- “동북고 변별 문항”
- FINAL의 실제 난도 흐름
을 정의.

### R1 — CURRENT SCHOOL MATERIAL
현재 학습지·보충자료·교사 강조자료.
난도보다 출제 가능성과 요구 사고수준 기준.

### R2 — VERIFIED WORKBOOK / HIGH-DIFFICULTY SET
사용자가 제공한 문제집, 고난도 N제, 공식/검증 자료.
문제집에 난도 라벨이 있으면 참고하되 그대로 신뢰하지 않고 구조점수와 비교.

### R3 — OFFICIAL EXTERNAL ASSESSMENT
교육청·평가원·EBS·공식 평가자료.
학교 시험보다 범위/목적이 다르면 구조 난도만 참고.

### R4 — ARC VERIFIED BANK
ARC 검증문항은행에서 같은 CONCEPT_ID 또는 유사 QUESTION_FORM의 기존 PASS 문항.

### R5 — AI STRUCTURAL ONLY
비교자료가 부족할 때만 BASE_DIFFICULTY_SCORE를 그대로 사용.

범위 밖 상위학년 자료는 절대 정답근거로 사용하지 않고,
난도 구조 비교에만 제한적으로 사용한다.

## 4. COMPARATIVE CALIBRATION

새 문항마다 가능한 경우 최소 2개의 기준문항과 비교한다.

REFERENCE_PAIR:
- ANCHOR_LOW: 새 문항보다 한 단계 쉬운 기준
- ANCHOR_HIGH: 새 문항보다 한 단계 어려운 기준

비교축:
- concept load
- reasoning depth
- data load
- distractor discrimination
- condition load
- novelty
- expected time burden

판정:
- 새 문항이 LOW와 유사 → LOW 부근
- LOW보다 명확히 어렵고 HIGH보다 명확히 쉬움 → 중간값
- HIGH와 유사 → HIGH 부근
- 두 기준과 구조가 너무 다름 → 비교 신뢰도 LOW, 구조점수 우선

REFERENCE_MATCH_SCORE:
HIGH / MEDIUM / LOW

## 5. SCHOOL-RELATIVE DIFFICULTY

절대 D1~D5 외에 내부용 상대난도를 함께 기록한다.

SCHOOL_RELATIVE:
- BELOW_SCHOOL
- SCHOOL_STANDARD
- SCHOOL_UPPER
- ABOVE_SCHOOL
- EXTREME

예:
D3 / SCHOOL_UPPER
D4 / SCHOOL_STANDARD

같은 D4라도 과목·시험에 따라 학교 상대 위치가 달라질 수 있다.

ARC FINAL은 SCHOOL_RELATIVE가 더 중요하고,
ARC N°는 절대 D등급과 개념 커버리지가 더 중요하다.

## 6. PRODUCT TARGET CURVES

### ARC N° 기본 — 70/30 BALANCED PROFILE
기본 목적:
- CORE_EXAM_POINT 70~80%
- ADVANCED_DISCRIMINATION 20~30%

권장 시작 분포:
D1 0~10%
D2 25~35%
D3 35~45%
D4 15~25%
D5 0~5%
D4+D5 기본 20~30%

단, CORE/ADVANCED 분류와 D등급은 같은 축이 아니다.
핵심문제도 강한 오답·대표 자료 적용으로 D3/D4가 될 수 있고,
심화문항도 문제 구조에 따라 D3일 수 있다.

과목 MASTER·실제 학교 기출 분석이 우선하되,
기본 ARC_N에서는 핵심 출제축 coverage 70~80%를 유지한다.
명시적 고난도/최상위 N제 요청일 때만 ADVANCED 비율을 상향할 수 있다.

N° 목적:
- 시험 핵심 개념/자료/관계의 반복 학습
- 표준 적용과 실수 방지
- 마지막 20~30%에서 상위 변별
- D5는 소수로 제한

### ARC FINAL
고정 분포를 강제하지 않는다.

우선순위:
1. 최근 같은 학교 실제 시험 난도 흐름
2. 시험 문항 배치
3. 자료밀도
4. 고난도 문항 위치와 비율

FINAL은 “고난도 문제집”이 아니라 “실제 시험 모사”다.

## 7. SUBJECT-SPECIFIC DIFFICULTY SIGNALS

### KOREAN
난도를 높이는 정상 요인:
- 복수 지문/보기 비교
- OBSERVED_FACT vs SPEAKER_INFERENCE 구분
- 표현효과+근거 동시판단
- HALF_TRUE
- 공통점/차이점 복합판단

난도로 인정하지 않는 것:
- 원문 과도 인용
- 작품 밖 배경지식
- 철학사 지엽지식

### SCIENCE
난도를 높이는 정상 요인:
- 복수조건 변화
- 그래프/입자모형/실험자료 연결
- 정성+정량 결합
- 반응성 관계 추론
- 전후 상태/순차투입

난도로 인정하지 않는 것:
- 상위학년 공식
- 조건 없는 질량/이온수 계산
- 불필요한 산술노동

### SOCIAL
난도를 높이는 정상 요인:
- 낯선 사례에 개념 적용
- 주장·근거·결론 분리
- 권리충돌/권리구제 복수판단
- 지도·통계자료 복합 해석
- SOURCE_FACT와 변형사례 구분

난도로 인정하지 않는 것:
- 시험범위 밖 판례 지식
- C파트 X 영역
- 기관명 암기만 지엽적으로 요구

### HISTORY
난도를 높이는 정상 요인:
- 사료 식별 + 시기 + 단체 연결
- 복수 사건 선후관계
- 인물·단체·계열 교차
- 지도/연표/신문 결합

난도로 인정하지 않는 것:
- 시험범위 밖 세부 연도 암기
- 사료 주체가 불명확한 문제

### AI
난도를 높이는 정상 요인:
- 탐색구조에서 순서 추론
- 데이터 전처리→시각화→해석 연결
- 코드 결과/개념 동시판단
- 상관관계 해석의 조건 구분

난도로 인정하지 않는 것:
- 범위 밖 문법/알고리즘
- 방문규칙 미명시 상태의 탐색 문제

## 8. BANK METADATA

모든 BANK_PASS 문항에 추가:

ARC_DIFFICULTY_LEVEL:
DIFFICULTY_SCORE:
SCHOOL_RELATIVE:
DIFFICULTY_CONFIDENCE: HIGH / MEDIUM / LOW

DIFFICULTY_COMPONENTS:
  CONCEPT_LOAD:
  REASONING_DEPTH:
  DATA_LOAD:
  DISTRACTOR_STRENGTH:
  CONDITION_LOAD:
  TRANSFER_NOVELTY:

REFERENCE_CALIBRATION:
  REFERENCE_1:
  REFERENCE_2:
  REFERENCE_MATCH_SCORE:
  CALIBRATION_DELTA:

OUTCOME_DATA:
  USER_ATTEMPTS: 0
  USER_CORRECT: 0
  SCHOOL_OR_GROUP_CORRECT_RATE: UNKNOWN
  MEDIAN_TIME: UNKNOWN

PASS_B_MEASUREMENT:
  REASONING_STEPS:
  EVIDENCE_COUNT:
  IMMEDIATE_ELIMINATION_COUNT:
  STRONG_DISTRACTOR_COUNT:
  SECOND_BEST_RISK:
  TRANSFER_REQUIRED:
  ACTUAL_DIFFICULTY:

DIFFICULTY_VERSION: ARC-DE-V1.5

## 9. CALIBRATION DELTA

비교자료를 사용한 최종점수:

FINAL_SCORE =
BASE_SCORE + CALIBRATION_DELTA

기본 DELTA 범위:
-15 ~ +15

권장:
±0~4   미세조정
±5~9   의미 있는 비교차이
±10~15 강한 외부 기준이 있을 때만

외부 문제의 “상/최상” 라벨만으로 ±10 이상 변경 금지.
실제 학교 기출 또는 충분한 누적 결과가 있을 때만 강한 보정.

최종점수 0~100 clipping.

## 10. OUTCOME RECALIBRATION

실제 풀이 데이터가 쌓이면 구조점수보다 결과 데이터를 일부 반영한다.

초기:
OUTCOME_WEIGHT = 0

사용자 시도 5개 이상 또는 신뢰 가능한 집단 정답률 확보:
OUTCOME_WEIGHT 증가 가능.

사용자 개인 데이터는 “개인 체감난도”로 별도 기록하고
학교 전체 난도로 곧바로 일반화하지 않는다.

가능한 장기 항목:
- EXPECTED_CORRECT_RATE
- OBSERVED_CORRECT_RATE
- EXPECTED_TIME
- OBSERVED_TIME
- PERSONAL_RELATIVE_DIFFICULTY

## 11. RECALIBRATION LOOP

3시간 QA마다:
1. 신규 20문항 생성
2. HARD FAIL 제거
3. PASS 문항 구조점수 산정
4. 같은 CONCEPT_ID/QUESTION_FORM BANK 검색
5. 학교 기출/문제집 기준문항과 비교 가능한 경우 비교
6. D등급 + SCHOOL_RELATIVE 부여
7. 검증문항은행 저장
8. 분포 확인
9. 새 문항이 특정 D등급에 과도하게 몰리면 생성 프롬프트가 아니라 난도 파라미터를 먼저 조정
10. 반복적으로 체계적 편향이 확인될 때만 MASTER/DIFFICULTY ENGINE 수정

## 12. DRIFT DETECTION

최근 100개 BANK_PASS 기준으로 과목별 분포를 본다.

ARC_N 경고:
- CORE_EXAM_POINT_RATE < 0.70 → CORE_COVERAGE_WARNING
- CORE_EXAM_POINT_RATE > 0.85 → ADVANCED_GAP_WARNING
- ADVANCED_DISCRIMINATION_RATE > 0.35 (명시적 고난도 요청 없음) → OVER_DISCRIMINATION_WARNING
- D1+D2 > 55% → TOO_EASY_WARNING
- D4+D5 > 40% (명시적 고난도 요청 없음) → TOO_HARD_WARNING
- D3가 15% 미만 → MID_GAP_WARNING
- 같은 QUESTION_FORM이 한 난도대의 35% 초과 → STRUCTURE_BIAS_WARNING

경고는 즉시 프롬프트 수정 사유가 아니다.
REFERENCE 비교와 QA 결과를 함께 확인한다.

## 13. REFERENCE SAMPLE POLICY

비교 시 문제집 전체를 매번 읽지 않는다.

먼저:
- 목차/난도구분/단원
- 현재 시험범위
- 대표 쉬운/중간/어려운 문항

을 골라 ANCHOR SET을 만든다.

과목별 추천 Anchor Set:
- SCHOOL_STANDARD 5~10문항
- SCHOOL_UPPER 3~5문항
- WORKBOOK_MID 5문항
- WORKBOOK_HIGH 5문항

Anchor 문항은 그대로 재사용하기 위한 자료가 아니다.
난도 구조 비교용이다.

저작권 자료의 문장·선지·그림을 새 문제에 복제하지 않는다.

## 14. DIFFICULTY ANCHOR REGISTRY TEMPLATE

```yaml
ANCHOR_ID:
SUBJECT:
SOURCE_TYPE: SCHOOL_EXAM / WORKBOOK / OFFICIAL / ARC_BANK
SOURCE_FILE:
SOURCE_ITEM:
CONCEPT_ID:
REFERENCE_LEVEL:
STRUCTURAL_SCORE:
SCHOOL_RELATIVE:
NOTES:
```

## 15. ERROR RELATION

오류문항은:
DIFFICULTY = INVALID

다음은 난도상승으로 취급 금지:
- 조건 부족
- 복수정답
- 자료 오류
- 범위 밖 지식
- 장문노동
- 애매성

ERROR_DATABASE에 기록 후 폐기한다.

## 16. RELEASE POLICY

DIFFICULTY ENGINE 수정은 아래 중 하나일 때만:
- 100문항 이상 누적 후 구조점수와 비교평가가 체계적으로 어긋남
- 실제 학교시험 결과가 기존 난도곡선과 지속적으로 불일치
- 같은 유형에서 3회 이상 난도 오분류
- 사용자 풀이 데이터가 충분히 쌓여 특정 과목 보정 필요

단발성 체감으로 기준 자체를 자주 바꾸지 않는다.

## 17. D4 / D5 MINIMUM GATE
구조점수 합계만으로 D4/D5를 부여하지 않는다.

D4 최소 조건:
- REASONING_DEPTH >= 14/25
- DISTRACTOR_STRENGTH >= 9/15
- 서로 다른 판단 또는 적용 단계가 최소 2개
- 정답 결정에 실제로 사용되는 조건/자료가 2개 이상이거나, 하나의 자료라도 내부 요소를 결합해야 함
- blind PASS B REASONING_STEPS >= 2
- blind PASS B STRONG_DISTRACTOR_COUNT >= 2
- blind PASS B IMMEDIATE_ELIMINATION_COUNT <= 2

D5 최소 조건:
- REASONING_DEPTH >= 20/25
- DISTRACTOR_STRENGTH >= 11/15
- 복수 조건/자료의 통합 없이는 정답 결정 불가
- 단순 장문 독해나 선택지 수 때문에 어렵게 느껴지는 경우 제외
- blind PASS B REASONING_STEPS >= 3
- blind PASS B STRONG_DISTRACTOR_COUNT >= 2
- blind PASS B EVIDENCE_COUNT >= 2
- blind PASS B IMMEDIATE_ELIMINATION_COUNT <= 1

게이트를 못 넘으면 합산 점수가 높아도:
D4 후보 → 최대 D3
D5 후보 → 최대 D4

## 18. EXPLICIT CUE DISCOUNT
<보기>/지문이 판단 원리를 직접 진술하고, 문항이 그 원리의 단순 재진술·직접 부정·1:1 매칭만 요구하면:
- REASONING_DEPTH <= 10
- TRANSFER_NOVELTY <= 5
- 최대 D3
- 실제 1단계면 D2 우선

<보기>가 있다는 사실 자체는 난도 상승 근거가 아니다.
긴 지문, 긴 선지, 철학 용어의 존재 자체도 난도 상승 근거가 아니다.

## 19. KOREAN DIFFICULTY SANITY
국어 D4는 다음 중 최소 하나를 요구한다.
- 관찰 사실과 화자/서술자의 추론을 동시에 구분
- 두 작품/두 자료의 공통점과 차이를 같은 선지에서 결합
- 표현법 판정과 그 효과의 근거를 함께 판정
- HALF_TRUE 선지에서 참인 부분과 틀린 부분을 분리
- <보기>의 원리를 둘 이상의 장면/작품에 교차 적용

단순 내용일치, 단일 표현법 확인, <보기> 문장 그대로의 적용은 D4 금지.

## 20. SOCIAL DIFFICULTY SANITY
사회 D4는 다음처럼 실제 구분·적용 부담이 있어야 한다.
- 서로 유사한 두 사상가/원칙을 낯선 사례에 교차 적용
- 한 사례 안에서 주장/근거/조건을 분리한 뒤 사상가별 판단
- 다수 조건 중 일부만 충족하는 HALF_TRUE를 배제
- 동일한 제도/권리의 적용 범위를 사례별로 구분

제시문에 정의를 써 주고 해당 문장을 그대로 찾는 유형은 최대 D2~D3.

## 21. PASS B DIFFICULTY RECONCILIATION
출제 단계 난도는 TARGET_DIFFICULTY이며 provisional이다.
blind PASS B는 정답·출제 의도·TARGET_DIFFICULTY를 보지 않고 ACTUAL_DIFFICULTY를 산정한다.

필수 처리:
- TARGET = ACTUAL → DIFFICULTY_MATCH=PASS
- TARGET != ACTUAL → 문항 수정 후 PASS A/B 재실행 또는 TARGET을 ACTUAL로 재분류
- D4/D5 minimum 미달 → D4_SHORT 또는 D5_MINIMUM_FAIL
- 즉시 제거 선지 3개 이상 + 1단계 해결 → TOO_EASY item flag
- set의 D3 공백 → MID_GAP set flag
- 특정 구조가 난도대를 지배 → STRUCTURE_BIAS set flag

불일치 상태에서는 BANK_PASS / CONTENT_LOCK 금지.

## 22. DONGBOOK PRODUCT PROFILE — V1.4
사용자 실전 피드백을 반영하되 ARC_N과 ARC_FINAL의 목적을 분리한다.

### ARC_N — 20 items
CONTENT LAYER:
- CORE_EXAM_POINT 14~16
- ADVANCED_DISCRIMINATION 4~6

DIFFICULTY:
- D1 0~10%
- D2 25~35%
- D3 35~45%
- D4 15~25%
- D5 0~5%
- D4+D5 기본 20~30%

ARC_N은 쉬워지는 것이 아니라,
핵심 범위에서 오답 경쟁력과 표준 적용을 강화하고
심화 과업의 비중을 20~30%로 제한하는 것이다.

명시적 고난도 N제 요청 또는 검증된 학교 앵커가 있으면 난도/ADVANCED 비율을 상향할 수 있다.

### ARC_FINAL — 20 items (앵커가 없는 과목·범위의 임시 하한 곡선; 앵커가 있으면 §23이 우선)
D1 0~5%
D2 10~20%
D3 40~50%
D4 25~35%
D5 5~10%
SCHOOL_RELATIVE=BELOW_SCHOOL target = 0
D4+D5 target >= 30%

학교 실제 기출의 검증된 난도 곡선이 있으면 그 곡선을 우선한다.
단, '기출을 닮았다'는 추정만으로 하한을 낮추지 않는다.

### OPTION COMPETITION DIFFICULTY CORRECTION
난도 점수는 선지 경쟁력이 낮으면 자동 하향한다.
- D3+인데 STRONG_DISTRACTOR_COUNT < 2 → 최대 D2
- D4/D5인데 EFFECTIVE_CHOICE_COUNT < 4 → 최대 D3
- IMMEDIATE_ELIMINATION_COUNT >= 3 → 최대 D2~D3 재분류
- CORRECT_OPTION이 길이/구체성 단서로 쉽게 식별되면 REASONING_DEPTH와 DISTRACTOR_STRENGTH를 재산정
- FIRST_PASS_PLAUSIBLE_CANDIDATES <= 2인 D3+ → DIFFICULTY_INFLATION_FAIL

난이도는 '내용이 어려워 보임'이 아니라 학생이 실제로 수행하는 구분·추론 부담으로 산정한다.

### FINAL POSITION CURVE
FINAL은 문항 순서까지 난도 설계에 포함한다.
- 초반: SCHOOL_STANDARD 중심이되 직접회상 연속 금지
- 중반: D3 자료/적용형 중심
- 후반 30%: D4+ 최소 2문항 권장
- D5는 억지 함정/장문노동이 아니라 정당한 통합추론으로만 사용




## 23. N° / FINAL DIFFICULTY DECOUPLING — 2026-09-26 USER DIRECTIVE

### ARC_N
ARC_N은 동북고 실제 시험의 난도 분포와 일치할 의무가 없다.

목적:
- 기본문제 → 표준 적용 → 심화문제의 학습 사다리
- 핵심 시험범위 coverage
- 오답 경쟁력과 다양한 판단축
- 학생이 약한 개념을 단계적으로 반복

따라서 다음을 ARC_N RELEASE 조건으로 사용하지 않는다:
- 학교시험 평균 난도 일치
- 학교시험 D12/D3/D45 비율 일치
- 학교시험 후반부 변별 문항 위치 일치

ARC_N에서 실제 기출 난도는 참고자료일 뿐이다.
단, 너무 쉬운 문제만 반복하거나 심화만 과도하게 몰리는 것을 막는 ARC_N_BALANCE_GATE는 유지한다.

### ARC_FINAL
ARC_FINAL은 모의고사이므로 난도 조절이 핵심이다.
FINAL은 과목별 실제 동북고 시험 난도 코퍼스에 맞춘다.

SOURCE:
quality/anchors/DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0.yaml

ACTIVE SUBJECT ANCHORS:
- KOR: quality/anchors/KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml
- SOC: quality/anchors/SOC_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml
- SCI-REDOX: quality/anchors/SCI_REDOX_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml
- HIS: FINAL 비활성. diagnostic profile만 존재.

FINAL은 한 시험 하나를 복제하지 않는다.
여러 실제 시험의 난도 분포와 변동폭을 앙상블하여 학교 난도대를 재현한다.

### CALIBRATION AXES
FINAL_DIFFICULTY는 최소 다음을 동시에 비교한다.
1. D1+D2 share
2. D3 share
3. D4+D5 share
4. mean difficulty level
5. late-section discrimination
6. expected time-class distribution
7. subject-specific data/condition load

평균만 맞고 분포가 무너지면 FAIL.
분포만 맞고 평균이 크게 벗어나도 FAIL.

### TARGET OFFSET — 2026-11-08 USER DIRECTIVE (PROVISIONAL)
목표는 "동북고 평균 난이도보다 조금 더 어렵게"다. 과목 앵커 평균에 +0.1~+0.3(중심 +0.2)을 더한 값을 FINAL 목표 평균으로 한다.
- 공통 하한(D4+D5 ≥ 30%)은 폐지하고 과목별 앵커 분포에 오프셋을 반영해 사용한다.
- 오프셋 수치는 사용자 확인 전까지 PROVISIONAL이며 ops/exams/EXAM_CONTEXTS_V1.yaml이 값을 보유한다.
- 평균과 분포 형태가 모두 맞아야 한다(아래 CALIBRATION AXES).

### DIFFICULTY ADJUSTMENT
FINAL이 학교보다 쉬운 경우:
- D1/D2를 말만 어렵게 고치지 않는다.
- 학교 빈출 task family를 유지한 채 HALF_TRUE / 조건누락 / 복수근거 / 자료 비교를 강화한다.
- weak distractor를 strong near-miss로 교체한다.
- 동일 핵심개념에서 reasoning step을 1단계 늘리는 방식 우선.
- 범위 밖 지식·지엽 암기·장문노동으로 올리지 않는다.

FINAL이 학교보다 어려운 경우:
- 핵심 개념이나 범위를 삭제하지 않는다.
- 동시에 관리해야 하는 조건 수를 줄인다.
- 자료량/계산량을 학교 기출 수준으로 낮춘다.
- 오답 품질은 유지하되 near-miss의 겹침을 완화한다.
- 낯선 형식 자체로 생긴 난도를 제거한다.

### DIRECT-SCOPE PRIORITY
현재 범위와 직접 겹치는 실제 기출 문항군이 있으면 가장 높은 가중치를 준다.
예: SCI-REDOX는 2025-2 중간 실제 산화·환원 8~12번을 직접범위 앵커로 사용한다.

### NO TEACHER-STYLE PREDICTION
과거 시험은 난도·구조·업무량 보정용이다.
교사의 다음 문제를 예측하거나 과거 문구/선지를 복제하지 않는다.

END ARC DIFFICULTY ENGINE V1.5
