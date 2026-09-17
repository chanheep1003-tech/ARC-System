---
name: arc-item-qa
description: 'ARC 문항을 기준참조형 rubric으로 검수해 PASS/REVISE/DISCARD를 결정한다. 정답 유일성, 범위, 추론, 오답, 자연스러움, 학교 적합성, 시각자료를 통합 평가한다.'
metadata:
  version: 1.0.0
  arc-role: item-quality-gate
---
# ARC Item QA

## 목적
막연한 “좋은 문제” 평가가 아니라 **관찰 가능한 문항 특성**으로 판정한다.

## 선행 규칙
기존 `quality/ARC_QA_BENCH_V1.0.md`와 `quality/ARC_ITEM_QUALITY_RUBRIC_V1.0.md`가 기준이다. 이 skill은 둘을 실행 순서로 묶는다.

## 평가 순서
### 1. Hard Fail Gate
범위 밖, 정답 다중/부재, 키 불일치, 필수 자료 누락, 제외범위 침입, 사실오류, 저작권 과복제 등을 먼저 확인한다.

### 2. Criterion Review
- Validity
- Clarity
- Distractor realism
- Reasoning quality
- School difficulty fit
- Originality
- Information efficiency
- Asset functionality

각 기준은 “좋다/나쁘다” 대신 실제 문항에 무엇이 존재하는지 기술한다.

### 3. Calibration Note
경계 사례는 왜 평가자가 갈릴 수 있는지 한 줄 기록한다. 예: “정답은 유일하지만 ③이 교과서 문맥 밖에서는 참으로 읽힐 수 있어 조건 보강 필요.”

### 4. Decision
- `PASS`: 바로 세트 편집 가능
- `REVISE`: 수정 포인트가 국소적
- `DISCARD`: 문항 골격 자체가 불량

## QA 원칙
- 점수가 높아도 Hard Fail 하나면 PASS 불가.
- 난도가 높다는 이유만으로 품질 점수를 올리지 않는다.
- 문항 검수와 세트 검수는 분리한다.
- 답지 검증은 독립적으로 한 번 더 수행한다.
