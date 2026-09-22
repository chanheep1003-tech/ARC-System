# ARC CONTENT BUNDLE CONTRACT V1.6
DATE: 2026-09-21
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
- HANDOFF_MD_STATUS=READY
- a self-contained UTF-8 ARC_HANDOFF_*.md artifact exists
- no unresolved placeholder remains
- required visual asset/spec information is complete enough to render without guessing

ARC_N / ARC_FINAL additionally:
- required answer key exists for verification
- ANSWER_KEY_COMPLETE=PASS
- ANSWER_COUNT_MATCH=PASS
- QA_EVIDENCE_COMPLETE=PASS
- UNIVERSAL_INDEPENDENT_SOLVE_GATE=PASS
- all eight set gates PASS

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
HANDOFF_MD_STATUS=READY
HANDOFF_MD_FILENAME
QA_EVIDENCE_SCHEMA_VERSION (ARC_N / ARC_FINAL)
QA_EVIDENCE_FILENAME (ARC_N / ARC_FINAL)

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

J. QA_EVIDENCE when PRODUCT_MODE=ARC_N or ARC_FINAL
- machine-readable YAML or JSON payload
- one entry per ITEM_ID
- PASS A / blind PASS B answers and evidence
- five option verdicts for MCQ5
- AXIS / CLAIM_KEY / EVIDENCE_REFS / COMPETITIVENESS for every option
- ANSWER_EVIDENCE / SCOPE_TRACE
- reasoning and actual-difficulty metrics
- required per-item semantic gates
- the eight required set gates
- KOR SOURCE_TEXT_LOCK payload when source text is used

K. optional editor notes that do not belong in student output

## 3-A. CANONICAL MARKDOWN SERIALIZATION
The canonical portable handoff is a single Markdown file:

ARC_HANDOFF_<PRODUCT>_<SUBJECT>_<BATCH_ID>_READY.md

Purpose:
- attach directly to a Typesetter chat/project
- eliminate copy/paste loss
- preserve locked content and internal layout metadata
- allow Typesetter to work without reloading Generator chat history

The file must contain:
1. YAML front matter with locked state and identity
2. TYPESETTER INSTRUCTIONS — INTERNAL / DO NOT PRINT
3. CORE ARCHITECTURE SUMMARY for ARC_CORE
4. STUDENT MANUSCRIPT
5. ANSWER KEY for ARC_N/ARC_FINAL
6. VISUAL / LAYOUT ASSET MANIFEST
7. SOURCE TEXT BLOCKS when applicable
8. QA EVIDENCE for ARC_N / ARC_FINAL
9. QC STATUS

Authoritative student-facing content:
the STUDENT MANUSCRIPT section.

Authoritative answer mapping:
the ANSWER KEY section for ARC_N/ARC_FINAL.

Typesetter must ignore INTERNAL / DO NOT PRINT sections for student PDF output while using them as production metadata.

Layout authority is not portable content. A handoff must not pin or prescribe:
- PDF master/template version
- one/two-column mode
- body font family, size, weight, or line-height
- CSS selectors/properties
- ReportLab Frame/PageTemplate geometry
- page margins or fixed page coordinates

The current SYSTEM_MANIFEST and active Typesetter rules are the only layout authority.
An older handoff may preserve locked student content, but its stale layout commands
must fail the handoff preflight rather than override the active layout stack.

For ARC_CORE, level-1 Markdown headings inside STUDENT MANUSCRIPT are semantic
PART/MAJOR_TOPIC boundaries. A/B/C parts and genuine top-level topic changes must
be represented this way. Typesetter must start every boundary on a new physical
page without inserting an empty page.

The Markdown serialization must be semantically identical to the locked CONTENT_BUNDLE.
If they differ:
HANDOFF_MD_STATUS=FAIL
HANDOFF_STATUS!=READY_FOR_TYPESET.

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
- delete or rewrite QA_EVIDENCE to conceal a failed gate

Allowed non-semantic actions:
- line wrapping that does not change source order/wording
- page/column continuation of SOURCE_TEXT_BLOCK while preserving its sequence
- keep stanza/paragraph units together when feasible
- pagination
- column/full-width selection
- typographic normalization outside TEXT_FIDELITY=EXACT source text
- spacing
- visual rendering from supplied specs
- non-semantic punctuation normalization only outside TEXT_FIDELITY=EXACT source text

For KOR TEXT_FIDELITY=EXACT, wording, punctuation, whitespace, line/stanza boundaries and paragraph boundaries are content, not typography. Typesetter must reflow the page rather than normalize the source.

If content appears wrong:
CONTENT_ERROR_FLAG=<item/section>
TYPESET_STATUS=RETURN_CONTENT
No silent correction.

## 4-A. PRE-LOCK QA EVIDENCE GATE
ARC_N / ARC_FINAL cannot set CONTENT_LOCK=true until:
- PASS A and blind PASS B agree
- exactly one option is TRUE and matches the answer key
- all option verdicts and evidence refs are complete
- semantic duplicate review is PASS
- answer evidence and scope evidence traces are PASS
- TARGET_DIFFICULTY equals ACTUAL_DIFFICULTY after any reclassification
- STRUCTURE / ANSWER_COUNT_MATCH / MANUSCRIPT_CONTAMINATION / TOO_EASY / MID_GAP / STRUCTURE_BIAS / D4_SHORT / PASSAGE_TRUNCATION are PASS
- the machine-readable payload passes `tooling/content_qa/content_qa_gate.py` when executable runtime is available

Runner PASS proves structural QA completeness, not factual truth. Human/independent semantic review remains authoritative.

For ARC_N / ARC_FINAL, the sibling QA_EVIDENCE payload must bind to the
final STUDENT MANUSCRIPT. After the last content edit, compute
`student_manuscript_sha256` on the exact UTF-8 bytes emitted by the canonical
serializer (`student_manuscript.strip() + "\n"`). The QA payload must carry
that 64-character lowercase digest; Typesetter compares it with
`STUDENT_MANUSCRIPT_SHA256` in the locked handoff. Any subsequent manuscript
revision invalidates the QA proof and requires regeneration/review. This
binding is not a substitute for independent semantic QA.

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

Required portable handoff filename:
ARC_HANDOFF_<PRODUCT>_<SUBJECT>_<BATCH_ID>_READY.md

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

## 10. CANONICAL SERIALIZER BOUNDARY
If SYSTEM_MANIFEST registers an executable handoff serializer, it is the only
authorized CONTENT_BUNDLE-to-Markdown path. It must reject PDF master, column,
font, CSS, PageTemplate, geometry, and margin authority anywhere in the bundle.
The emitted handoff records its canonical filename and the SHA-256 of normalized
STUDENT MANUSCRIPT. Handoff preflight verifies both immediately before Typesetter
acceptance; mismatch is a hard fail, never an auto-correction.

END ARC CONTENT BUNDLE CONTRACT V1.6
