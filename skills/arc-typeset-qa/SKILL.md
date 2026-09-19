---
name: arc-typeset-qa
description: ARC CORE/N°/FINAL 조판에서 제품 레이아웃 격리, 의미 단위 페이지네이션, 인쇄 타이포그래피, 렌더 기반 PDF QA를 JIT로 수행한다.
metadata:
  version: 1.0.0
  arc-role: typesetting-quality
---

# ARC Typeset QA

## 목적
조판 소스가 그럴듯한지가 아니라 최종 렌더가 읽기 좋은지와 PRODUCT_MODE 불변식을 검사한다.
Rendered output is the source of truth for release 판단이다.

## Authority
1. user explicit requirements
2. SYSTEM_MANIFEST
3. active PDF master + product patch
4. Typesetter contract
5. this skill
6. external design references

이 skill은 콘텐츠를 수정하지 않는다.

## 1. Product isolation
### ARC CORE
- main reading flow = ONE_COLUMN
- ARC N°/FINAL two-column body selectors 금지
- comparison/table micro-grid만 제한적으로 허용
- substantial two-lane body flow 발견 시 HARD FAIL

### ARC N°
- problem pages = fixed TWO_COLUMN COLUMN_ONLY

### ARC FINAL
- active exam layout rules를 따른다.

## 2. Typography tokens
CORE default:
- Pretendard Regular(400), fallback Noto Sans KR Regular(400)
- body target 9.9pt
- line-height target 1.54~1.58
- body color dark neutral
- Light/Thin 금지
- Part > Chapter > Section > Functional label의 size/weight/spacing hierarchy 유지

타이포그래피 값은 페이지마다 즉흥적으로 바꾸지 말고 document-level token으로 관리한다.

## 3. Semantic pagination
Atomic/keep groups:
- heading + first body
- callout label + first body
- table header + first row
- figure + caption/direct explanation

Rules:
- heading은 후속 본문 약 3줄과 함께 둔다.
- bottom 20% heading orphan 금지.
- widows/orphans 3줄 목표.
- table row mid-split 금지.
- figure/diagram clipping 금지.
- 긴 section 전체에 break-inside:avoid를 걸어 sparse page를 만들지 않는다.
- 1~3줄 carry-over는 reflow 우선.

## 4. Source overflow audit
Editable HTML source가 있으면 PDF export 전:
- page/content element scrollHeight - clientHeight 측정
- >2px = HOLD
- 0~10px boundary case = final PDF visual recheck
- fixed-height + overflow:hidden으로 long-form body를 숨기지 않는다.

## 5. Render review
가능한 host:
1. 300 DPI render
2. all pages per-page pass
3. cross-page consistency
4. active product reference와 drift 확인
5. preflight JSON + visual findings 통합

확인:
- clipped sentence/table/box/figure
- empty or near-empty carry-over
- font fallback/too-light body
- title hierarchy
- margin/header/footer drift
- CORE 2-column contamination
- ARC N°/CORE style crossover

실행 환경이 없으면 TOOLING_UNAVAILABLE을 기록하고 PASS를 가장하지 않는다.

## 6. Action order
HOLD:
- clipping/overflow
- CORE two-column flow
- unreadable/light body font
- missing content
- heading isolated at page bottom with broken section start

REFLOW:
- sparse page
- 1~3 line carry-over
- awkward table continuation
- hierarchy ambiguity

NOTE:
- minor spacing rhythm
- non-blocking optical alignment

## 7. External design references
REFERENCE_ONLY; no upstream code/text vendored.
- jelaludo/claude-skill-typography: token-first typography audit, line-height/weight/spacing hierarchy concepts.
- thedanielmay/visual-review-skill: render-first QA, fixed-height overflow audit, clipped-content and density review concepts.
Upstream license was not established in this intake, therefore only general design patterns are adapted independently.

## 8. Output
TYPESET_QA_STATUS
PRODUCT_LAYOUT_ISOLATION
CORE_COLUMN_FLOW
SEMANTIC_PAGINATION
HEADING_ORPHAN
MID_BLOCK_CLIP
FONT_TOKEN_COMPLIANCE
PRINT_LEGIBILITY
PAGE_OCCUPANCY_AUDIT
RAW_MARKUP_LEAK
METADATA_LEAK
TOOLING_EXECUTED
FINDINGS[]

END ARC TYPESET QA V1.0
