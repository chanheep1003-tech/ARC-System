---
name: arc-item-generator
description: 'ARC N°/FINAL용 고품질 객관식 문항을 범위·난도·학교 벤치에 맞춰 생성한다. COMMON_GENERATION_ENGINE과 과목 MASTER를 보조하며 문항 자체의 추론 구조와 시험 적합성에 집중한다.'
metadata:
  version: 1.1.0
  arc-role: generation
---
# ARC Item Generator

## 목적
교과서 문장 재진술이 아니라 **조건 해석, 자료 적용, 관계 추론, 개념 구분**을 요구하는 학교 시험형 문항을 만든다.

## 선행 입력
1. `SYSTEM_MANIFEST.yaml`
2. 해당 과목 MASTER
3. `ARC_SCOPE_LEDGER`
4. 필요 시 SOURCE_PACKET / RESEARCH_PACKET
5. `ARC_SCHOOL_DIFFICULTY_BENCH`
6. 해당 과목 `quality/gold/*_GOLD_ANCHORS_V1.0.md`

## GOLD ANCHOR CALIBRATION
- 생성 전에 해당 과목 GOOD 3 + BAD 3을 읽는다.
- 초안마다 `NEAREST_GOOD_ANCHOR`, `NEAREST_BAD_ANCHOR`, `ANCHOR_MATCH_NOTE`를 내부 설계 카드에 기록한다.
- GOOD의 문장 표면을 모방하지 않고, 자료 기능·추론 단계·오답 강도·정보 밀도를 비교한다.
- BAD와 구조적으로 가까우면 해당 BAD의 score ceiling 또는 DISCARD 사유를 생성 단계부터 적용한다.
- 앵커는 현재 범위/학습지/교과서보다 우선하지 않는다.

## 생성 규칙
- 출제 의도보다 학생이 실제로 수행할 사고과정을 먼저 설계한다.
- 문항마다 `PRIMARY_CONCEPT_ID`를 내부 메타데이터로 둔다.
- 정답 도출에 필요한 정보와 조건을 충분히 주되 불필요한 설명은 제거한다.
- 단순 암기, 말장난, 비정상적으로 지엽적인 지식으로 난도를 만들지 않는다.
- 고난도는 정보량이 아니라 관계 수, 조건 결합, 오답 간 경계, 추론 단계로 만든다.
- 정답 선지는 원문 복사보다 의미 보존형 재진술을 우선한다.
- 자료형 문항은 자료가 실제 풀이에 필요해야 한다.

## 내부 설계 카드
- concept
- target difficulty
- reasoning steps
- required conditions
- evidence/material
- answer path
- distractor axes
- visual requirement
- copyright transformation note
- nearest good anchor
- nearest bad anchor
- anchor match note

## 생성 후 즉시 넘길 skill
객관식이면 `arc-distractor-engine` → 필요 시 `arc-visual-renderer` → `arc-fact-audit` → `arc-item-naturalness-audit` → `arc-item-qa`.

## Hard Fail
- 범위 밖 지식 없이는 풀 수 없음
- 정답이 0개 또는 2개 이상
- 지문/자료 없이도 보기 패턴만으로 풀림
- 교과서/기출 문장을 과도하게 복제
- 고난도를 계산량·독해량으로만 위장
