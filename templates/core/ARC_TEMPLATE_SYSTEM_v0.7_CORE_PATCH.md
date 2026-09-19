# ARC_TEMPLATE_SYSTEM_v0.7_CORE_PATCH
DATE: 2026-09-19
STATUS: ACTIVE PATCH
ENGINE: ARC_CORE_CONTENT_ENGINE_V1.3

## PURPOSE
ARC CORE를 'AI 카드 모음'이 아니라 실제 내신 참고서처럼 보이게 하는 조판 패치다.
내용 완결성과 읽기 흐름을 우선하며, 고정 블록 반복을 피한다.

## RETIRED FROM v0.3
다음 학생용 노출 규칙을 폐기한다.
- CONCEPT_ID 학생용 표시
- N° 연결 블록 학생용 표시
- 모든 concept에 고정된 9블록 순서
- 모든 concept에서 동일한 MUST/CONFUSING/EXAM CONNECTION 구성

내부 CONCEPT_ID와 N_GENERATION_LINKS는 metadata에서만 유지한다.

## STUDENT-FACING CORE
기본:
1. TITLE
2. 자연스러운 CORE EXPLANATION

선택:
- RELATION / PROCESS
- VISUAL
- MUST
- CONFUSING
- TRAP
- EXAM CONNECTION

선택 블록은 실제 필요가 있을 때만 사용한다.
한 concept에 모든 선택 블록을 강제하지 않는다.

## TRAP
- 실제 오개념/검수/학교자료 근거가 있을 때만
- 본문과 같은 내용을 다시 쓰는 용도 금지
- 과도한 경고 아이콘/색상 사용 금지
- 짧고 정확하게, 판단축 중심
- 매 concept마다 하나씩 강제 배치 금지

## EDITORIAL NATURALNESS
필수 참조:
quality/ARC_CORE_EDITORIAL_NATURALNESS_V1.2.md
engine/core/ARC_CORE_DEPTH_ENGINE_V1.1.md

금지:
- 카드 UI 과다
- 같은 박스 구조 반복
- 같은 길이의 bullet 반복
- 모든 페이지의 기계적 대칭
- 지나친 굵은 글씨
- 이모지/마케팅 카피
- '시험에 무조건' 같은 예측형 문장
- 빈 공간을 장식으로 채움
- 학생용 내부 metadata 노출

권장:
- 단일 컬럼 본문 흐름
- 필요한 경우에만 비교표/도식
- 문단/개념 길이의 자연스러운 차이
- 교과서+상위권 내신 참고서의 편집 밀도
- 본문이 박스보다 시각적으로 우세
- chapter opening은 중심 질문/흐름을 3~6문장으로 제시하고 카드 묶음으로 시작하지 않음
- 연속 요약 전용 페이지는 실제 synthesis 기능이 있을 때만 허용
- 같은 네이비 헤더 카드가 한 페이지에 과도하게 반복되지 않게 함

## KOREAN CORE
- KOREAN_MASTER_V4.1 SOURCE-BOUND ORIGINAL TEXT MODE 적용
- SOURCE_TEXT_BLOCK은 작품/지문 시작 부분에 배치 가능
- 원문과 해설은 시각적으로 구분
- 시의 행/연, 산문의 문단 순서 보존
- 원문을 concept마다 반복하지 않고 작품 단위 공유
- 작품 전체 흐름을 먼저 보여 주고 세부 표현/시어/정서/관계를 설명
- '주제/정서/표현법' 카드가 연속되는 구조를 피함
- 학교 보충자료의 해석 구조를 편집 기준으로 우선

## ADAPTIVE DEPTH PRESENTATION
DEPTH_PRIORITY는 학생용에 표시하지 않는다.

STANDARD:
- 짧고 밀도 높은 본문
- 필요 없는 박스/표 없음

ADVANCED:
- 설명과 비교가 자연스럽게 조금 확장
- 필요한 경우에만 표/도식/CONFUSING

HIGH_DIFFICULTY:
- 더 많은 페이지/공간 사용 허용
- 조건·경계·근거·비교축을 충분히 보여 줌
- 필요한 TRAP/도식/비교표 허용
- '심화', '킬러', '고난도' 배지로 시각적 과장 금지
- STANDARD와 같은 디자인 언어를 유지하고 정보 밀도와 설명 깊이로 차이를 만든다
- FOUNDATION/CONDITIONS/BOUNDARIES 등 내부 depth 단계명을 고정 소제목으로 출력 금지

고난도 concept가 많아도 각 페이지를 같은 패턴으로 만들지 않는다.

## MACRO LAYOUT ARCHITECTURE
필수 참조:
engine/core/ARC_CORE_EDITORIAL_ARCHITECTURE_V2.0.md

CORE 지면의 기본 단위는 concept card가 아니라 chapter/cluster다.

기본 페이지 인상:
- 연속 본문이 시각적으로 가장 큰 면적
- 소제목은 chapter flow를 따라 사용
- 표/도식은 관계를 보여 줄 때만
- 경고/주의 박스는 희소하게
- chapter 끝에 여러 recap 블록을 겹쳐 배치하지 않음

진단용 soft target:
- prose 65~75%
- functional table/diagram 15~20%
- warning/summary/support blocks 5~15%

정확한 비율을 강제하지 않지만, 보조 블록이 본문보다 우세하면 재조판 대상이다.

### ONE SYNTHESIS PRINCIPLE
chapter 마지막은 기본적으로 다음 중 하나를 중심으로 선택한다.
- integrated paragraph
- one timeline/causal chain
- one comparison matrix
- one decision frame

동일 chapter 끝에 시간축 + 요약 bullet + 문제 적용 + 카드 도식을 관성적으로 모두 넣지 않는다.

### NO DUPLICATE VISUAL RECAP
본문에서 충분히 설명한 사실을 같은 페이지/다음 페이지에 동일 내용 카드로 다시 만드는 것을 금지한다.
도식이 추가될 경우 반드시 새로운 관계/순서/비교 기능을 제공해야 한다.

## CORE TYPOGRAPHY — PRINT-FIRST
- 본문은 Pretendard Regular(400) 이상을 기본으로 한다.
- Noto Sans KR fallback도 Regular(400) 이상.
- Thin/ExtraLight/Light는 본문·표·캡션에 사용하지 않는다.
- 본문 9.6~10.2 pt, line-height 1.45~1.60 권장.
- 소제목은 Medium/SemiBold, 파트 제목은 SemiBold/Bold.
- 본문 대비는 인쇄 기준으로 충분히 진하게 유지한다.
- Warm Gray는 보조 면/선에 사용하며 본문 텍스트 색으로 사용하지 않는다.

## PAGE RHYTHM
- 1 concept = 1 page 강제 금지
- 짧은 concept 2~3개가 자연스럽게 이어질 수 있음
- 복잡한 concept는 1페이지 이상 허용
- compare/visual은 필요 시 전폭 또는 내부 2단 가능
- concept block 중간 분할은 가능한 피함
- 그러나 블록 전체 이동 때문에 다음 페이지가 과도하게 비면 문단 경계 분할을 허용
- 일반 본문 페이지 45% 미만 점유 시 재조판
- 25% 미만 near-empty page는 명시적 의도가 없으면 FAIL
- ARC_CORE 표지 뒤 blank verso 삽입 금지
- 다음 페이지에 1~3줄만 남는 orphan/widow는 reflow 우선
- 파트 전환에서도 불필요한 강제 page-break를 만들지 않음
- 국어 긴 SOURCE_TEXT_BLOCK은 PDF MASTER 규칙에 따라 이어서 조판 가능

## DESIGN
- templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md 적용
- ARC CORE secondary label/divider는 warm-gray dark #8A877F
- master ARC geometry는 N°/FINAL과 동일
- 흰 배경, Deep Navy / Warm Gray / Burgundy 체계 유지
- 장식보다 정보 위계와 가독성 우선
- 흑백 출력에서도 MUST/CONFUSING/TRAP의 구분이 유지되어야 함
- TRAP을 강한 경고색 블록으로 만들지 말고 restrained editorial treatment 사용

## RAW MARKUP / PRODUCTION NOTE
- <br>, <b>, HTML/Markdown token이 학생 PDF에 보이면 FAIL
- Drive 상태, source 누락, 제작 과정 메모가 학생 PDF에 보이면 FAIL
- 내부 DO NOT PRINT section은 layout 판단에만 사용

## QC
CORE_EDITORIAL_ARCHITECTURE = PASS
MACRO_COHERENCE = PASS
ANTI_LISTING = PASS
SYNTHESIS_TRANSFORMS = PASS
CORE_EDITORIAL_NATURALNESS = PASS
STUDENT_METADATA_LEAK = PASS
BLOCK_REPETITION = PASS
PRINT_LEGIBILITY = PASS
FONT_WEIGHT_AUDIT = PASS
PAGE_OCCUPANCY_AUDIT = PASS
SPARSE_PAGE = NONE
ORPHAN_WIDOW = PASS
RAW_MARKUP_LEAK = 0
TRAP_EVIDENCE_CHECK = PASS
SOURCE_TERMINOLOGY_MATCH = PASS
KOR_SOURCE_TEXT_FIDELITY = PASS/NOT_APPLICABLE
DEPTH_LABEL_LEAK = PASS
DEPTH_VISUAL_NATURALNESS = PASS

END ARC TEMPLATE SYSTEM v0.7 CORE PATCH
