# ARC KOREAN ITEM ENGINE V1.5
VERSION: 1.5
DATE: 2026-11-05
STATUS: ACTIVE-DEV
ROLE: ARC_N / ARC_FINAL 국어 문항 설계·지문 활용·오답 경쟁력 전용 엔진

## 0. PURPOSE
국어 문항은 같은 지문을 사용해도 문항 설계 품질에 따라 평가 가치가 크게 달라진다.
이 엔진의 목적은 '지문 옆 개념 확인형' 문제를 줄이고, 실제 지문 근거를 읽고 결합하고 판단해야 풀리는 문항을 안정적으로 생성하는 것이다.

핵심 원칙:
- PASSAGE BEFORE LABEL
- CORE EXAM POINT COVERAGE BEFORE DISCRIMINATION
- EVIDENCE BEFORE SPECULATION
- BALANCED PRACTICE BEFORE EXTREME FILTERING
- COMPETITIVE DISTRACTORS BEFORE OBVIOUS WRONGS
- HIGH DIFFICULTY SHOULD DEEPEN CORE AXES, NOT REPLACE THEM
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

## 1-A. CURRENT SCHOOL POINT MAP INTAKE — REQUIRED WHEN REGISTERED
If SYSTEM_MANIFEST declares `active.quality.korean_supplement_point_map`, load it after RAW SCHOOL SOURCE and before ITEM_SLOTS.

The point map is a secondary design reference, not source-text or answer authority.

Required process:
1. RAW SCHOOL SOURCE first
2. registered point map second
3. classify each candidate point as VERIFIED_IN_SCHOOL_SOURCE / VERIFIED_IN_OFFICIAL_EXTERNAL / BACKGROUND_ONLY / DISPUTED_OR_UNVERIFIED
4. only VERIFIED_IN_SCHOOL_SOURCE may directly support the answer
5. use verified confusion boundaries to seed CONFUSION_AXES and distractor TRUE_KERNELS

A user-curated point map may increase attention to a likely axis, but it may never override the exact school excerpt or create teacher-intent claims.

## 2. REASONING DEPTH + PRODUCT BALANCE

R0_DIRECT_RECALL
- 명시정보·핵심 개념·기본 표현 직접 확인
- ARC_N에서는 시험 핵심 포인트 FOUNDATION 슬롯으로 허용한다.

R1_SINGLE_EVIDENCE_INTERPRETATION
- 한 행/문장/표현의 의미·표현 효과·핵심 기능을 판단
- 내신의 표현법/소재/정서·태도 점검 중심층이다.

R2_MULTI_EVIDENCE_INTEGRATION
- 둘 이상의 행/문장/문단/장면을 결합

R3_TRANSFER_COMPARISON
- <보기>/새 사례/학생 판단/다른 작품·관점 적용

R4_HIGH_INTEGRATION
- 복수 근거 + 조건/관점/비교축을 동시에 처리

### 2-A. ARC_N BALANCED SCHOOL-PREP OVERRIDE
국어 ARC_N은 '상위권 선별 시험'이 아니라 **핵심 내신 포인트를 빠짐없이 점검하면서 학교 수준의 변별까지 연습하는 학습용 N제**다.
국어 ARC_N에서는 common engine의 일반 ARC_N difficulty floor보다 이 과목별 balance profile을 우선한다.

지문 10문항 기본:
- CORE_EXAM_POINT / FOUNDATION: 3
- SCHOOL_STANDARD_APPLICATION: 4
- SCHOOL_UPPER_DISCRIMINATION: 2
- EXTREME: 0~1

기본 난도:
- D1 0~10%
- D2 30~40%
- D3 30~40%
- D4 15~25%
- D5 0~5%
- D4+D5 기본 20~30%

사용자가 명시적으로 고난도/최상위/변별용을 요청하거나 현재 학교 앵커가 더 높은 난도를 명확히 요구하면 상향 가능하다.
그 경우에도 CORE_EXAM_POINT_COVERAGE는 유지한다.
ARC_FINAL에는 이 override를 적용하지 않는다.

### 2-B. CORE EXAM POINT COVERAGE MATRIX — HARD GATE
문학 10문항에서 모두 한 번 이상:
- THEME_OR_CENTRAL_MEANING
- SPEAKER_ATTITUDE_OR_EMOTION
- EXPRESSION_METHOD_AND_EFFECT
- KEY_WORD_IMAGE_OBJECT_FUNCTION
- STRUCTURE_OR_DEVELOPMENT

최소 3문항은 FOUNDATION_CORE_ITEM=true.

비문학 10문항에서 모두 한 번 이상:
- CENTRAL_CLAIM_OR_CONCEPT
- TEXT_OR_ARGUMENT_STRUCTURE
- KEY_CONCEPT_RELATION_OR_CONTRAST
- EXPLICIT_CONTENT_ACCURACY
- APPLICATION_OR_CONDITION

최소 3문항은 FOUNDATION_CORE_ITEM=true.

### 2-C. HIGH-FREQUENCY EXAM POINT RATE
지문군 10문항 중 최소 6문항은 학교자료/교과서 학습활동/등록 point map이 확인하는 핵심 출제축을 직접 강화한다.
필드:
CORE_EXAM_POINT = YES|NO
CORE_EXAM_AXIS
CORE_EXAM_EVIDENCE

### 2-D. RARE / DISCRIMINATION-ONLY TASK BUDGET
다음은 주력이 될 수 없다:
- 행/문장 삭제 가정
- 단어/표현 치환 후 의미 변화
- 극미세 지칭어 변천 추적
- 본문 임의 변형 반사실 문제

10문항 지문군:
- COUNTERFACTUAL_EDIT / DELETE_REPLACE_TASK 합계 최대 1
- MICRO_REFERENCE_TRACE 최대 1
- DISCRIMINATION_ONLY_TASK 합계 최대 2

핵심 원칙:
**변별력은 낯선 발문 조작보다, 익숙한 핵심 포인트에서 강한 오답과 정확한 근거 구분으로 만든다.**

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

ARC_N 기본 세트 기준:
- P0 <= 20%
- P2+P3+P4 >= 40%
- 10문항 지문군에서 P2+P3+P4 최소 4문항
- 비문학 10문항 지문군에서 서로 다른 문단 2개 이상을 연결하는 문항 최소 3문항
- 문학 10문항 지문군에서 실제 시어/행/장면 근거를 2곳 이상 연결하는 문항 최소 3문항

P0_LABEL_ONLY가 정답 정확성에 필요하지 않은데 존재하면 우선 교체한다.

## 4. LITERATURE DESIGN — CORE FIRST, THEN DISCRIMINATION
문학 ARC_N은 작품을 공부하게 해야 한다. 주제·정서·표현법을 줄이고 미세 추론만 늘리는 설계를 금지한다.

먼저 확보:
- 작품 전체 핵심 주제/의미
- 화자의 상황·정서·태도
- 반복/대조/설의/의인/비유/감각적 이미지 등 중요 표현법과 효과
- 중요 시어·소재·공간·이미지의 기능
- 시상 전개/시간 구조/태도 변화

그 다음 심화:
- 관찰 사실 vs 추론
- 복수 근거 결합
- <보기> 적용
- 작품 비교
- 과잉해석/근거범위
- HALF_TRUE strong distractor

규칙:
- THEME_OR_CENTRAL_MEANING >=1
- EXPRESSION_METHOD_AND_EFFECT >=1
- KEY_WORD_IMAGE_OBJECT_FUNCTION >=1
- STRUCTURE_OR_DEVELOPMENT >=1
- 위 네 축 중 최소 세 축은 서로 다른 문항으로 직접 점검
- 삭제/치환/미세 지칭어 추적은 rare-task budget 적용

좋은 고난도는 표현법→문맥 효과→주제/태도 연결을 더 정밀하게 만드는 문제다.

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
- central claim / key concept / structure 직접 점검 최소 3
- direct definition/lookup 최대 3
- paragraph-crossing integration 최소 2
- transfer/application 최소 2
- viewpoint/comparison 최소 1
- 고난도 문항이 기본 개념 확인 슬롯을 밀어내지 않는다.

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

## 7. ATTRACTIVE DISTRACTOR ENGINE — HARD GATE
User field feedback from the previous ARC N° Korean set confirmed a major realism gap: correct answers often stood out immediately and wrong options did not remain credible long enough to require source-based discrimination.

Therefore a distractor is not "strong" merely because it is grammatically plausible.

### 7-1. STRONG DISTRACTOR DEFINITION
A STRONG_DISTRACTOR must satisfy all:
1. SAME_AXIS: competes on the same judgment axis as the correct option
2. TRUE_KERNEL: contains at least one source-supported true component or relation
3. LOCAL_DISTORTION: becomes false because of a precise nearby distortion, not because the whole option is nonsense
4. EVIDENCE_REFUTABLE: the decisive flaw can be rejected with an exact source span / relation
5. STYLE_PARITY: similar granularity, specificity and linguistic naturalness to the correct option

Preferred distortion classes:
- FACT_TO_INFERENCE_UPGRADE
- INFERENCE_TO_FACT_DOWNGRADE
- TEMPORAL_STAGE_SWAP
- SPEAKER_ACTION_OVERSTATEMENT
- CORRECT_DEVICE_WRONG_EFFECT
- TRUE_COMMONALITY_FALSE_DIFFERENCE
- SCOPE_OVERREACH
- DEGREE_ABSOLUTIZATION
- CONCEPT_PAIR_SWAP
- EXPLICIT_POSITION_VS_CRITIQUE_SWAP
- CONDITION_PARTIAL_MATCH

The following are WEAK_DISTRACTOR:
- unrelated claim
- obviously impossible action/event
- pure opposite of an explicit sentence
- extreme quantifier used as the only flaw
- out-of-scope fact
- awkward sentence removable without reading the passage
- option that fails on three or more unrelated axes at once

### 7-2. DISTRACTOR PROOF PAYLOAD
For every wrong option record internally:
TRUE_KERNEL
DISTORTION_CLASS
WHY_TEMPTING
DECISIVE_FLAW
DECISIVE_EVIDENCE_REF
IMMEDIATE_ELIMINATION = YES|NO
STRONG_DISTRACTOR = YES|NO

A distractor cannot be marked STRONG_DISTRACTOR=YES unless TRUE_KERNEL and DECISIVE_EVIDENCE_REF are both non-empty.

### 7-3. ADVERSARIAL DEFENSE PASS
After writing the option set, run a key-hidden adversarial pass.

For each wrong option:
- argue the strongest passage-grounded case FOR choosing it
- then identify the single decisive evidence/relation that defeats it

If no credible passage-grounded defense can be written, that option is weak and must be rewritten.

This is not an ambiguity license. The final set must still have exactly one answer.

### 7-4. FIRST-PASS CANDIDATE GATE
Before the answer key is revealed, a blind reviewer ranks the top candidate options.

Required:
- D2: at least 2 initially viable options when the task is not direct recall
- D3: FIRST_PASS_CANDIDATE_COUNT >= 3
- D4/D5: FIRST_PASS_CANDIDATE_COUNT >= 3 and at least two wrong options are STRONG_DISTRACTOR=YES
- D3+ IMMEDIATE_ELIMINATION_COUNT <= 2
- D4/D5 IMMEDIATE_ELIMINATION_COUNT <= 1

If the correct answer is obvious from option tone, length, extremeness, or relevance before evidence comparison:
OBVIOUS_ANSWER_FLAG=FAIL
and the item must be rewritten.

### 7-5. SECOND-BEST OPTION GATE
Every D3+ item must identify:
SECOND_BEST_OPTION
SECOND_BEST_WHY_PLAUSIBLE
SECOND_BEST_DECISIVE_REFUTATION

The second-best option must be plausible for a student who understood the broad idea but missed one condition, scope boundary, time layer, agency, or evidence distinction.

If SECOND_BEST_OPTION can be dismissed without a specific source-based reason, the item is too easy for D3+.

### 7-6. SET-LEVEL REALISM
For 20+ item ARC_N sets:
- every D3/D4/D5 item: STRONG_DISTRACTOR_COUNT >= 2
- every D4/D5 item: NEAR_MISS_DISTRACTOR_COUNT >= 2
- OBVIOUS_ANSWER_FLAG count <= 10% of the set; any D3+ obvious-answer item is REVISE
- at least 50% of all items should contain two source-grounded near-miss options unless the item is intentionally basic
- same distortion class may not dominate more than 35% of distractors in one passage group
- at least three different distortion classes per 10-item passage group

### 7-7. PROHIBITED EASY-ANSWER PATTERNS
Hard revise:
- correct option is the only one that mentions the passage's central concept correctly
- four distractors are about unrelated actions/events and one option merely restates the text
- comparison item has one generic shared theme and four obviously unrelated claims
- expression-effect item has one conventional textbook effect and four effects from unrelated devices
- philosophy item has one accurate term-definition pair and four direct reversals
- <보기> itself states the rule and the correct option simply repeats it while distractors contradict it crudely

STRONG_DISTRACTOR_COUNT < 2 => D3+ forbidden.
OBVIOUS_ANSWER_FLAG=FAIL => item cannot CONTENT_LOCK.

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

## 9-A. KOREAN QUESTION-TASK MIX
국어는 '윗글에 대한 설명으로 가장 적절한 것은?' 유형에 편중되지 않게 한다.

지문 10문항 기본 진단:
- SINGLE_BEST_STATEMENT 최대 4
- EXCEPT_INCORRECT 최대 2
- CASE_APPLICATION 최소 2
- EVIDENCE_SUPPORT / MULTI_JUDGMENT / COMPARISON_MATRIX / ERROR_CORRECTION / STRUCTURE_RELATION 중 최소 2개 이상 사용
- 총 QUESTION_TASK_FORM 최소 4종
- 동일 task form 3문항 연속 금지

권장 국어 task form:
- SINGLE_BEST_STATEMENT
- EXCEPT_INCORRECT
- MULTI_JUDGMENT
- CASE_APPLICATION
- EVIDENCE_SUPPORT
- COMPARISON_MATRIX
- ERROR_CORRECTION
- STRUCTURE_RELATION
- SEQUENCE_ORDER
- CONDITION_CHANGE
- STUDENT_RESPONSE_EVALUATION

중요:
- '적절한 것'을 '적절하지 않은 것'으로 바꾸는 것은 충분한 다양화가 아니다.
- 부정형 문항은 독해력보다 실수 유발이 커지지 않게 제한한다.
- <보기>, 학생 발언, 근거 선택, 관계 대응, 순서 판단 등 실제 사고 과업을 바꾼다.
- 같은 지문에서 주제/정서/태도 판단을 SINGLE_BEST 형식으로 연속 배치하지 않는다.

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

## 12. ARC_N DEFAULT BLUEPRINT — 10 ITEMS
1. 핵심 주제/중심 의미 또는 중심 주장
2. 중요 표현법과 효과 / 핵심 개념 관계
3. 핵심 시어·소재·이미지·문단 기능
4. 시상/논리 전개 또는 내용 일치
5. 표준 문맥 의미·근거 판단
6. 표준 복수 근거 결합
7. 표준 <보기>/학생 반응/사례 적용
8. 상위 HALF_TRUE 또는 비교
9. 상위 복수 근거·조건 통합
10. 최상위 변별 0~1개

필수:
- FOUNDATION_CORE_ITEM 최소 3
- CORE_EXAM_POINT=YES 최소 6
- DISCRIMINATION_ONLY_TASK 최대 2
- COUNTERFACTUAL_EDIT / DELETE_REPLACE_TASK 최대 1

## 13. PRE-LOCK KOREAN SET GATES
필수:
KOR_PASSAGE_MAP = PASS
KOR_CORE_EXAM_POINT_COVERAGE = PASS
KOR_DIFFICULTY_BALANCE = PASS
KOR_RARE_TASK_BUDGET = PASS
KOR_PASSAGE_UTILIZATION = PASS
KOR_REASONING_DIVERSITY = PASS
KOR_DUPLICATE_AXIS = PASS
KOR_DISTRACTOR_COMPETITIVENESS = PASS
KOR_ATTRACTIVE_DISTRACTOR_GATE = PASS
KOR_OBVIOUS_ANSWER_GATE = PASS
KOR_SECOND_BEST_GATE = PASS
KOR_ANSWER_LENGTH_AUDIT = PASS
KOR_STEM_DIVERSITY = PASS
KOR_TASK_FORM_DIVERSITY = PASS
KOR_ANSWER_PATTERN = PASS
KOR_SOURCE_TEXT_FIDELITY = PASS when applicable

하나라도 FAIL이면 CONTENT_LOCK 금지.

## 14. QA REPORT — INTERNAL
지문별로 최소 기록:
PASSAGE_ID
ITEM_COUNT
FOUNDATION_CORE_COUNT
CORE_EXAM_POINT_COUNT
CORE_EXAM_AXIS_COVERAGE[]
DIFFICULTY_DISTRIBUTION
DISCRIMINATION_ONLY_TASK_COUNT
COUNTERFACTUAL_EDIT_COUNT
MICRO_REFERENCE_TRACE_COUNT
R0/R1/R2/R3/R4 distribution
P0/P1/P2/P3/P4 distribution
REASONING_AXIS distribution
DIRECT_LOOKUP_COUNT
MULTI_EVIDENCE_COUNT
TRANSFER_COUNT
DUPLICATE_AXIS_FLAGS[]
WEAK_DISTRACTOR_ITEMS[]
OBVIOUS_ANSWER_ITEMS[]
FIRST_PASS_CANDIDATE_COUNTS[]
SECOND_BEST_OPTIONS[]
DISTRACTOR_CLASS_DISTRIBUTION
ANSWER_LENGTH_FLAGS[]
STEM_PATTERN_FLAGS[]
TASK_FORM_DISTRIBUTION
TASK_FORM_FLAGS[]

학생용에는 노출하지 않는다.

## 12. SCHOOL-REALISM BLUEPRINT — V1.5
문항 생성 전에 KOR_DONGBOOK_EXAM_TYPE_PROFILE_2025_2026_V1.0을 구조 앵커로 로드한다.
과거 시험의 원문/선지 문장을 복제하지 않고 TASK FAMILY와 난도 감각만 사용한다.

ITEM_SLOT마다 SCHOOL_TASK_FAMILY를 기록한다.
권장 family:
CONTENT_UNDERSTANDING / SPEAKER_CHARACTER_ATTITUDE / EXPRESSION_EFFECT /
MARKED_EXPRESSION_FUNCTION / KEY_WORD_IMAGE_OBJECT_FUNCTION / STRUCTURE_DEVELOPMENT /
VIEW_APPLICATION / COMPARE_CONTRAST / MULTI_JUDGMENT /
CENTRAL_CLAIM_CONCEPT / CONCEPT_RELATION_CONTRAST / CASE_APPLICATION.

AI-like generation 방지:
- 먼저 고난도 장치를 만든 뒤 지문을 끼워 맞추지 않는다.
- 학생 대화/메모 wrapper는 사고 기능이 있을 때만 쓴다.
- 내부 QA 언어를 학생 발문으로 변환하지 않는다.
- 모든 선지를 장문의 설명문으로 통일하지 않는다.
- 오답은 실제 학생의 부분 이해를 반영하되 한두 근거 차이로 탈락하게 한다.
- 한 문항 안에서 정답/오답의 정보밀도와 문체를 비슷하게 맞춘다.
- 정답만 조심스럽고 복합적인 문장, 오답만 과격한 문장인 패턴을 금지한다.

세트 생성 후 executable Korean Exam Realism Gate에 필요한 counts payload를 작성한다.
KOR_EXAM_REALISM_GATE=PASS 전에는 CONTENT_LOCK 금지.


END ARC KOREAN ITEM ENGINE V1.5

## 14. KOR ORTHOGRAPHY SUBCLAUSE & EXCEPT-STEM GATE (V1.5 / 2026-11-05)

For all KOR ARC N°/FINAL content, read `quality/korean/ARC_KOR_NORM_20261105_CORRECTION_POLICY.md`.

- Every normative explanation specifies **exact** subsection (e.g. 한글 맞춤법 제25항 1. / [붙임] / 2.), affected lexeme and part of speech; official primary-source check mandatory.
- Define STEM_POLARITY: POSITIVE or NEGATIVE. With five-option item: POSITIVE requires TRUE×1 + FALSE×4; NEGATIVE ('적절하지 않은 것은') requires FALSE×1 + TRUE×4. No HALF_TRUE/UNSUPPORTED release.
- Author must record atomic facts for each alternative. Blind reviewer gets an isolated packet and determines all five truth values and exact source evidence, not just predicted answer.
- Corpus item: passage source lock, original work vs extant edition date, quote fidelity, passage sequence and title. Generate TOC from actual content, then verify each entry against rendered PDF and question range.
- After any student text/answer/solution edits, invalidate prior review hash and rerun source and five-option validation; static PDF regex check alone NEVER permits CONTENT_LOCK.
- Test with `tooling/content_qa/korean_norm_regression_gate.py`; maintain actual negative regression examples in `quality/reviews/ARC_KOR_N_20261105_REVIEW_REPORT.md`. Current 2026-11-05 patched PDFs remain REVIEW_PENDING until full independent audit.

## 15. ARC 5-LEVEL LEARNING LADDER (2026-11-05 / REQUIRED)
Load quality/korean/ARC_KOR_V1_V5_LEVEL_POLICY_V1.1.md on every new KOR ARC_N or KOR ARC_FINAL item build; this ladder does not apply to other subjects. Select external text **per item and per run** through quality/korean/ARC_KOR_DYNAMIC_SOURCE_SELECTION_V1.0.yaml; first decide skill/comparison axis and then search and compare new texts. Never preassign songs, writers or medieval excerpts from a static list. Use verified school exam evidence only to determine question style.
- V1 ARC_N: full textbook range + diverse item families + foundational concepts, NOT a subset focused only on frequent rules.
- V2 ARC_N: higher share for evidence-backed priority concepts; require more interdependent decisions/diagnosis.
- V3 ARC_N: unfamiliar authorized outside passage or genuinely novel examples. Passage must be necessary to solve; no unteachable outside concept.
- V4 ARC_N: true advanced discrimination based on compound evidence/conditions and strong distractors with exactly one supported answer.
- V5 ARC_FINAL: re-create measured school examination structure, stems, passage loading, answer choices, difficulty and time from **verified Dongbuk past exams**; not guaranteed harder than V4 and never claim to predict teacher intent.
Item metadata MUST retain level, product, textbook anchor, novel passage origin when V3, and verified-school-exam anchor when V5. Version maps: V1-V4=ARC_N; V5=ARC_FINAL. Do not call V1 ARC_CORE.
When a project explicitly requests V1~V3 orthography, the per-level slots and coverage are defined by quality/korean/ARC_KOR_ORTHOGRAPHY_V123_TEXTBOOK_REBUILD_SPEC_20261105.md. Older V3 "DISCRIMINATION only" terminology is overridden by this requirement.

## 16. GENRE-DEPENDENT UNSEEN KOR PASSAGE (2026-11-06)
Literature: actual new literary text with comparison axes; nonfiction: unfamiliar X/Y concepts defined within new self-contained passage then applied to an unfamiliar example; grammar: unfamiliar old-Korean documentary excerpts OR modern orthography evidence in short licensed song lyrics, poems, novel dialogue, school diary, SNS. For medieval texts lock original edition, period, original lines and modernization and avoid duplicate excerpts. Song transcripts may contain nonstandard artist spelling; do not treat a lyric as the standard dictionary. Cite rule and original words separately, and obtain rights to print extensive copyrighted lyrics/modern creative passages. Example must be necessary (if removable, reject V3). Match V5 only to confirmed Dongbuk exam formats. Evidence: 2025 final Q4–10 and Q15–21, 2026 mid Q1 and Q20–22, not generalization about lyric frequency.

## KOR V6 precision specialist (2026-11-06, active override)
Load `quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md` as the canonical KOR-only version policy. The former `quality/korean/ARC_KOR_V1_V5_LEVEL_POLICY_V1.1.md` is historical. For level=V6 use `quality/korean/ARC_KOR_V6_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY_V1.0.md`: ARC N° short-context unusual lexemes/idioms with exact contextual POS, morphology, orthography clause and correct wording. Build an item-specific source and dictionary receipt *before* generating options. Do not hard-code specific rare words to every question or infer clause numbers from a token alone. Blind-solve before comparing the answer. V5 ARC FINAL stays school-simulation; no automatic level inheritance to SCI/SOC. V6 100 items remain NOT_PRODUCED until actual generated and independently reviewed.
