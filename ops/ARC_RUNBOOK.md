# ARC single-run entry point

This runbook is the operational entry point for current production tasks. It replaces duplicated startup instructions in prompts; archived policy versions remain preserved. Current user scope and the pinned manifest decide the subject, file format, quantity and active rules. Do not inherit older 5-subject/Google-Docs defaults when the current request specifies a different job.

## One request, one state

Run `python tooling/workflow/arc_workflow.py` with a local JSON request and one durable `state.json` per unique batch. Persist the same state beside actual artifacts through the authorized Drive connector; never overwrite another batch. One coordinator owns the state. Worker outputs are separate evidence files. The coordinator records their receipts and transitions in this state, not in competing status documents.

The CLI checks stage order, IDs, counts, revision hashes, declared evidence, ownership and state version. It does not call any AI/API, read Drive, upload PDFs, establish independent review or decide factual truth. A supported host performs those actions and supplies actual receipts. Connector-only hosts follow this same JSON contract and report `TOOLING_UNAVAILABLE` if they cannot run the CLI. Do not claim automatic cross-provider dispatch.

States: request -> source -> draft -> review -> publish. Failures preserve the completed stage and store BLOCKED reasons. Reload status and repair the failed input before continuing. `publish` means a checked storage receipt, not human final release. Mode `draft` is allowed directly after drafting and keeps active=0; mode `verified` requires all requested IDs to pass review, fact, scope and quality gates.

## Commands

```bash
python tooling/workflow/arc_workflow.py init --state runs/BATCH/state.json --input request.json --actor GPT --manifest SYSTEM_MANIFEST.yaml
python tooling/workflow/arc_workflow.py status --state runs/BATCH/state.json
python tooling/workflow/arc_workflow.py record --state runs/BATCH/state.json --actor GPT --expected-version 1 --stage source --input source.json
python tooling/workflow/arc_workflow.py handoff --state runs/BATCH/state.json
```

Every successful mutation increments version. Failed stage gates also record a BLOCKED event and increment it. Re-read status before the next mutation. Wrong-owner and stale-version requests do not change state. Local file locking protects a shared local file only; it is not a distributed Drive lock. Use one coordinator and explicit ownership transfer for multiple hosts. Compare the remote state version before replacement; never overwrite a newer remote copy.

`transfer --new-owner GEMINI --reason "explicit handoff"` requires the current owner and expected version. Receiving worker must load the latest state and referenced artifacts before continuing.

## JSON contracts

Request example (replace the commit with the actual pinned SHA):

```json
{"batch_id":"SCI-NEUTRAL-20261030-05","subject":"SCI","scope":"user-authorized neutralization","product":"ARC_N","count":5,"ruleset_commit":"0000000000000000000000000000000000000000","outputs":["student.pdf","solutions.pdf"],"source_mix_mode":"original_trial"}
```

Source payload: `{"refs":[{"file_ref":"actual source file ID or path","location":"page/section","verified":true}]}`. Verified is a host attestation after an actual read; unknown or conflicting sources block this stage.

Draft payload: `{"items":[{"id":"SCI-001","sha256":"64-character actual student-manuscript hash","student_ref":"student-only file reference","author_answer":3}]}`. Record each chunk as another draft payload with new IDs; duplicate IDs and counts beyond the target fail. Partial counts remain visible and resumable. Review requires the complete requested bundle.

`handoff` after drafting emits only IDs, student references, hashes and neutral source references. It omits the author key. Keep the private state and author solution out of the reviewer's context; a role label cannot establish isolation.

Review payload:

```json
{"rounds":1,"fresh_context":true,"excluded_inputs":["answer_key","author_solution","author_history","target_difficulty"],"items":[{"id":"SCI-001","sha256":"same actual manuscript hash","answer":3,"option_verdicts":[false,false,true,false,false],"evidence_refs":["source file#page"],"fact_pass":true,"scope_pass":true,"quality_pass":true}]}
```

Record actual all-option judgments and independent source/fact/scope/quality evidence. Answer agreement alone does not pass an item. A one-round blind result binds only the reviewed manuscript. `revise --input revised-draft.json --reason "record exact edits"` after review archives the old result and clears current checked/eligible counts. It preserves IDs and records post_blind_edits; another blind round is rejected under the current policy. Publish the revised bundle as draft unless a future user-authorized policy supplies the required current-revision gate evidence.

Publish payload: `{"mode":"draft","artifacts":[{"file_ref":"actual saved PDF ID/path","readback_verified":true}]}`. A successful render without a storage readback is not a persistence receipt. Verified mode requires every requested item to be eligible and `gate_receipts` entries for `exam_scope`, `generation_source`, `similarity`, `product_quality`, each with `pass:true` and an actual `evidence_ref`. These attestations must follow the manifest-selected gates, including required visual/PDF checks within product_quality. Record applicable original-trial source policy rather than fabricating a 70% past-exam ratio. Missing/not-run gates permit draft output only. The ledger does not replace semantic or executable checks.

## Common startup for every provider

1. Read this runbook, the pinned SYSTEM_MANIFEST, AGENTS and assigned role/skill files. Resolve current engine/MASTER/QA paths from that manifest.
2. Reuse a matching incomplete batch by its state and content IDs; do not count resumed items as new items. Detect an active different owner and wait or obtain explicit transfer.
3. Confirm actual source access, then produce and save chunks with student/key separation.
4. Dispatch a fresh reviewer only if supported. If unavailable, continue justified drafts, save them as draft and report WAITING_FOR_WORKER.
5. Verify actual artifacts and save the state/receipts. Report drafted/checked/eligible/active counts separately and list remaining blockers.

The scheduled task's short request supplies only its scope, count, sources and destination. Avoid copying a second full policy into every AI's prompt.

## KOR corpus/norm correction gate (2026-11-05)
Load quality/korean/ARC_KOR_NORM_20261105_CORRECTION_POLICY.md, active Korean engine and tooling/content_qa/korean_norm_regression_gate.py. Each KOR 5-option evidence item must specify POSITIVE/NEGATIVE polarity; NEGATIVE = one FALSE with four TRUE and no unsupported alternatives. Require authoritative subsection/POS and actual passage TOC reconciliation, original-and-corrected SHA and rendered PDF glyph audit. When semantic blind review is not executed report REVIEW_PENDING, never VERIFIED/active; preserve old originals reversibly.
