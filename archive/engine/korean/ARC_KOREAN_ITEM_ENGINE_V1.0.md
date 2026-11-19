# ARC KOREAN ITEM ENGINE V1.0
VERSION: 1.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC_N / ARC_FINAL 국어 문항 설계·지문 활용·오답 경쟁력 전용 엔진

## 0. PURPOSE
국어 문항은 같은 지문을 사용해도 문항 설계 품질에 따라 평가 가치가 크게 달라진다.
이 엔진의 목적은 '지문 옆 개념 확인형' 문제를 줄이고, 실제 지문 근거를 읽고 결합하고 판단해야 풀리는 문항을 안정적으로 생성하는 것이다.

핵심 원칙:
- PASSAGE BEFORE LABEL
- EVIDENCE BEFORE THEME
- INTEGRATION BEFORE RECALL
- COMPETITIVE DISTRACTORS BEFORE OBVIOUS WRONGS
- ITEM QUALITY BEFORE ITEM COUNT
- SET BLUEPRINT BEFORE GENERATION

## 1. PASSAGE-FIRST BLUEPRINT — REQUIRED
문항을 바로 1번부터 쓰지 않는다.
각 지문마다 먼저 PASSAGE_MAP을 만든다.

Required internal fields:
PASSAGE_ID
PASSAGE_TYPE = LITERATURE | NONFICTION
STRUCTURE_MAP[]
EVIDENCE_SPANS[]
INTERPRETIVE_AXES[]
CONFUSION_AXES[]
TRANSFER_AXES[]
ITEM_SLOTS[]

EVIDENCE_SPAN은 실제 지문의 행/연/문장/문단 위치를 가리켜야 한다.
기억이나 일반 해설로 대체하지 않는다.

ITEM_SLOTS는 문항 번호를 만들기 전에 서로 다른 판단 목적을 배정한다.
동일 판단축을 표현만 바꿔 중복 생성하지 않는다.

## 2. REASONING DEPTH
각 문항을 내부적으로 하나로 분류한다.

R0_DIRECT_RECALL
- 갈래/정의/명시정보를 한 문장 또는 한 표현에서 바로 확인
- 필요하지만 비중을 제한한다.

R1_SINGLE_EVIDENCE_INTERPRETATION
- 하나의 행/문장/표현을 해석하거나 효과를 판단
- 단순 재진술이면 R0로 강등한다.

R2_MULTI_EVIDENCE_INTEGRATION
- 둘 이상의 행/문장/문단/장면을 결합
- 관찰→추론, 앞부분→뒷부분 태도 변화, 주장→근거 결합 등

R3_TRANSFER_COMPARISON
- <보기>/새 사례/학생 판단/다른 작품·관점에 적용
- 최소 2단계 판단 요구

R4_HIGH_INTEGRATION
- 복수 근거 + 조건/관점/비교축을 동시에 처리
- 정답과 최소 2개 오답이 끝까지 경쟁

ARC_N 기본 목표(20문항 이상):
- R0 <= 20%
- R0+R1 <= 40%
- R2+R3+R4 >= 60%
- R3+R4 >= 25%

지문별 10문항 구성에서는 기본적으로:
- direct/basic 2 이하
- evidence interpretation 2~3
- multi-evidence 2~3
- transfer/comparison 2 이상
- high integration 1 이상
을 목표로 하되 지문 성격에 따라 조정한다.

이 수치는 품질 진단용이다. 약한 고난도를 억지로 만들기 위해 범위를 확장하지 않는다.

## 3. PASSAGE UTILIZATION GATE
문항은 PASSAGE_USE_CLASS를 가진다.

P0_LABEL_ONLY
- 작품명/갈래/개념 라벨만 알면 지문을 거의 읽지 않아도 풀이 가능

P1_SINGLE_SPAN
- 한 행/문장만 보면 해결

P2_LINKED_SPANS
- 둘 이상의 근거 연결 필요

P3_WHOLE_STRUCTURE
- 작품/글 전체 흐름, 문단 관계, 태도 변화, 논증 구조 필요

P4_TRANSFER
- 지문 구조를 새 보기/사례/비교에 적용

세트 기준:
- P0 <= 15%
- P2+P3+P4 >= 55%
- 10문항 지문군에서 P2+P3+P4 최소 5문항
- 비문학 10문항 지문군에서 서로 다른 문단 2개 이상을 연결하는 문항 최소 3문항
- 문학 10문항 지문군에서 실제 시어/행/장면 근거를 2곳 이상 연결하는 문항 최소 3문항

P0_LABEL_ONLY가 정답 정확성에 필요하지 않은데 존재하면 우선 교체한다.

## 4. LITERATURE DESIGN
문학은 주제·갈래·정서 라벨 찾기에서 멈추지 않는다.

우선 설계축:
- 시적 상황/서술 상황의 변화
- 화자/서술자의 관찰 사실 vs 추론
- 특정 표현의 기능을 작품 전체 흐름과 연결
- 앞/뒤 태도 변화의 근거
- 동일 표현이 문맥에서 만드는 의미
- 작품 내부 두 장면의 공통/차이
- <보기> 원리를 작품 근거에 적용
- 두 작품 비교 시 양쪽 작품의 근거를 각각 확인
- 과잉해석/근거범위 판단

제한:
- 주제 직접 확인 1개 초과는 특별한 이유가 없으면 금지
- 갈래 직접 확인은 세트 전체에서 과다 사용 금지
- '연민/고독/체념' 등 동일 정서 축을 같은 지문에서 여러 번 재질문 금지
- 같은 관찰/추론 축을 2문항 이상 쓰면 반드시 요구 사고가 달라야 함

## 5. NONFICTION DESIGN
비문학은 문장 찾기형 정의 확인에 머물지 않는다.

우선 설계축:
- 문단별 주장/근거 역할
- 개념 A/B의 공통점과 차이
- 조건이 바뀔 때 판단 변화
- 사례를 개념에 적용
- 학생 발언/가상 사례 평가
- 문단 삭제/순서 변경 시 논리 영향
- 앞 문단 전제 → 뒤 문단 결론 연결
- 서로 다른 문단의 정보를 결합한 추론
- 필자의 주장에 부합하는 새 사례
- 비슷한 개념을 같은 판단축에서 구분

비문학 10문항 지문군:
- direct definition/lookup 최대 3
- paragraph-crossing integration 최소 3
- transfer/application 최소 2
- viewpoint/comparison 최소 2
- 단, 중복 없이 설계한다.

## 6. DUPLICATE-AXIS BLOCK
각 지문군은 ITEM_REASONING_AXIS를 기록한다.

예:
THEME
GENRE
ATTITUDE
OBSERVATION_INFERENCE
EXPRESSION_EFFECT
TEMPORAL_CHANGE
STRUCTURE
COMPARE
TRANSFER
EVIDENCE_SCOPE
CLAIM_GROUND
CONDITION_CHANGE

동일 ITEM_REASONING_AXIS가 같은 지문 10문항 중 2개를 초과하면 기본적으로 REVISE.
2개를 사용할 경우에도:
- 근거 위치가 다르거나
- 요구 판단 단계가 다르거나
- 적용 대상이 달라야 한다.

실질적으로 같은 정답 논리를 다른 문장으로 묻는 것은 DUPLICATE_AXIS_FAIL.

## 7. DISTRACTOR COMPETITIVENESS
정답이 맞는 것보다 '왜 오답이 그럴듯한가'를 설계한다.

각 문항:
- 최소 2개 오답이 정답과 같은 판단축에서 경쟁
- 최소 1개 HALF_TRUE 가능
- 오답은 실제 지문 표현/관계/부분 진실을 활용
- 범위 밖 지식 없이 배제 가능

금지:
- 작품/지문과 명백히 무관한 선지 3개 이상
- '모두/완전히/오직/아무런 관련이 없다/반드시'만으로 쉽게 제거되는 극단 선지 남발
- 정답만 온건하고 나머지는 비상식적 극단
- 정답만 유독 길고 조건이 자세함
- 정답만 복합문이고 오답은 짧은 단문
- 같은 오답 원리 3문항 이상 반복

STRONG_DISTRACTOR_COUNT < 2이면 D3 이상 부여 금지.
STRONG_DISTRACTOR_COUNT < 2가 세트 25% 이상이면 SET_REVISE.

## 8. ANSWER LENGTH / LANGUAGE LEAK AUDIT
각 문항:
CORRECT_OPTION_LENGTH
DISTRACTOR_LENGTHS[]
MEDIAN_OPTION_LENGTH
CORRECT_TO_MEDIAN_RATIO

정답이 의미상 필요 없이 유독 길면 수정한다.
CORRECT_TO_MEDIAN_RATIO > 1.35이면 LENGTH_CLUE_REVIEW.

20문항 이상 세트:
- 정답이 5개 선지 중 '단독 최장'인 비율 > 50% => ANSWER_LENGTH_PATTERN_REVISE
- > 65% => SET_FAIL
- 정답이 상위 2개 길이에 속하는 비율 > 75% => LENGTH_BIAS_REVISE

길이를 억지로 동일하게 맞추지 않는다.
목표는 비예측 가능성이다.

## 9. STEM DIVERSITY
같은 발문 뼈대의 반복을 줄인다.

예:
- 가장 적절한 것은?
- 적절하지 않은 것은?
- <보기>를 바탕으로 이해한 것은?
- 두 학생의 판단을 평가한 것은?
- 문맥을 고려할 때 타당한 것은?
- 앞뒤 관계를 고려한 설명은?
- 근거로 삼기에 가장 적절한 것은?
- 수정/보완할 내용으로 적절한 것은?

규칙:
- 동일 stem skeleton 3연속 금지
- 20문항 이상 세트에서 단일 stem skeleton이 60% 초과하면 REVISE
- 발문 다양화를 위해 의미 없는 형식 변형은 금지

## 10. ANSWER POSITION
정답 위치는 완전 균등이 목표가 아니다.

필수:
- current SET EDITORIAL answer-position rules 적용
- ①②③④⑤ 주기 반복 금지
- 5문항 단위 완벽 순환 패턴도 PERIODIC_SEQUENCE로 처리
- exact equal distribution + 주기 패턴 결합 시 SET_FAIL
- 선지 재배열 후 PASS A/B 재검증

## 11. ITEM QUALITY BEFORE COUNT
요청 문항 수를 맞추기 위해 약한 문제를 남기지 않는다.

문항이 FAIL하면:
1. 같은 ITEM_SLOT에서 새 설계로 재생성
2. PASS A/B
3. passage utilization / distractor gate 재검사
4. 통과 후 번호 확정

'40문항을 만들었으므로 완료'가 아니라
'40문항 모두 gate를 통과했으므로 완료'가 기준이다.

## 12. SET BLUEPRINT EXAMPLE — 10 ITEMS
고정 템플릿이 아니라 최소 다양성 예시:

1. 핵심 상황/구조 기본 확인
2. 특정 표현의 문맥 기능
3. 두 근거 결합
4. <보기> 적용
5. 태도/관점 변화
6. 오답 경쟁형 세부 판단
7. 구조/문단 관계
8. 새 사례/학생 판단
9. 복수근거 통합
10. 고난도 비교/조건 적용

실제 지문에 맞지 않는 슬롯은 교체한다.

## 13. PRE-LOCK KOREAN SET GATES
필수:
KOR_PASSAGE_MAP = PASS
KOR_PASSAGE_UTILIZATION = PASS
KOR_REASONING_DIVERSITY = PASS
KOR_DUPLICATE_AXIS = PASS
KOR_DISTRACTOR_COMPETITIVENESS = PASS
KOR_ANSWER_LENGTH_AUDIT = PASS
KOR_STEM_DIVERSITY = PASS
KOR_ANSWER_PATTERN = PASS
KOR_SOURCE_TEXT_FIDELITY = PASS when applicable

하나라도 FAIL이면 CONTENT_LOCK 금지.

## 14. QA REPORT — INTERNAL
지문별로 최소 기록:
PASSAGE_ID
ITEM_COUNT
R0/R1/R2/R3/R4 distribution
P0/P1/P2/P3/P4 distribution
REASONING_AXIS distribution
DIRECT_LOOKUP_COUNT
MULTI_EVIDENCE_COUNT
TRANSFER_COUNT
DUPLICATE_AXIS_FLAGS[]
WEAK_DISTRACTOR_ITEMS[]
ANSWER_LENGTH_FLAGS[]
STEM_PATTERN_FLAGS[]

학생용에는 노출하지 않는다.

END ARC KOREAN ITEM ENGINE V1.0
