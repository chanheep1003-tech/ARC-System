# ARC SCHOOL ARCHETYPE GATE V1.1
VERSION: 1.1
DATE: 2026-11-26 (V1.0 2026-11-11)
STATUS: ACTIVE
ROLE: 문항을 확인된 학교 시험 원형에서 만들게 하는 생성 규칙이자 게이트
LEDGER: quality/school/ARC_SCHOOL_EVIDENCE_LEDGER_V1.0.yaml
KOR_GRAMMAR_LIBRARY: quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml
KOR_ORTHO_LIBRARY: quality/korean/ARC_KOR_ORTHO_ARCHETYPES_V2.0.yaml (V6 맞춤법 — 아래 §3-1 V2 검사 추가)
KOR_ORTHO_RULES: quality/korean/ARC_KOR_ORTHO_ITEM_RULES_V2.0.md
SUPERSEDES: quality/ARC_SCHOOL_ARCHETYPE_GATE_V1.0.md
TOOL: tooling/korean/archetype_gate.py

## 0. 왜 필요한가
2026-11-11 국어 V6 세트 A(50문항)는 정답성과 조판 게이트를 통과했지만 사용자에게 "동북고 내신 느낌이 아니다"라는 판정을 받았다.
원인: 문항을 개념에서 바로 만들었고, 실제 시험의 문항 형식이 어떤 게이트에도 없었다.
대부분이 <보기> 없는 "다음 중 바른 것은? + 문장 5개" 형식이었으나, 2025-2 기말 원안의 문법 문항은 모두 <보기>를 적용하는 형식이었다.

## 1. 생성 순서
1. 원형 선택: 라이브러리에서 문항 원형을 고른다. 원형에 없는 형식은 만들지 않는다.
2. 개념 대입: 현재 범위의 규정·개념과 새 예문을 넣는다. 기출의 문장과 선지는 쓰지 않는다.
3. 함정 설계: 오답 선지마다 함정 유형(trap)을 하나 지정한다.
4. 세트 편성: 단원 세트 안에서 같은 원형은 2회까지. 서답형을 포함한다.

## 2. 근거 등급
- D1 원안 직접 확인, D2 내부 기록, D3 외부 추정.
- 게이트와 문항 형식은 D1·D2 근거로만 정한다. D3는 생성 힌트로만 쓴다.
- D3를 올리려면 원안지와 대조한다. 어긋나면 장부의 rejected에 남긴다.
- 교사 개인 성향, 학생 집단 가정, 보유하지 않은 프린트 문구는 규칙으로 삼지 않는다.

## 3. 게이트 (번들에 `archetype_library`가 있으면 적용)
| 코드 | 실패 조건 |
|---|---|
| ARCHETYPE_UNREGISTERED | 문항의 `archetype`이 라이브러리에 없음 |
| VIEW_MISSING / VIEW_ANCHOR_RATE_LOW | 원형이 요구하는 <보기>가 없음 / <보기> 기반 문항 90% 미만 |
| TRAP_UNCLASSIFIED | 오답 선지에 함정 유형이 없음 |
| D1_RECALL_FORBIDDEN | D1 문항 |
| MASKED_SPACING | [ ]로 띄어쓰기를 가림 (분류 원형의 <보기 2> 제외) |
| SINGLE_WORD_OPTIONS | 단어 하나짜리 선지 |
| STUDENT_TEXT_SPOT_COUNT | 학생 글 원형의 표시가 6곳이 아님 |
| CR_CONDITIONS_SHORT / CR_RUBRIC_MISSING | 서답형 <조건> 3개 미만 / 모범답·채점 기준 없음 |
| CONSTRUCTED_RATIO_LOW | 서답형 비율 8% 미만 |
| ARCHETYPE_OVERUSE | 한 원형이 단원 세트당 2회 초과 |

이 게이트는 형식을 본다. 정답의 사실성은 독립 재풀이와 전 선지 근거 검수가 맡는다.

## 3-1. V2 맞춤법 검사 (2026-11-26 추가 — 라이브러리에 `item_contract`가 있으면 적용)
근거: 학교 기출 18개교 114문항 학습(`quality/korean/ARC_KOR_ORTHO_SCHOOL_EXAM_LEARNING_20261126.md`). 2026-11-23 V6 50문항이 형식 게이트는 통과했지만 띄어쓰기 쏠림·두음 법칙 0문항·가짜 난도로 다시 거절된 일을 막는다.

| 코드 | 실패 조건 |
|---|---|
| ORTHO_FIELD_MISSING | 문항에 topic / rules / judgment_units / levers가 없음 |
| TOPIC_UNKNOWN / LEVER_UNKNOWN | 라이브러리에 없는 주제·레버 |
| FAKE_DIFFICULTY_UNITS / _RULES / _LEVERS | 판정 단위·동원 조항·레버가 난도 하한 미만 (D3 4·1 / D4 8·2 / D5 12·2·레버 2) |
| ARCHETYPE_DIFFICULTY_OUT_OF_RANGE | 원형이 낼 수 없는 난도 (예: K11 괄호 고르기에 D5) |
| MARKED_SPOT_COUNT | K6 밑줄 수가 6~9곳 밖 |
| PASSAGE_SET_INCOMPLETE | K4 해설문 세트가 2문항 미만 (같은 set_id) |
| TOPIC_SHARE_OUT_OF_RANGE | 띄어쓰기 40% 초과, 또는 30문항 이상 번들에서 주제 비중이 목표 범위(±1문항) 밖 |
| TOPIC_COVERAGE_MISSING | 30문항 이상 번들에 6개 주제 중 빠진 것이 있음 |
| TOPIC_DIVERSITY_LOW | 8~29문항 블록에 주제가 4개 미만 |
| TEXTBOOK_EXAMPLE_FLOOD | 규정 해설·교과서 예시 재사용 문항이 30% 초과 |
| LEXICON_ONLY_TRAP | 표준어 사전 정보가 필요한데 근거를 <보기>에 넣지 않음 |
| CONSTRUCTED_BELOW_RECOMMENDED (WARN) | 서답형 10% 미만. 사용자가 객관식만 요청하면(`user_override`) 경고하지 않음 |

난도 범위(D2 0~10%, D3 25~40%, D4 35~55%, D5 10~25%, D4+D5 50~70%)는 번들의 `balance_profile: KOR_N_ORTHO_SCHOOL`로 생산 파이프라인이 검사한다(`tooling/production/production_pipeline.py` NAMED_PROFILES).
회귀 테스트: `tooling/korean/test_archetype_gate_v2.py` (정상 블록 통과 + 고장 15종 차단).

## 4. 다른 과목
사회·과학은 원안 대조 전이라 라이브러리가 없다. 장부의 SOC-H01, SCI-H01은 D3 힌트다.
2025-2 기말 통합사회2·통합과학2 원안을 대조해 과목별 라이브러리를 만든 뒤 같은 게이트를 적용한다.

## 5. 시험 뒤
실제 원안이 나오면 원형 분포와 함정 유형을 대조해 장부를 갱신한다 (`ops/ARC_POST_EXAM_CALIBRATION_V1.0.md`).
