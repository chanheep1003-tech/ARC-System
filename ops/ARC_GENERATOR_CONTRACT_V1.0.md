# ARC GENERATOR CONTRACT V1.0
DATE: 2026-09-18
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

## 2. LOAD
Use JIT:
SYSTEM_MANIFEST
active subject MASTER
subject GOLD
current Drive scope/materials
required QA/source/visual rules
ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.0.md

Do not load PDF layout/brand rules unless needed to prepare asset constraints; the Typesetter owns PDF production.

## 3. GENERATION
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

## 4. CONTENT BUNDLE
Must satisfy ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.0.md.
No unresolved placeholders.
Essential visual specs must be complete enough that Typesetter does not infer subject matter.

## 5. NO PDF
Do not spend context/tokens on full PDF master, brand rendering, pagination, or PDF preflight during content generation.
If user asked for PDF too, finish READY_FOR_TYPESET and hand off to a dedicated Typesetter session/project.

## 6. GOVERNANCE
GitHub READ_ONLY.
Drive APPEND_ONLY.
No system-rule mutation.
System defects go to SYSTEM_FEEDBACK.

END ARC GENERATOR CONTRACT V1.0
