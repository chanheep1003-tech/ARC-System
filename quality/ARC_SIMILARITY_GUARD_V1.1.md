# ARC_SIMILARITY_GUARD_V1.1
VERSION: 1.1
DATE: 2026-09-18
STATUS: ACTIVE
ROLE: 문항·세트 중복/유사 구조 감지

## PURPOSE
문장 표절뿐 아니라 AI가 반복하는 '구조적 중복'도 차단한다.
V1.1은 AI 구조판정에 sentence-transformers + local Qdrant cosine similarity를 추가한다.
실행 규칙: quality/similarity/ARC_SIMILARITY_IMPLEMENTATION_V1.0.md
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

## 2. QUANTITATIVE LAYER
tooling/similarity/arc_similarity.py로 FULL_ITEM / STEM / DISTRACTORS 임베딩을 각각 비교한다.
한국어가 포함되므로 multilingual model을 기본 사용한다.
Qdrant는 local persistent mode를 기본으로 하여 BANK 원문을 외부 vector service로 보내지 않는다.

threshold는 임의 숫자로 고정하지 않는다.
quality/similarity/SIMILARITY_THRESHOLDS_V1.0.yaml이 CALIBRATION_REQUIRED이면 raw cosine은 advisory다.
실제 BANK 라벨쌍으로 calibrate한 뒤에만 cosine score를 HIGH/CRITICAL hard decision에 사용한다.

최종 위험도는 semantic score + structural match count + 최근 사용이력을 결합한다.

## 3. RISK LEVEL
LOW: 공통 개념만 같고 해결 구조가 다름
MEDIUM: 2~3개 축이 유사
HIGH: 4개 이상 핵심 축이 유사
CRITICAL: 문장/선지/수치만 바꾼 사실상 동일 문항

CRITICAL은 즉시 폐기.
HIGH는 원칙적으로 재설계.
MEDIUM은 동일 세트 내에서는 중복 위치와 목적을 확인.

## 4. AI REPETITION FLAGS
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

## 5. CURRENT SET RULE
- 동일 STEM_PATTERN 3회 이상 금지
- 동일 REASONING_FORM 3연속 금지
- 동일 DISTRACTOR_PATTERN 3연속 금지
- 동일 VISUAL_TEMPLATE 3연속 금지
- 같은 CONCEPT_ID 연속 배치 최소화
- 유사 문항은 최소 5문항 이상 간격 권장

## 6. BANK RULE
BANK_PASS 전에 최근 동일 CONCEPT_ID/QUESTION_FORM 후보와 비교.
HIGH 이상이면:
- 새 문항의 평가목표가 명확히 다르면 구조 재설계
- 실질적 중복이면 폐기
- 단순 수치/상황 치환은 허용하지 않음

## 7. PRODUCT REUSE
DIRECT reuse는 사용 이력 확인.
최근 N°에서 사용한 문항을 FINAL에 대량 재사용 금지.
ADAPTED도 새 문항처럼 similarity + QA 재검증.

## 8. ORIGINALITY ≠ NOVELTY FOR NOVELTY'S SAKE
억지로 희귀한 상황을 만들 필요 없음.
학교시험에 자연스러운 범위에서 해결 구조와 오답 설계를 다양화한다.

## 9. METADATA
SIMILARITY_RISK:
SIMILARITY_FLAGS: []
NEAREST_BANK_ITEM:
NEAREST_PRODUCT_ITEM:
STRUCTURAL_DELTA:
SEMANTIC_MODEL:
FULL_ITEM_COSINE:
STEM_COSINE:
DISTRACTOR_COSINE:
STRUCTURAL_MATCH_COUNT:
THRESHOLD_STATUS:
SIMILARITY_VERSION: ARC-SG-V1.1

## 10. FEEDBACK
같은 AI 반복 플래그가 3회 이상 발생하면 생성 규칙 패치 후보.
수정 후 QA BENCH와 세트 편집검사를 다시 수행.

END ARC SIMILARITY GUARD V1.0
