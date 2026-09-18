---
name: arc-eval-regression
description: 'ARC 엔진·MASTER·QA 규칙 변경 전후의 품질 회귀를 고정 fixture로 검출한다. 30개 frozen fixture와 기대 판정을 사용해 버전 비교할 때 사용한다.'
metadata:
  version: 1.1.0
  arc-role: regression-evaluation
---
# ARC Eval Regression

## 목적
엔진을 고친 뒤 느낌상 좋아졌다고 판단하지 않고, **같은 고정 입력이 같은 품질 판정을 유지하는지** 확인한다.

## 활성 기준
- quality/regression/ARC_REGRESSION_POLICY_V1.0.md
- quality/regression/REGRESSION_FIXTURES_V1.0.yaml
- quality/ARC_QA_BENCH_V1.2.md

## Frozen Dataset
V1.0은 과목별 GOLD GOOD 3 + BAD 3을 참조한다.
총 30 fixtures:
- KOR 6
- SCI 6
- SOC 6
- HIS 6
- AI 6

fixture는 anchor ID를 참조하되 expected decision/score/hard-fail을 별도로 고정한다.
테스트를 통과시키기 위해 fixture 기대값을 즉석 수정하지 않는다.

## 반드시 실행하는 변경
- COMMON ENGINE
- subject MASTER의 구조/QA 규칙
- ITEM QUALITY RUBRIC
- QA BENCH
- item QA / fact audit / distractor engine
- difficulty engine/anchors
- SOURCE_LEDGER 판정 규칙
- BANK promotion rule

단순 README/오탈자 변경은 생략 가능.

## 절차
1. 변경 전 baseline version과 변경 목적을 기록한다.
2. REGRESSION_FIXTURES_V1.0 30개를 로드한다.
3. 각 anchor 입력을 candidate 규칙으로 재평가한다.
4. expected decision, score range/ceiling, hard-fail 여부를 비교한다.
5. 결과를 PASS / WARN / FAIL로 분류한다.
6. FAIL 하나라도 있으면 main promotion 금지.
7. RUN_LOG/CHANGELOG에 요약을 남긴다.

## 판정
### GOOD
- expected BANK_A → REVISE/DISCARD면 FAIL
- expected score에서 ±2는 허용
- ±3~5는 WARN
- 5점 초과 drift는 FAIL
- 새 Hard Fail은 FAIL

### BAD-REVISE
- BANK_A/PREMIUM으로 승격되면 FAIL
- expected_max_item +3 초과 시 score inflation FAIL

### BAD-DISCARD
- PASS/BANK 승격은 FAIL
- REVISE로 바뀌어도 hard-fail semantics가 BANK를 막으면 WARN
- hard fail이 사라져 BANK 가능해지면 FAIL

## Release Gate
- regression_fail_count = 0
- 새로운 hard-fail class 없음
- GOOD fixture의 구조적 품질 판정 유지
- BAD fixture가 고득점/은행으로 역승격되지 않음

## 금지
- 변경 때마다 benchmark를 바꿔 개선처럼 보이게 하기
- 개인 학생 오답을 regression fixture로 사용
- fixture 기대값을 후보 규칙에 맞춰 수정
- 30개 중 일부만 돌리고 전체 통과라고 보고

END ARC EVAL REGRESSION V1.1
