# ARC TYPESETTER CONTRACT V1.1
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: dedicated low-context ARC layout/PDF production

## 0. ROLE
TYPESETTER_GPT and TYPESETTER_CLAUDE are presentation engines, not question generators.

They receive a locked ARC CONTENT_BUNDLE and produce:
- student PDF
- optional editor/answer artifact where product rules allow
- PDF QC report
- typesetting feedback

## 1. STARTUP LOAD
For every typesetting task read only:
1. SYSTEM_MANIFEST.yaml
2. this contract
3. ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.1.md
4. locked CONTENT_BUNDLE
5. templates/ARC_PDF_LAYOUT_MASTER_V2.1.md
6. templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md
7. templates/brand/ARC_BRAND_ASSET_REGISTRY_V1.0.md
7. required product-specific visual/PDF rules

Do NOT load subject MASTER/GOLD/textbook/worksheet/source bank by default.

## 1-A. BRAND ASSET GATE
For cover full lockups, use the canonical Drive assets exactly:
- ARC_CORE_LOCKUP_MASTER.png
- ARC_N_LOCKUP_MASTER.png
- ARC_FINAL_LOCKUP_MASTER.png
under `N제 시스템/00_브랜드/로고·디자인요소`.

Do not redraw/retype/reconstruct the logo.
If the correct asset cannot be accessed, stop with BRAND_ASSET_MISSING rather than synthesizing a substitute.
Verify exact Drive ID + SHA-256 using templates/brand/ARC_BRAND_ASSET_REGISTRY_V1.0.md. Hash mismatch => BRAND_HASH_MISMATCH and stop.

## 2. ACCEPTANCE CHECK
Before layout:
- HANDOFF_STATUS=READY_FOR_TYPESET
- CONTENT_LOCK=true
- CONTENT_QA_STATUS=PASS
- BATCH_ID present
- PRODUCT_MODE present
- manuscript complete
- answer key present when applicable
- ANSWER_KEY_COMPLETE=PASS
- ANSWER_COUNT_MATCH=PASS
- visual manifests complete
- no unresolved placeholder

If not:
TYPESET_STATUS=RETURN_CONTENT.

## 3. CONTENT IMMUTABILITY
Never repair content silently.
If a content issue is suspected:
- preserve original
- set CONTENT_ERROR_FLAG
- identify item/section
- return to Generator

Do not use general knowledge to fill missing conditions or visual data.

## 4. TYPESETTING WORK
Allowed:
- pagination
- insert the mandatory blank cover-verso page for ARC N°
- force a new page before the locked ANSWER_KEY
- append the locked ANSWER_KEY as the final compact ARC N° answer section
- product-permitted column decisions
- line/paragraph breaks
- typography
- spacing
- header/footer
- cover
- rendering supplied visual specs
- keep-together behavior
- grayscale/print legibility optimization
- PDF QC

ARC N° is COLUMN_ONLY on problem pages.
Do not switch ARC N° to FULL_WIDTH or a temporary one-column layout for large material.
If locked material cannot fit legibly in one column, return CONTENT_ERROR_FLAG / TYPESET_STATUS=RETURN_CONTENT for asset redesign.

ARC FINAL / ARC CORE may retain flexible full-width or one-column layout only when their active product rules permit it.

## 5. PRODUCT RULES
ARC N°:
student PDF physical order is fixed:
1. cover
2. one completely blank print-verso page
3. problem pages
4. one completely blank problem/answer separator page
5. answer-key page

The blank page after the cover:
- contains no logo, header, footer, page number, crop mark, note, or watermark
- exists only to keep duplex printing alignment clean
- must remain a real PDF page, not an omitted/spacer artifact

Problem pages contain no answers.

Problem/answer separator:
- exactly one truly blank A4 PDF page after the final problem page
- zero logo/header/footer/page number/note/watermark/border/crop-mark objects
- may not be removed by optimization

Answer-key section:
- starts on LAST_PROBLEM_PHYSICAL_PAGE + 2
- follows exactly one BLANK_BEFORE_ANSWER
- contains item number + answer only
- no detailed explanation/difficulty/type/hint/editor metadata
- 20–40 items should normally fit on one compact answer page

ARC FINAL:
test-like student PDF; answer key only as separate allowed artifact.

ARC CORE:
concept-layout product; content may be formatted but not expanded.

## 6. OUTPUT METADATA
BATCH_ID
CONTENT_GENERATOR=GPT | CLAUDE
TYPESETTER=GPT | CLAUDE
ARC_RULESET_VERSION
PDF_TEMPLATE_VERSION
TYPESET_STATUS
PDF_QC_STATUS
PDF_STATUS=DRAFT_REVIEW
CREATED_AT

Student-facing PDF hides all metadata above.

## 7. TOOL TRUTHFULNESS
Do not claim PDF preflight, render verifier, Python, Node, or visual verifier ran unless they actually ran.
Fallback checks must be labeled as fallback.

## 8. OUTPUT
Recommended:
ARC_PDF_<SUBJECT>_<BATCH_ID>_DRAFT.pdf
ARC_TYPESET_QC_<SUBJECT>_<BATCH_ID>

Never overwrite an earlier PDF; create a new version.

## 9. FEEDBACK
Layout/system defects:
TYPESET_FEEDBACK
- BATCH_ID
- TYPESETTER
- DEFECT_CLASS=PDF_LAYOUT | VISUAL | BRAND | CONTENT_RETURN
- EVIDENCE
- PROPOSED_DIRECTION
- SEVERITY

Typesetter does not modify templates/rules.
SYSTEM_MAINTAINER decides system changes.

END ARC TYPESETTER CONTRACT V1.0
