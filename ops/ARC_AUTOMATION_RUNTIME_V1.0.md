# ARC_AUTOMATION_RUNTIME_V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: scheduled ARC generation runtime resilience

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

## 3. SUBJECT CHECKPOINT ORDER
Default priority:
1. SOC
2. SCI
3. KOR
4. HIS
5. AI

Each subject is an independent transaction.
Failure in one subject must not erase completed subjects.

## 4. PERSIST-FIRST
For each subject:
A. generate 20-item RAW
B. immediately persist RAW as a native Google Doc
C. then run QA
D. persist subject QA summary
E. persist `SOURCE_LEDGER_<RUN_ID>_<SUBJECT>` as native Google Doc when source-sensitive claims exist; if none, record SOURCE_REQUIRED_RECORDS=0
F. persist BANK_PASS candidates as a native Google Doc in subject bank only after source gate passes
G. continue to next subject

Do not wait until all 100 items are complete before the first write.

## 5. FILE FORMAT
Background automation uses native Google Docs for RAW, QA report, BANK batch, RUN log, and failure log.
Markdown may be used in interactive/manual runs but is not required for scheduled automation.

Reason: native Docs creation/write is the most reliable available Drive write path in scheduled runs.

## 6. RESUME CONTRACT
Run folder contains STATUS markers in the QA report:
- SOC: PENDING/RUNNING/DONE/FAILED
- SCI: PENDING/RUNNING/DONE/FAILED
- KOR: PENDING/RUNNING/DONE/FAILED
- HIS: PENDING/RUNNING/DONE/FAILED
- AI: PENDING/RUNNING/DONE/FAILED

If a run stops early, the next scheduled run may resume unfinished subjects after verifying existing checkpoint docs.

## 7. FAILURE CONTRACT
On any failure:
- write failure stage
- last completed subject
- error/tool stage if known
- created file IDs
- resume target
Do not report SUCCESS when required artifacts are absent.

## 8. QUALITY CONTRACT
Use ARC_ITEM_QUALITY_RUBRIC_V1.1, ARC_QA_BENCH_V1.1, and the subject GOLD_ANCHORS_V1.0 pack.
Do not assign target-looking scores before inspecting the actual item.
Score components require evidence.
Direct recall and weak distractor score ceilings apply automatically.
Each item records nearest GOOD/BAD anchor internally; BAD-match defects apply before BANK decision.
SOURCE_REQUIRED claims follow ARC_SOURCE_LEDGER_V1.0; ANSWER_BASIS sources must be reopened and VERIFIED before BANK write.
SOURCE ledger Drive folder: `1CmiPOP_Ma9FIuoyLOTEhjFpX7-tYwYwZ`.

## 9. OPTIMIZATION
No engine/prompt optimization until subject production and persistence completes.
Repeated defect >=3 may create a patch candidate; do not mutate GitHub during ordinary scheduled generation.

END ARC AUTOMATION RUNTIME V1.0
