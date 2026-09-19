# ARC PRODUCTION ORCHESTRATOR V1.1
VERSION: 1.1
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: end-to-end ARC production continuity controller

## 0. PRINCIPLE
ARC keeps Generator, Typesetter, and Publisher as separate roles, but normal PASS transitions do not require user confirmation.
All roles resolve versions only from `SYSTEM_MANIFEST.yaml` and obey the active pipeline integrity contract.

AUTO_CONTINUE_UNTIL_HARD_FAIL = true

Default end-to-end route:
REQUEST
→ GENERATOR
→ CONTENT_QA
→ CONTENT_LOCK
→ TYPESETTER
→ PDF_QC
→ PUBLISHER
→ STORAGE_PLACEMENT
→ READY_FOR_PHYSICAL_REVIEW
→ HUMAN_REVIEW
→ FINAL_RELEASED

A role handoff is an internal state transition, not a reason to stop and ask the user.

## 1. RUN MODES
END_TO_END:
- default when user asks to make, proceed, complete, publish, typeset, or produce a PDF
- continue through storage verification unless a HARD STOP occurs

CONTENT_ONLY:
- stop at READY_FOR_TYPESET only when user explicitly asks for manuscript/content only

TYPESET_ONLY:
- consume an already locked CONTENT_BUNDLE

PUBLISH_ONLY:
- consume an already typeset PDF + TYPESET_QC_REPORT

## 2. HARD STOP
Stop and ask for intervention only when the system cannot safely continue.

CONTENT hard stops:
- unresolved scope conflict
- required source missing or contradictory
- no unique answer / multiple-answer risk not resolvable by Generator
- CONTENT_QA_STATUS != PASS after allowed repair
- essential visual/data specification missing

TYPESET hard stops:
- canonical brand asset cannot be obtained after registry-ID lookup and available verified cache/file-reference lookup
- canonical asset hash mismatch
- answer key cannot be mapped exactly to locked item IDs
- required visual cannot fit/render legibly without changing answer-bearing content
- unresolved glyph/clipping/overlap affecting solving
- mandatory blank-page or ARC N° physical-order failure after repair

STORAGE hard stops:
- final artifact itself is unavailable/corrupt
- upload/write failure leaves no durable local/file-reference artifact and no recoverable handoff

## 3. SOFT STATES — DO NOT ASK
The following are not user-confirmation points:
- READY_FOR_TYPESET
- TYPESET_STATUS=PASS
- PDF_QC_STATUS=PASS
- DRAFT_REVIEW
- storage target already known from manifest/registry/handoff
- exact parent metadata recheck
- manual-upload fallback caused only by inefficient binary transport
- physical print review pending

Continue automatically and record state.

## 4. INTERNAL REPAIR
When a defect is owned by an earlier role and can be repaired without user judgment:
- route internally to that role
- repair
- rerun only affected gates
- resume from the interrupted stage

Do not surface a HOLD to the user merely because RETURN_TARGET is Generator or Typesetter.

Examples:
- manuscript submitted to Publisher → route to Generator lock / Typesetter automatically if the artifacts are available
- answer-table transcription mismatch → Typesetter re-renders from locked ANSWER_KEY
- blank page removed → Typesetter rebuilds page structure
- storage parent mismatch → Publisher/Drive adapter repairs placement and rechecks exact FILE_ID

## 5. USER-JUDGMENT STOPS
Ask the user only for genuine preference decisions, such as:
- competing visual identities with no approved ARC precedent
- scope choice not inferable from supplied school materials
- intentional content change after CONTENT_LOCK
- physical HUMAN REVIEW approval for FINAL_RELEASED

## 6. SAMPLE POLICY
Intermediate sample approval is NOT the default.

SAMPLE_REQUIRED only when:
- user explicitly asks for a sample, or
- a new product family has no usable approved/digitally accepted layout reference and full rendering would be materially risky

If an ARC product already has an accepted layout reference:
- reuse it
- render the full DRAFT
- perform PDF QC
- do not stop for another sample approval

A sample review never replaces final HUMAN REVIEW.

## 7. PUBLISHER AUTHORITY BOUNDARY
Publisher owns:
- artifact identity
- PDF/QC presence
- storage
- release-state transitions

Publisher does NOT:
- re-grade philosophical/scientific/historical correctness
- recompute correct answers independently
- rewrite items
- change option order
- override Generator PASS A/B

Publisher may compare the PDF answer table byte/logically against the locked ANSWER_KEY to detect typesetting transcription errors.
It must not derive a new answer distribution from its own content interpretation.

## 8. STORAGE TARGET RESOLUTION
Resolve target without asking in this order:
1. ops/ARC_STORAGE_TARGETS_V1.0.yaml
2. SYSTEM_MANIFEST runtime/product configuration
3. locked CONTENT_BUNDLE / handoff metadata
4. existing subject output registry

Ask the user for a folder only if no target exists in any authoritative source.

## 9. BINARY TRANSPORT
Preferred:
FILE_REFERENCE / file_uri → direct upload → exact parent verification.

Inline base64 for PDF/binary is disabled by default because it wastes context/tokens.

If the environment only supports expensive inline base64:
- do not ask the user to choose between expensive upload and manual upload
- set STORAGE_STATUS=MANUAL_UPLOAD_REQUIRED
- preserve the final artifact
- provide target folder + filename
- resume exact-ID verification after the file becomes visible

## 10. RELEASE SEMANTICS
Successful digital production and storage ends at:
RELEASE_STATUS=READY_FOR_PHYSICAL_REVIEW

Physical HUMAN REVIEW is a final release gate, not a blocker for Generator, Typesetter, PDF QC, or storage.

Only explicit HUMAN_REVIEW_STATUS=PASS permits:
FINAL_RELEASED=true

## 11. RELEASE APPROVAL DISAMBIGUATION
Generic positive user sentiment does not satisfy the physical HUMAN REVIEW gate.

Do not infer PHYSICAL_PRINT_REVIEW=PASS from words such as:
좋아 / 좋다 / 성공적 / 괜찮다 / 완벽 / 오케이 / PASS
unless the active HUMAN_REVIEW contract says the exact response is grounded to an explicit physical-print confirmation prompt.

When uncertain:
- keep RELEASE_STATUS=READY_FOR_PHYSICAL_REVIEW
- keep FINAL_RELEASED=false
- do not ask the same question repeatedly
- wait for an explicit report that the printed/physical copy was inspected

## 12. CANONICAL STORAGE STATE
Canonical successful storage state:
STORAGE_PLACEMENT=VERIFIED

PASS may be accepted as a legacy input alias, but all new ARC outputs must normalize it to VERIFIED before downstream state evaluation.

END ARC PRODUCTION ORCHESTRATOR V1.1
