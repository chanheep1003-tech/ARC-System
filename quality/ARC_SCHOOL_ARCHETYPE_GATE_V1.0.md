# ARC SCHOOL ARCHETYPE GATE V1.0
VERSION: 1.0
DATE: 2026-11-11
STATUS: ACTIVE
ROLE: 문항을 확인된 학교 시험 원형에서 만들게 하는 생성 규칙이자 게이트
LEDGER: quality/school/ARC_SCHOOL_EVIDENCE_LEDGER_V1.0.yaml
KOR_GRAMMAR_LIBRARY: quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml
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

## 4. 다른 과목
사회·과학은 원안 대조 전이라 라이브러리가 없다. 장부의 SOC-H01, SCI-H01은 D3 힌트다.
2025-2 기말 통합사회2·통합과학2 원안을 대조해 과목별 라이브러리를 만든 뒤 같은 게이트를 적용한다.

## 5. 시험 뒤
실제 원안이 나오면 원형 분포와 함정 유형을 대조해 장부를 갱신한다 (`ops/ARC_POST_EXAM_CALIBRATION_V1.0.md`).
