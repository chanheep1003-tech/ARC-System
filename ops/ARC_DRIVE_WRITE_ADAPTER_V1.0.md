# ARC DRIVE WRITE ADAPTER V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: connection-aware native Google Docs persistence

## 0. PURPOSE
ARC scheduled runs must not assume that Google Drive native file creation can target a folder directly.
OAuth/delegated Drive connections can reject `create_file(parent_folder_id=...)` even when file creation and metadata moves are allowed.

## 1. WRITE STRATEGY
### MODE A — direct service-account connection
If direct native creation into a writable shared-drive folder is supported:
1. create native file with destination parent
2. verify destination contains the returned file ID

### MODE B — OAuth/delegated connection (DEFAULT SAFE PATH)
Do NOT pass parent_folder_id to native `create_file`.
1. create native Google Doc/Sheet/Slide at the provider default/root
2. persist returned FILE_ID immediately
3. read current parent IDs
4. move with Drive metadata update:
   - addParents = target folder ID
   - removeParents = current parent IDs that are not the target
5. verify target folder contains FILE_ID
6. only then set STORAGE_PLACEMENT=VERIFIED

This create-then-move flow is the default when connection mode is unknown.

## 2. PERSIST-FIRST SEMANTICS
A successfully created native file is durable persistence even before the move.
Therefore a folder-placement failure must NOT discard completed generation work.

If create succeeds but move fails:
- PERSISTED=true
- STORAGE_PLACEMENT=MOVE_PENDING
- record FILE_ID and current parent
- continue required QA for that subject
- retry the move once after the subject checkpoint
- if still unresolved, finish the run as COMPUTE_COMPLETE_STORAGE_REPAIR_NEEDED rather than deleting output

If native file creation itself fails:
- PERSISTED=false
- subject may become FAILED_PENDING_RESUME

## 3. TARGET VERIFICATION
Never infer successful placement from the move call alone.
Verify the file ID appears in the destination folder or its returned parent_ids include the target.

## 4. FILE TYPES
Scheduled ARC artifacts should remain native Google Docs unless a product requires another format:
- RAW
- QA report
- SOURCE_LEDGER
- BANK_PASS candidate report
- RUN/FAILURE log

## 5. RUN FOLDER
Run folders may be created directly under the appropriate root when folder creation supports a parent.
Native Docs inside that folder still use MODE B when required.

## 6. FAILURE LOG
Failure logs must use the same adapter.
If placement fails, a root-level durable failure log is acceptable temporarily, but it must be marked MOVE_PENDING and retried.

## 7. SUCCESS METADATA
Report:
- DRIVE_WRITE_MODE = DIRECT_PARENT | CREATE_THEN_MOVE
- STORAGE_PLACEMENT = VERIFIED | MOVE_PENDING
- ORPHANED_FILE_IDS = []
- STORAGE_REPAIR_NEEDED = true/false

A run may not claim full storage success when MOVE_PENDING remains.

END ARC DRIVE WRITE ADAPTER V1.0
