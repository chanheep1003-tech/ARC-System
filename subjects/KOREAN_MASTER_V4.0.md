# 00_ACTIVE_공통국어2_동북고_MASTER_V4.0
# BASE: ARC COMMON GENERATION ENGINE V4.0
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

## 6. 조건형 서답
요청 시에만 생성.
조건은 채점 가능한 원자 단위로 분해한다.
예: `공통점 1개 + 차이점 1개 + 각 작품의 표현 근거`.
모범답이 조건을 모두 충족하는지 독립 검증.
조건 하나라도 애매하면 문항 폐기.

## 7. COPYRIGHT
현대문학 전문/장문 복제 금지.
필요한 최소 인용만 사용하고 학교 제공 원문이 있으면 그 범위 안에서 출제.
외부 유료 문제는 메타 구조만 참고하며 우회 취득 금지.

## 8. INDEPENDENT ANSWER VERIFICATION
PASS A: 출제자 풀이.
PASS B: 선지 순서를 가린 독립 재풀이.
검사:
- 정답 정확히 1개
- 본문/보기만으로 결정 가능
- HALF_TRUE 오답이 실제로 전체 명제로 거짓
- 표현효과가 과잉해석 아님
- 비교문항에서 공통/차이 축 혼동 없음
불일치 시 출력 금지.

## 9. OUTPUT
SECTION A QUESTION_MANUSCRIPT: 학생용 원고만.
SECTION B ANSWER_KEY: 번호+정답만.
SECTION C LAYOUT_ASSET_MANIFEST: 문항번호/ASSET_CLASS/ASSET_TYPE/VISUAL_ID/STATUS/KEEP_TOGETHER.
SECTION D QC_STATUS:
SCOPE / DRIVE_FIRST / UNIQUE_ANSWER / INDEPENDENT_RECHECK / COPYRIGHT / NUMBERING / PDF_HANDOFF.

## 10. HARD FAIL
범위 밖 필수지식 / 복수정답 / 조건 부족 / 원문 왜곡 / 작품 전문 복제 / 가짜 시각자료 / placeholder / 상세해설 출력 / 학생용 원고에 편집자 메타데이터 혼입.


## 11. ARC HANDOFF
공통 엔진 V4.0의 HANDOFF_META와 SECTION A~D를 그대로 따른다. ANSWER_KEY는 편집/검증용이며 학생 PDF에 직접 삽입하지 않는다. FINAL 요청도 별도 FINAL 프롬프트를 쓰지 않고 PRODUCT_MODE=ARC_FINAL로 처리한다.
