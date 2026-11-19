# ARC GENERATOR CONTRACT V1.3
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: dedicated ARC content production

## 0. ROLE
GENERATOR_GPT and GENERATOR_CLAUDE produce and validate ARC content.
They do NOT typeset student PDFs.

## 1. OUTPUT TARGET
Generator work ends when a complete locked CONTENT_BUNDLE reaches:
CONTENT_QA_STATUS=PASS
CONTENT_LOCK=true
HANDOFF_STATUS=READY_FOR_TYPESET

## 2. LOAD — PRODUCT-AWARE JIT
Always:
SYSTEM_MANIFEST
active subject MASTER
current Drive scope/materials
ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.2.md

ARC_N / ARC_FINAL:
- manifest-selected common generation engine
- subject GOLD
- manifest-selected item/set QA rules
- required source/visual rules

ARC_CORE:
- manifest-selected core content engine
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
→ set blueprint
→ generation
→ PASS A
→ independent PASS B
→ source/fact audit
→ item QA
→ visual-spec completeness
→ set editorial
→ CONTENT_BUNDLE
→ CONTENT_LOCK

### ARC_CORE
SCOPE_LOCK
→ source load
→ concept map
→ CONCEPT_ID integrity
→ DEPTH_PRIORITY assignment
→ source-grounded CORE manuscript
→ required visual/source-text preparation
→ CORE editorial naturalness audit
→ CORE QA bench
→ CORE_LINK_INDEX
→ CONTENT_BUNDLE
→ CONTENT_LOCK

ARC_CORE does not run distractor/answer-position/item-answer gates unless the CORE manuscript intentionally contains a separately requested practice item section.

## 4. CONTENT BUNDLE
Must satisfy ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.2.md.
No unresolved placeholders.
Essential visual specs must be complete enough that Typesetter does not infer subject matter.

## 4-A. ARC CORE HARD GATE
For ARC_CORE:
- CORE_MANUSCRIPT required
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

END ARC GENERATOR CONTRACT V1.3
