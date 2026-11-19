# ARC CONTENT BUNDLE CONTRACT V1.4
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: lossless handoff from ARC Generator to ARC Typesetter

## 0. PURPOSE
Generator and Typesetter are separate sessions/projects.
The Generator owns content correctness.
The Typesetter owns layout/rendering correctness.
The handoff artifact is CONTENT_BUNDLE.

## 1. REQUIRED STATE
All products:
- CONTENT_QA_STATUS=PASS
- CONTENT_LOCK=true
- HANDOFF_STATUS=READY_FOR_TYPESET
- no unresolved placeholder remains
- required visual asset/spec information is complete enough to render without guessing

ARC_N / ARC_FINAL additionally:
- required answer key exists for verification
- ANSWER_KEY_COMPLETE=PASS
- ANSWER_COUNT_MATCH=PASS

ARC_CORE additionally:
- CORE_MANUSCRIPT exists
- CORE_EDITORIAL_ARCHITECTURE=PASS
- MACRO_COHERENCE=PASS
- ANTI_LISTING=PASS
- CORE_EDITORIAL_NATURALNESS=PASS
- CORE_QA_STATUS=PASS

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
- exactly ITEM_COUNT entries
- one unique answer per ITEM_ID
- no blank/TBD/UNKNOWN values
- ANSWER_KEY_COMPLETE=PASS
- ANSWER_COUNT_MATCH=PASS
- no detailed explanations by default
C. LAYOUT_ASSET_MANIFEST
D. VISUAL_ASSET references and/or complete VISUAL_SPEC
E. QC_STATUS
F. SOURCE_STATUS_SUMMARY
G. PRODUCT_METADATA
H. SOURCE_TEXT_BLOCKS when required by subject policy
For each block:
- SOURCE_TEXT_ID
- WORK_TITLE
- AUTHOR
- SOURCE_KIND
- SOURCE_ID_OR_FILE
- SOURCE_LOCATION
- INCLUSION_MODE
- TEXT_FIDELITY
- TEXT_BODY
- LINKED_ITEM_IDS

Rules:
- TEXT_BODY is locked content
- VERBATIM_FULL/VERBATIM_RANGE requires a user-provided/uploaded or connected user-accessible source
- poetry line/stanza boundaries and prose paragraph boundaries are semantically protected
- Typesetter may line-wrap only where layout requires, but may not rewrite, summarize, omit, modernize, or silently correct the source
- source blocks are normally printed once and shared by linked item groups
- incomplete/garbled source text blocks block READY_FOR_TYPESET

I. CORE_ARCHITECTURE_SUMMARY when PRODUCT_MODE=ARC_CORE
- CHAPTER_ID
- CENTRAL_QUESTION
- DOMINANT_ORGANIZATION
- BACKBONE_NODES
- END_SYNTHESIS_MODE
- CORE_EDITORIAL_ARCHITECTURE
- MACRO_COHERENCE
These are Typesetter guidance metadata and must not be printed as student-facing system labels.

J. optional editor notes that do not belong in student output

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
- alter SOURCE_TEXT_BLOCK wording
- drop source lines/paragraphs for space
- modernize spelling/punctuation without explicit source metadata
- merge separate source blocks into a rewritten composite

Allowed non-semantic actions:
- line wrapping that does not change source order/wording
- page/column continuation of SOURCE_TEXT_BLOCK while preserving its sequence
- keep stanza/paragraph units together when feasible
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

## 9. CONTINUOUS STATE MACHINE
When active ARC_PRODUCTION_ORCHESTRATOR is in END_TO_END mode, normal PASS states advance automatically.

Canonical state machine:
DRAFT_GENERATION
→ CONTENT_QA
→ CONTENT_LOCKED
→ READY_FOR_TYPESET
→ TYPESETTING
→ PDF_QC
→ PUBLISH_STORAGE
→ READY_FOR_PHYSICAL_REVIEW
→ HUMAN_REVIEW
→ FINAL_RELEASED

No user confirmation is required at READY_FOR_TYPESET, PDF_QC PASS, or storage parent recheck.

Content-return branch remains:
TYPESETTING
→ RETURN_CONTENT
→ CONTENT_QA
→ CONTENT_LOCKED
→ READY_FOR_TYPESET
→ TYPESETTING

Physical HUMAN REVIEW is required only for the FINAL_RELEASED transition.

END ARC CONTENT BUNDLE CONTRACT V1.4
