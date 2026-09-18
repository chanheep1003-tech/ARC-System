# ARC_AUTOMATION_RUNTIME_V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: scheduled ARC generation runtime resilience

## 0. DRIVE PERSISTENCE PREFLIGHT
Before loading KOR sources or generating any RAW items, read `ops/ARC_DRIVE_WRITE_ADAPTER_V1.0.md` and perform its one-time write preflight.
For the current OAuth/delegated connector, default to CREATE_THEN_MOVE:
create native Doc at root/default → read parent_ids → move to target with addParents/removeParents → verify target parent → write/verify content.

If DRIVE_PREFLIGHT_STATUS != PASS, stop before expensive generation and log DRIVE_PERSISTENCE_PREFLIGHT.
Do not retry direct parent creation for every artifact after a capability error.

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
A. generate 20-item RAW
B. immediately persist RAW as a native Google Doc using the active Drive write adapter
C. then run QA
D. persist subject QA summary
E. persist `SOURCE_LEDGER_<RUN_ID>_<SUBJECT>` as native Google Doc when source-sensitive claims exist; if none, record SOURCE_REQUIRED_RECORDS=0
F. persist BANK_PASS candidates as a native Google Doc in subject bank only after source gate passes
G. continue to next subject

Do not wait until all 100 items are complete before the first write.

## 5. FILE FORMAT
Background automation uses native Google Docs for RAW, QA report, BANK batch, RUN log, and failure log.
Markdown may be used in interactive/manual runs but is not required for scheduled automation.

Reason: native Docs creation/write is reliable only when connection-aware persistence is used.
On OAuth/delegated Drive, direct `parent_folder_id` creation is not a valid assumption; use CREATE_THEN_MOVE.

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
Use ARC_ITEM_QUALITY_RUBRIC_V1.1, ARC_QA_BENCH_V1.2, and the subject GOLD_ANCHORS_V1.0 pack.
Do not assign target-looking scores before inspecting the actual item.
Score components require evidence.
Direct recall and weak distractor score ceilings apply automatically.
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
