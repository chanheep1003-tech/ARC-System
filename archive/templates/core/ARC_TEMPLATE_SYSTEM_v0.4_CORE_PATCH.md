# ARC_TEMPLATE_SYSTEM_v0.4_CORE_PATCH
DATE: 2026-09-19
STATUS: ACTIVE PATCH
ENGINE: ARC_CORE_CONTENT_ENGINE_V1.1

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
quality/ARC_CORE_EDITORIAL_NATURALNESS_V1.0.md

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

## KOREAN CORE
- KOREAN_MASTER_V4.1 SOURCE-BOUND ORIGINAL TEXT MODE 적용
- SOURCE_TEXT_BLOCK은 작품/지문 시작 부분에 배치 가능
- 원문과 해설은 시각적으로 구분
- 시의 행/연, 산문의 문단 순서 보존
- 원문을 concept마다 반복하지 않고 작품 단위 공유
- 작품 전체 흐름을 먼저 보여 주고 세부 표현/시어/정서/관계를 설명
- '주제/정서/표현법' 카드가 연속되는 구조를 피함
- 학교 보충자료의 해석 구조를 편집 기준으로 우선

## PAGE RHYTHM
- 1 concept = 1 page 강제 금지
- 짧은 concept 2~3개가 자연스럽게 이어질 수 있음
- 복잡한 concept는 1페이지 이상 허용
- compare/visual은 필요 시 전폭 또는 내부 2단 가능
- concept block 중간 분할은 가능한 피함
- 국어 긴 SOURCE_TEXT_BLOCK은 PDF MASTER 규칙에 따라 이어서 조판 가능

## DESIGN
- templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md 적용
- ARC CORE secondary label/divider는 warm-gray dark #8A877F
- master ARC geometry는 N°/FINAL과 동일
- 흰 배경, Deep Navy / Warm Gray / Burgundy 체계 유지
- 장식보다 정보 위계와 가독성 우선
- 흑백 출력에서도 MUST/CONFUSING/TRAP의 구분이 유지되어야 함
- TRAP을 강한 경고색 블록으로 만들지 말고 restrained editorial treatment 사용

## QC
CORE_EDITORIAL_NATURALNESS = PASS
STUDENT_METADATA_LEAK = PASS
BLOCK_REPETITION = PASS
TRAP_EVIDENCE_CHECK = PASS
SOURCE_TERMINOLOGY_MATCH = PASS
KOR_SOURCE_TEXT_FIDELITY = PASS/NOT_APPLICABLE

END ARC TEMPLATE SYSTEM v0.4 CORE PATCH
