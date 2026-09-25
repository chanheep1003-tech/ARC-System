# ARC KOREAN EXAM REALISM GATE V1.0
VERSION: 1.0
DATE: 2026-09-25
STATUS: ACTIVE-DEV
VALIDATION_MARKER: KOR_REALISM_20260925
ROLE: KOR ARC_N / ARC_FINAL school-exam realism + AI-style leak blocker

## 0. PURPOSE
국어 문항은 정답이 맞고 난도가 높아도 실제 내신 시험지처럼 읽히지 않으면 실전 가치가 낮다.
이 gate는 "AI가 만든 문제처럼 보이는가"를 감상적으로 평가하지 않고, 동북고 실제 시험의 반복 과업과 학생용 문체 규칙으로 분해해 검사한다.

REFERENCE PROFILE:
quality/source/KOR_DONGBOOK_EXAM_TYPE_PROFILE_2025_2026_V1.0.yaml

과거 시험은 구조·난도·과업 빈도 보정용일 뿐이며 문제 문장/선지 복제와 교사 의도 추정은 금지한다.

## 1. SCHOOL TASK FAMILY GATE
현재 시험범위에서 우선 허용되는 SCHOOL-LIKE TASK FAMILY:
- CONTENT_UNDERSTANDING
- SPEAKER_CHARACTER_ATTITUDE
- EXPRESSION_EFFECT
- MARKED_EXPRESSION_FUNCTION
- KEY_WORD_IMAGE_OBJECT_FUNCTION
- STRUCTURE_DEVELOPMENT
- VIEW_APPLICATION
- COMPARE_CONTRAST
- MULTI_JUDGMENT
- CENTRAL_CLAIM_CONCEPT
- CONCEPT_RELATION_CONTRAST
- CASE_APPLICATION

ARC_N:
- SCHOOL_TASK_FAMILY_RATE >= 0.75
- DISTINCT_SCHOOL_TASK_FAMILIES >= 5 for 20+ items
- 10-item passage group: at least 4 distinct school-like families

ARC_FINAL:
- SCHOOL_TASK_FAMILY_RATE >= 0.80
- familiar school forms are made harder through evidence competition and distractor quality, not exotic stem mechanics

KOR_SCHOOL_TASK_FAMILY_GATE=PASS / REVISE / FAIL

## 2. AI-STYLE LEAK — HARD FAIL
### 2.1 UNANCHORED META LANGUAGE
학교 자료나 <보기>가 실제로 제시한 표현이 아닌데 다음 내부 편집·QA 언어가 학생용 발문/선지에 노출되면 수정:
판단축 / 근거 범위 / 독해 전략 / 독해 원칙 / 검토 절차 / 정답 후보 / 추론 단계 /
second-best / true kernel / distractor / "어떻게 검증해야 하는가"류 평가자 메타 발문.

### 2.2 TEMPLATE-PROSE CHOICES
- 정답만 온건하고 세밀한 복합문, 오답은 극단적 단문
- 다섯 선지가 같은 틀에 단어 하나만 바꾼 기계적 평행문
- 오답들이 여러 관련 없는 축에서 동시에 틀려 지문 없이도 제거 가능
- 모두/오직/완전히/반드시/전혀가 오답 판별의 핵심인 선지 3개 이상
- 설명문처럼 친절한 정답 vs 엉성한 오답
- 정답이 가장 길고 가장 교과서적인 문장이라는 표면 단서

### 2.3 WRAPPER WITHOUT FUNCTION
학생 정리글/학생 대화/교사 질문 형식 자체는 실제 학교에서도 사용하므로 금지하지 않는다.
다만 wrapper를 제거해도 요구 사고가 완전히 동일하면 UNFUNCTIONAL_STUDENT_WRAPPER.
10문항 지문군에서 UNFUNCTIONAL_STUDENT_WRAPPER > 1이면 REVISE.

### 2.4 ARTIFICIAL DISCRIMINATION
삭제/치환/반사실/극미세 지칭어 추적은 핵심 내신형 보완용으로만 사용.
RARE_ARTIFICIAL_TASK_RATE > 0.10 without explicit school anchor => REVISE.
FINAL도 낯선 발문 자체로 어렵게 만들지 않는다.

KOR_AI_STYLE_LEAK_GATE=PASS / FAIL

## 3. NATURAL KOREAN EXAM LANGUAGE
- 발문은 짧고 평가 대상을 분명히 한다.
- 선지는 한 문항 안에서 비슷한 정보 밀도와 문체 수준을 갖는다.
- 전문 용어는 학교자료/교과서 표현을 우선한다.
- 작품 해석은 원문 근거에 붙어 있고 불필요한 이론 언어를 덧붙이지 않는다.
- 어려움은 한 단어 함정이 아니라 두세 후보 사이 근거 구분에서 발생한다.

금지:
- 내부 분류명/메타데이터 학생 노출
- "종합적으로 고려하면", "정확한 근거를 바탕으로", "판단 기준에 따라" 같은 범용 AI 문구 반복
- 현실적으로 아무도 하지 않을 해석/행동을 오답으로 삽입
- 선지마다 과도한 이유절을 붙여 해설문처럼 만듦

## 4. HIGH-FREQUENCY SCHOOL FORM PRIORITY
문학: 내용 이해 → 화자/서술자 정서·태도 → 표현법과 효과 → 핵심 시어·소재·이미지 기능 →
시상/구조/시간 전개 → <보기> 적용 → 작품 비교 → ㄱㄴㄷ/복수 판단.

비문학: 중심 주장/핵심 개념 → 문단/논증 구조 → 개념 관계·차이 → 내용 일치/불일치 →
<보기>/사례 적용 → 복수 판단 → 두 관점 비교.

고난도는 위 빈출 과업에서 strong distractor와 복합 근거를 강화해 만든다.

## 5. SET METRICS
SCHOOL_TASK_FAMILY_RATE
DISTINCT_SCHOOL_TASK_FAMILIES
UNANCHORED_META_TASK_COUNT
RARE_ARTIFICIAL_TASK_COUNT
UNFUNCTIONAL_STUDENT_WRAPPER_COUNT
AI_CHOICE_PATTERN_COUNT
SAME_STEM_SKELETON_MAX_RUN
CORRECT_LENGTH_CUE_COUNT
SCHOOL_REALISM_NOTES

HARD FAIL:
- AI_CHOICE_PATTERN_COUNT > 0
- CORRECT_LENGTH_CUE_COUNT > 0 after final option audit
- SAME_STEM_SKELETON_MAX_RUN > 2
- student-facing internal QA jargon exposure
- SCHOOL_TASK_FAMILY_RATE below minimum after one revision pass

## 6. RELEASE
KOR_EXAM_REALISM_GATE=PASS
KOR_AI_STYLE_LEAK_GATE=PASS
KOR_SCHOOL_TASK_FAMILY_GATE=PASS

ARC_N / ARC_FINAL 모두 위 세 값이 PASS가 아니면 KOR content lock 금지.

END ARC KOREAN EXAM REALISM GATE V1.0
