# ARC FALSE DIFFICULTY & OBSERVABLE DISTRACTOR GATE V1.0
VERSION: 1.0
DATE: 2026-11-07 (registered 2026-11-10)
STATUS: ACTIVE-DEV
APPLIES_TO: ARC_N / ARC_FINAL, all subjects
SUPPLEMENTS: manifest-selected item quality rubric (`active.quality.item_quality`)

## 0. WHY THIS FILE EXISTS
이 게이트는 2026-11-07에 폐기된 `archive/quality/ARC_ITEM_QUALITY_RUBRIC_V1.0.md`의 8절로 추가되어 실제 생성 경로에서 읽히지 않았다.
2026-11-10에 내용 변경 없이 이 파일로 옮기고 `SYSTEM_MANIFEST.yaml`의 `active.quality.false_difficulty_gate`로 등록했다.
현행 문항 품질 루브릭과 함께 읽으며, 과목 특수 규칙이 더 엄격하면 그 규칙이 우선한다.

## 1. GATE
정답률·풀이 시간 자료 없이 D3/D4/D5 라벨을 붙일 때는 '예상 난도'로 구분한다. 문제의 길이나 낯선 용어 자체는 난도 증거가 아니다.

- 5지 선지 각각 `판정(TRUE/FALSE/UNDETERMINED) + 독립 근거 + 오답 유인 이유 + 정확한 반박`이 내부에 존재해야 한다.
- 정답 번호를 가린 재풀이자가 원문 없이 표면 힌트만으로 3개 이상을 즉시 버리면 `OBVIOUS_ELIMINATION` / `WEAK_DISTRACTOR`로 REVISE.
- `모두, 오직, 항상, 전혀, 예외 없이` 자체는 금지어가 아니지만 근거 없는 단정이 정답 신호로 작동하면 교체한다.
- 문제에서 제공된 보기의 수치·개념을 그대로 복사/단순 부정해 답을 얻으면 D4/D5로 인정하지 않는다. 장문·표·기술어를 제거해도 정답이 유지되면 자료의 필요성을 재설계한다.
- D3는 서로 독립적인 적용 조건 2개 이상, D4는 3개 이상의 실질 추론 단계와 경쟁 오답 2개 이상, D5는 새로운 자료로의 전이 및 반례/예외 판단을 필수 검토한다. 과목 특수 규칙이 더 엄격하면 우선한다.
- 출처가 불분명하거나 원문 해석에 이견이 있는데 판정 조건이 주어지지 않으면 `UNDETERMINED`로 HOLD. 오류를 난도로 승격시키지 않는다.
- 품질 개선을 선언하려면 이전/이후 동일 조건의 QA 벤치 결과를 실제로 비교해야 한다. 정책 문구 수정만으로 품질 개선 완료라 하지 않는다.
