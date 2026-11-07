# ARC CORE — PURE B&W LAYOUT V1.0 (과목별 · 2개 에디션)
DATE: 2026-11-07
STATUS: ACTIVE — ARC_CORE 조판의 유일한 기준. 아래를 폐기/대체한다.
- ARC_TEMPLATE_SYSTEM_v0.3_CORE_PATCH (이 파일로 대체됨)
- ARC_PDF_LAYOUT_MASTER_V2.0 §8의 구 CORE 규칙(2~4개/페이지, 4~8줄)과 Navy/Burgundy/Warm Gray CORE 스타일
- ARC_CORE_master_v0.2.html의 샘플 본문과 컬러 스타일

## 0. 구성 원칙
- 과목별로 제작한다 (통합과학2 / 통합사회2 / 공통국어2 / 한국사2 / 인공지능기초).
- 과목마다 에디션 2종: `DETAIL`(상세 개념서), `COMPACT`(시험 직전 압축본).
- 두 에디션은 같은 CONCEPT_ID 체계, 같은 순수 흑백 스타일, 같은 표지·머리글·꼬리말을 쓴다. 차이는 콘텐츠 밀도와 블록 구성뿐이다.
- 요청에 에디션이 없으면 DETAIL을 기본으로 한다. "압축/직전/요약" → COMPACT.
- 조판 단계는 내용을 줄이거나 늘리지 않는다. 분량 문제는 CORE_LENGTH_FLAG로 원고 단계에 반환한다.

## 1. 공통 스타일 (N°와 동일한 순수 흑백)
- A4 세로, 좌우 여백 12.8mm, 흰 배경, 텍스트·선 #000000. 색·회색 음영·채우기 금지.
- 표지: `templates/n/ARC_N_BW_LAYOUT_V1.0.md`의 표지 구조를 따른다 (상단 기관선, 외곽선 에디션 배지, 2줄 굵은 제목, 범위 박스). 배지 문구는 `CORE 상세` / `CORE 압축`.
- 순서: 표지 → 완전 백지(머리말·꼬리말 없음) → 본문 → (끝). 정답표 없음.
- 러닝헤드 8.8pt 굵게 + 하단 얇은 선: 좌 `ARC CORE | 과목 · 에디션 [Vx.x]`, 우 현재 단원명.
- 꼬리말 8pt, 상단 얇은 선, 중앙 물리 페이지 번호.
- 본문 1단. 비교표·그래프·지도·실험도·입자모형 등 큰 시각자료는 전폭. 2단은 쓰지 않는다.
- 폰트: 한글 Pretendard 우선(fallback Noto Sans KR), 영문·숫자 Inter, 문학 인용은 Noto Serif CJK KR. 7pt 이하 금지.

## 2. 블록 위계 (색 대신 선 종류로 구분)
|블록|표현|
|---|---|
|CONCEPT_ID + TITLE|`ARC-SCI-EV-001` 7.5pt 작게 + 제목 12pt 굵게, 하단 1.1pt 실선|
|ONE-LINE DEFINITION|제목 아래 굵은 한 줄 (DETAIL만 필수)|
|CORE EXPLANATION|본문, 외곽선 없음|
|RELATION / PROCESS|`A → B → C` 흐름 또는 얇은 실선 표|
|VISUAL|0.7pt 실선 프레임, 캡션 포함, 설명 문장과 KEEP_TOGETHER|
|MUST|1.1pt 실선 박스, 라벨 `MUST` (외곽선 태그)|
|CONFUSING|0.8pt **점선** 박스, 라벨 `CONFUSING` — 비교는 `× / ○` 2줄|
|EXAM CONNECTION|박스 없이 좌측 2pt 세로선 + 본문 (DETAIL만)|
|N° LINK|맨 아래 얇은 실선 위 한 줄: `N° 연결 → 기본 / 적용 / 고난도`|
|중요도 태그|DETAIL 본문 안에서 `[필수]` `[이해]` `[보충]` 텍스트 태그 사용|

## 3. DETAIL — 상세 개념서
- 1페이지 1~2개 핵심 개념. 복합 개념은 1~1.5페이지 허용. 페이지 압축보다 내용 완결성 우선.
- 블록 전체 사용: CONCEPT_ID+TITLE → 한 줄 정의 → 핵심 설명 → 관계/과정 → 시각자료 → MUST(최대 3개) → CONFUSING(실제 혼동만) → 시험 연결 → N° 연결.
- 본문 8.5~9.2pt, 행간 1.60~1.72.
- 시각자료는 `ARC_VISUAL_AUTHENTICITY_RUBRIC`를 통과해야 하며, 이해에 필요하면 적극 사용한다.
- 카드처럼 과도하게 조각내지 않는다 (흐름 단절 금지).

## 4. COMPACT — 시험 직전 압축본
- 1페이지 2~4개 개념. 개념 본문 4~8줄.
- 블록: CONCEPT_ID+TITLE → 핵심 설명 → MUST(필수) → CONFUSING(있을 때만) → 비교표/흐름도(글보다 빠를 때만) → N° 연결 한 줄.
- 생략: 한 줄 정의, 별도 EXAM CONNECTION(MUST/CONFUSING에 흡수), 보충 시각자료.
- 본문 8.3~8.8pt, 행간 1.50~1.60.
- 페이지가 비어도 박스로 채우지 않는다.
- 압축은 **원고 단계에서** 한다. 조판 AI가 DETAIL을 임의 요약해 COMPACT를 만들지 않는다.

## 5. 입력 계약 (원고)
CORE_META: SUBJECT / TARGET_RANGE / SOURCE_SCOPE / CORE_VARIANT(DETAIL|COMPACT) / CONCEPT_COUNT
각 개념: CONCEPT_ID / SCOPE_CONCEPT_ID / TITLE / DEFINITION(DETAIL) / EXPLANATION / RELATION(optional) / VISUAL_ID(optional) / MUST / CONFUSING(optional) / EXAM_CONNECTION(DETAIL) / N_LINK
CORE_PRIORITY: REQUIRED | SUPPORTING | OPTIONAL — REQUIRED 누락 시 CONTENT_ERROR_FLAG.

## 6. 페이지네이션 / KEEP_TOGETHER
- 개념 제목 + 첫 설명 문단, MUST 라벨+내용, CONFUSING 라벨+내용, 표 머리글+첫 행, 그림+직접 설명 문장은 분리 금지.
- 안 들어가면 블록 전체를 다음 페이지로 보낸다. 글자 크기를 줄여 해결하지 않는다.

## 7. 합격 기준 (CORE PASS)
- 에디션별 밀도 규칙 준수 (DETAIL 1~2개/페이지, COMPACT 2~4개/페이지)
- 컬러·회색 음영 0, 정답표 0, 샘플/placeholder 0
- REQUIRED 개념 전부 존재, MUST 누락 0, CONFUSING은 원고에 있을 때만
- 시각자료 TRUE_VISUAL 실제 렌더
- 표지 에디션 배지가 요청 에디션과 일치

## 8. 파일명
`ARC_CORE_<DETAIL|COMPACT>_<과목>_<범위>_Vx.x.pdf`
