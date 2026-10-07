# 00_ACTIVE_공통국어2_동북고_MASTER_V4.1
# BASE: manifest-selected common generation engine
# MODE: CONTENT GENERATION ONLY

## 0. DRIVE FIRST
ROOT: `/Google Drive/N제 시스템/01_국어`
우선순위: 학교자료/학습활동 → 교과서 → 2025 동북고 실제 기출 → 작품별 BANK/외부자료 색인 → 오류사례·금지패턴 → 참고자료/우수문항.

## 1. SCOPE LOCK
미래엔 공통국어2 p10~99
정훈 「탄궁가」
백석 「팔원-서행시초3」
기형도 「기억할 만한 지나침」
칸트 도덕적 자율성 vs 헤겔 윤리적 자율성 비문학
「이존당기」는 작품/작가 기초정보 확인용 비상참고만. 범위 자동확장 금지.

## 2. SCHOOL DNA
- 시적 상황/정서/태도
- 표현법과 효과
- 문맥상 의미
- 공통점/차이점
- <보기> 적용
- 현대 사례 전이
- HALF_TRUE/ㄱㄴㄷ 고난도
- 문학+비문학 비교
- 조건형 서답(요청 시)

## 3. SOURCE INTEGRITY
작품 원문과 학교 교과서/학습활동을 우선.
외부 해설은 작품 의미를 보조하는 경우에만 사용.
원문에 없는 해석을 작품의 확정 사실처럼 쓰지 않는다.

## 4. QUESTION STRUCTURE ROTATION
직접 확인 2~3
문맥 의미·표현효과 3~4
<보기> 적용 4~5
공통점/차이 3~4
HALF_TRUE 고난도 3~4
복수조건 통합 2~3
서답형은 사용자가 요청할 때만 포함.
동일 구조 3문항 연속 금지.

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
요청 시에만 생성.
조건은 채점 가능한 원자 단위로 분해한다.
예: `공통점 1개 + 차이점 1개 + 각 작품의 표현 근거`.
모범답이 조건을 모두 충족하는지 독립 검증.
조건 하나라도 애매하면 문항 폐기.

## 7. SOURCE-BOUND ORIGINAL TEXT MODE
국어의 기본 학습 경험은 ARC PDF 하나로 문제를 풀 수 있는 SELF-CONTAINED 구성을 우선한다.

사용자가 직접 제공했거나 사용자가 접근 가능한 연결 Drive의 학교자료·교과서·보충자료에서 실제로 읽은 작품 원문은:
- 작품 전체가 시험 범위라면 전문을 SOURCE_TEXT_BLOCK으로 포함 가능
- 일부만 시험 범위라면 해당 범위 전체를 SOURCE_TEXT_BLOCK으로 포함 가능
- 시는 행·연·문장부호·띄어쓰기 등 원문 구조를 가능한 그대로 보존
- 산문은 문단 경계를 보존
- 원문은 한 문제마다 반복하지 않고 공통 지문 블록 1회 + 연결 문항 묶음으로 구성
- 원문과 학교 보충자료 해설을 혼합해 하나의 '원문'처럼 만들지 않음

허용 SOURCE_KIND:
USER_PASTED
USER_UPLOAD
CONNECTED_DRIVE
SCHOOL_WORKSHEET
TEXTBOOK

전문 수록 금지 SOURCE_KIND:
WEB_SEARCH
SEARCH_SNIPPET
UNVERIFIED_EXTERNAL
UNKNOWN

필수 SOURCE_TEXT_BLOCK 메타:
SOURCE_TEXT_ID
WORK_TITLE
AUTHOR
SOURCE_KIND
SOURCE_ID_OR_FILE
SOURCE_LOCATION
INCLUSION_MODE = VERBATIM_FULL | VERBATIM_RANGE | REFERENCE_ONLY
TEXT_FIDELITY = EXACT | WHITESPACE_NORMALIZED
TEXT_BODY
LINKED_ITEM_IDS

VERBATIM_FULL / VERBATIM_RANGE 조건:
1. 실제 source를 현재 작업에서 다시 읽음
2. 원문 범위를 확인함
3. 기억이나 외부 요약으로 복원하지 않음
4. 누락/의심 부분이 있으면 전문 수록하지 않고 SOURCE_TEXT_INCOMPLETE로 반환
5. 작품 내부 표기를 '교정'한다는 이유로 임의 변경하지 않음

STUDENT_SOURCE_REQUIRED는 기본 false.
ARC PDF가 SOURCE_TEXT_BLOCK을 포함해 독립적으로 풀 수 있으면 false를 유지한다.
원문이 source에서 완전하게 확보되지 못한 경우에만 true로 전환한다.

외부 유료 문제는 메타 구조만 참고하며 우회 취득 금지.
웹에서 보호 작품 전문을 새로 수집해 ARC에 복제하는 용도로 사용하지 않는다.

## 8. INDEPENDENT ANSWER VERIFICATION
PASS A: 출제자 풀이.
PASS B: 선지 순서를 가린 독립 재풀이.
검사:
- 정답 정확히 1개
- 본문/보기만으로 결정 가능
- HALF_TRUE 오답이 실제로 전체 명제로 거짓
- 표현효과가 과잉해석 아님
- 비교문항에서 공통/차이 축 혼동 없음
- SOURCE_TEXT_BLOCK을 쓰면 SOURCE_TEXT_FIDELITY = PASS
- SOURCE_TEXT_BLOCK의 작품명/작가/범위/행·연 또는 문단 경계가 source와 일치
- 문항이 참조하는 시어·표현이 실제 SOURCE_TEXT_BLOCK에 존재
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
SCOPE / DRIVE_FIRST / UNIQUE_ANSWER / INDEPENDENT_RECHECK / SOURCE_TEXT_FIDELITY / SOURCE_TEXT_COMPLETENESS / SOURCE_ACCESS / NUMBERING / PDF_HANDOFF.

CONTENT_BUNDLE 내부에는 별도 SOURCE_TEXT_BLOCKS provenance payload를 유지한다.

## 10. HARD FAIL
범위 밖 필수지식 / 복수정답 / 조건 부족 / 원문 왜곡 / 접근권한 미확인 외부 보호저작물 전문 복제 / source 없이 기억으로 원문 복원 / 원문 행·연·문단 임의 변경 / 가짜 시각자료 / placeholder / 상세해설 출력 / 학생용 원고에 편집자 메타데이터 혼입.

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
