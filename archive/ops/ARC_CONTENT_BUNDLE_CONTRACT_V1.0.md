# ARC CONTENT BUNDLE CONTRACT V1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: lossless handoff from ARC Generator to ARC Typesetter

## 0. PURPOSE
Generator and Typesetter are separate sessions/projects.
The Generator owns content correctness.
The Typesetter owns layout/rendering correctness.
The handoff artifact is CONTENT_BUNDLE.

## 1. REQUIRED STATE
A bundle may enter typesetting only when:
- CONTENT_QA_STATUS=PASS
- CONTENT_LOCK=true
- HANDOFF_STATUS=READY_FOR_TYPESET
- no unresolved placeholder remains
- required answer key exists for verification
- required visual asset/spec information is complete enough to render without guessing

## 2. REQUIRED METADATA
ARC_RULESET_VERSION
BATCH_ID
GENERATOR=GPT | CLAUDE
SUBJECT
PRODUCT_MODE
SCOPE
ITEM_COUNT
CREATED_AT
CONTENT_QA_STATUS
CONTENT_LOCK=true
HANDOFF_STATUS=READY_FOR_TYPESET
TYPESET_STATUS=PENDING

## 3. REQUIRED PAYLOAD
A. QUESTION_MANUSCRIPT or CORE_MANUSCRIPT
B. ANSWER_KEY
- required for ARC_N and ARC_FINAL
- ARC_N Typesetter uses it for the final compact answer section
- no detailed explanations by default
C. LAYOUT_ASSET_MANIFEST
D. VISUAL_ASSET references and/or complete VISUAL_SPEC
E. QC_STATUS
F. SOURCE_STATUS_SUMMARY
G. PRODUCT_METADATA
H. optional editor notes that do not belong in student output

## 4. CONTENT LOCK
After CONTENT_LOCK=true:
Typesetter MUST NOT:
- change the correct answer
- alter a stem's meaning
- rewrite distractor semantics
- add or remove answer conditions
- add new curriculum content
- resolve an ambiguity by guessing
- silently fix factual content

Allowed non-semantic actions:
- line wrapping
- pagination
- column/full-width selection
- typographic normalization
- spacing
- visual rendering from supplied specs
- non-semantic punctuation normalization when meaning is unchanged

If content appears wrong:
CONTENT_ERROR_FLAG=<item/section>
TYPESET_STATUS=RETURN_CONTENT
No silent correction.

## 5. VISUAL HANDOFF
For every essential visual:
VISUAL_ID
ASSET_TYPE
DATA
LABELS
AXES_OR_LAYOUT
LEGEND
ESSENTIAL=true
RENDER_NOTES
KEEP_TOGETHER
LAYOUT_HINT

ARC N° rule:
LAYOUT_HINT=COLUMN_ONLY.
Do not hand off ARC N° assets that require FULL_WIDTH or a one-column page.
If a visual/table/passage cannot remain legible inside one ARC N° column, redesign/split the asset at the content stage without changing answer-bearing meaning, or return CONTENT_RETURN_REQUIRED.

ARC FINAL / ARC CORE may use flexible layout hints when their active product rules permit it.

If these are insufficient to reproduce the intended visual exactly enough for the answer:
return CONTENT_RETURN_REQUIRED.

## 6. STORAGE / NAMING
Recommended content-bundle title:
ARC_CONTENT_<SUBJECT>_<BATCH_ID>_READY

The bundle stays associated with the original BATCH_ID.
Typesetting creates a separate artifact and never overwrites the content bundle.

## 7. STATE MACHINE
DRAFT_GENERATION
→ CONTENT_QA
→ CONTENT_LOCKED
→ READY_FOR_TYPESET
→ TYPESETTING
→ PDF_QC
→ DRAFT_REVIEW
→ HUMAN_REVIEW
→ FINAL_RELEASED

Content-return branch:
TYPESETTING
→ RETURN_CONTENT
→ CONTENT_QA
→ CONTENT_LOCKED
→ READY_FOR_TYPESET

## 8. TOKEN / CONTEXT RULE
Typesetter should NOT reload textbooks, worksheets, GOLD anchors, generation-engine details, or source originals by default.
The locked bundle is the content authority.
Only reopen source material when the bundle explicitly flags a content verification blocker; normally return to Generator instead.

END ARC CONTENT BUNDLE CONTRACT V1.0
