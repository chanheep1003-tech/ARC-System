# ARC_SIMILARITY_GUARD_V1.0
VERSION: 1.1
DATE: 2026-09-30
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
HIGH는 원칙적으로 재설계(단, §6 EVOLVE로 개선된 핵심 문항은 예외 허용).
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

## 6. PRODUCT REUSE — 핵심 문항 진화 재사용 (개정 2026-09-30)
새로 만드는 세트가 이전 세트·문제은행과 **겹치는 것은 허용**한다. 무조건 새 문항일 필요가 없다.
**중요한(핵심 개념·출제 가능성이 높은) 문항은 이전 문항을 가져와 고쳐 쓰는 것을 권장한다.**

허용 방식 (EVOLVE): 아래 중 **최소 하나**를 실제로 바꾸고, 바꾼 결과가 이전보다 좋아야 한다.
- OPTION_REBUILD: 선지 재구성 — 단일 변이 규칙으로 오답을 다시 만들어 CDI를 올리고 선지 린트를 통과시킴
- ASK_SHIFT: 묻는 축 변경 — 같은 지문 근거로 다른 개념·다른 관점·다른 유형(적절한↔부적절한, 단일↔<보기>/ㄱ~ㅁ)을 묻기
- CONTEXT_UPGRADE: 자료·<보기>·사례를 바꿔 전이 요소를 추가
- FIX: 오류·모호성 수정

금지 (COPY): 문장·선지·수치만 치환하고 구조·품질이 그대로인 재사용 = CRITICAL, 폐기.
개선 판정: (린트 지표 또는 CDI 상승) 또는 (발문 경로 난도 상승) 중 하나가 기록으로 확인되어야 EVOLVE로 인정.

세트 운영:
- 같은 세트 안에서는 동일 문항·동일 근거 반복을 금지(§4 유지).
- ARC FINAL에서도 이전 N° 문항의 진화 재사용을 허용한다. 원형 그대로(COPY) 재사용은 세트의 10% 이하로 제한하고 사용 이력을 남긴다.
- 사용 이력이 많은 문항은 진화 강도를 높인다(선지·발문을 함께 변경).

계보 기록(LINEAGE): 문항 메타에 `parent`(예: `N11-27`, `FINAL01-05`), `change`(OPTION_REBUILD/ASK_SHIFT/CONTEXT_UPGRADE/FIX 조합), `delta`(무엇이 어떻게 좋아졌는지 한 줄)를 남긴다.

ADAPTED도 새 문항처럼 similarity + QA + 선지 린트 재검증.

## 7. ORIGINALITY ≠ NOVELTY FOR NOVELTY'S SAKE
억지로 희귀한 상황을 만들 필요 없음.
학교시험에 자연스러운 범위에서 해결 구조와 오답 설계를 다양화한다.

## 8. METADATA
SIMILARITY_RISK:
SIMILARITY_FLAGS: []
NEAREST_BANK_ITEM:
NEAREST_PRODUCT_ITEM:
STRUCTURAL_DELTA:
LINEAGE: {parent: , change: [], delta: }
SIMILARITY_VERSION: ARC-SG-V1.1

## 9. FEEDBACK
같은 AI 반복 플래그가 3회 이상 발생하면 생성 규칙 패치 후보.
수정 후 QA BENCH와 세트 편집검사를 다시 수행.

END ARC SIMILARITY GUARD V1.0
