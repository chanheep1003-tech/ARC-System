# ARC_DIFFICULTY_ENGINE_V1.0
VERSION: 1.0
DATE: 2026-09-17
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

난이도는 학생 PDF에 표시하지 않는다.
ARC N°/FINAL의 내부 설계와 문제은행 메타데이터에만 사용한다.

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

### ARC N° 기본
권장 시작 분포:
D1 10%
D2 25%
D3 35%
D4 25%
D5 5%

단, 과목 MASTER·학교 기출 분석이 우선한다.

N° 목적:
- D2~D4 중심
- 기본 확인만 과도하게 늘리지 않음
- D5는 소수의 변별형으로 제한
- 같은 CONCEPT_ID에서 난도 계단을 구성할 수 있음

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

DIFFICULTY_VERSION: ARC-DE-V1.0

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

경고:
- D1+D2 > 55% → TOO_EASY_WARNING
- D4+D5 > 50% → TOO_HARD_WARNING
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

END ARC DIFFICULTY ENGINE V1.0
