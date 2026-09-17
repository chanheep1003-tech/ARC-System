---
name: arc-eval-regression
description: 'ARC 엔진·MASTER·QA 규칙 변경 전후의 품질 회귀를 검출한다. 검증문항은행과 고정 benchmark set을 golden dataset으로 사용해 버전 비교할 때 사용한다.'
metadata:
  version: 1.0.0
  arc-role: regression-evaluation
---
# ARC Eval Regression

## 목적
엔진을 고친 뒤 “느낌상 좋아졌다”로 끝내지 않고 **고정 평가세트에서 실제로 악화된 항목이 없는지** 확인한다.

## Golden Dataset
개인 오답 데이터가 아니라 다음만 사용한다.
- QA PASS 검증문항
- 학교 난도 anchor
- 반복적으로 문제가 됐던 회귀 사례
- 과목별 대표 문항 구조

## 변경 전후 비교 항목
- 범위 위반 수
- 정답 유일성 실패 수
- 사실오류 수
- ITEM QUALITY 점수
- commercial/editorial naturalness
- distractor realism
- visual hard fail
- similarity 반복
- set-level diversity
- difficulty distribution drift

## 절차
1. 변경 목적과 기대효과를 선언한다.
2. 동일 입력/범위로 baseline과 candidate를 생성한다.
3. 가능한 한 동일 rubric과 판정 순서를 적용한다.
4. 개선과 악화를 항목별로 나눈다.
5. 중대한 회귀 하나라도 있으면 main 승격을 중단한다.
6. 결과를 `ops/RUN_LOG`와 변경 기록에 남긴다.

## Release Gate
- Hard Fail 증가 없음
- 핵심 품질지표의 의미 있는 하락 없음
- 새 규칙이 특정 과목만 과도하게 최적화하지 않음
- 범위·난도 분포가 의도치 않게 이동하지 않음

## 금지
- 매번 benchmark 자체를 바꿔 개선처럼 보이게 하기
- 개인 학생 성적을 golden dataset으로 사용
- 한두 개 예시만 보고 전체 엔진 승격
