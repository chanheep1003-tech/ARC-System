# ARC_SET_EDITORIAL_ENGINE_V1.0
VERSION: 1.0
DATE: 2026-09-17
STATUS: ACTIVE
ROLE: ARC N°/FINAL 세트 단위 편집 품질 관리

## PURPOSE
개별 문항이 우수해도 세트 전체가 반복적이면 AI 티가 난다.
20~40문항을 '문항 모음'이 아니라 실제 시중 문제집 편집자가 구성한 세트처럼 설계한다.

## 1. SET EDITORIAL SCORE — 100
- CONCEPT_COVERAGE /20
- QUESTION_FORM_DIVERSITY /15
- REASONING_DIVERSITY /15
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
- 같은 ㄱㄴㄷ 구조/자료형 과다 반복
- 모든 문제 길이가 비슷함
- 모든 선지가 비슷한 리듬/길이
- 동일 오답 원리 3문항 이상 반복
- 자료형 문항이 특정 구간에만 몰림
- D4/D5가 끝부분에 기계적으로만 몰림
- 개념 순서가 교과서 목차를 그대로 따라가며 변주 없음
- 정답번호 패턴이 인위적으로 규칙적임
- 시각자료가 일정 간격으로 기계적으로 배치됨

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
REASONING_DISTRIBUTION:
DIFFICULTY_DISTRIBUTION:
VISUAL_DISTRIBUTION:
DISTRACTOR_DISTRIBUTION:
AI_SET_FLAGS: []
SET_EDITORIAL_VERSION: ARC-SEE-V1.0

## 7. RELEASE
문항별 PREMIUM_BANK_A 비율이 높아도 SET_EDITORIAL이 FAIL이면 출판하지 않는다.
좋은 문제를 일부 교체해서 전체 리듬을 살리는 것을 허용한다.

END ARC SET EDITORIAL ENGINE V1.0
