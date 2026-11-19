# ARC_SIMILARITY_GUARD_V1.0
VERSION: 1.0
DATE: 2026-09-17
STATUS: ACTIVE
ROLE: 문항·세트 중복/유사 구조 감지

## PURPOSE
문장 표절뿐 아니라 AI가 반복하는 '구조적 중복'도 차단한다.
비교 대상:
1. 현재 생성 세트 내부
2. 최근 검증문항은행
3. 최근 ARC N°/FINAL 사용 문항
4. 비교 가능한 사용자 제공 문제집/기출의 구조

## 1. SIMILARITY AXES
- STEM_PATTERN
- QUESTION_FORM
- CONCEPT_ID
- REASONING_FORM
- DISTRACTOR_PATTERN
- DATA_LAYOUT
- VISUAL_TEMPLATE
- CONTEXT_PATTERN
- CONDITION_PATTERN
- ANSWER_PATH

## 2. RISK LEVEL
LOW: 공통 개념만 같고 해결 구조가 다름
MEDIUM: 2~3개 축이 유사
HIGH: 4개 이상 핵심 축이 유사
CRITICAL: 문장/선지/수치만 바꾼 사실상 동일 문항

CRITICAL은 즉시 폐기.
HIGH는 원칙적으로 재설계.
MEDIUM은 동일 세트 내에서는 중복 위치와 목적을 확인.

## 3. AI REPETITION FLAGS
SIM_STEM_SKELETON
SIM_DISTRACTOR_LOGIC
SIM_CONTEXT_SWAP
SIM_NUMBER_SWAP
SIM_VISUAL_LAYOUT
SIM_REASONING_PATH
SIM_CONDITION_STACK
SIM_CHOICE_RHYTHM
SIM_RECENT_BANK
SIM_RECENT_PRODUCT

## 4. CURRENT SET RULE
- 동일 STEM_PATTERN 3회 이상 금지
- 동일 REASONING_FORM 3연속 금지
- 동일 DISTRACTOR_PATTERN 3연속 금지
- 동일 VISUAL_TEMPLATE 3연속 금지
- 같은 CONCEPT_ID 연속 배치 최소화
- 유사 문항은 최소 5문항 이상 간격 권장

## 5. BANK RULE
BANK_PASS 전에 최근 동일 CONCEPT_ID/QUESTION_FORM 후보와 비교.
HIGH 이상이면:
- 새 문항의 평가목표가 명확히 다르면 구조 재설계
- 실질적 중복이면 폐기
- 단순 수치/상황 치환은 허용하지 않음

## 6. PRODUCT REUSE
DIRECT reuse는 사용 이력 확인.
최근 N°에서 사용한 문항을 FINAL에 대량 재사용 금지.
ADAPTED도 새 문항처럼 similarity + QA 재검증.

## 7. ORIGINALITY ≠ NOVELTY FOR NOVELTY'S SAKE
억지로 희귀한 상황을 만들 필요 없음.
학교시험에 자연스러운 범위에서 해결 구조와 오답 설계를 다양화한다.

## 8. METADATA
SIMILARITY_RISK:
SIMILARITY_FLAGS: []
NEAREST_BANK_ITEM:
NEAREST_PRODUCT_ITEM:
STRUCTURAL_DELTA:
SIMILARITY_VERSION: ARC-SG-V1.0

## 9. FEEDBACK
같은 AI 반복 플래그가 3회 이상 발생하면 생성 규칙 패치 후보.
수정 후 QA BENCH와 세트 편집검사를 다시 수행.

END ARC SIMILARITY GUARD V1.0
