# ARC CLAUDE HANDOFF V1.2
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: Claude generation handoff without duplicating ARC

## 0. OPERATING PRINCIPLE
Claude is a permanent first-class ARC content generator, not a temporary test engine and not a separate ARC fork.
Claude and GPT both produce ARC batches on a recurring basis.
System/code/rule optimization belongs exclusively to the SYSTEM_MAINTAINER defined by `ops/ARC_MULTI_MODEL_GOVERNANCE_V1.0.md`.
Use the same source-of-truth as ChatGPT:
- engine/rules: GitHub `chanheep1003-tech/ARC-System` latest `dev`
- textbooks/worksheets/past exams: Google Drive `N제 시스템`
- verified item bank: Google Drive
Do not create a Claude-specific copy of MASTER/QA rules.

## 1. STARTUP / ABSORPTION GATE
Before generating any item in a fresh Claude/Cowork environment, perform SYSTEM ABSORPTION first.
For later sessions, if the last absorbed ARC_RULESET_VERSION equals the current SYSTEM_MANIFEST version and the relevant MASTER/QA files did not change, use FAST_REFRESH instead of re-reading the entire system.
Do not generate questions during this phase.

Read in this order:
1. `SYSTEM_MANIFEST.yaml`
2. this handoff
3. the manifest-selected Generator / Content Bundle contracts
4. the requested subject ACTIVE MASTER
5. current-scope Drive materials and relevant folder structure

Then branch by PRODUCT_MODE.

ARC_N / ARC_FINAL:
6. manifest-selected common generation engine
7. corresponding GOLD anchor pack
8. manifest-selected QA / item-quality / set-editorial / source rules
9. active visual policies when needed

ARC_CORE:
6. manifest-selected core content engine
7. manifest-selected core depth engine
8. manifest-selected CORE editorial-naturalness policy
9. manifest-selected CORE QA bench
10. source/source-text rules required by the subject
11. active visual policies when needed
12. GOLD anchor pack only when a specific CORE judgment benefits from it

Never use a hardcoded old version when SYSTEM_MANIFEST points to a newer active file.

After reading, produce a short readiness digest containing:
- source-of-truth hierarchy
- scope lock and exclusion hierarchy
- generation → QA → CONTENT_LOCK → READY_FOR_TYPESET separation
- hard-fail conditions
- source verification rules
- visual rules
- batch metadata contract
- output/storage contract
- subject-specific hard constraints

Set `CLAUDE_ARC_ABSORPTION_STATUS=PASS` only if every required rule/source actually opened is understood.
Never claim a file was read if it was not opened.
After PASS, record LAST_ABSORBED_RULESET_VERSION.
Then wait for the user's subject/item-count command or an explicitly configured recurring production task.

FAST_REFRESH:
1. read current SYSTEM_MANIFEST
2. compare ARC_RULESET_VERSION
3. if unchanged, read only the requested subject MASTER/GOLD + current Drive scope + any changed files
4. if changed, re-run full absorption for affected rules before producing

## 1A. JIT LOAD ORDER DURING GENERATION
At the start of every generation task:
1. read `SYSTEM_MANIFEST.yaml`
2. resolve PRODUCT_MODE
3. read the active subject MASTER
4. read only the current-range Drive materials needed for that subject
5. load the manifest-selected engine/QA stack for that PRODUCT_MODE
6. inspect existing fresh ARC batches before generating when duplicate avoidance applies

ARC_CORE must not preload N° item-generator/distractor/set-editor rules unless the task explicitly contains a problem-generation subtask.
ARC_N / ARC_FINAL must not preload CORE depth/editorial rules unless needed for a stated cross-product analysis.

Do not preload every subject or every Drive file.

## 2. GENERATOR IDENTITY
Every generated batch records:
- GENERATOR=CLAUDE
- MODEL_FAMILY=CLAUDE
- BATCH_ID
- SUBJECT
- CREATED_AT
- SCOPE_ID or scope description
- SOURCE_SET
- ITEM_COUNT
- QA_STATUS
- STORAGE_STATUS

Recommended BATCH_ID:
`ARC-CLAUDE-YYYYMMDD-SUBJECT-NN`

Student-facing PDFs never expose generator metadata.

## 3. DUPLICATE AVOIDANCE
Before generation, inspect fresh RAW/BANK/batch records.
Do not regenerate a batch already completed by Claude or GPT for the same cycle unless the user explicitly requests an alternate set.

A batch is considered occupied when it has:
- same subject
- materially same scope
- same cycle/date target
- status STUDY_READY, BANK_PASS, or COMPUTE_SUCCESS_ROOT_STAGED

If occupied, advance to the next unfinished batch.

## 4. RECURRING PRODUCTION
Default subject priority remains:
KOR → SOC → SCI → HIS → AI

Claude may regularly create independent ARC batches even when GPT also generates the same subject, provided each batch has a unique BATCH_ID and the user intended an alternate/new set.
Do not overwrite or revise GPT batches in place.
Do not edit ARC rules during production.
When a batch reveals a systemic defect, write SYSTEM_FEEDBACK and leave the actual system patch to the maintainer.

## 5. PRODUCTION MODE
Prioritize throughput over redundant cross-model review.

Default:
- one item is authored by one generator
- do not ask another model to rewrite or re-grade every item
- each generator applies ARC's normal QA to its own batch
- cross-model review is selective, not universal

Additional independent review is reserved for:
- D3+ / highest-difficulty items
- ambiguous answer-risk items
- source-sensitive answer basis
- essential numerical/structural visuals
- science particle/redox or other high-risk data consistency cases

## 5-A. ARC CORE PRODUCTION
When PRODUCT_MODE=ARC_CORE:
- use ARC CORE CONTENT ENGINE selected by SYSTEM_MANIFEST
- use the subject MASTER primarily for scope, source hierarchy, factual/interpretive safety, exclusions, and subject-specific concept constraints
- N°/FINAL-specific OUTPUT, ANSWER_KEY, item quota, distractor, and item-handoff clauses inside a subject MASTER do not override the active CORE product contract
- run concept mapping before drafting pages
- assign internal DEPTH_PRIORITY using the active CORE DEPTH ENGINE
- keep CONCEPT_ID / N_GENERATION_LINKS / DEPTH_PRIORITY / QA metadata hidden from student-facing manuscript
- use TRAP only with evidence
- apply CORE editorial-naturalness and CORE QA bench before CONTENT_LOCK
- output CORE_MANUSCRIPT + CORE_LINK_INDEX + QC + SOURCE_TEXT_BLOCKS/VISUAL specs when applicable
- do not create ANSWER_KEY unless a separately requested practice-item section requires one
- do not run N° answer-position or distractor gates on pure CORE content

Current high-depth priorities are resolved from the active depth engine, not from Claude memory.
For the current ruleset this includes user-designated Social punishment debate, Science OR/EM, supplement-centered Korean, and evidence-detected History clusters.

## 6. SUBJECT RULES
Always obey the active subject MASTER and current Drive scope.

Hard current constraints include:
- Social C worksheet handwritten X-mark regions are OUT OF SCOPE and must never be used.
- Historical/different-teacher exams are for difficulty/broad-format calibration only; teacher-style prediction is disabled.
- Do not expand beyond the current curriculum/scope merely because a source is available.

## 7. QA
Use the manifest-selected current QA stack.
At minimum:
- scope validity
- unique answer
- factual accuracy
- source gate where required
- distractor plausibility
- naturalness
- difficulty consistency
- required visual correctness
- set-level balance

Apply score ceilings for DIRECT_RECALL / WEAK_DISTRACTOR / GENERIC_CONTEXT / UNGROUNDED_STYLE.
Do not label trivial concept-check items as premium.

## 8. SOURCE HANDLING
For source-sensitive ANSWER_BASIS:
- attach SOURCE_ID
- reopen the original source before VERIFIED
- search snippets, filenames, or AI summaries are not sufficient for VERIFIED
- SOURCE_MISSING or SOURCE_CONFLICT blocks BANK/RELEASE for that answer basis

## 9. VISUALS
Use deterministic/editable visual construction for numeric/structural exam visuals.
Do not substitute generative art for graphs, particle models, experiment diagrams, maps, or structural data visuals when exactness matters.
Follow the active ARC visual policies.

## 10. OUTPUT / STORAGE
Use the existing subject folders; do not create a parallel Claude folder tree.

KOR:
- manuscript target: Drive folder `01_국어/출제원고` ID `1oPnRTZPczmXWlcDgg3aIMwuw2NWECBYQ`
- review/QA target: `01_국어/검수·수정본` ID `1d1nDUT7nAo-KIZZ78wb_yhXWBAqD1Z5L`
- finished N° PDF target: `01_국어/완성N제` ID `15P1JUMyrWoRO-VaJzg4F5cH9NIOXLoBZ`

SOC:
- manuscript target: `03_통합사회/출제원고` ID `1w25IxhXPuF7t4vKNLHwDF8n4U6o-E8Eo`
- review/QA target: `03_통합사회/검수·수정본` ID `1RtlCgV2whtzyMJjxbZpThqoO4JKfkMaY`
- finished N° PDF target: `03_통합사회/완성N제` ID `1ZloquIO4K5vF1V35g85IC93Mj_epHL-0`

Required generator outputs:

ARC_N / ARC_FINAL:
1. SOURCE/LOAD manifest or short audit note
2. QUESTION_MANUSCRIPT + ANSWER_KEY + LAYOUT_ASSET_MANIFEST + QC_STATUS
3. QA report
4. complete VISUAL_ASSET/VISUAL_SPEC handoff where needed
5. locked CONTENT_BUNDLE with CONTENT_QA_STATUS=PASS, CONTENT_LOCK=true, HANDOFF_STATUS=READY_FOR_TYPESET

ARC_CORE:
1. SOURCE/LOAD manifest or short audit note
2. CORE_MANUSCRIPT + internal CORE_LINK_INDEX + QC_STATUS
3. CORE QA report
4. SOURCE_TEXT_BLOCKS and VISUAL_ASSET/VISUAL_SPEC where needed
5. locked CONTENT_BUNDLE with CONTENT_QA_STATUS=PASS, CONTENT_LOCK=true, HANDOFF_STATUS=READY_FOR_TYPESET

Naming:
ARC_N / ARC_FINAL:
- `ARC_N_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_MANUSCRIPT`
- `ARC_N_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_QA`

ARC_CORE:
- `ARC_CORE_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_MANUSCRIPT`
- `ARC_CORE_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_QA`

All products:
- `ARC_CONTENT_<SUBJECT>_<BATCH_ID>_READY`

Every saved artifact must record:
GENERATOR=CLAUDE
BATCH_ID
SUBJECT
SCOPE
ITEM_COUNT
QA_STATUS
CREATED_AT

If the connected environment cannot place a file directly, preserve a durable staged artifact and record its intended target instead of discarding work.
Do not typeset the student PDF in the Generator project. A dedicated Typesetter project consumes READY_FOR_TYPESET bundles.

## 11. GOVERNANCE / GITHUB SAFETY
Read `ops/ARC_MULTI_MODEL_GOVERNANCE_V1.0.md`.
During ordinary item generation:
- GitHub rules/MASTER are read-only
- do not edit MASTER, QA, manifest, or policy files
- system changes require maintainer review
- never patch a rule because your own batch failed it
- system feedback must be evidence-based and stored separately from student-facing output

## 12. START COMMAND — FIRST SESSION / MAJOR RULESET CHANGE
Use this command when beginning a fresh Cowork session:

`Enter ARC SYSTEM ABSORPTION mode. Read the latest dev SYSTEM_MANIFEST and ARC_CLAUDE_HANDOFF. Resolve active files from the manifest instead of hardcoding versions. Learn the product-aware Generator/Content Bundle contracts and only the engine/QA stack needed for the product I request. Do not generate content yet. Produce a compact ARC readiness digest and set CLAUDE_ARC_ABSORPTION_STATUS=PASS only after the required mechanism is understood. Then wait for my ARC_CORE / ARC_N / ARC_FINAL command.`

When the user later requests KOR or SOC:
- generate exactly the requested batch
- the current user override permits an independent Claude KOR even if GPT KOR exists
- run ARC content QA
- create and lock the CONTENT_BUNDLE
- save manuscript + QA + READY_FOR_TYPESET content bundle
- if RUN_MODE=CONTENT_ONLY, stop after the requested subject at READY_FOR_TYPESET.
- if RUN_MODE=END_TO_END, continue automatically through Typesetter → Publisher → storage without asking for another continue command.


## 13. SYSTEM FEEDBACK OUTPUT
When a recurring defect is observed, create a short SYSTEM_FEEDBACK record instead of modifying GitHub.

Required:
BATCH_ID
GENERATOR=CLAUDE
ARC_RULESET_VERSION
DEFECT_CLASS
OBSERVED_BEHAVIOR
REPRODUCTION_EVIDENCE
PROPOSED_DIRECTION
SEVERITY

The maintainer will compare Claude and GPT evidence before changing ARC.

## 14. END-TO-END CONTINUITY
When the user's request is end-to-end production rather than content-only, obey the active ARC_PRODUCTION_ORCHESTRATOR.

Normal PASS flow must not pause for:
- READY_FOR_TYPESET confirmation
- repeated sample approval when an active ARC N° layout reference exists
- a Drive folder ID already registered in ARC_STORAGE_TARGETS
- a choice between expensive inline base64 and manual upload
- exact parent metadata verification

Maintain role separation:
Generator → Typesetter → Publisher
but switch/handoff roles automatically when the host can continue the workflow.

If the host has a file-reference/file_uri upload path, use it for PDFs and verify the exact parent automatically.
If the host only has inline base64 for binary upload, do not consume large context by default; set MANUAL_UPLOAD_REQUIRED without asking a 1/2 choice.

Publisher must not independently re-grade locked answers or generate a new answer distribution. It may only compare the typeset answer table against the locked ANSWER_KEY.

Final normal digital endpoint:
RELEASE_STATUS=READY_FOR_PHYSICAL_REVIEW
FINAL_RELEASED=false

Only explicit physical HUMAN REVIEW PASS permits FINAL_RELEASED=true.

END ARC CLAUDE HANDOFF V1.2
