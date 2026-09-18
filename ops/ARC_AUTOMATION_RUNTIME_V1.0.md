# ARC_AUTOMATION_RUNTIME_V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: scheduled ARC generation runtime resilience

## 0. DRIVE PERSISTENCE PREFLIGHT
Scheduled/background runs use `ROOT_STAGING`, not CREATE_THEN_MOVE.
Do not call Drive metadata move/update_file in scheduled QA because background safety checks may block parent mutations.

For the first subject, create the actual RAW shell at root/default, write its staging header, re-read it, and use that as the persistence preflight.
If create/write/read succeeds, set DRIVE_PREFLIGHT_STATUS=PASS and continue.

Before loading KOR sources or generating any RAW items, read `ops/ARC_DRIVE_WRITE_ADAPTER_V1.1.md` and perform its one-time write preflight.
Default scheduled path:
root create → staging-header write → non-empty readback → chunked content append.

If DRIVE_PREFLIGHT_STATUS != PASS, stop before expensive generation and log DRIVE_PERSISTENCE_PREFLIGHT.
Folder placement is deferred; it is not part of scheduled preflight.

## 1. ROOT CAUSE TARGET
Background automation must not attempt one monolithic 100-item transaction.
A run is checkpointed by subject and must leave recoverable Drive artifacts after each stage.

## 2. JIT LOAD
Do not preload all five subject masters and all source files.
Per subject:
1. read SYSTEM_MANIFEST
2. read only that subject MASTER + required quality files + subject GOLD anchor pack + ARC_SOURCE_LEDGER_V1.0
3. read only current-scope Drive sources needed for that subject
4. generate
5. checkpoint
Then release that subject context and continue.

## 4. SUBJECT CHECKPOINT ORDER
Default priority follows `ops/ARC_RUNTIME_PRIORITY_POLICY_V1.0.md`:
1. KOR
2. SOC
3. SCI
4. HIS
5. AI

Normal 100-item runs still target 20 items per subject. Priority controls processing order, retries, extra review, research, and context budget rather than reducing required item counts.

Each subject is an independent transaction.
Failure in one subject must not erase completed subjects.

## 4. PERSIST-FIRST
For each subject:
A. create a ROOT_STAGED RAW Google Doc and verify its staging header
B. generate RAW in chunks of 5 items and append each chunk immediately
C. after each 5-item chunk, verify readable/non-empty state
D. after 20 RAW items are durable, run QA
E. persist subject QA summary as ROOT_STAGED
F. persist SOURCE_LEDGER as ROOT_STAGED when source-sensitive claims exist; if none, record SOURCE_REQUIRED_RECORDS=0
G. persist BANK_PASS candidate report as ROOT_STAGED after source gate passes
H. continue to next subject

Do not wait until all 100 items are complete before the first write.

## 5. FILE FORMAT
Background automation uses native Google Docs for RAW, QA report, BANK batch, RUN log, and failure log.
Markdown may be used in interactive/manual runs but is not required for scheduled automation.

Reason: native Docs creation/write is reliable only when connection-aware persistence is used.
On scheduled OAuth/delegated Drive, direct parent creation and metadata moves are both unsafe assumptions; use ROOT_STAGING.

## 6. RESUME CONTRACT
Run folder contains STATUS markers in the QA report:
- SOC: PENDING/RUNNING/DONE/FAILED
- SCI: PENDING/RUNNING/DONE/FAILED
- KOR: PENDING/RUNNING/DONE/FAILED
- HIS: PENDING/RUNNING/DONE/FAILED
- AI: PENDING/RUNNING/DONE/FAILED

If a run stops early, the next scheduled run may resume unfinished subjects after verifying existing checkpoint docs.

## 8. FAILURE CONTRACT
On any failure:
- write failure stage
- last completed subject
- error/tool stage if known
- created file IDs
- resume target
- mark subject FAILED_PENDING_RESUME
Do not report SUCCESS when required artifacts are absent.

A subject failure is isolated. After logging, continue to the next subject. After one pass across all subjects, resume failed subjects in KOR → SOC → SCI → HIS → AI order. Default automatic retry budget is one retry per failed subject/stage; do not loop indefinitely.

## 8. QUALITY CONTRACT
Use ARC_ITEM_QUALITY_RUBRIC_V1.2, ARC_QA_BENCH_V1.3, and the subject GOLD_ANCHORS_V1.0 pack.
Do not assign target-looking scores before inspecting the actual item.
Score components require evidence.
Direct recall, explicit-cue/restatement, weak-distractor, and distractor-distance ceilings apply automatically.
All D4/D5 and BANK_A candidates use blind score recheck.
For 20+ item sets, ZERO-REJECTION / BANK_A-rate / D4+D5-rate audits are mandatory when triggered.
Each item records nearest GOOD/BAD anchor internally; BAD-match defects apply before BANK decision.
SOURCE_REQUIRED claims follow ARC_SOURCE_LEDGER_V1.0; ANSWER_BASIS sources must be reopened and VERIFIED before BANK write.
SOURCE ledger Drive folder: `1CmiPOP_Ma9FIuoyLOTEhjFpX7-tYwYwZ`.

Executable tooling:
- local/CI host: run quantitative similarity, deterministic visual verifier, PDF preflight, and X-mark detector where applicable.
- connector-only scheduled host: do not fake execution. Record TOOLING_UNAVAILABLE and apply policy fallback. Essential accuracy gates remain mandatory.

## 10. RUNTIME BUDGET
Follow `ops/ARC_RUNTIME_PRIORITY_POLICY_V1.0.md`.

Stage priority:
P0 Scope/Accuracy/Unique Answer
P1 Actual Item Production
P2 Required QA
P3 Required Visuals
P4 Bank/Set Editorial
P5 Research/Optimization

If runtime is constrained, defer P5 first, then nonessential P4, then nonessential P3. P0–P2 must never be skipped. Required visuals are not optional.

Recommended extra-resource shares:
KOR 30 / SOC 25 / SCI 20 / HIS 15 / AI 10.

## 11. OPTIMIZATION
No engine/prompt optimization until subject production and persistence completes.
Repeated defect >=3 may create a patch candidate; do not mutate GitHub during ordinary scheduled generation.

END ARC AUTOMATION RUNTIME V1.0


## 12. HOURLY PRODUCTION MODE
For hourly automation, reliability beats one-run breadth.

- minimum success target per run: one complete 20-item subject batch through required QA
- if runtime remains, continue to the next subject
- do not regenerate a subject that already has a fresh STUDY_READY/COMPUTE_SUCCESS_ROOT_STAGED batch from the current cycle
- subject order remains KOR → SOC → SCI → HIS → AI
- after all five have fresh batches, begin a new cycle
- persist every 5 RAW items to limit loss on interruption

This prevents a 100-item monolithic hourly transaction from repeatedly timing out or losing all progress.


## 13. MULTI-MODEL BATCH COORDINATION
ARC may use ChatGPT and Claude as independent generators sharing the same source-of-truth.

Required batch metadata:
- GENERATOR = GPT | CLAUDE
- BATCH_ID
- SUBJECT
- SCOPE
- CREATED_AT
- QA_STATUS

Before generation, inspect fresh batch metadata and skip materially equivalent completed work from either generator.
Do not duplicate a Claude batch when GPT resumes, and do not duplicate a GPT batch when Claude is active.

Default policy is throughput-first:
- one batch has one primary generator
- universal cross-model regrading is disabled
- extra independent review is selective for D3+, ambiguous-answer, source-sensitive, and essential-visual high-risk items

Claude-specific startup instructions are in `ops/ARC_CLAUDE_HANDOFF_V1.0.md`.


## 14. GENERATOR / MAINTAINER SEPARATION
All scheduled GPT production follows `ops/ARC_MULTI_MODEL_GOVERNANCE_V1.0.md`.

GPT scheduled production is GENERATOR work only:
- GitHub READ_ONLY
- Drive APPEND_ONLY
- new unique BATCH_ID for every batch
- pin ARC_RULESET_VERSION at batch start
- never modify engine/MASTER/QA/template/tooling during generation
- write SYSTEM_FEEDBACK when a systemic defect is suspected

Interactive ChatGPT maintenance is the exclusive SYSTEM_MAINTAINER role.
System optimization must not occur inside a production automation.


## 15. STORAGE EXACT-ID CHECK
For every artifact that claims STORAGE_PLACEMENT=VERIFIED:
- verify exact FILE_ID
- verify target parent or exact FILE_ID in target folder
- verify non-empty content/size

A root-level PDF or Doc is not VERIFIED merely because upload succeeded.
If actual metadata and QA/placement-note status disagree, set STORAGE_METADATA_MISMATCH and repair before release.
