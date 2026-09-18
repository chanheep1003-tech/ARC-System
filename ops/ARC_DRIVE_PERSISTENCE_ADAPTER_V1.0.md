# ARC DRIVE PERSISTENCE ADAPTER V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: reliable Google Drive persistence for OAuth/delegated and service-account connections

## 0. ROOT CAUSE
Google Drive native file creation differs by connection mode.
- service account/shared-drive paths may support create_file(parent_folder_id=...)
- OAuth/delegated connections may reject parent_folder_id during create_file

Therefore scheduled ARC runs must not assume direct-to-folder native Google Doc creation is available.

## 1. CANONICAL WRITE PATH
Default safe path for native Google Docs:
1. create_file(title, mime_type) with NO parent_folder_id
2. fetch/get metadata for the created file and read current parent_ids
3. update_file(addParents=TARGET_FOLDER_ID, removeParents=CURRENT_PARENT_IDS)
4. verify final parent_ids contains TARGET_FOLDER_ID
5. only then mark PERSISTED=true

Direct create_file(parent_folder_id=TARGET) is an optional fast path only when the connection explicitly supports it.
If direct creation fails once with a connection-capability error, switch the run to CREATE_THEN_MOVE mode and do not retry direct creation for every artifact.

## 2. WRITE PREFLIGHT
Before generating the first subject RAW artifact, perform a lightweight persistence preflight:
- create a tiny native Google Doc at root
- move it to the RUN_LOG or failure/test destination using CREATE_THEN_MOVE
- verify parent

If preflight fails:
- stop before expensive generation
- write the best-effort failure log wherever possible
- set failure_stage=DRIVE_PERSISTENCE_PREFLIGHT
- do not spend generation tokens producing unsavable artifacts

If preflight passes:
- DRIVE_WRITE_MODE=CREATE_THEN_MOVE or DIRECT_PARENT_CREATE
- reuse that mode for the entire run

## 3. SUBJECT TRANSACTION
For each subject:
A. generate RAW
B. persist RAW using active DRIVE_WRITE_MODE
C. verify saved file parent
D. only then start expensive QA
E. persist QA, SOURCE_LEDGER, BANK candidate using same adapter

No subject is considered complete unless required artifacts are verified in their target folders.

## 4. FAILURE ISOLATION
If a move/verify operation fails:
- preserve created file ID
- record its current parent
- set PERSISTENCE_STATE=ORPHANED_ROOT or WRONG_PARENT
- do not regenerate the same artifact from scratch before attempting recovery
- continue subject-failure isolation policy after logging

## 5. FILE VERIFICATION
Success requires:
- file exists
- expected MIME type
- expected target parent
- non-empty content for RAW/QA/BANK/report docs

Title alone is not sufficient evidence of successful persistence.

## 6. CONNECTION CAPABILITY CACHE
Per-run fields:
DRIVE_CONNECTION_MODE: SERVICE_ACCOUNT | OAUTH_DELEGATED | UNKNOWN
DRIVE_WRITE_MODE: DIRECT_PARENT_CREATE | CREATE_THEN_MOVE
DRIVE_PREFLIGHT_STATUS: PASS | FAIL

When OAuth/delegated behavior is detected, prefer CREATE_THEN_MOVE without repeated capability probing.

## 7. CURRENT ARC TARGETS
RAW root: 1OLxewFVlFsU7BETfszP_GPiLVnZtg_C-
QA REPORT root: 1UJk3gzBYBqozOEHwIEKL8LyNlfZrFuGM
SOURCE LEDGER root: 1CmiPOP_Ma9FIuoyLOTEhjFpX7-tYwYwZ
RUN LOG root: 1qaELb_KR95cCjsFsfdrCZviQLhjR-d4y
FAIL root: 1-RTu3H6XY9pdoEz7ROVoSysKPFkkaaAC

END ARC DRIVE PERSISTENCE ADAPTER V1.0