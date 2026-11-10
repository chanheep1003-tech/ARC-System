# ARC PIPELINE INTEGRITY CONTRACT V1.0
VERSION: 1.0
SYSTEM_LINE: 1.8
DATE: 2026-09-19
STATUS: ACTIVE-DEV

## 0. AUTHORITY
`SYSTEM_MANIFEST.yaml` is the only active-version resolver. GitHub `dev` is the source of truth for engines, MASTERs, QA, templates, contracts, tooling, and checksums. Google Drive is source/storage for current school materials, textbooks, worksheets, past exams, verified item-bank records, canonical brand binaries, generated PDFs, and mirror-status confirmation. A Drive mirror never overrides a newer manifest-selected GitHub rule.

Conflict order:
1. current user scope and exclusions
2. manifest-selected active subject MASTER scope/source rules
3. this integrity contract and product hard gates
4. manifest-selected engine/QA/template/role contracts
5. historical or superseded files, which are reference-only

No runtime may select a version by filename recency, Drive title, or an `00_ACTIVE` label outside the manifest.

## 1. GLOBAL PRE-FLIGHT LOCK
Every batch records before generation:
- `ARC_RULESET_VERSION`
- active-file map resolved from the manifest
- `BATCH_ID`, product, subject, school, curriculum, item count or CORE scope
- `SCOPE_LOCK` with INCLUDED / EXCLUDED / UNKNOWN
- source inventory and source-access state
- checksum of every locked input and the final handoff Markdown

Unresolved `UNKNOWN`, missing school material required by the request, or a changed checksum after lock is a hard stop. Scope may become narrower during repair; it may not expand from web, bank, visual, difficulty, or layout sources.

## 2. ITEM PIPELINE HARD GATES
ARC_N and ARC_FINAL must enforce all of the following:

1. `SCHOOL_SOURCE_PRIORITY=PASS`: current school worksheets/teacher marks and current textbook range lead; past exams calibrate difficulty and task realism only.
2. `SCOPE_LOCK=PASS`: no correct answer or distractor elimination requires out-of-scope knowledge.
3. `UNIQUE_ANSWER=PASS`: one and only one best answer under the written conditions.
4. `PASS_A=PASS` and independent `PASS_B=PASS`; any option shuffle reruns both passes.
5. `DIFFICULTY_CALIBRATION=PASS`: evidence-based reasoning depth, not passage length, decoration, or obscure outside knowledge.
6. `SIMILARITY=PASS`: no near-duplicate stem/option/logic pattern beyond active thresholds.
7. `VISUAL_AUTHENTICITY=PASS`: every essential visual is source-grounded or transparently redesigned, solve-relevant, legible, and cross-checked against the item and answer.
8. `ANSWER_INTEGRITY=PASS`: item count, answer count, unique ITEM_IDs, actual correct-option positions, locked key, and rendered answer section agree exactly.

A generic score cannot override a failed hard gate. Verified-bank content is reusable only after current-scope and current-ruleset revalidation.

## 3. CORE ANTI-REGRESSION GATE
ARC_CORE is chapter/cluster-first and prose-led. Before concept drafting it requires `CENTRAL_QUESTION`, `CHAPTER_THESIS`, `DOMINANT_ORGANIZATION`, `BACKBONE_NODES`, essential relations, depth evidence, and one purposeful synthesis choice.

Internal-only metadata may include `CONCEPT_ID`, `DEPTH_PRIORITY`, `N_GENERATION_LINKS`, source IDs, and QA state. The student manuscript must not expose them.

The following legacy v0.3 behavior is forbidden:
- fixed nine-block concept cards
- student-facing `CONCEPT_ID` or N-degree links
- mandatory `MUST`, `CONFUSING`, `TRAP`, or `EXAM CONNECTION` for every concept
- one-concept-one-page or equal-length concept layouts
- repeated recap cards/tables/diagrams that add no new relation

Typesetter acceptance for CORE is based on the locked chapter/cluster manuscript, architecture summary, internal integrity index, and assets—not the presence of a particular optional student-facing block.

## 4. PDF AND BRAND HARD GATES
The Typesetter may paginate and make non-semantic line-break changes only. It may not re-grade, rewrite, omit, summarize, add content, or alter the locked answer.

ARC_N physical order is immutable:
`COVER -> BLANK_COVER_VERSO -> PROBLEM_PAGES -> BLANK_BEFORE_ANSWER -> ANSWER_KEY`.

Both blank pages are real, completely empty A4 pages: no logo, header, footer, page number, note, watermark, border, or hidden print object. The answer section is mandatory, starts immediately after the required separator blank, and contains exactly one entry per locked item.

Cover logos use only registry-approved canonical ARC master assets. Redrawing, retyping, tracing, generative recreation, or unnecessary re-export is forbidden. Missing or hash-mismatched assets stop production.

Preflight must verify physical order, true blankness, answer completeness/match, embedded fonts/glyphs, overflow/clipping, asset count/mapping, minimum readable size, brand ID/hash, and a rendered-page inspection. Mechanical checks alone do not prove release readiness.

## 5. ROLE HANDOFF
The only forward state path is:
`GENERATOR -> CONTENT_LOCKED -> READY_FOR_TYPESET -> TYPESETTER -> PDF_QC_PASS -> PUBLISHER -> DRAFT_REVIEW -> FINAL_RELEASED`.

- Generator owns scope, content, answer, source, difficulty, similarity, and visual specifications.
- Typesetter owns layout, pagination, render, and PDF preflight; content defects return to Generator.
- Publisher owns locked-key comparison, artifact/checksum verification, exact storage-parent verification, and release state; it cannot re-grade or rewrite.
- Any semantic change after `CONTENT_LOCK=true` invalidates downstream artifacts and creates a new content-lock checksum.

## 6. VERSION, MIRROR, CHECKSUM, REGRESSION
- A file is active only through the manifest. Historical versioned files remain read-only reference material.
- Every active entry with a Drive mirror declares `drive_id` and `drive_mirror_status`; `pending_sync` is visible debt, never silent equivalence.
- `CHECKSUMS.sha256` covers every Git-tracked production/rule/tooling file except itself and ephemeral outputs.
- `tooling/validate_system.py` must pass on every manifest/rule/template/contract change.
- The frozen 30-fixture set must remain loadable and unchanged unless a documented re-baseline creates a new fixture version.
- Full model-scored regression is claimed only when baseline/candidate outputs and a persisted result artifact exist. Static/smoke PASS must be reported separately.

END ARC PIPELINE INTEGRITY CONTRACT V1.0
