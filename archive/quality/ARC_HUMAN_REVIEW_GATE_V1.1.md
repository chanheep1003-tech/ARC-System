# ARC HUMAN REVIEW GATE V1.1
VERSION: 1.1
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: final human approval before student-facing PDF release

## 0. PURPOSE
AI 검수는 전수 수행하되, 사람이 더 잘 확인할 수 있는 범위/표시/렌더/최종 산출물 이상을 PDF 배포 직전에 확인한다.
사용자에게 전체 문항을 다시 풀게 하지 않는다.

## 1. POSITION IN PIPELINE
GENERATION
→ FACT/ANSWER QA
→ ITEM/SET QA
→ VISUAL RENDER
→ VISUAL PASS A/B
→ PDF PREFLIGHT
→ PDF FULL RENDER QC
→ HUMAN_REVIEW_PACKET
→ HUMAN_REVIEW_GATE
→ RELEASE_READY=true
→ FINAL RELEASE

HUMAN_REVIEW_GATE 이전 PDF는 DRAFT_REVIEW 상태다.
사용자의 명시적 승인 없이 FINAL_RELEASED로 표기하지 않는다.

## 2. AI MUST FINISH FIRST
사람에게 넘기기 전에 AI가 반드시 완료:
- SCOPE_LOCK
- UNIQUE_ANSWER / independent recheck
- ANSWER_KEY item-number match
- C_X_MARK_FILTER where applicable
- X_MARK_DETECT_REPORT when executable tooling is available
- VISUAL_PASS_A/B + QUESTION_VISUAL_CROSSCHECK for ESSENTIAL visuals
- PDF_PREFLIGHT_STATUS + clipping/overlap/glyph/page-break QC
- student PDF answer/QC metadata leak check

AI가 FAIL인 항목을 사람에게 '승인해 달라'고 넘기지 않는다.
먼저 수정하거나 BLOCKED로 표시한다.

## 3. HUMAN REVIEW PACKET
사람이 볼 것은 한 페이지/짧은 요약으로 만든다.

Required fields:
REVIEW_ID:
PRODUCT_MODE:
SUBJECT:
TARGET_RANGE:
ITEM_COUNT:
AI_QA_STATUS:
HIGH_RISK_ITEMS:
SOCIAL_C_USED: YES/NO
TRUE_VISUAL_COUNT:
DRAFT_PDF:
ANSWER_KEY_PREVIEW:
FLAGS_REQUIRING_HUMAN_ATTENTION:

### USER CHECK A — 범위
사용자가 확인:
- 내가 요청한 시험범위가 맞는가?
- 빠져야 할 단원이 들어가 있지 않은가?
- 학교에서 따로 제외한다고 한 내용이 들어가 있지 않은가?

AI는 범위를 짧은 목록으로 제시한다.
사용자는 교과서 페이지를 다시 전부 확인할 필요가 없다.

### USER CHECK B — 통합사회 C파트 X 표시
SOCIAL_C_USED=YES일 때만 필수.
AI는:
- 사용한 C파트 개념/자료 목록
- 해당 학습지 페이지 번호
- 경계가 불명확했던 후보
를 제시한다.

사용자는 실제 C 학습지의 손글씨 X표시와 대조해
C_X_HUMAN = PASS / CHANGE_REQUIRED만 판단한다.

X표시가 걸친 영역이나 경계가 애매하면 승인하지 않고 제외한다.

### USER CHECK C — 시각자료
TRUE_VISUAL이 있을 때만 필수.
AI는 모든 시각자료의 축소 미리보기 또는 페이지 번호 목록을 제공한다.
사용자는:
- 그림/그래프가 실제로 보이는가
- 잘리거나 겹치지 않았는가
- 글자/축/범례가 읽히는가
- 문제에서 말하는 그림과 눈에 보이는 그림이 명백히 어긋나지 않는가
만 확인한다.

수치 정확성/화학·역사 사실 검산은 AI QA 책임이며 사용자가 전부 재계산하지 않는다.

### USER CHECK D — 정답/최종본 sanity
AI는 전체 정답을 독립 검증한다.
사용자는 전 문항을 다시 풀지 않는다.

사용자가 확인:
- 정답표 번호가 문항 번호와 맞아 보이는가
- AI가 HIGH_RISK_ITEMS로 표시한 문항 중 이상한 것이 없는가
- 학생용 PDF에 정답/해설/내부 메타데이터가 섞이지 않았는가
- 문항 누락/중복/페이지 이상이 눈에 띄지 않는가

HIGH_RISK_ITEMS 기본:
- D4/D5
- 계산/정량
- 복수판단
- 역사 연표/사료
- DFS/BFS
- 권리구제/철학 비교
- AI 재검수 점수 차이가 큰 문항
최대 5개를 우선 노출한다.

## 4. USER RESPONSE CONTRACT
사용자는 다음 둘 중 하나만 하면 된다.

APPROVE examples:
- 승인
- 이대로 사용
- PASS

CHANGE_REQUIRED examples:
- 수정: 7번 그래프 축 확인
- 수정: C파트 이 부분 제외
- 수정: 12번 정답 의심

승인 시:
HUMAN_REVIEW_STATUS = PASS
RELEASE_READY = true

수정 요청 시:
HUMAN_REVIEW_STATUS = CHANGE_REQUIRED
RELEASE_READY = false
해당 부분 수정 → 관련 AI QA 재실행 → 새 REVIEW_PACKET 생성.

## 5. PRODUCT RULE
ARC_N / ARC_FINAL:
- FINAL release 전에 HUMAN_REVIEW_GATE 필수.
- 정답 독립 검증은 AI 책임.
- 사용자 검토는 sanity + 범위/표시/렌더 확인 중심.

ARC_CORE:
- 범위와 핵심 개념 누락/과잉 포함 여부
- 시각자료 렌더
- 명백한 오탈자/조판 이상
만 확인.
문장별 사실 검증은 AI가 선행한다.

## 6. FAST MODE
시험 직전 시간 절약용.
다음이 모두 AI PASS면 사용자는 4개 항목만 본다:
1. 범위 한 줄 요약
2. C파트 X 표시 해당 여부
3. 시각자료 페이지
4. HIGH_RISK 최대 5문항 + 학생 PDF 누출 여부

FAST_HUMAN_REVIEW도 사용자 승인 자체를 생략하지 않는다.

## 7. HARD BLOCKS
다음은 HUMAN 승인으로 덮을 수 없다:
- 복수정답/정답 없음
- 범위 밖 필수지식
- C X표시 침범 확인
- X-mark detector의 AUTO_EXCLUDE 영역 사용
- 필수 시각자료 누락
- 데이터/그래프 수치 불일치
- 역사 사실 오류
- DFS/BFS 유일성 오류
- 학생 PDF 정답 노출
- placeholder
- clipping/overlap that affects solving
- ESSENTIAL visual PASS B 미실행/FAIL
- PDF_PREFLIGHT FAIL

## 8. CONTINUITY / RELEASE-ONLY GATE
HUMAN_REVIEW is a FINAL RELEASE gate, not an intermediate production gate.

Before asking for physical review, the system should normally already have:
- CONTENT_LOCK=PASS
- TYPESET_STATUS=PASS
- PDF_QC_STATUS=PASS
- storage attempted
- exact parent verification completed when technically possible

A pending physical print review must not stop:
- full PDF rendering
- PDF QC
- Drive upload
- exact parent metadata verification

Normal digital endpoint:
RELEASE_STATUS=READY_FOR_PHYSICAL_REVIEW
FINAL_RELEASED=false

Only explicit user approval changes FINAL_RELEASED to true.

## 9. INTERMEDIATE SAMPLE REDUCTION
Do not require a repeated sample review for every ARC N° batch.
If an active digitally accepted layout reference exists and no material template/brand change occurred, render the full draft and proceed to final review.

Request an intermediate sample only when:
- user explicitly asks for it
- no usable layout reference exists for a new product family
- a material layout/brand change makes full rendering unusually risky

END ARC HUMAN REVIEW GATE V1.1