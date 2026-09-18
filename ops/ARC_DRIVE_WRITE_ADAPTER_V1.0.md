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

### MODE B — OAuth/delegated interactive connection
Interactive/manual sessions may use CREATE_THEN_MOVE when metadata moves are allowed.

### MODE C — scheduled/background connection (DEFAULT FOR AUTOMATIONS)
Scheduled automations must assume metadata moves can be blocked by safety checks even when root creation and body writes work.

Use ROOT_STAGING:
1. create native Google Doc at provider root/default with NO parent_folder_id
2. immediately write a staging header
3. verify non-empty content
4. keep the file at root for the scheduled run
5. record INTENDED_TARGET_FOLDER_ID in the document body
6. do NOT call update_file(addParents/removeParents) from the scheduled run
7. interactive/manual maintenance may move staged files later

ROOT_STAGING is a valid durable persistence state and must not stop QA generation.
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

## 2. SCHEDULED WRITE PREFLIGHT
Do not create a separate move probe.

The first real RAW shell is the preflight:
1. create `ARCSTAGE__<RUN_ID>__RAW__<SUBJECT>` at root/default
2. write only metadata header first
3. re-read and confirm non-empty content
4. set DRIVE_PREFLIGHT_STATUS=PASS and DRIVE_WRITE_MODE=ROOT_STAGING
5. generate/write item chunks into that same document

Required staging header:
RUN_ID
ARTIFACT_TYPE
SUBJECT
INTENDED_TARGET_FOLDER_ID
STORAGE_PLACEMENT=ROOT_STAGED
CREATED_AT

If root create or body write/read fails, stop before expensive generation.
If only folder move is unavailable, do not treat that as a generation failure because scheduled mode does not attempt move.

## 3. WRITE PREFLIGHT — INTERACTIVE
Before KOR generation starts, run exactly one small native-Doc write probe.

Canonical preflight:
1. create a tiny native Google Doc with NO parent_folder_id
2. read its current parent_ids
3. move it to RUN_LOG with addParents/removeParents
4. write a short probe body
5. re-read metadata and verify target parent + non-empty content

If this passes:
- DRIVE_PREFLIGHT_STATUS=PASS
- DRIVE_WRITE_MODE=CREATE_THEN_MOVE
- do not re-probe capability for each artifact

If this fails:
- stop BEFORE expensive item generation
- failure_stage=DRIVE_PERSISTENCE_PREFLIGHT
- persist the probe/failure FILE_ID if possible
- do not generate unsavable RAW content

Current verified OAuth/delegated pattern on 2026-09-18:
root create → parent read → move → body write → target-parent verify = PASS.

## 4. PERSIST-FIRST SEMANTICS
A successfully created native file is durable persistence even before the move.
Therefore a folder-placement failure must NOT discard completed generation work.

Scheduled mode:
- root create + verified non-empty write = PERSISTED=true
- STORAGE_PLACEMENT=ROOT_STAGED
- no move attempt
- continue QA normally
- record INTENDED_TARGET_FOLDER_ID for later repair

Interactive mode:
- move may be attempted
- if move fails, use MOVE_PENDING and preserve FILE_ID

If native file creation itself fails:
- PERSISTED=false
- subject may become FAILED_PENDING_RESUME

## 5. TARGET VERIFICATION
Never infer successful placement from the move call alone.
Verify the file ID appears in the destination folder or its returned parent_ids include the target.

## 6. FILE TYPES
Scheduled ARC artifacts should remain native Google Docs unless a product requires another format:
- RAW
- QA report
- SOURCE_LEDGER
- BANK_PASS candidate report
- RUN/FAILURE log

## 7. RUN FOLDER
Run folders may be created directly under the appropriate root when folder creation supports a parent.
Native Docs inside that folder still use MODE B when required.

## 8. FAILURE LOG
Failure logs must use the same adapter.
If placement fails, a root-level durable failure log is acceptable temporarily, but it must be marked MOVE_PENDING and retried.

## 9. SUCCESS METADATA
Report:
- DRIVE_CONNECTION_MODE = SERVICE_ACCOUNT | OAUTH_DELEGATED | UNKNOWN
- DRIVE_PREFLIGHT_STATUS = PASS | FAIL
- DRIVE_WRITE_MODE = DIRECT_PARENT | CREATE_THEN_MOVE | ROOT_STAGING
- STORAGE_PLACEMENT = VERIFIED | MOVE_PENDING | ROOT_STAGED
- ORPHANED_FILE_IDS = []
- STORAGE_REPAIR_NEEDED = true/false

Scheduled compute success is allowed with ROOT_STAGED if every required artifact exists and is non-empty.
Use status `COMPUTE_SUCCESS_ROOT_STAGED`, not FULL_STORAGE_SUCCESS.
MOVE_PENDING remains a repair state, not a generation failure.

END ARC DRIVE WRITE ADAPTER V1.0
