# ARC CLAUDE HANDOFF V1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: Claude generation handoff without duplicating ARC

## 0. OPERATING PRINCIPLE
Claude is a first-class ARC generator, not a separate ARC fork.
Use the same source-of-truth as ChatGPT:
- engine/rules: GitHub `chanheep1003-tech/ARC-System` latest `dev`
- textbooks/worksheets/past exams: Google Drive `N제 시스템`
- verified item bank: Google Drive
Do not create a Claude-specific copy of MASTER/QA rules.

## 1. STARTUP LOAD ORDER
At the start of every generation session:
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

## 4. CURRENT PRODUCTION ORDER
Default subject priority:
KOR → SOC → SCI → HIS → AI

Today: Claude may start production first.
When GPT resumes later, GPT must inspect Claude batch metadata and continue from the next unfinished batch rather than recreating Claude work.

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
Prefer the existing ARC Drive destinations and metadata contracts.
Do not silently create a parallel Claude folder tree.
If the connected environment cannot place a file directly, preserve a durable staged artifact and record its intended target rather than discarding work.

## 11. GITHUB SAFETY
During ordinary item generation:
- GitHub rules/MASTER are read-only
- do not edit MASTER, QA, manifest, or policy files
- system changes require a separate maintenance task

## 12. CURRENT START COMMAND
Use this command when beginning work:

`Read the latest ARC-System dev SYSTEM_MANIFEST and this CLAUDE_HANDOFF. Inspect existing fresh batches first. Start from the highest-priority unfinished subject in KOR→SOC→SCI→HIS→AI order. Generate one ARC batch under the active subject MASTER and current Drive scope, record GENERATOR=CLAUDE and a unique BATCH_ID, apply the normal ARC QA, and do not duplicate an existing GPT/Claude batch. Use selective extra review only for high-risk items.`

END ARC CLAUDE HANDOFF V1.0
