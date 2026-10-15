# ARC_SET_EDITORIAL_ENGINE_V1.2
VERSION: 1.2
DATE: 2026-09-17
STATUS: ACTIVE
ROLE: ARC N°/FINAL 세트 단위 편집 품질 관리

## PURPOSE
개별 문항이 우수해도 세트 전체가 반복적이면 AI 티가 난다.
20~40문항을 '문항 모음'이 아니라 실제 시중 문제집 편집자가 구성한 세트처럼 설계한다.

## 1. SET EDITORIAL SCORE — 100
- CONCEPT_COVERAGE /20
- QUESTION_FORM_DIVERSITY /10
- QUESTION_TASK_DIVERSITY /10
- REASONING_DIVERSITY /10
- DIFFICULTY_FLOW /15
- VISUAL_RHYTHM /10
- DISTRACTOR_DIVERSITY /10
- LANGUAGE_RHYTHM /10
- ANSWER_PATTERN_SANITY /5

## 2. PASS
92~100 SET_A
86~91 SET_B
80~85 REVISE
79 이하 FAIL

ARC FINAL은 원칙적으로 SET_A 요구.
ARC N°는 SET_A/B만 출판 후보.

## 3. AI SET PATTERN FAIL
- 같은 발문 뼈대 3문항 이상 연속
- SINGLE_BEST_STATEMENT가 세트의 지배 형식이 되어 다른 판단 과업이 사라짐
- 긍정형 과다를 해결한다며 EXCEPT/옳지 않은 것만 대량 추가
- 동일 QUESTION_TASK_FORM 4문항 이상 연속
- 같은 ㄱㄴㄷ 구조/자료형 과다 반복
- 모든 문제 길이가 비슷함
- 모든 선지가 비슷한 리듬/길이
- 동일 오답 원리 3문항 이상 반복
- 자료형 문항이 특정 구간에만 몰림
- D4/D5가 끝부분에 기계적으로만 몰림
- 개념 순서가 교과서 목차를 그대로 따라가며 변주 없음
- 정답번호 패턴이 인위적으로 규칙적임
- ITEM_COUNT >= 10인데 특정 정답 번호가 0회
- 동일 정답 번호 3연속 이상
- ①②③④⑤ 같은 단순 주기 반복
- 정확한 균등분배를 목표로 선지 순서를 기계적으로 맞춘 흔적
- 시각자료가 일정 간격으로 기계적으로 배치됨

## 3-1. ANSWER POSITION EDITORIAL AUDIT
5지선다 세트의 정답 위치는 '완전 균등'이 아니라 '비예측 가능하면서 과도한 편향이 없는 분포'를 목표로 한다.

EXPECTED = ITEM_COUNT / 5
SOFT_MIN = max(1, floor(EXPECTED)-1)
SOFT_MAX = ceil(EXPECTED)+1

예:
- 20문항: 각 번호 3~5회 권장
- 30문항: 각 번호 5~7회 권장

규칙:
- SOFT BAND 이탈은 즉시 HARD FAIL이 아니라 EDITORIAL_FLAG이며, 정당한 이유가 없으면 재배열한다.
- exact equal distribution은 허용되지만 목표값으로 강제하지 않는다.
- 분포 수정은 실제 선지 reorder로만 수행한다. answer label만 바꾸지 않는다.
- reorder 후 ITEM별 UNIQUE_ANSWER + ANSWER_KEY_SYNC + PASS A/B를 다시 확인한다.
- 표형/조합형/OX형은 단순 shuffle 과정에서 대응관계가 깨지기 쉬우므로 별도 재검산한다.

ANSWER_PATTERN_FLAGS:
ZERO_SLOT
THREE_PLUS_STREAK
PERIODIC_SEQUENCE
OUTSIDE_SOFT_BAND
MECHANICAL_EQUALIZATION
ANSWER_KEY_DESYNC

## 3-2. QUESTION TASK-FORM AUDIT
문항별 QUESTION_TASK_FORM을 기록한다.

기본 분류:
SINGLE_BEST_STATEMENT
EXCEPT_INCORRECT
MULTI_JUDGMENT
PAIR_MATCH
SEQUENCE_ORDER
CASE_APPLICATION
EVIDENCE_SUPPORT
ERROR_CORRECTION
DATA_INFERENCE
CONDITION_CHANGE
SOURCE_IDENTIFICATION
COMPARISON_MATRIX

20문항 이상 기본 기준:
- SINGLE_BEST_STATEMENT <= 40%
- SINGLE_BEST_STATEMENT + EXCEPT_INCORRECT <= 60%
- NEGATIVE STEM <= 25%
- 사용 task form >= 5
- transformed task forms 합계 >= 35%

transformed task forms:
MULTI_JUDGMENT / PAIR_MATCH / SEQUENCE_ORDER / CASE_APPLICATION /
EVIDENCE_SUPPORT / ERROR_CORRECTION / DATA_INFERENCE /
CONDITION_CHANGE / SOURCE_IDENTIFICATION / COMPARISON_MATRIX

위 기준은 과목 특성에 따라 MASTER가 조정할 수 있으나,
단일 '옳은 설명 고르기' 형식이 지배하는 세트는 SET_A를 받을 수 없다.

QUESTION_TASK_FLAGS:
SINGLE_BEST_OVERUSE
NEGATIVE_OVERUSE
TASK_FORM_LOW_DIVERSITY
TASK_FORM_STREAK
SURFACE_VARIATION_ONLY

SURFACE_VARIATION_ONLY:
발문 문구만 바뀌었고 실제 학생 과업이 계속 동일한 경우.

## 4. COMMERCIAL SET RHYTHM
실제 상용 문제집처럼:
- 직접확인형과 자료형을 초반부터 혼합
- 짧은 문항/중간 문항/긴 자료형의 길이 리듬 변주
- 같은 개념도 다른 reasoning form으로 변주
- 고난도는 단순히 뒤에 몰지 않고 필요 시 중간에도 배치
- 시각자료는 내용상 필요할 때만 사용
- 세트 전체에서 '한 사람이 같은 틀로 20개 만든 느낌' 제거

## 5. PRODUCT MODE
### ARC_N
개념 커버리지 + 유형 다양성 + 난도 계단을 우선.
같은 CONCEPT_ID를 반복할 때는 질문형/자료형/오답원리 중 최소 2개를 변경.

### ARC_FINAL
동북고 실제 시험의 문항 길이, 자료밀도, 난도 흐름, 시각자료 배치, 고난도 위치를 우선.
상용 N제처럼 과하게 다양하게 만들지 말고 실제 시험 리듬을 모사.

## 6. SET METADATA
SET_EDITORIAL_SCORE:
SET_EDITORIAL_TIER:
FORM_DISTRIBUTION:
TASK_FORM_DISTRIBUTION:
STEM_POLARITY_DISTRIBUTION:
REASONING_DISTRIBUTION:
DIFFICULTY_DISTRIBUTION:
VISUAL_DISTRIBUTION:
DISTRACTOR_DISTRIBUTION:
ANSWER_DISTRIBUTION:
ANSWER_PATTERN_FLAGS: []
QUESTION_TASK_FLAGS: []
AI_SET_FLAGS: []
SET_EDITORIAL_VERSION: ARC-SEE-V1.2

## 7. RELEASE
문항별 PREMIUM_BANK_A 비율이 높아도 SET_EDITORIAL이 FAIL이면 출판하지 않는다.
좋은 문제를 일부 교체해서 전체 리듬을 살리는 것을 허용한다.

END ARC SET EDITORIAL ENGINE V1.2
