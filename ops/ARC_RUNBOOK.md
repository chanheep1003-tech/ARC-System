# ARC single-run entry point

This runbook is the operational entry point for current production tasks. It replaces duplicated startup instructions in prompts; archived policy versions remain preserved. Current user scope and the pinned manifest decide the subject, file format, quantity and active rules. Do not inherit older 5-subject/Google-Docs defaults when the current request specifies a different job.

## Plan before production (2026-11-11)
Every production request first becomes a plan card: `python tooling/arc.py plan --subject … --scope … [--version] [--count]`. Rules: `ops/ARC_REQUEST_PLANNING_V1.0.md`; map: `ARC_MAP.md`. Draft one unit set, show it, then continue. KOR grammar bundles declare `archetype_library` and must pass `tooling/korean/archetype_gate.py`.

## Quick start (shell hosts)

```bash
python tooling/arc.py doctor      # deps + Korean fonts
python tooling/arc.py status      # KOR/SOC/SCI x CORE/N/FINAL readiness and blockers
python tooling/arc.py start --subject SCI --product ARC_N --count 20 --scope "산화·환원"
python tooling/arc.py log --run-id SCI-N-20261110-01 --product ARC_N --subject SCI --range "산화·환원" --items 20
python tooling/arc.py checksums   # after any tracked-file edit
python tooling/arc.py ci          # same steps as GitHub Actions
```

`start` fills batch_id, the pinned ruleset commit and the exam_context hash, runs `arc_workflow.py init`, and prints the manifest-selected files for that subject/product. It is a convenience wrapper around the contract below, not a second workflow. `scope` records a school-confirmed range supplied by the user (units, sources, evidence, optional FINAL anchor); it refuses to mark a range confirmed without evidence. Run directories under `runs/` are local and git-ignored; persist state beside the artifacts in Drive.

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


## KOR-only stage routing and outside text gate (2026-11-06)
For KOR only, load quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md, quality/korean/ARC_KOR_DONGBUK_UNSEEN_ANALYSIS_V1.0.md and quality/korean/ARC_KOR_DYNAMIC_SOURCE_SELECTION_V1.0.yaml. V1–V4 and V6 are Korean ARC_N, V5 Korean ARC_FINAL. No assumption about other subjects' numbered levels. For every V3 question, first fix the intended skill and inferential act, then search fresh sources at that production run; do not pick from a preset author/work/song roster. Literature: new work comparison; nonfiction: self-contained unseen X/Y concepts; grammar: unfamiliar documented text such as lyrics/poem/novel/diary or a freshly written original with passage necessity. Lyrics and copyrighted modern text require exact source/rights before reproduction; candidate metadata alone does not permit printing. If style evidence, source fidelity, lexical analysis, license, or 5-choice semantic proof is missing, block release.

## KOR V6 item routing (2026-11-06)
The active Korean-only version contract is `quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md`; its specialist supplement is `quality/korean/ARC_KOR_V6_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY_V1.0.md`. Dispatch V6 as ARC N° and V5 as ARC FINAL. V6 first chooses an in-scope orthography rule and inferential target; then finds a new unfamiliar short expression or writes one, checks POS/lexical meaning and normative authority separately, rejects context ambiguity, uses all-five-option truth checks, independent blinded solving before opening answer key, and retains a per-item rule+dictionary+novelty receipt. Never silently treat V3 genre-source load as V6; do not apply to SCI/SOC or claim new PDFs exist.

## KOR V6 spacing/particle decision gate (2026-11-06)
Read `quality/korean/ARC_KOR_V6_SPACING_POS_MINIMAL_PAIRS_V1.0.md` with the parent V6 policy. The upgraded 100-question TARGET is 30 particle (including 보조사) vs dependent-noun, 20 noun vs ending/suffix, 15 auxiliary-predicate/spacing-permissible/unit-noun, 20 rare lexeme/compound/saisiot, 15 authentic unknown sentence synthesis. Direct spacing TARGET = 65/100. Apply school textbook print scope before selecting material. Rule 41 particle attachment and Rule 42 dependent noun spacing must be based on official lexicon/POS and context, not token spelling; especially ‘만큼’ may be adverbial-case particle or auxiliary particle. Confirm Article 47 optional spacing. No completed claim without key-blind proof and all-five-option QA.

## Registered-file rule and Middle Korean routing (2026-11-10)
Rules take effect only in manifest-selected files. The 2026-11-07 Middle Korean and false-difficulty patches had been appended to superseded files and were never loaded; they now live in `subjects/KOREAN_MIDDLE_KOREAN_QUALITY_RULES_V1.0.md` (`runtime.korean_middle_korean_policy`, explicit user scope only) and `quality/ARC_FALSE_DIFFICULTY_GATE_V1.0.md` (`active.quality.false_difficulty_gate`, all subjects). The regression suite remains DEFINED_NOT_EXECUTED until actually run.
