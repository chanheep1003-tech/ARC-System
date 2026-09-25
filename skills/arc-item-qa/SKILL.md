---
name: arc-item-qa
description: 'ARC 문항을 기준참조형 rubric으로 검수해 PASS/REVISE/DISCARD를 결정한다. 정답 유일성, 범위, 추론, 오답, 자연스러움, 학교 적합성, 시각자료를 통합 평가한다.'
metadata:
  version: 1.4.0
  arc-role: item-quality-gate
---
# ARC Item QA

## 목적
막연한 “좋은 문제” 평가가 아니라 관찰 가능한 문항 특성과 근거로 판정한다.
자동 QA의 점수 인플레이션과 형식상 PASS를 차단한다.

## 선행 규칙
- quality/ARC_QA_BENCH_V1.2.md
- quality/ARC_ITEM_QUALITY_RUBRIC_V1.1.md
- 필요 시 quality/ARC_VISUAL_AUTHENTICITY_RUBRIC_V1.1.md
- quality/ARC_SIMILARITY_GUARD_V1.1.md
- quality/visual/ARC_VISUAL_PASS_AB_V1.0.md
- 자동화 실행 시 ops/ARC_AUTOMATION_RUNTIME_V1.0.md
- 해당 과목 `quality/gold/*_GOLD_ANCHORS_V1.0.md`
- quality/ARC_SOURCE_LEDGER_V1.0.md

## 평가 순서
### 1. Hard Fail Gate
범위 밖, 정답 다중/부재, 키 불일치, 필수 자료 누락, 제외범위 침입, 사실오류, 저작권 과복제 등을 먼저 확인한다.

### 2. Anchor Comparison
초안을 가장 가까운 GOOD/BAD 앵커와 비교한다.
- GOOD보다 어떤 평가 요소가 부족한지 기록
- BAD와 같은 결함이 있으면 해당 상한/판정을 상속
- 문장 표현이 비슷하다는 이유가 아니라 추론 구조·자료 기능·오답 현실성으로 비교

### 3. Evidence-Based Criterion Review
각 항목마다 점수와 한 줄 근거를 남긴다.
- Validity
- Clarity
- Distractor realism
- Reasoning quality
- School/current-material fit
- Originality
- Information efficiency
- Asset functionality

'검토 완료', '적절함', 'independently checked'만 기록하는 것은 금지한다.

### 4. Anti-Inflation Ceilings
V1.1의 DIRECT_RECALL, WEAK_DISTRACTOR, GENERIC_CONTEXT, UNGROUNDED_STYLE 상한을 적용한다.
상한이 적용되면 총점이 상한을 넘을 수 없다.

### 5. Difficulty Cross-Check
D3 이상은 실제로 자료·조건·다단계 추론 부담이 있는지 확인한다.
1단계 직접개념 문항을 D3+로 표기하면 REVISE한다.

### 6. Sentinel Recheck
과목 20문항 세트에서 최소 4문항을 독립 재검수한다.
점수 차이 6점 이상 또는 PASS/REVISE 반전 시 과목 전체를 재채점한다.

### 7. Source Verification Gate
SOURCE_REQUIRED=true인 문항은 PASS B에서 ANSWER_BASIS SOURCE_ID를 실제로 재열람한다.
모두 VERIFIED여야 BANK_PASS 후보가 된다.
UNVERIFIED면 STUDY_DRAFT/REVISE, SOURCE_MISSING 또는 SOURCE_CONFLICT 정답근거가 있으면 DISCARD/BLOCKED 처리한다.

### 8. Similarity Gate
실행 가능한 로컬/CI 환경이면 sentence-transformers + Qdrant quantitative similarity를 사용한다.
THRESHOLD_STATUS=CALIBRATION_REQUIRED이면 raw cosine은 참고값이며 구조판정을 대체하지 않는다.
CALIBRATED 이후 CRITICAL은 DISCARD, HIGH는 원칙적으로 REVISE한다.
정량 도구를 실행하지 못하면 TOOLING_UNAVAILABLE을 기록하고 기존 structural guard를 수행한다.

### 9. Visual Gate
ESSENTIAL visual은 VISUAL_PASS_A=PASS, VISUAL_PASS_B=PASS, QUESTION_VISUAL_CROSSCHECK=PASS가 필수다.
하나라도 없거나 FAIL이면 BANK/FINAL 후보 금지.

### 10. Decision
- PASS: 세트 편집/BANK 후보
- REVISE: 국소 수정 후 처음부터 재검증
- DISCARD: 문항 골격 불량 또는 hard fail

## QA 원칙
- 점수가 높아도 Hard Fail 하나면 PASS 불가.
- 난도가 높다는 이유로 품질 점수를 올리지 않는다.
- 직접 개념 확인형은 깔끔하다는 이유만으로 PREMIUM이 될 수 없다.
- 문항 검수와 세트 검수는 분리한다.
- 답지 검증은 독립적으로 한 번 더 수행한다.
- 점수 분포가 기계적으로 반복되면 전체 재검토한다.
