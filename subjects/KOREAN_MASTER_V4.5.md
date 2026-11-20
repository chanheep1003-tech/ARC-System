# 00_ACTIVE_공통국어2_동북고_MASTER_V4.5
# VERSION_DATE: 2026-11-19
# SUPERSEDES: archive/subjects/KOREAN_MASTER_V4.4.md (archived)
# CHANGE: 기말 범위 참조로 SCOPE LOCK 교체, 난도는 요청별 계획(N°)·동북고 앵커 이상(FINAL), 서답형·배점 필수화, 인쇄 무결성
# BASE: manifest-selected common generation engine
# MODE: CONTENT GENERATION ONLY

## 0. DRIVE FIRST
ROOT: `/Google Drive/N제 시스템/01_국어`
우선순위: 학교자료/학습활동 → 교과서 → 2025 동북고 실제 기출 → 작품별 BANK/외부자료 색인 → 오류사례·금지패턴 → 참고자료/우수문항.

## 1. SCOPE LOCK — 2026학년도 2학기 기말 (학교 공지 2026-11-13)
범위의 유일한 근거: `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml` + `ops/exams/EXAM_CONTEXTS_V1.yaml` (KOR)
- 미래엔 공통국어2 교과서 3단원, 4-1단원 (104~149쪽)
- 보충 프린트 전범위
- 시험 구조: 선택형 22문항(80점) + 서술형 4문항(20점)

중간고사 범위(교과서 p10~99, 「탄궁가」·「팔원」·「기억할 만한 지나침」·칸트/헤겔 비문학)는
`EXAM_SCOPE=ARCHIVED_REPLAY`로 명시 요청할 때만 쓴다. 기말 문항의 정답 근거로 쓰지 않는다.
범위 밖 작품·개념으로 정답을 결정하지 않는다. 범위가 바뀌면 이 문서가 아니라 공지 파일을 갱신한다.

## 2. SCHOOL DNA
- 시적 상황/정서/태도
- 표현법과 효과
- 문맥상 의미
- 공통점/차이점
- <보기> 적용
- 현대 사례 전이
- HALF_TRUE/ㄱㄴㄷ 고난도
- 문학+비문학 비교
- 조건형 서답 (FINAL 필수 4문항, N°는 계획 카드의 서답형 수)

## 3. SOURCE INTEGRITY
작품 원문과 학교 교과서/학습활동을 우선.
외부 해설은 작품 의미를 보조하는 경우에만 사용.
원문에 없는 해석을 작품의 확정 사실처럼 쓰지 않는다.

## 4. ARC_N BALANCED SCHOOL-PREP PROFILE
국어 N°는 변별 문제만 모은 세트가 아니다.

지문 10문항 기본:
- 핵심 내신 포인트 3
- 표준 적용 4
- 상위 변별 2
- 최상위 0~1

문학 필수:
- 주제/중심 의미
- 화자 정서·태도
- 중요 표현법과 효과
- 핵심 시어·소재·이미지 기능
- 시상/시간/태도 전개

비문학 필수:
- 중심 주장/핵심 개념
- 글의 구조/서술 방식
- 핵심 개념 관계
- 내용 일치
- 사례/조건 적용

지문당 CORE_EXAM_POINT=YES 최소 6.
FOUNDATION_CORE_ITEM 최소 3.
삭제/치환/반사실적 변형 최대 1.
미세 지칭어 추적 최대 1.

ARC_N 난도·문항 수 (V4.5):
- 요청마다 다르다. 계획 카드(`python tooling/arc.py plan --subject KOR …`)가 정한 분포를 번들 `plan:`에 옮긴다.
- 사용자가 값을 말하지 않으면 `ops/planning/ARC_PLAN_DEFAULTS_V1.yaml`의 `kor_versions`(V1~V4, V6)를 쓴다.
- 계획이 어떤 분포든 CORE_EXAM_POINT_COVERAGE(지문당 최소 6)는 유지한다.

ARC_FINAL 난도:
- 동북고 국어 다회차 앵커(`quality/anchors/KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.1.yaml`)와 같거나 살짝 더 어렵게.

서답형:
- ARC_FINAL: 학교 구조 그대로 4문항(합계 20점). 선택형 22문항 배점 합계 80점.
- ARC_N: 계획 카드의 서답형 수(`--constructed`). 0문항도 계획이 정하면 허용.

## 5. DISTRACTOR ENGINE
반드시 세트 전체에서 다양화:
HALF_TRUE
HALF_TRUE_OBSERVATION_INFERENCE_SWAP
SPEAKER_KNOWLEDGE_OVERREACH
EMOTION_TRIGGER_SWAP
TEMPORAL_POSITION_SWAP
SAME_AUTHOR_SAME_ATTITUDE
COMMON_DIFFERENCE_SWAP
RIGHT_EXPRESSION_WRONG_EFFECT
RIGHT_THEME_WRONG_EVIDENCE
AUTONOMY_AS_ARBITRARY_CHOICE
COMMON_CORE_DIFFERENT_GROUND_SWAP

오답은 문장의 일부가 참이어도 전체 명제가 명확히 거짓이어야 한다.
범위 밖 지식이 있어야만 틀렸음을 알 수 있는 선지는 HARD FAIL.

### KOR HIGH-DIFFICULTY GATE
D4/BANK_A 후보는 최소 2개의 오답이 첫 독해에서 실제 후보로 남아야 한다.
각 핵심 오답은 HALF_TRUE / 관찰-추론 교환 / 표현법은 맞고 효과는 틀림 / 공통점은 맞고 차이 한 축만 틀림처럼 같은 판단축에서 경쟁해야 한다.

다음은 D4 금지:
- <보기>가 정답 원리를 직접 말하고 정답이 그 문장을 그대로 재진술
- <보기>의 한 문장을 단순 부정한 선지만 고르면 끝나는 구조
- 3개 이상의 오답이 작품/자료와 명백히 무관하여 즉시 제거 가능
- 긴 지문 또는 철학 용어 때문에 겉보기만 어려운 문항

D4는 실제로 최소 2개 판단단계를 요구해야 한다.
예: 관찰 사실 확인 → 화자의 추론 구분 / 두 작품 각각 판단 → 공통·차이 결합 / 표현법 판정 → 효과 근거 검증.

BANK_A 후보와 D4 후보는 최초 점수/난도를 보지 않은 blind recheck를 거친다.

## 6. 조건형 서답
FINAL은 항상, N°는 계획이 정한 수만큼 생성한다.
필수 필드: `conditions`(2~3개), `model_answer`, `accepted_variants`, `rubric`(부분점수 포함), `points`, `answer_targets`.
조건은 채점 가능한 원자 단위로 분해한다.
예: `공통점 1개 + 차이점 1개 + 각 작품의 표현 근거`.
모범답이 조건을 모두 충족하는지 독립 검증.
조건 하나라도 애매하면 문항 폐기.

## 7. KOR EXACT SOURCE-BOUND ORIGINAL TEXT MODE
국어의 기본 학습 경험은 ARC PDF 하나로 문제를 풀 수 있는 SELF-CONTAINED 구성을 우선한다.

학생용 문제지의 문학·비문학 원문은 사용자가 제공한 교과서·학교 보충자료·업로드 또는 연결 Drive의 RAW SCHOOL SOURCE에서 실제로 다시 읽은 원문만 사용한다.

허용 SOURCE_ORIGIN:
- USER_UPLOAD
- USER_PROVIDED_SCHOOL_SUPPLEMENT
- USER_PROVIDED_TEXTBOOK
- CONNECTED_DRIVE_RAW_SCHOOL_SOURCE

금지 SOURCE_ORIGIN:
- WEB_SEARCH / SEARCH_SNIPPET / UNVERIFIED_EXTERNAL / UNKNOWN
- ARC_N_OUTPUT / ARC_FINAL_OUTPUT / ARC_CORE_OUTPUT
- GENERATED_MANUSCRIPT / VERIFIED_BANK / DEEP_RESEARCH / EXTERNAL_PROBLEM_BOOK

허용된 작품 원문은:
- 작품 전체가 시험 범위라면 전문을 SOURCE_TEXT_BLOCK으로 포함 가능
- 일부만 시험 범위라면 해당 범위 전체를 SOURCE_TEXT_BLOCK으로 포함 가능
- 시는 행·연·문장부호·띄어쓰기 등 원문 구조를 가능한 그대로 보존
- 산문은 문단 경계를 보존
- 원문은 한 문제마다 반복하지 않고 공통 지문 블록 1회 + 연결 문항 묶음으로 구성
- 원문과 학교 보충자료 해설을 혼합해 하나의 '원문'처럼 만들지 않음

SOURCE_ROLE은 반드시 RAW_SCHOOL_SOURCE이다.
기존 ARC 산출물이나 문제은행에서 보이는 원문은 원본이 아니므로 raw 교과서/보충자료까지 역추적하지 못하면 사용 금지한다.

필수 SOURCE_TEXT_BLOCK 메타:
SOURCE_TEXT_ID
WORK_TITLE
AUTHOR
SOURCE_KIND
SOURCE_ID_OR_FILE
SOURCE_LOCATION
INCLUSION_MODE = VERBATIM_FULL | VERBATIM_RANGE | REFERENCE_ONLY
TEXT_FIDELITY = EXACT
SOURCE_TEXT_SHA256
SOURCE_ROLE = RAW_SCHOOL_SOURCE
TEXT_BODY
LINKED_ITEM_IDS

VERBATIM_FULL / VERBATIM_RANGE 조건:
1. 실제 source를 현재 작업에서 다시 읽음
2. 원문 범위를 확인함
3. 기억이나 외부 요약으로 복원하지 않음
4. 누락/의심 부분이 있으면 전문 수록하지 않고 SOURCE_TEXT_INCOMPLETE로 반환
5. 작품 내부 표기를 '교정'한다는 이유로 임의 변경하지 않음
6. 단어·문장부호·띄어쓰기·행·연·문단 경계를 source와 대조
7. SOURCE_TEXT_SHA256을 잠그고 CONTENT_BUNDLE에 유지

WHITESPACE_NORMALIZED는 학생용 원문에 사용 금지한다.
시 한 행이 조판 공간에 맞지 않아도 출제/조판 엔진이 자의적으로 분할·재작성하지 않고 레이아웃을 재배치한다.

STUDENT_SOURCE_REQUIRED는 기본 false.
ARC PDF가 SOURCE_TEXT_BLOCK을 포함해 독립적으로 풀 수 있으면 false를 유지한다.
원문이 source에서 완전하게 확보되지 못한 경우에만 true로 전환한다.

외부 유료 문제는 메타 구조만 참고하며 우회 취득 금지.
웹에서 보호 작품 전문을 새로 수집해 ARC에 복제하는 용도로 사용하지 않는다.

## 8. INDEPENDENT ANSWER VERIFICATION
공통 Universal Independent Solve & Difficulty Gate를 모두 적용한다.
PASS A: 출제자 풀이와 원문 근거 기록.
PASS B: ANSWER_KEY / PASS A / 출제 의도 / 목표 난도를 가린 독립 재풀이.
검사:
- 정답 정확히 1개
- 본문/보기만으로 결정 가능
- HALF_TRUE 오답이 실제로 전체 명제로 거짓
- 표현효과가 과잉해석 아님
- 비교문항에서 공통/차이 축 혼동 없음
- SOURCE_TEXT_BLOCK을 쓰면 SOURCE_TEXT_FIDELITY = PASS
- SOURCE_TEXT_BLOCK의 작품명/작가/범위/행·연 또는 문단 경계가 source와 일치
- 문항이 참조하는 시어·표현이 실제 SOURCE_TEXT_BLOCK에 존재
- 모든 선지의 TRUE/FALSE/HALF_TRUE/UNSUPPORTED 판정과 행·연·문단 근거 존재
- TARGET_DIFFICULTY와 ACTUAL_DIFFICULTY 일치
불일치 시 출력 금지.

## 9. OUTPUT
SECTION A QUESTION_MANUSCRIPT:
- 학생용 원고만.
- SOURCE_TEXT_BLOCK 사용 시 작품 원문 블록을 연결 문항군 앞에 실제 학생용 지문으로 포함.
- 작품명/작가 표시는 학생용에 필요한 수준으로 유지.
- 내부 SOURCE_FILE_ID/Drive ID/QC 메타는 노출하지 않음.

SECTION B ANSWER_KEY: 번호+정답만.
SECTION C LAYOUT_ASSET_MANIFEST: 문항번호/ASSET_CLASS/ASSET_TYPE/VISUAL_ID/STATUS/KEEP_TOGETHER.
SECTION D QC_STATUS:
SCOPE / DRIVE_FIRST / UNIQUE_ANSWER / INDEPENDENT_RECHECK / ALL_OPTION_AUDIT / OPTION_SEMANTIC_DUPLICATION_REVIEW / ANSWER_EVIDENCE_TRACE / SCOPE_EVIDENCE_TRACE / DIFFICULTY_MATCH / KOR_SOURCE_TEXT_EXACT_LOCK / SOURCE_TEXT_FIDELITY / SOURCE_TEXT_COMPLETENESS / SOURCE_ACCESS / NUMBERING / PDF_HANDOFF.

CONTENT_BUNDLE 내부에는 별도 SOURCE_TEXT_BLOCKS provenance payload를 유지한다.

## 10. HARD FAIL
범위 밖 필수지식 / 복수정답 / 조건 부족 / 원문 왜곡 / WHITESPACE_NORMALIZED / 기존 ARC 산출물·BANK·웹을 원문 권위로 사용 / 접근권한 미확인 외부 보호저작물 전문 복제 / source 없이 기억으로 원문 복원 / 원문 단어·문장부호·띄어쓰기·행·연·문단 임의 변경 / 가짜 시각자료 / placeholder / 상세해설 출력 / 학생용 원고에 편집자 메타데이터 혼입.

## 11. ARC HANDOFF
manifest-selected 공통 엔진의 HANDOFF_META와 SECTION A~D를 그대로 따른다.
ARC_N ANSWER_KEY는 편집/검증용 잠금 데이터이면서 Typesetter가 문제 종료 후 필수 빈 페이지를 거쳐 최종 compact answer section으로 삽입한다.
ARC_FINAL은 해당 제품 정책에 따라 학생 문제지와 정답 산출물을 분리한다.
FINAL 요청도 별도 FINAL 프롬프트를 쓰지 않고 PRODUCT_MODE=ARC_FINAL로 처리한다.

## 12. GOLD STANDARD ANCHORS
필수 로드: manifest-selected Korean GOLD anchor pack.
생성 전 GOOD 3문항, BAD 3문항을 실제 비교 기준으로 읽는다.
각 생성 문항 내부 메타데이터에 `NEAREST_GOOD_ANCHOR / NEAREST_BAD_ANCHOR / ANCHOR_MATCH_NOTE`를 기록한다.
앵커는 범위를 확장하지 않으며 현재 SCOPE/학교자료가 항상 우선한다.

## 13. DONGBOOK EXAM REALISM + AI-STYLE REMOVAL — V4.4
등록 필수:
- quality/source/KOR_DONGBOOK_EXAM_TYPE_PROFILE_2025_2026_V1.0.yaml
- quality/ARC_KOREAN_EXAM_REALISM_GATE_V1.0.md

실제 동북고 기출은 문제 문장 복제나 교사 의도 예측에 사용하지 않는다.
사용 목적은 반복되는 과업 형식, 정보 밀도, 보기 활용, 비교/복수판단 방식과 난도 감각의 보정이다.

현재 우선 과업:
문학 = 내용 이해 / 화자 태도 / 표현법·효과 / 핵심 시어·소재 기능 / 구조·전개 / <보기> 적용 / 작품 비교 / 복수 판단.
비문학 = 중심 개념 / 구조 / 개념 관계 / 내용 일치 / <보기>·사례 적용 / 복수 판단 / 관점 비교.

국어 N°와 FINAL은 KOR_EXAM_REALISM_GATE=PASS, KOR_AI_STYLE_LEAK_GATE=PASS, KOR_SCHOOL_TASK_FAMILY_GATE=PASS가 필수다.
난도는 낯선 발문이나 인위적 삭제·치환보다 익숙한 내신 과업에서 매력적 오답과 복수 근거를 강화해 만든다.
학생용 원고에 판단축/QA/second-best/true-kernel 등 내부 편집 용어가 노출되면 HARD FAIL.



## 14. PRINT-EXAM INTEGRITY — V4.5
- 문법·맞춤법 `<보기>`: 조항 원문과 사실 자료만 (`quality/ARC_VIEW_EVIDENCE_POLICY_V1.0.md`)
- 형식: `quality/korean/ARC_KOR_SCHOOL_HYBRID_FORMAT_V1.0.md` (무힌트 조항 적용 + 실전 텍스트 복합 교정 + 조건부 서답형)
- 선택형 표제어·예문을 서답형에서 다시 쓰지 않는다 (`quality/ARC_SET_CROSS_ITEM_LEAK_GATE_V1.0.md`)
- 문항마다 `headwords`, 의도한 오류 선지는 `intended_errors`
- 생산 파이프라인 `PRINT_INTEGRITY_GATE` FAIL이면 CONTENT_LOCK 금지
