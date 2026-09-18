# ARC SCHOOL REFERENCE PROFILE V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: lightweight historical school-exam reference

## PURPOSE
과거 학교시험을 다음 시험의 교사 스타일 예측에 사용하지 않고 난이도·자료밀도·큰 형식의 참고치로만 보존한다.

## REFERENCE RECORD
각 시험은 최소:
- YEAR
- TERM / EXAM
- SUBJECT
- ITEM_COUNT
- TEACHER_RELATION: SAME / DIFFERENT / UNKNOWN
- BROAD_FEATURES:
  - MATERIAL_BASED: LOW/MEDIUM/HIGH
  - VISUAL_USAGE: LOW/MEDIUM/HIGH
  - MULTI_CONDITION_REASONING: LOW/MEDIUM/HIGH
  - DIRECT_RECALL: LOW/MEDIUM/HIGH
- ROUGH_DIFFICULTY: LOW/STANDARD/UPPER/EXTREME
- CONFIDENCE: LOW/MEDIUM/HIGH
- SOURCE_FILE_ID / PAGE(optional)

## RESTRICTIONS
- teacher_style_prediction = disabled
- exact item-type frequency prediction = disabled
- exact difficulty-position prediction = disabled
- wording imitation = disabled
- current worksheet/textbook/scope always override historical reference
- different-teacher exams are difficulty/broad-format reference only

## USAGE
허용:
- 학교 평균 난도 감각
- 자료형/시각자료의 대략적 밀도
- 실전 세트의 너무 쉬움/너무 어려움 경고

금지:
- “올해도 이 유형이 나온다”
- “이 교사는 이 선지를 좋아한다”
- 과거 비율을 현재 출제 비율로 강제

END ARC SCHOOL REFERENCE PROFILE V1.0
