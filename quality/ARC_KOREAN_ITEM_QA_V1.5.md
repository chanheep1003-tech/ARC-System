# ARC KOREAN ITEM QA V1.5
VERSION: 1.5
DATE: 2026-09-24
STATUS: ACTIVE-DEV
ROLE: 국어 ARC_N / ARC_FINAL 전용 문항·지문군 품질 게이트

## 0. PURPOSE
국어는 지문이 좋아도 문항이 단순 확인형·중복형·정답 노출형이면 세트 품질이 급격히 떨어진다.
이 QA는 '정답이 맞다'와 '좋은 국어 문항이다'를 분리한다.

## 1. ITEM HARD FAIL
다음 중 하나면 해당 문항 REVISE/DISCARD:
- 지문을 거의 읽지 않고 작품명/갈래/라벨만으로 해결 가능하며 그 문항이 기본 확인 슬롯으로 명시되지 않음
- 정답이 지문의 한 문장을 거의 그대로 반복하고 오답 3개 이상이 즉시 제거 가능
- STRONG_DISTRACTOR_COUNT < 2인데 D3 이상으로 분류
- D3 이상인데 FIRST_PASS_CANDIDATE_COUNT < 3
- D3 이상인데 SECOND_BEST_OPTION / SECOND_BEST_DECISIVE_REFUTATION 누락
- D3 이상인데 IMMEDIATE_ELIMINATION_COUNT > 2
- D4/D5인데 IMMEDIATE_ELIMINATION_COUNT > 1
- 정답이 지문 근거 비교 전에 관련성/문체/길이/극단성만으로 눈에 띄는 OBVIOUS_ANSWER_FLAG
- 정답만 의미상 필요 없이 유독 길고 구체적
- 극단 표현 하나만 보고 오답을 제거할 수 있는 선지가 3개 이상
- 같은 지문에서 기존 문항과 실질적으로 동일한 판단축/정답 논리를 재사용
- 문학 해석이 작품 내부 근거 없이 외부 지식에 의존
- 비문학 문항이 정의 문장 위치 찾기만 요구하면서 적용/추론형으로 분류됨

## 2. PASSAGE-GROUP GATE — BALANCED ARC_N
지문군 10문항:
- FOUNDATION_CORE_ITEM 최소 3
- CORE_EXAM_POINT=YES 최소 6
- P2+P3+P4 최소 4
- transfer/application 최소 1
- multi-evidence 최소 2
- DISCRIMINATION_ONLY_TASK 최대 2
- COUNTERFACTUAL_EDIT / DELETE_REPLACE_TASK 합계 최대 1
- MICRO_REFERENCE_TRACE 최대 1

문학 필수:
- THEME_OR_CENTRAL_MEANING >=1
- SPEAKER_ATTITUDE_OR_EMOTION >=1
- EXPRESSION_METHOD_AND_EFFECT >=1
- KEY_WORD_IMAGE_OBJECT_FUNCTION >=1
- STRUCTURE_OR_DEVELOPMENT >=1

비문학 필수:
- CENTRAL_CLAIM_OR_CONCEPT >=1
- TEXT_OR_ARGUMENT_STRUCTURE >=1
- KEY_CONCEPT_RELATION_OR_CONTRAST >=1
- EXPLICIT_CONTENT_ACCURACY >=1
- APPLICATION_OR_CONDITION >=1

KOR_CORE_EXAM_POINT_COVERAGE: PASS / REVISE / FAIL
KOR_RARE_TASK_BUDGET: PASS / FAIL

## 2-A. ARC_N DIFFICULTY BALANCE GATE
국어 ARC_N 기본:
- D1 0~10%
- D2 30~40%
- D3 30~40%
- D4 15~25%
- D5 0~5%
- D4+D5 기본 20~30%

OVER_DISCRIMINATION_REVISE:
- D4+D5 >35%인데 명시적 고난도 요청/학교 앵커 근거 없음
- FOUNDATION_CORE_ITEM <30%
- CORE_EXAM_POINT_RATE <60%
- 변형·삭제·치환·미세추적 문항이 핵심 주제·표현법·소재 기능 문항보다 많음

이 gate는 국어 ARC_N에서 common ARC_N 난도 하한보다 우선한다.
ARC_FINAL에는 적용하지 않는다.

KOR_DIFFICULTY_BALANCE: PASS / REVISE / FAIL

## 2-B. ATTRACTIVE DISTRACTOR / OBVIOUSNESS GATE
Every MCQ option set must include an internal distractor proof.

For each wrong option:
- TRUE_KERNEL
- DISTORTION_CLASS
- WHY_TEMPTING
- DECISIVE_FLAW
- DECISIVE_EVIDENCE_REF
- IMMEDIATE_ELIMINATION
- STRONG_DISTRACTOR

A strong distractor requires a real source-grounded true kernel and a precise decisive flaw.

### Key-hidden adversarial pass
Before viewing the key, independently:
1. rank the top 3 candidates
2. record FIRST_PASS_CANDIDATE_COUNT
3. identify the SECOND_BEST_OPTION
4. state why the second-best looks plausible
5. reject it using exact passage evidence/relation

D3+:
- FIRST_PASS_CANDIDATE_COUNT >= 3
- STRONG_DISTRACTOR_COUNT >= 2
- IMMEDIATE_ELIMINATION_COUNT <= 2
- SECOND_BEST evidence payload complete

D4/D5:
- STRONG_DISTRACTOR_COUNT >= 2
- NEAR_MISS_DISTRACTOR_COUNT >= 2
- IMMEDIATE_ELIMINATION_COUNT <= 1

Any item whose correct answer is obvious before evidence comparison must be REVISE regardless of nominal difficulty score.

### Set-level
20+ item set:
- D3+ obvious-answer items = 0
- total OBVIOUS_ANSWER_FLAG <= 10%
- at least 3 distractor distortion classes per 10-item passage group
- one distortion class >35% of passage-group distractors => REVISE
- if more than 20% of items have only one credible alternative, SET_FAIL

KOR_ATTRACTIVE_DISTRACTOR_GATE:
PASS / REVISE / FAIL

KOR_OBVIOUS_ANSWER_GATE:
PASS / FAIL

KOR_SECOND_BEST_GATE:
PASS / REVISE / FAIL

## 3. ANSWER-LENGTH LEAK
20문항 이상:
- 정답이 단독 최장 선지인 비율 > 50% => REVISE
- > 65% => FAIL
- 정답이 상위 2개 길이에 속하는 비율 > 75% => REVISE

문항 단위:
CORRECT_TO_MEDIAN_RATIO > 1.35 => 검토 필수.

길이를 기계적으로 동일화하지 않는다.
정답 위치와 문장 길이가 예측 신호가 되지 않게 한다.

## 4. STEM / LANGUAGE PATTERN
- 동일 stem skeleton 3연속 => FAIL
- 단일 stem skeleton 60% 초과 => REVISE
- '가장 적절한 것은?' 반복 자체보다 실제 요구 사고의 중복을 더 중요하게 본다.
- 정답만 온건한 복합문이고 오답은 모두 극단 단문이면 AI_CHOICE_PATTERN.

## 4-A. QUESTION TASK-FORM GATE
지문군 10문항:
- SINGLE_BEST_STATEMENT <= 4
- EXCEPT_INCORRECT <= 2
- QUESTION_TASK_FORM 종류 >= 4
- 동일 task form 3연속 금지
- CASE_APPLICATION >= 1
- 단순 SINGLE_BEST + EXCEPT만으로 7문항 이상 구성되면 FAIL

다양성은 발문 표현이 아니라 실제 판단 과업으로 측정한다.

KOR_TASK_FORM_DIVERSITY:
PASS / REVISE / FAIL

## 5. DUPLICATE REASONING AUDIT
지문별로 모든 문항에 ITEM_REASONING_AXIS를 부여한다.

동일 축 2개까지 허용 가능하나 둘 사이에 최소 하나가 달라야 한다:
- 근거 범위
- 요구 단계
- 적용 대상
- 비교 대상
- 조건

같은 축 + 같은 근거 + 같은 결론이면 DUPLICATE_AXIS_FAIL.

## 6. PASSAGE UTILIZATION SCORE
지문군마다 100점:
- CORE_EXAM_POINT_COVERAGE /25
- DISTRACTOR_COMPETITIVENESS /20
- DIFFICULTY_BALANCE /15
- SOURCE_GROUNDED /15
- REASONING_DIVERSITY /15
- LANGUAGE_NONLEAK /10

90+ = PASS
84~89 = REVISE
83 이하 = FAIL

단, hard fail은 점수 무관.

## 7. SET RELEASE GATE
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
KOR_SOURCE_TEXT_EXACT_LOCK = PASS when applicable
KOR_ALL_OPTION_AUDIT = PASS
KOR_OPTION_SEMANTIC_DUPLICATION_REVIEW = PASS
KOR_ANSWER_EVIDENCE_TRACE = PASS
KOR_SCOPE_EVIDENCE_TRACE = PASS
KOR_DIFFICULTY_MATCH = PASS

하나라도 FAIL이면 CONTENT_QA_STATUS=PASS 금지.

SOURCE_TEXT_BLOCK을 쓰는 경우 TEXT_FIDELITY=EXACT만 허용한다.
WHITESPACE_NORMALIZED, ARC 산출물/BANK/웹 원문 재사용, SHA-256·파일 위치 누락은 KOR_SOURCE_TEXT_EXACT_LOCK=FAIL이다.

## 7-A. UNIVERSAL PASS B PAYLOAD
모든 문항은 공통 독립 재풀이 gate의 QA_EVIDENCE를 보유한다.
- ANSWER_KEY / PASS A / AUTHOR_INTENT / TARGET_DIFFICULTY 제외 확인
- 전 선지 verdict + AXIS + CLAIM_KEY + 원문 위치 근거
- SECOND_BEST_OPTION / 경쟁 위험
- REASONING_STEPS / EVIDENCE_COUNT / 즉시 제거 선지 수
- ACTUAL_DIFFICULTY

같은 작품 해석을 표현만 바꾼 선지는 OPTION_SEMANTIC_DUPLICATION_REVIEW에서 FAIL한다.

## 8. CURRENT FAILURE SENTINELS
다음 유형은 특히 재발 방지한다:
- 같은 지문에서 주제/정서/태도 문항을 표현만 바꿔 반복
- 관찰과 추론 구분을 3문항 이상 반복
- 비문학 10문항 중 대부분이 문장 직접 찾기
- 정답 선지가 거의 항상 가장 길고 상세함
- ①②③④⑤가 5문항 단위로 순환
- 오답이 '모두/완전히/오직/무조건' 같은 단어만으로 탈락
- 한 선지만 작품/지문의 핵심 개념을 정상적으로 말하고 나머지 네 선지는 관련 없는 행동·정서·효과를 제시
- 표현 효과 문항에서 정답만 교과서적으로 자연스럽고 나머지 선지는 다른 표현법의 효과를 섞음
- 공통점 문항에서 정답만 넓고 상식적인 공통점이며 오답은 작품과 무관
- 철학 개념 문항에서 정답만 정확한 용어-정의 결합이고 나머지는 단순 반대·자리바꿈
- 주제/정서·태도/표현법/핵심 소재 기능보다 변별형 미세 추론이 과다
- 삭제·치환·미세 지칭어 추적이 학습 핵심보다 반복
- D4+ 비율을 높이기 위해 핵심 내신 포인트 문항을 삭제

## 9. INTERNAL REPORT
PASSAGE_ID별:
ITEM_COUNT
FOUNDATION_CORE_COUNT
CORE_EXAM_POINT_COUNT
CORE_EXAM_POINT_RATE
CORE_EXAM_AXIS_COVERAGE
DIFFICULTY_DISTRIBUTION
DISCRIMINATION_ONLY_TASK_COUNT
COUNTERFACTUAL_EDIT_COUNT
MICRO_REFERENCE_TRACE_COUNT
PASSAGE_USE_DISTRIBUTION
REASONING_DEPTH_DISTRIBUTION
REASONING_AXIS_DISTRIBUTION
DIRECT_LOOKUP_COUNT
MULTI_EVIDENCE_COUNT
TRANSFER_COUNT
STRONG_DISTRACTOR_DEFICIT_ITEMS
OBVIOUS_ANSWER_ITEMS
FIRST_PASS_CANDIDATE_COUNTS
SECOND_BEST_OPTIONS
DISTRACTOR_CLASS_DISTRIBUTION
ANSWER_LENGTH_FLAGS
STEM_PATTERN_FLAGS
TASK_FORM_DISTRIBUTION
TASK_FORM_FLAGS
DUPLICATE_AXIS_FLAGS
PASSAGE_UTILIZATION_SCORE

학생용 출력 금지.

## 10. EXAM REALISM / AI-STYLE LEAK GATE — V1.5
모든 ARC_N / ARC_FINAL 국어 세트는 quality/ARC_KOREAN_EXAM_REALISM_GATE_V1.0.md를 적용한다.

필수 내부값:
SCHOOL_TASK_FAMILY_RATE
DISTINCT_SCHOOL_TASK_FAMILIES
UNANCHORED_META_TASK_COUNT
RARE_ARTIFICIAL_TASK_COUNT
UNFUNCTIONAL_STUDENT_WRAPPER_COUNT
AI_CHOICE_PATTERN_COUNT
SAME_STEM_SKELETON_MAX_RUN
CORRECT_LENGTH_CUE_COUNT

필수 결과:
KOR_EXAM_REALISM_GATE=PASS
KOR_AI_STYLE_LEAK_GATE=PASS
KOR_SCHOOL_TASK_FAMILY_GATE=PASS

특히 다음은 최종 학생용 PDF 전에 다시 읽고 제거:
- 내부 QA/편집 용어가 발문이나 선지에 남음
- 정답만 섬세한 복합문이고 오답은 극단 단문
- 모든 선지가 같은 문장 골격에 단어 하나만 교체됨
- 학생 대화/정리 wrapper가 실제 사고 과정을 바꾸지 않음
- 삭제/치환/반사실 과업이 내신 핵심형보다 반복됨
- 범용 AI 문구가 여러 문항에 반복됨

실제 동북고 빈출 과업을 우선하되, 과거 기출 문구를 복제하지 않는다.


END ARC KOREAN ITEM QA V1.5
