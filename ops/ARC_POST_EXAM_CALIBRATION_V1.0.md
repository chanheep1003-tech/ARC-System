# ARC POST-EXAM CALIBRATION V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: DORMANT-UNTIL-ACTUAL-EXAM
ROLE: evidence-based calibration after the real school exam

## TRIGGER
실제 해당 시험지가 확보된 뒤에만 실행한다.
시험 전에는 이 문서를 근거로 다음 시험 출제를 예측하지 않는다.

## COMPARE
실제 시험 vs 시험 전 ARC N°/FINAL:
- scope coverage
- actual vs ARC difficulty
- broad item forms
- material/visual usage
- reasoning forms
- distractor strength
- missed concepts
- overprepared concepts
- time/density
- factual/visual failure if any

## OUTPUT
- ACTUAL_EXAM_REFERENCE_RECORD
- CALIBRATION_DELTA
- MISSED_COVERAGE
- OVERPREPARED_AREAS
- DIFFICULTY_DELTA
- QA_FAILURE_LESSONS
- candidate rule patches

## UPDATE RULE
업데이트는 관찰된 evidence weight와 reference profile에 한정한다.
“다음 시험도 같은 패턴”이라는 예측 규칙을 만들지 않는다.
MASTER 변경은 별도 regression fixtures를 통과해야 한다.

END ARC POST-EXAM CALIBRATION V1.0
