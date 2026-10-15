# ARC_TEMPLATE_SYSTEM_v0.9_CORE_BOOK_PATCH
DATE: 2026-10-15
STATUS: ACTIVE PATCH (core_profile = BOOK)
ENGINE: ARC_CORE_CONTENT_ENGINE_V1.3 + engine/core/ARC_CORE_BOOK_EDITORIAL_V1.0.md
SUPERSEDES: templates/core/ARC_TEMPLATE_SYSTEM_v0.8_CORE_PATCH.md (core_profile = LEGACY 전용으로 보존)
PDF MASTER: templates/ARC_PDF_LAYOUT_MASTER_V2.4.md — ARC_CORE 항목 중 아래에서 **재정의한 값만** BOOK에서 이 문서가 우선한다.

## PURPOSE
사용자가 승인한 ‘상세 개념서’(동북고 공통국어2 중세 국어 V2.0)의 지면 규칙을 ARC CORE 표준으로 옮긴다.
모든 과목 CORE에 적용되며, 단일 manifest 값 `runtime.core_profile`(BOOK | LEGACY)로 선택한다.

## PRODUCT ISOLATION — HARD LOCK
- BOOK에서도 CORE 본문의 **reading flow는 1단**이다. 본문이 좌/우 독립 lane으로 흐르는 것은 계속 금지한다.
- 허용되는 core-book 전용 micro-grid(제품 격리 namespace `[data-product="arc-core"]` 안에서만):
  1) 소단락 옆 칸 `.s.sd` (본문 + 폭 36mm 보조 칸, 같은 소단락 안에서만)
  2) 표 `table.t`, 흐름도 `.flow`
  3) 점검표/모의 문제의 2열 grid `.cols2` (페이지당 1개 이내, 문항 번호가 열 안에 있어야 함)
- ARC N°의 `.cols/.col`, ARC FINAL 시험지 grid를 CORE에 재사용하는 것은 계속 금지한다.
- **page-flow wrapper에 단일 단 값(column-count 1)을 주지 않는다.** multicol 컨텍스트가 생겨 `break-before:page`가 단 나눔으로 바뀐다(실측: 68쪽 → 50쪽). `column-count:auto!important`로 격리한다.
- `fixed-height page + overflow:hidden` 방식 금지. 본문 초과를 숨기지 않고 다음 쪽을 생성한다.
- `CORE_TWO_COLUMN_FLOW = 0` (본문 흐름 기준). 위 micro-grid 때문에 PDF 검사에서 `CORE_TWO_COLUMN_FLOW` 신호가 잡히면 BOOK에서는 **WARN**이며, 본문 단 구조인지 사람이 한 번 확인한다. LEGACY에서는 계속 FAIL이다.

HTML/CSS rendering path:
- BOOK: `active.layout.core_book_html_master` (`templates/core/ARC_CORE_BOOK_master_v0.4.html`) + `templates/core/book/ARC_CORE_BOOK_style_v0.4.css`
- LEGACY: `active.layout.core_html_master` (v0.3)
- 선택 근거는 `runtime.core_profile`이다. typesetter_gateway가 profile을 고정하고, preflight는 `--core-profile`로 같은 값을 받는다.
- `ARC_CORE_SOURCE_PREFLIGHT`가 HOLD면 PDF export 금지.

## STUDENT-FACING CORE (BOOK)
v0.8의 ‘기본 2블록 + 선택 블록’ 구성을 **대체**한다. 학생용 구성요소는 다음과 같고, 반복되는 구성요소는 의도된 문법이다.
- 표지 · 읽는 방법 · 차례 · 시작하기 전에 · 장 시작 쪽 · 개념(번호 박스+제목+lead) · 번호 소단락
- 중요 포인트 · 심화 포인트 · 참고 · 예제 · 확인 문제 · (학교 시험 근거가 있을 때) 시험 포인트 상자
- 시험 대비 장 · 모의 문제 · 정답과 해설 · 색인
v0.8에서 폐기했던 ‘고정 블록 반복 금지 / 박스 구조 반복 금지’는 BOOK에서 적용하지 않는다.
단, 같은 내용을 박스로 두 번 쓰는 것(NO DUPLICATE VISUAL RECAP)은 계속 금지한다.

## RETAINED FROM v0.8
- 내부 메타데이터 비노출(`STUDENT_METADATA_LEAK`), `<br>/<b>` 등 raw markup 노출 금지
- 출제 예측 단정 금지, 이모지/마케팅 카피 금지
- 소스 충실도(KOR SOURCE-BOUND ORIGINAL TEXT MODE) · 학교 자료 우선
- 흑백 출력에서 구성요소 구분 유지 → BOOK에서는 **처음부터 흑백 전용**(회색조 외 색 금지)
- `CORE_REGISTERED_BOUNDARY_REMAINDER`: 등록된 대경계(장 시작 쪽) 직전 쪽의 점유율 부족은 INFO로 허용

## CHANGED FROM v0.8 (BOOK)
| 항목 | v0.8 (LEGACY) | v0.9 (BOOK) |
|---|---|---|
| 개념 ID 학생 노출 | 금지 | 소형 단원 코드 허용(N° 연결표는 내부 전용) |
| 구성 | prose 65~75% + 선택 블록 | 소단락·표·흐름·상자 구조화, 연속 줄글 ≤ 3~4문장 |
| 본문 폰트 | Pretendard/Noto Sans KR 9.9pt | Noto Serif CJK KR 9.7pt / 줄 1.82, 제목·표는 Pretendard/Noto Sans |
| 색 | Navy/Warm Gray/Burgundy | 회색조 전용 |
| 개념 시작 | 1 concept = 1 page 금지 | 개념은 새 쪽에서 시작, 1~3쪽 |
| 소단락 분할 | 가능한 피함 | `break-inside:avoid` 강제 |
| 쪽 점유 | FAIL < 25% / WARN < 45% | FAIL < 10% / WARN < 20% (preflight 측정값 기준) |
| 본문 폰트 하한 | FAIL < 9.2pt | FAIL < 7.5pt (측정 평균, 표·옆 칸 포함) |
| 2단 신호 | FAIL | WARN (micro-grid 한정) |
| 표지 로고 | canonical asset | canonical asset (동일, 텍스트 로고 금지) |

## INFORMATION HIERARCHY — FOUR LEVELS (BOOK)
LEVEL 1 장(Ⅰ·Ⅱ…): opener 쪽, 로마 숫자 78pt + 25pt 제목, 새 쪽에서 시작, 빈 쪽 금지
LEVEL 2 개념: 검정 번호 박스 + 18pt 제목 + 1.6pt 아래선, 새 쪽에서 시작
LEVEL 3 소단락: 번호(테두리 박스) + 11pt 굵은 소제목 + 0.6pt 아래선
LEVEL 4 기능 라벨: 중요(검정 반전 머리띠) · 심화(회색 머리띠, 점선 테두리) · 참고(왼쪽 굵은 선) · 확인(이중선) · 시험 포인트(검정 머리띠 표)
금지: 색으로만 위계를 표현, 레벨 간 크기·굵기 차이가 거의 없는 구성.

## PAGE RULES (BOOK)
- 소단락 · 중요/심화 상자 · 확인 · 시험 포인트 · 표 행 · 점검 문항은 쪽 중간에서 끊기지 않는다.
- 상자의 태그(머리띠)는 상자 **안**에 둔다(절대 위치로 상자 밖에 걸치지 않는다 — 쪽 경계에서 태그만 남는 결함 방지).
- 개념 마지막 쪽 점유 35% 미만이면 예제/보충 소단락을 추가한다(장식 금지). preflight WARN은 이 기준의 보조 신호다.
- 제목은 최소 후속 본문 3줄과 함께 둔다. 제목이 쪽 하단 20%에 고립되면 이동한다.
- PART/장 시작 쪽은 새 쪽에서 시작하고 blank page를 만들지 않는다. 표지 뒤 blank verso 금지.
- HTML source 사용 시 export 전 overflow audit(`scrollHeight/clientHeight`)를 수행한다. render_pdf.js가 `.s .imp .adv .chk .ex`를 검사한다.

## CORE TYPOGRAPHY — PRINT-FIRST (BOOK)
- 본문 Noto Serif CJK KR 9.7pt / 1.82 / #111. 정렬 left, `word-break:keep-all`.
- 표 8.7pt, 옆 칸 8pt, 라벨 ≥ 7.6pt, 머리말/쪽번호 7.8~8.4pt.
- Thin/ExtraLight/Light는 어떤 요소에도 사용하지 않는다.
- 옛한글(ᄠ ᄡ ᄯ ᄫ ᅀ ᅙ ᇙ ᆞ 등)·한자가 있으면 폰트 보유를 확인하고 래스터로 눈으로 본다(GLYPH_MISSING 금지).

## DESIGN
- templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md 적용. 표지 로고는 canonical lockup asset의 SHA-256을 확인한 것만 쓴다.
- 흑백 전용: 검정·회색·흰색. 장식(그림자, 둥근 알약, 그라디언트) 금지.
- 표지는 로고 + 과목/단원 제목 + 범위 문장 + 학교·시험·연도. 내부 코드/상태 문구 금지.

## RAW MARKUP / PRODUCTION NOTE
- <br>, <b>, HTML/Markdown token이 학생 PDF에 보이면 FAIL
- Drive 상태, source 누락, QC_STATUS, 확인 필요 목록(◇ 상세), CORE_LINK_INDEX 등 제작 과정 메모가 학생 PDF에 보이면 FAIL
- 내부 DO NOT PRINT section은 layout 판단에만 사용

## QC
CORE_PROFILE = BOOK
CORE_LAYOUT_MODE = ONE_COLUMN (main flow)
CORE_TWO_COLUMN_FLOW = 0 (본문 흐름 기준; micro-grid 신호는 WARN)
GRAYSCALE_ONLY = PASS (source color check + raster channel diff ≤ 8)
SMALL_UNIT_BREAK_INSIDE = PASS (소단락 쪽 중간 분할 0)
BOX_TAG_ORPHAN = 0
TOC_PAGE_NUMBERS = PASS (2-pass 안정)
HEADING_ORPHAN = 0
RAW_MARKUP_LEAK = 0
STUDENT_METADATA_LEAK = PASS
PAGE_OCCUPANCY_AUDIT = PASS (BOOK 임계)
CORE_REGISTERED_BOUNDARY_REMAINDER = INFO
BOOK_COMPONENT_COVERAGE = PASS (quality/ARC_CORE_BOOK_QA_V1.0.md)
EXAM_PREDICTION_ASSERTION = 0

END ARC TEMPLATE SYSTEM v0.9 CORE BOOK PATCH
