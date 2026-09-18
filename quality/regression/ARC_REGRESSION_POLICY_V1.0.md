# ARC REGRESSION POLICY V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: fixed regression fixture governance for ARC QA/engine changes

## 0. PURPOSE
MASTER, QA rubric, generation engine, source rules, difficulty rules를 바꾼 뒤 기존의 좋은 판정과 나쁜 판정이 깨지지 않았는지 고정 입력으로 확인한다.
회귀 테스트는 '새 문제를 더 잘 만들었는가'가 아니라 '기존에 맞던 판정이 망가지지 않았는가'를 본다.

## 1. FIXTURE SOURCE
초기 V1.0 fixture는 과목별 GOLD ANCHOR PACK의 GOOD 3 + BAD 3을 사용한다.
총 30개:
- KOR 6
- SCI 6
- SOC 6
- HIS 6
- AI 6

GOLD anchor 문장을 복사해 별도 파일에 중복 저장하지 않고, fixture는 anchor ID와 고정 기대결과를 참조한다.
Anchor pack 자체가 바뀌면 fixture baseline이 자동으로 바뀌는 것으로 간주하지 않는다. Anchor 변경은 fixture 버전 변경 또는 명시적 re-baseline이 필요하다.

## 2. EXPECTED OUTCOME
각 fixture는 최소 다음을 고정한다:
- fixture_id
- subject
- anchor_id
- class: GOOD | BAD
- expected_decision
- expected_item_min / expected_item_max 또는 expected_max_item
- expected_hard_fail
- forbidden_decisions
- regression_reason

GOOD fixture:
- 기대 판정이 BANK_A이면 REVISE/DISCARD는 regression fail
- ITEM score가 기대 범위보다 3점 이상 벗어나면 score drift
- Hard Fail 발생 시 fail

BAD fixture:
- 기대 REVISE를 BANK_A/PREMIUM으로 올리면 fail
- 기대 DISCARD를 PASS/BANK로 올리면 hard regression
- expected_max_item을 3점 이상 초과하면 score inflation regression

## 3. DECISION SEVERITY
GOOD → REVISE/DISCARD: FAIL
BAD-REVISE → BANK_A/PREMIUM: FAIL
BAD-DISCARD → REVISE: WARN only if hard-fail semantics remain blocked from BANK
BAD-DISCARD → PASS/BANK: FAIL
GOOD score drift within ±2: allowed
GOOD score drift ±3~5: WARN
GOOD score drift >5: FAIL unless rubric-version change has explicit migration note

## 4. WHEN TO RUN
반드시 실행:
- COMMON GENERATION ENGINE 변경
- subject MASTER의 구조/QA 규칙 변경
- ARC_ITEM_QUALITY_RUBRIC 변경
- ARC_QA_BENCH 변경
- arc-item-qa / arc-fact-audit / arc-distractor-engine 변경
- difficulty engine/anchors 변경
- source verification rule 변경
- BANK promotion rule 변경

선택 실행:
- 단순 문서 오탈자
- README/경로 설명
- 실행에 영향 없는 주석

## 5. RUN PROTOCOL
1. 변경 전 baseline version 기록
2. 동일 fixture set 로드
3. candidate QA/engine으로 30개 fixture 재평가
4. expected decision/score/hard-fail과 비교
5. PASS/WARN/FAIL 집계
6. FAIL 하나라도 있으면 main promotion 금지
7. 결과를 ops/RUN_LOG에 남김

## 6. FREEZE / CHANGE CONTROL
fixture는 테스트를 통과시키기 위해 즉석 수정하지 않는다.
기대값을 바꾸려면:
- 왜 기존 기대값이 잘못됐는지 근거
- old expected / new expected
- 영향을 받는 rubric/MASTER version
- re-baseline reason
- changelog
를 남기고 fixture version을 올린다.

## 7. EXPANSION
V1.0은 GOLD 30개로 시작한다.
향후 실제 QA에서 검증된 대표 문항을 추가할 수 있다.
추가 우선순위:
- 실제 학교 시험형 자료문항
- C_X_MARK hard-fail
- REDOX_LEDGER
- 역사 chronology overlap
- DFS/BFS underspecified
- source-ledger missing/reopen failure
- visual/data mismatch

fixture 수를 무작정 늘리지 않는다. 새로운 실패 클래스를 대표하는 케이스만 추가한다.

END ARC REGRESSION POLICY V1.0