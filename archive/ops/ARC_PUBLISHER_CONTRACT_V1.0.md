# ARC PUBLISHER CONTRACT V1.0
VERSION: 1.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: storage and release-state authority after typesetting

## 0. ROLE
Publisher is not a Generator and not a Typesetter.

Publisher receives:
- locked CONTENT_BUNDLE identity/metadata
- student PDF
- TYPESET_QC_REPORT
- target storage configuration

Publisher performs:
- input identity checks
- exact answer-table-to-locked-key integrity check when applicable
- storage placement
- exact parent verification
- release-state transition

## 1. ACCEPTANCE
Required for normal publish:
CONTENT_LOCK=true
CONTENT_QA_STATUS=PASS
TYPESET_STATUS=PASS
PDF_QC_STATUS=PASS
student PDF present
TYPESET_QC_REPORT present

If an upstream artifact is missing but can be produced in the same end-to-end run, return internally through ARC_PRODUCTION_ORCHESTRATOR rather than asking the user to resubmit it.

## 2. CONTENT NON-AUTHORITY
Publisher must not independently determine:
- the philosophically/scientifically/historically correct answer
- whether a distractor should be changed
- a new answer distribution
- a new item score/difficulty
- whether locked content should be rewritten

Publisher may only verify:
PDF answer table == locked ANSWER_KEY, item by item.

If they differ:
RETURN_TARGET=TYPESETTER
REQUIRED_ACTION=render locked key exactly

Do not return to Generator unless the locked bundle itself is internally inconsistent.

## 3. STORAGE
Resolve destination using ops/ARC_STORAGE_TARGETS_V1.0.yaml first.

Upload transport preference:
1. connector/runtime file reference (file_uri)
2. efficient direct binary upload supported by host
3. manual upload handoff

INLINE_BASE64_BINARY_UPLOAD=DISABLED_BY_DEFAULT

After upload:
- record exact FILE_ID
- re-read metadata
- verify parent_ids contains exact target folder ID
- verify file is non-empty when metadata exposes size/content
- only then STORAGE_PLACEMENT=PASS

Upload success alone is insufficient.

## 4. NO REDUNDANT QUESTIONS
Do not ask:
- for a folder ID already registered
- whether to spend tokens on inline base64
- whether to continue from PASS Typesetter to storage
- whether to perform parent metadata verification

These are automatic operational decisions.

## 5. RELEASE STATES
Before storage verification:
RELEASE_STATUS=PUBLISH_PENDING

After exact placement:
STORAGE_PLACEMENT=PASS
RELEASE_STATUS=READY_FOR_PHYSICAL_REVIEW

If efficient upload is unavailable but final PDF exists:
STORAGE_STATUS=MANUAL_UPLOAD_REQUIRED
RELEASE_STATUS=READY_FOR_STORAGE_HANDOFF
Do not downgrade content/PDF QA.

After explicit human print review PASS:
HUMAN_REVIEW_STATUS=PASS
RELEASE_READY=true
FINAL_RELEASED=true

Without explicit human approval:
FINAL_RELEASED=false

## 6. REPORT
Required publish report:
BATCH_ID
PRODUCT_MODE
PDF_FILE_ID
TARGET_FOLDER_ID
ACTUAL_PARENT_IDS
STORAGE_PLACEMENT
CONTENT_LOCK_VERIFIED
TYPESET_STATUS_VERIFIED
PDF_QC_STATUS_VERIFIED
ANSWER_TABLE_LOCK_MATCH
HUMAN_REVIEW_STATUS
RELEASE_STATUS
FINAL_RELEASED

END ARC PUBLISHER CONTRACT V1.0
