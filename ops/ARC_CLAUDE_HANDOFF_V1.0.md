# ARC CLAUDE HANDOFF V1.0
DATE: 2026-09-18
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
3. `engine/common/COMMON_GENERATION_ENGINE_V4.0_ARC.md`
4. the requested subject MASTER
5. the corresponding GOLD anchor pack
6. `quality/ARC_QA_BENCH_V1.2.md`
7. `quality/ARC_ITEM_QUALITY_RUBRIC_V1.1.md`
8. `quality/ARC_SOURCE_LEDGER_V1.0.md`
9. active visual/content policies when visuals may be used
10. `ops/ARC_GENERATOR_CONTRACT_V1.0.md`
11. `ops/ARC_CONTENT_BUNDLE_CONTRACT_V1.0.md`
12. current-scope Drive materials and relevant folder structure

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
2. read the active subject MASTER only
3. read the corresponding GOLD anchor pack
4. read only the current-range Drive materials needed for that subject
5. read required QA/source/visual rules on demand
6. inspect existing fresh ARC batches before generating

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
1. SOURCE/LOAD manifest or short audit note
2. QUESTION_MANUSCRIPT + ANSWER_KEY + LAYOUT_ASSET_MANIFEST + QC_STATUS
3. QA report
4. complete VISUAL_ASSET/VISUAL_SPEC handoff where needed
5. locked CONTENT_BUNDLE with CONTENT_QA_STATUS=PASS, CONTENT_LOCK=true, HANDOFF_STATUS=READY_FOR_TYPESET

Naming:
- `ARC_N_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_MANUSCRIPT`
- `ARC_N_<SUBJECT>_CLAUDE_<YYYYMMDD>_<BATCH_ID>_QA`
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
Use this command when beginning today's Cowork session:

`Enter ARC SYSTEM ABSORPTION mode. Read the latest dev SYSTEM_MANIFEST, ARC_CLAUDE_HANDOFF, common generation engine, KOR/SOC active MASTERs, KOR/SOC GOLD anchors, QA/item-quality/source rules, PDF layout master, brand lockup spec, and the current-scope Drive structure/materials needed to understand the system. Do not generate questions yet. Produce a compact ARC readiness digest and set CLAUDE_ARC_ABSORPTION_STATUS=PASS only after the required mechanism is understood. Then wait for my KOR or SOC generation command.`

When the user later requests KOR or SOC:
- generate exactly the requested batch
- the current user override permits an independent Claude KOR even if GPT KOR exists
- run ARC content QA
- create and lock the CONTENT_BUNDLE
- save manuscript + QA + READY_FOR_TYPESET content bundle
- stop after the requested subject unless the user explicitly asks to continue.

END ARC CLAUDE HANDOFF V1.0


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

END RECURRING GENERATOR PATCH
