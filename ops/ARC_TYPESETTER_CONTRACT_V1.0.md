# ARC TYPESETTER CONTRACT V1.0
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
3. ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.0.md
4. locked CONTENT_BUNDLE
5. templates/ARC_PDF_LAYOUT_MASTER_V2.0.md
6. templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md
7. required product-specific visual/PDF rules

Do NOT load subject MASTER/GOLD/textbook/worksheet/source bank by default.

## 2. ACCEPTANCE CHECK
Before layout:
- HANDOFF_STATUS=READY_FOR_TYPESET
- CONTENT_LOCK=true
- CONTENT_QA_STATUS=PASS
- BATCH_ID present
- PRODUCT_MODE present
- manuscript complete
- answer key present when applicable
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
student problem-only PDF, no answer/explanation/difficulty/type/hint/editor metadata.

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
