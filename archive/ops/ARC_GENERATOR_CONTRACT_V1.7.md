# ARC GENERATOR CONTRACT V1.7
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: dedicated ARC content production

## 0. ROLE
GENERATOR_GPT and GENERATOR_CLAUDE produce and validate ARC content.
They do NOT typeset student PDFs.

## 1. OUTPUT TARGET
Generator work ends only when:
CONTENT_QA_STATUS=PASS
CONTENT_LOCK=true
HANDOFF_STATUS=READY_FOR_TYPESET
HANDOFF_MD_STATUS=READY

The Generator must create one self-contained Markdown handoff file for Typesetter after content lock.
Chat-only prose is not considered a complete production handoff.

## 2. LOAD — PRODUCT-AWARE JIT
Always:
SYSTEM_MANIFEST
active pipeline integrity contract
active subject MASTER
current Drive scope/materials
manifest-selected active CONTENT_BUNDLE contract

ARC_N / ARC_FINAL:
- manifest-selected common generation engine
- active subject MASTER
- manifest-declared subject-specific item engine when required
- subject GOLD
- manifest-selected item/set QA rules
- manifest-declared subject-specific QA when required
- required source/visual rules

ARC_CORE:
- manifest-selected core content engine
- core editorial architecture
- core depth engine
- core editorial naturalness policy
- core QA bench
- required source/visual rules
- subject GOLD is optional unless a specific CORE judgment needs it

Do not load PDF layout/brand rules unless needed to prepare asset constraints; the Typesetter owns PDF production.

## 3. GENERATION — PRODUCT ROUTES

### ARC_N / ARC_FINAL
SCOPE_LOCK
→ source load
→ SCHOOL_SOURCE_PRIORITY gate
→ subject-specific item engine load when required
→ set blueprint
→ generation
→ PASS A
→ independent PASS B
→ source/fact audit
→ item QA
→ subject-specific QA when required
→ visual-spec completeness
→ difficulty calibration + similarity + visual authenticity gates
→ answer integrity gate
→ set editorial
→ CONTENT_BUNDLE
→ CONTENT_LOCK
→ input/handoff checksum lock
→ HANDOFF_MD

### ARC_CORE
SCOPE_LOCK
→ source load
→ chapter/cluster map
→ CENTRAL_QUESTION + CHAPTER_THESIS
→ DOMINANT_ORGANIZATION + BACKBONE_NODES
→ concept map inside backbone
→ CONCEPT_ID integrity
→ CLUSTER_DEPTH_PRIORITY + DEPTH_PRIORITY assignment
→ source-grounded CORE manuscript
→ required visual/source-text preparation
→ macro editorial architecture audit
→ CORE editorial naturalness audit
→ CORE QA bench
→ CORE_LINK_INDEX
→ CONTENT_BUNDLE
→ CONTENT_LOCK
→ HANDOFF_MD

ARC_CORE does not run distractor/answer-position/item-answer gates unless the CORE manuscript intentionally contains a separately requested practice item section.

## 4. CONTENT BUNDLE
Must satisfy the manifest-selected active CONTENT_BUNDLE contract.
No unresolved placeholders.
Essential visual specs must be complete enough that Typesetter does not infer subject matter.

## 4-A. ARC CORE HARD GATE
For ARC_CORE:
- CORE_MANUSCRIPT required
- CORE_EDITORIAL_ARCHITECTURE = PASS
- MACRO_COHERENCE = PASS
- CHAPTER_BACKBONE_PRESENT = PASS
- DOMINANT_ORGANIZATION_CLEAR = PASS
- INFORMATION_HIERARCHY = PASS
- ANTI_LISTING = PASS
- REDUNDANCY_BUDGET = PASS
- SYNTHESIS_TRANSFORMS = PASS
- CONCEPT_ID metadata complete internally
- student-facing internal metadata leak = 0
- DEPTH_ASSIGNMENT / DEPTH_EVIDENCE / DEPTH_SCOPE_SAFETY / DEPTH_BUDGET = PASS
- CORE_EDITORIAL_NATURALNESS = PASS
- CORE_QA_STATUS = PASS
- SOURCE_TEXT fidelity gates PASS when applicable
- CORE_LINK_INDEX internal payload complete
Failure blocks READY_FOR_TYPESET.

## 4-B. ANSWER HARD GATE
For ARC_N / ARC_FINAL:
- ANSWER_KEY required
- exactly ITEM_COUNT answer entries
- each ITEM_ID appears exactly once
- no blank/TBD/UNKNOWN answer
- PASS A and PASS B must agree
- ANSWER_KEY_COMPLETE=PASS
- ANSWER_COUNT_MATCH=PASS

Failure blocks READY_FOR_TYPESET.

## 4-C. HANDOFF MARKDOWN — REQUIRED
After CONTENT_LOCK=true, serialize the locked bundle into one UTF-8 Markdown file.

Canonical filename:
ARC_HANDOFF_<PRODUCT>_<SUBJECT>_<BATCH_ID>_READY.md

Examples:
ARC_HANDOFF_CORE_HIS_ARC-GPT-20260919-HIS-01_READY.md
ARC_HANDOFF_N_SOC_ARC-GPT-20260919-SOC-02_READY.md

The Markdown file is the direct Typesetter input. It must be downloadable/attachable as a file, not only displayed inside chat.

Required top-level structure:

---
ARC_HANDOFF_VERSION: 1.0
ARC_RULESET_VERSION: <version>
BATCH_ID: <id>
GENERATOR: GPT|CLAUDE
PRODUCT_MODE: ARC_CORE|ARC_N|ARC_FINAL
SUBJECT: <code>
SCOPE: <scope>
CONTENT_QA_STATUS: PASS
CONTENT_LOCK: true
HANDOFF_STATUS: READY_FOR_TYPESET
TYPESET_STATUS: PENDING
---

# TYPESETTER INSTRUCTIONS — INTERNAL / DO NOT PRINT
Content-preservation rules only. The Generator must not pin a PDF master,
column count, font size, CSS selector, ReportLab Frame/PageTemplate, margin,
or page geometry. The Typesetter resolves every layout rule from the current
SYSTEM_MANIFEST at render time.

# CORE ARCHITECTURE SUMMARY — INTERNAL / DO NOT PRINT
Required for ARC_CORE only:
CENTRAL_QUESTION
DOMINANT_ORGANIZATION
BACKBONE_NODES
END_SYNTHESIS_MODE
CORE_EDITORIAL_ARCHITECTURE
MACRO_COHERENCE

# STUDENT MANUSCRIPT
The complete locked student-facing manuscript.
This section is the primary printable content.

For ARC_CORE, Markdown heading levels are structural and mandatory:
- `#` = PART or MAJOR_TOPIC boundary; every such heading starts a new physical page
- `##` = CHAPTER
- `###` = SECTION
- `####` = FUNCTIONAL_LABEL only when a heading is semantically appropriate

Social Studies A/B/C parts must each use a level-1 heading such as
`# A파트 · 사회 정의`. A real top-level topic change must also use level 1.
Do not use level 1 merely for visual emphasis.

# ANSWER KEY — INTERNAL / DO NOT PRINT ON PROBLEM PAGES
Required for ARC_N / ARC_FINAL.
ARC_N Typesetter may render the compact answer section according to product rules.

# VISUAL / LAYOUT ASSET MANIFEST — INTERNAL / DO NOT PRINT
All essential visual specs, asset references, keep-together rules, and layout hints.

# SOURCE TEXT BLOCKS — INTERNAL SOURCE PAYLOAD
Only when required by active subject policy.

# QC STATUS — INTERNAL / DO NOT PRINT
Required QA state fields.

Rules:
- No unresolved placeholder/TBD/UNKNOWN.
- Do not omit content because it already appeared in chat.
- Do not create a second conflicting manuscript outside this file.
- The MD file and locked CONTENT_BUNDLE must be semantically identical.
- Internal sections must be explicitly marked DO NOT PRINT.
- STUDENT MANUSCRIPT must contain no internal metadata.
- STUDENT MANUSCRIPT must not contain bracketed CONCEPT_ID/SOURCE_ID labels.
- Handoff Markdown must not contain product-layout commands; any stale layout
  instruction makes HANDOFF_MD_STATUS=FAIL until regenerated under the active ruleset.
- The file must be saved/generated before reporting READY_FOR_TYPESET.

HANDOFF_MD_STATUS values:
PENDING | READY | FAIL

READY_FOR_TYPESET requires HANDOFF_MD_STATUS=READY.

## 4-D. SUBJECT-SPECIFIC ITEM ENGINE GATE
If SYSTEM_MANIFEST declares a subject-specific item engine or QA as required, READY_FOR_TYPESET is blocked until those gates pass.

Current KOR requirements:
- engine/korean/ARC_KOREAN_ITEM_ENGINE_V1.0.md
- quality/ARC_KOREAN_ITEM_QA_V1.0.md

Required KOR status:
KOR_PASSAGE_MAP=PASS
KOR_PASSAGE_UTILIZATION=PASS
KOR_REASONING_DIVERSITY=PASS
KOR_DUPLICATE_AXIS=PASS
KOR_DISTRACTOR_COMPETITIVENESS=PASS
KOR_ANSWER_LENGTH_AUDIT=PASS
KOR_STEM_DIVERSITY=PASS
KOR_ANSWER_PATTERN=PASS

A generic ITEM_QA PASS cannot override a failed subject-specific gate.

## 5. NO PDF
Do not spend context/tokens on full PDF master, brand rendering, pagination, or PDF preflight during content generation.
If user asked for PDF too, finish READY_FOR_TYPESET and hand off to a dedicated Typesetter session/project.

## 6. SOURCE-BOUND TEXT
Copyright-protected text does not automatically block ARC generation.

When the active subject policy permits SOURCE_TEXT_BLOCK:
- user-pasted/uploaded or connected user-accessible school/textbook/supplement source may be included verbatim in the bundle
- re-open and read the actual source before creating VERBATIM_FULL/VERBATIM_RANGE
- preserve wording and meaningful structure; do not reconstruct from memory
- include SOURCE_TEXT_BLOCK metadata and LINKED_ITEM_IDS
- use one shared source block for a question cluster instead of duplicating the full text per item
- if the source is incomplete/garbled/unavailable, do not fabricate the missing text; set SOURCE_TEXT_INCOMPLETE and return for source repair
- web search/snippets/unverified external pages are not valid authority for full protected-text reproduction

The Generator owns source-text fidelity; the Typesetter must not alter source wording.

## 7. GOVERNANCE
GitHub READ_ONLY.
Drive APPEND_ONLY.
No system-rule mutation.
System defects go to SYSTEM_FEEDBACK.

## 8. AUTO HANDOFF
Generator still does not typeset PDFs.

However, when RUN_MODE=END_TO_END and the bundle reaches:
CONTENT_QA_STATUS=PASS
CONTENT_LOCK=true
HANDOFF_STATUS=READY_FOR_TYPESET

the ARC_PRODUCTION_ORCHESTRATOR automatically transfers the locked bundle to Typesetter.
Do not stop merely to ask the user whether to continue.

If user explicitly requested CONTENT_ONLY, stop at READY_FOR_TYPESET.

## 9. REPAIR OWNERSHIP
If Typesetter/Publisher detects a true content defect and returns an item:
- repair only the flagged content
- rerun affected Generator QA gates
- issue a new locked bundle version
- hand back automatically under END_TO_END

Publisher disagreement by itself is not a content defect. Publisher is not allowed to independently re-grade correct answers.

END ARC GENERATOR CONTRACT V1.7
