## 1.7.5-dev — 2026-09-19
- Added ARC_PRODUCTION_ORCHESTRATOR_V1.0 with AUTO_CONTINUE_UNTIL_HARD_FAIL. Generator → Typesetter → Publisher transitions no longer require user confirmation after normal PASS states.
- Added ARC_PUBLISHER_CONTRACT_V1.0. Publisher is restricted to artifact integrity, locked-answer-table comparison, storage, exact parent verification, and release-state transitions; it may not independently re-grade answers or rewrite content.
- Added ARC_STORAGE_TARGETS_V1.0 as a central destination registry so registered KOR/SOC output folder IDs are resolved without asking again.
- Activated ARC_GENERATOR_CONTRACT_V1.4, ARC_CONTENT_BUNDLE_CONTRACT_V1.3, and ARC_TYPESETTER_CONTRACT_V1.3 with automatic end-to-end handoff while preserving role separation.
- Activated ARC_DRIVE_WRITE_ADAPTER_V1.2 with FILE_REFERENCE_FIRST binary upload. Inline base64 PDF upload is disabled by default; hosts with only expensive inline base64 use MANUAL_UPLOAD_REQUIRED without a redundant 1/2 choice.
- Activated ARC_HUMAN_REVIEW_GATE_V1.1. Physical HUMAN REVIEW is now explicitly a FINAL_RELEASE-only gate and does not block full typesetting, PDF QC, upload, or exact parent verification.
- Added ARC_N_TYPESET_REFERENCE_V1.0 using the digitally accepted Kant–Beccaria N° PDF as a reusable layout reference; repeated intermediate sample approval is skipped when the PDF master/brand system is materially unchanged.
- Activated ARC_CLAUDE_HANDOFF_V1.2 so end-to-end Claude/Cowork runs follow the same continuity, storage-target, binary-transport, and Publisher authority rules.
- Fixed Typesetter startup to resolve the active PDF master from SYSTEM_MANIFEST instead of hardcoding V2.1.
- No executable frozen-fixture regression was claimed in this connector-only maintenance pass.

## 1.7.4-dev — 2026-09-19
- Activated ARC_CORE_CONTENT_ENGINE_V1.2 with adaptive concept depth.
- Added ARC_CORE_DEPTH_ENGINE_V1.0 with internal STANDARD / ADVANCED / HIGH_DIFFICULTY priorities. Depth labels remain hidden from student-facing CORE.
- HIGH_DIFFICULTY now expands condition, boundary, premise, trap-logic, and multi-step reasoning only when supported by scope/evidence; it does not authorize out-of-scope enrichment.
- User-designated high-depth priorities: Social Kant–Beccaria punishment/death-penalty debate; Science OR redox and EM electromagnetic induction; Korean supplement-centered interpretation. History uses evidence-based difficulty-signal detection instead of a fixed hard unit.
- Science OR/EM depth remains bounded by SCIENCE_MASTER's ADVANCED LEAK BLOCK; high depth emphasizes data/condition reasoning rather than upper-grade formulas.
- Korean CORE source emphasis now prioritizes school supplements/worksheets and uses textbook content primarily for original text, foundations, and gap filling rather than repetitive re-summary.
- History CORE detects clusters with overlapping periods, similar organizations/policies, formation-split-unification, ideological relations, source-speaker inference, map/region coupling, and multi-period actors before increasing depth.
- Activated ARC_CORE_QA_BENCH_V1.1 with DEPTH_ASSIGNMENT, DEPTH_EVIDENCE, DEPTH_SCOPE_SAFETY, DEPTH_BUDGET, and HIGH_DIFFICULTY_COMPLETENESS gates.
- Activated ARC_CORE_EDITORIAL_NATURALNESS_V1.1 and ARC_TEMPLATE_SYSTEM_v0.5_CORE_PATCH so adaptive depth changes information density rather than adding repetitive "advanced/killer" badges or fixed deep-dive cards.
- Activated ARC_GENERATOR_CONTRACT_V1.3 with separate ARC_CORE and ARC_N/FINAL production routes.
- Activated ARC_CLAUDE_HANDOFF_V1.1. Claude now resolves active versions from SYSTEM_MANIFEST and loads a CORE-specific stack for PRODUCT_MODE=ARC_CORE instead of hardcoded legacy N° files.
- ARC_CORE subject MASTER use is scope/source/factual authority; N°-specific output, answer-key, distractor, and item-handoff clauses do not override the active CORE product contract.
- GitHub dev remains source of truth; new CORE/Depth mirrors are pending_sync.
- Executable frozen-fixture regression was not claimed in this connector-only maintenance pass.

## 1.7.3-dev — External skill intake addendum — 2026-09-19
- Added ARC_EXTERNAL_SKILL_INTAKE_POLICY_V1.0 for governed use of public GitHub skills when ARC has a capability gap.
- External skills are on-demand and remain below ARC scope/master/engine/QA authority.
- Default intake is REFERENCE_ONLY or ADAPT; automatic vendoring is disabled.
- License, executable-code, credential, network, write-capability, overlap, and instruction-conflict checks are required before adoption.
- Proprietary/source-available skills may be used only as design references unless a compatible license explicitly permits reuse.
- Registered the intake policy in SKILL_REGISTRY, skill governance, orchestration, and SYSTEM_MANIFEST.
- Initial design references: OpenAI official skills/skill-creator patterns for JIT loading and skill validation; Anthropic skills repository only where licensing permits, with proprietary document skills treated as reference-only.

## 1.7.3-dev — 2026-09-19
- Activated ARC_CORE_CONTENT_ENGINE_V1.1.
- CORE student output no longer exposes CONCEPT_ID, N° linkage, priority, BANK, QA, or internal source metadata.
- Replaced student-facing N° LINK with internal-only N_GENERATION_LINKS for future N° blueprint coverage and concept combination.
- Added evidence-gated TRAP blocks; unsupported or invented traps are removed instead of being shown to students.
- Added ARC_CORE_EDITORIAL_NATURALNESS_V1.0 to suppress repetitive card layouts, fixed block counts, repeated phrasing, redundant summaries, decorative boxes, and unsupported exam-prediction language.
- Added ARC_CORE_QA_BENCH_V1.0 with set-level AI-pattern sentinels, redundancy audit, TRAP evidence audit, student-view audit, and Korean-specific source/interpretation checks.
- Activated ARC_TEMPLATE_SYSTEM_v0.4_CORE_PATCH. CORE now uses paragraph-led reference-book flow with optional MUST / CONFUSING / TRAP / EXAM CONNECTION blocks instead of a fixed nine-block template.
- Korean CORE now follows KOREAN_MASTER_V4.1 SOURCE-BOUND ORIGINAL TEXT MODE: user-provided/uploaded or connected user-accessible school/textbook/supplement source text may be embedded as verified SOURCE_TEXT_BLOCK, preserving poem line/stanza and prose paragraph order.
- Korean CORE prioritizes whole-work flow and school-supplement interpretation structure over fragmented theme/emotion/expression cards.
- GitHub dev remains source of truth; the new CORE engine Drive mirror is pending_sync.
- Executable regression was not claimed in this connector-only maintenance pass.

## 1.7.2-dev — 2026-09-19
- Activated COMMON_GENERATION_ENGINE_V4.3 with SOURCE-BOUND TEXT EXCEPTION for user-pasted/uploaded and connected user-accessible school/textbook/supplement sources.
- Activated KOREAN_MASTER_V4.1. Korean ARC output now defaults to self-contained source presentation when the original text is actually available from an allowed source.
- Added SOURCE_TEXT_BLOCK with source provenance, inclusion mode, fidelity state, exact text body, and linked item IDs.
- Protected modern literary works may be included as VERBATIM_FULL or VERBATIM_RANGE when the text comes from a user-provided/uploaded or connected user-accessible source; web search/snippets/unverified external pages cannot authorize full protected-text reproduction.
- Added source-text fidelity checks for poem line/stanza order, prose paragraph order, completeness, source access, and question linkage.
- Activated Generator / Content Bundle / Typesetter contracts V1.2 and PDF layout master V2.2 for lossless source-text handoff and two-column pagination.
- Activated KOR_GOLD_ANCHORS_V1.1 and QA BENCH V1.5 with KOR-B04 source-text fidelity bench.
- ARC N° Korean source blocks may continue across columns/pages while remaining COLUMN_ONLY; Typesetter may not omit or rewrite source text to force fit.
- Korean ARC N° answer-key handoff was aligned with the current mandatory blank separator + compact final answer section.
- New GitHub rules are authoritative; Drive mirrors for new Common/Korean master remain pending_sync until explicitly mirrored.
- Executable frozen-fixture regression was not claimed in this connector maintenance pass.

## 1.7.1-dev — 2026-09-18
- Activated COMMON_GENERATION_ENGINE_V4.2 with natural five-choice answer-position planning: soft distribution bands, streak/periodicity flags, and mandatory re-verification after option shuffling.
- Added CLAIM_FIDELITY safeguards for thinker/theory items: explicit position vs supported implication vs opponent critique vs straw-man risk.
- Activated SOCIAL_MASTER_V4.1 with PHILOSOPHY_ATTRIBUTION, CRITIQUE_TARGET_FIDELITY, and ABSOLUTE_WORDING_AUDIT gates.
- Activated ARC_ITEM_QUALITY_RUBRIC_V1.3, ARC_SET_EDITORIAL_ENGINE_V1.1, and ARC_QA_BENCH_V1.4.
- Added SOC-B04 Kant/Beccaria punishment-theory bench target for attribution, critique fidelity, absolute wording, and answer-position distribution.
- Corrected manifest answer-key placement wording to AFTER_REQUIRED_SEPARATOR_BLANK, consistent with the required blank page before the answer section.
- Drive mirrors for the newly activated Common/Social masters are marked pending_sync; GitHub dev remains the rules source of truth.
- Executable 30-fixture regression was not claimed in this connector-only maintenance pass; release promotion still requires the existing regression gate.

## 1.7.0-dev — 2026-09-18
- ARC N° physical order locked to COVER → BLANK_COVER_VERSO → PROBLEM_PAGES → BLANK_BEFORE_ANSWER → ANSWER_KEY.
- Added mandatory ANSWER_KEY_COMPLETE / ANSWER_COUNT_MATCH release gates.
- Added immutable ARC logo registry with Drive IDs, pixel dimensions and SHA-256 hashes.
- Activated COMMON_GENERATION_ENGINE_V4.1 and ARC_PDF_LAYOUT_MASTER_V2.1.
- Activated Generator / Content Bundle / Typesetter contracts V1.1.
- Drive mirror/start docs updated; older active references retained only as superseded history.
- GitHub remains engine/rules source of truth; Google Drive remains school/source/bank/PDF storage.

# CHANGELOG

## 1.6.4-dev — 2026-09-18
- ARC N° physical PDF order is now fixed for duplex printing: cover → one completely blank cover-verso page → problem pages → answer key.
- The cover-verso blank page is a real A4 PDF page with no logo, header, footer, page number, note, watermark, or decoration; the first problem begins on physical page 3.
- ARC N° answer key now has a mandatory page break before it and starts on the immediate physical page after the last problem page, even when space remains on the final problem page.
- No extra blank spacer is inserted between the problem section and answer key.
- Added explicit PDF QC fields for blank-verso presence, first-problem physical page, and answer-key page placement.

## 1.6.3-dev — 2026-09-18
- ARC N° now includes a compact answer-key section at the end of the same student PDF by default; detailed explanations remain disabled.
- Problem pages still prohibit answer exposure.
- Reworked ARC N° cover into a left-aligned Swiss-editorial grid to avoid the previous floating centered composition.
- Locked cover full logos to exact canonical Drive assets for CORE / N° / FINAL.
- Logo retyping/redrawing/regeneration is forbidden; missing logo assets now return BRAND_ASSET_MISSING instead of synthesizing a substitute.
- Canonical ARC N° logo preserves the approved burgundy arc, both endpoint dots, wordmark geometry, divider, and N° label.
- Uploaded canonical full-cover lockup assets into `N제 시스템/00_브랜드/로고·디자인요소`.

## 1.6.2-dev — 2026-09-18
- Hardened ARC self-scoring against score/difficulty inflation after review of Claude KOR batch ARC-CLAUDE-20260918-KOR-01.
- Added ITEM QUALITY V1.2 with EXPLICIT_CUE_RESTATEMENT ceiling, distractor-distance audit, blind rescoring for BANK_A/D4/D5, and zero-rejection/premium-rate audits.
- Added DIFFICULTY ENGINE V1.1 with minimum D4/D5 gates and explicit-cue discount; long passages or the presence of a <보기> no longer count as difficulty by themselves.
- Added KOR high-difficulty gate requiring at least two genuinely competitive distractors and multi-step reasoning for D4/BANK_A.
- Added QA BENCH V1.3 adversarial D4 sentinels and set-level inflation checks.
- Added DRIVE WRITE ADAPTER V1.1 exact-file-ID parent verification. Root-level files may no longer be reported as STORAGE_PLACEMENT=VERIFIED for a subject folder.
- Repaired the reviewed Claude KOR PDF placement by moving its exact PDF FILE_ID into the canonical KOR 완성N제 folder.
- Existing Claude KOR batch remains a v1.5.0 DRAFT_REVIEW artifact; new rules apply to subsequent batches.

## 1.6.1-dev — 2026-09-18
- Added KOR PROTECTED_TEXT_MODE: protected modern literary works remain valid generation sources, but ARC outputs avoid full/long continuous reproduction and use school-source references when full text is required.
- Added STUDENT_SOURCE_REQUIRED / SOURCE_REFERENCE handoff behavior for protected works and prohibited invention of unseen wording or lineation.
- ARC N° problem pages are now strictly COLUMN_ONLY two-column layout.
- Removed ARC N° FULL_WIDTH and temporary one-column fallback for large passages, tables, graphs, maps, timelines, experiment diagrams, and composite visuals.
- Oversized ARC N° assets must be redesigned/split safely at content handoff or returned to Generator; Typesetter may not change layout mode to force fit.
- ARC FINAL and ARC CORE retain flexible layout only where their own active product rules permit it.

## 1.6.0-dev — 2026-09-18
- Split ARC production into dedicated Generator and Typesetter roles to reduce repeated context usage.
- Added ARC_GENERATOR_CONTRACT_V1.0, ARC_CONTENT_BUNDLE_CONTRACT_V1.0, and ARC_TYPESETTER_CONTRACT_V1.0.
- Generators now stop at CONTENT_QA_STATUS=PASS + CONTENT_LOCK=true + HANDOFF_STATUS=READY_FOR_TYPESET.
- Dedicated Typesetter sessions load only the locked bundle, PDF master, brand spec, and necessary layout/visual rules.
- Typesetters do not reload subject textbooks, worksheets, GOLD anchors, or generation QA by default.
- Locked content cannot be silently edited during layout; suspected content defects return via CONTENT_ERROR_FLAG.
- GPT and Claude may each serve as Generator or Typesetter, but one role is used per project/session.
- System maintenance remains exclusive to ChatGPT interactive SYSTEM_MAINTAINER.

## 1.5.0-dev — 2026-09-18
- Established permanent multi-model governance: GPT and Claude are recurring ARC generators; ChatGPT interactive maintenance is the single system/code/rule maintainer.
- Added `ops/ARC_MULTI_MODEL_GOVERNANCE_V1.0.md` with single-writer GitHub rules and append-only Drive production.
- Generator batches now pin ARC_RULESET_VERSION and use unique BATCH_ID metadata.
- GPT/Claude may both produce independent sets without overwriting each other.
- Generators may report SYSTEM_FEEDBACK but cannot patch MASTER/QA/templates/tooling during production.
- Claude absorption is persistent by ruleset version: full absorption on first use or relevant rule change, FAST_REFRESH otherwise.
- Scheduled GPT production is explicitly separated from interactive system maintenance.

## 1.4.7-dev — 2026-09-18
- Added a mandatory Claude/Cowork ARC system-absorption gate before first item generation in a fresh session.
- Claude must read the canonical manifest, common engine, requested subject MASTER/GOLD, QA/source rules, PDF master, brand lockup, and relevant Drive structure before claiming readiness.
- Added explicit user override allowing an independent Claude KOR batch even when a GPT KOR batch exists.
- Added canonical KOR/SOC manuscript, QA, and finished-N° Drive destinations for Claude E2E production.
- Claude-produced PDFs default to DRAFT_REVIEW and are intended for user + ChatGPT post-production review before any ARC rule/template change.

## 1.4.6-dev — 2026-09-18
- Added `ops/ARC_CLAUDE_HANDOFF_V1.0.md` so Claude can generate ARC batches from the same GitHub/Drive source-of-truth without maintaining a separate ARC fork.
- Added required generator attribution and BATCH_ID metadata for GPT/Claude batch coordination.
- Added duplicate-batch avoidance across generators.
- Default multi-model mode is throughput-first: one primary generator per batch, no universal cross-model regrading, selective independent review only for high-risk items.
- Claude starts production first for the current cycle; GPT resumes later by skipping fresh Claude batches.

## 1.4.5-dev — 2026-09-18
- Diagnosed the 18:57 QA failure: root native-Doc creation and read succeeded, but background Drive metadata move was blocked by a safety check.
- Scheduled QA no longer performs Drive parent mutations.
- Added ROOT_STAGING as the scheduled persistence mode: create/write/read at provider root, record intended target folder, and defer folder organization to interactive maintenance.
- The first real RAW shell now doubles as the persistence preflight, eliminating disposable probe overhead.
- RAW generation is checkpointed every 5 items.
- Hourly QA now targets at least one fully QA-complete 20-item subject per run and continues to the next subject only if runtime remains, avoiding fragile 100-item monolithic transactions.
- ROOT_STAGED artifacts count as compute persistence success but are not reported as full storage placement success.

## 1.4.4-dev — 2026-09-18
- Locked the approved ARC master logo/sub-brand system into the template layer.
- ARC wordmark and burgundy arc symbol are now identical across CORE / N° / FINAL.
- Divider geometry, label baseline, spacing, and overall lockup proportions are fixed across all three product variants.
- Product differentiation is restricted to secondary label/divider color: CORE warm gray, N° deep navy, FINAL burgundy.
- N° may receive limited optical glyph compensation while retaining the same label zone.
- Cover volume numbers are separate metadata and no longer distort the ARC N° lockup.
- PDF and CORE template rules now reference ARC_BRAND_LOCKUP_SPEC_V1.0.

## 1.4.3-dev — 2026-09-18
- Added mandatory one-time Drive write preflight before any expensive subject generation.
- Verified OAuth/delegated persistence end-to-end: root native Doc creation → parent read → addParents/removeParents move → content write → destination verification.
- Canonicalized Drive persistence on `ops/ARC_DRIVE_WRITE_ADAPTER_V1.0.md`; the duplicate persistence-policy file is now a deprecated alias.
- Scheduled runtime now defaults to CREATE_THEN_MOVE after a connection-capability mismatch and does not repeatedly retry unsupported direct parent creation.
- QA generation stops before consuming item-generation budget when persistence preflight fails.

## 1.4.2-dev — 2026-09-18
- Diagnosed RUN10 failure as a Drive persistence adapter incompatibility, not an item-QA failure.
- OAuth/delegated native Google Doc creation rejects direct `parent_folder_id` placement on the connected Drive.
- Added ARC_DRIVE_WRITE_ADAPTER_V1.0: create at provider root/default, persist FILE_ID, move with addParents/removeParents, then verify destination.
- Folder-placement failure after durable creation no longer destroys or aborts completed subject work; it becomes MOVE_PENDING with one repair retry.
- Moved RUN10 failure log into the canonical failure folder.
- Verified the new create-then-move path end-to-end with a native Google Doc smoke test in the RUN_LOG folder.
- Scheduled QA should use CREATE_THEN_MOVE by default when connection mode is unknown.

## 1.4.1-dev — 2026-09-18
- Added lightweight SCHOOL_REFERENCE_PROFILE; historical exams remain difficulty/broad-format references only and teacher-style prediction stays disabled.
- Added dormant POST_EXAM_CALIBRATION skeleton for use only after the real exam is available.
- Added GitHub Actions smoke checks for Python syntax, YAML parsing, and exact 30-fixture loading.
- Completed manifest wiring for the executable tooling layer.

## 1.4.0-dev — 2026-09-18
- Added executable tooling layer instead of policy-only checks.
- Added promptfoo regression runner for the 30 frozen fixtures with side-by-side baseline/candidate adapters and decision/score/hard-fail assertions.
- Added sentence-transformers + local Qdrant similarity engine with FULL/STEM/DISTRACTOR embeddings and structural metadata.
- Similarity thresholds now require labeled BANK calibration; raw cosine does not become a hard gate before calibration.
- Added PyMuPDF PDF preflight for page-boundary, margin, overlap, glyph, image/drawing, empty-page and render screening.
- Added Social C-part X-mark detector: PDF annotations → vector diagonal crossings → OpenCV raster fallback.
- Added deterministic visual renderer for graphs, particle models and major social diagrams plus an independent visual PASS B verifier.
- Added mandatory Visual PASS A/B + QUESTION_VISUAL_CROSSCHECK for essential visuals, including REDOX_LEDGER ↔ particle-count cross-check.
- Expanded social visual specification to MAP/STAT/DATA/FLOW/CASEBOX/COMPARE/INSTITUTION with explicit required fields and hard checks.
- Upgraded active visual template/authenticity/anchors and similarity guard to V1.1.
- Added runtime truthfulness rule: connector-only environments must report TOOLING_UNAVAILABLE rather than pretending local tools executed.

## 1.3.4-dev — 2026-09-18
- Added ARC_RUNTIME_PRIORITY_POLICY_V1.0.
- Default subject execution order is now KOR → SOC → SCI → HIS → AI.
- Normal 100-item QA still targets 20 items per subject; priority controls order, retries, extra review, research, and context allocation.
- Added recommended extra-resource weights 30/25/20/15/10.
- Added stage priorities P0–P5 and explicit degradation order: defer P5, then nonessential P4, then nonessential P3; P0–P2 are never skipped.
- Subject failures are isolated, checkpointed, and resumed after the first pass instead of terminating the entire run.
- Default retry budget is one automatic retry per failed subject/stage.

## 1.3.3-dev — 2026-09-18
- Added frozen regression fixture system.
- Registered 30 fixed cases: 5 subjects × GOOD 3 + BAD 3, referenced from the subject GOLD anchor packs.
- Each fixture now has a fixed expected decision, score range/ceiling, and hard-fail expectation.
- Added ARC_REGRESSION_POLICY_V1.0 and upgraded arc-eval-regression to run all fixtures for engine/MASTER/QA/source/bank-rule changes.
- Added QA BENCH V1.2; main promotion now requires REGRESSION_FAIL_COUNT=0.
- Regression fixtures are versioned and cannot be silently rewritten to make a candidate rule pass.

## 1.3.2-dev — 2026-09-18
- Added ARC SOURCE_LEDGER V1.0 and machine-readable schema.
- Source-sensitive claims now carry SOURCE_ID, source role, location, and one of VERIFIED / UNVERIFIED / SOURCE_MISSING.
- PASS B must re-open the original source for ANSWER_BASIS claims; search snippets, filenames, and previous AI summaries cannot establish VERIFIED.
- Added Drive checkpoint folder `92_자동화실행/04_SOURCE_LEDGER`.
- BANK_PASS is blocked when required answer-basis sources are unverified, missing, conflicting, or not reopenable.
- Basic low-risk curriculum definitions do not require source records, avoiding unnecessary ledger overhead.

## 1.3.1-dev — 2026-09-18
- Added mandatory HUMAN_REVIEW_GATE before FINAL release of ARC N°/FINAL/CORE PDFs.
- Human review is intentionally lightweight: scope, Social C X-mark exclusion where applicable, rendered visuals, and answer/final-PDF sanity only.
- AI remains responsible for full answer verification, fact checks, data checks, and render QC before human review.
- Added DRAFT_REVIEW → HUMAN_REVIEW → FINAL_RELEASED state contract.
- Added FAST_HUMAN_REVIEW for exam-period use with high-risk items capped at five.

## 1.3.0-dev — 2026-09-18
- Added fixed GOLD STANDARD anchor system for all five active subjects.
- Each subject now has 3 GOOD + 3 BAD ARC-original example items with expected scores, decisions, and explicit reasons.
- Subject MASTER files now require their GOLD anchor pack during generation and QA.
- Item generator/QA/runtime record nearest GOOD/BAD anchor and apply BAD score ceilings before BANK decisions.
- Anchors calibrate structure, reasoning, distractor realism, and evidence use without expanding scope or copying copyrighted source items.

## 1.2.2-dev — 2026-09-18
- Diagnosed RUN09 scheduled QA failure: run folder created, then execution stopped before first subject artifact write.
- Added checkpointed automation runtime policy with per-subject JIT loading and persist-first behavior.
- Scheduled runs now prefer native Google Docs for RAW/QA/BANK/log artifacts.
- Added ITEM QUALITY V1.1 anti-inflation ceilings and evidence-required scoring.
- Added QA BENCH V1.1 sentinel recheck and score-distribution audit.
- Added BANK POLICY V1.1: pre-V1.1 BANK remains stored but is inactive until V1.1 revalidation.
- Direct recall, weak distractors, generic contexts, and ungrounded style can no longer receive inflated PREMIUM scores.
- Automation failures must preserve partial progress and resume targets instead of reporting success.

## 1.2.1-dev — 2026-09-18
- MCP server registration changed to persistent-by-default.
- Connections remain available when the host supports persistence; actual tool invocation stays on-demand.
- Added startup health checks and automatic reconnect policy.
- Avoids preloading every MCP tool into working context, preserving token efficiency.

## 1.2.0-dev — 2026-09-18
- Added ARC MCP Tool Layer.
- Registered GitHub official MCP, draw.io official MCP, ChemCP, and Timeline Generator MCP.
- GitHub MCP is read-only by default during question-generation runs; write tools are reserved for explicit system maintenance.
- Google Drive remains on the existing connector and third-party Drive MCP is disabled.
- Added MCP security policy, server registry, orchestration, host setup examples, and fallback matrix.
- MCP tools are on-demand only and never override Scope Lock, MASTER, QA, or difficulty rules.

## 1.1.2-dev — 2026-09-18
- Added Reference-First visual protocol: inspect real textbook/school exam/worksheet/workbook visuals before rendering.
- Visuals now extract layout grammar, density, labeling, and print conventions without copying source artwork.
- Added reference-gap and copy-risk gates to visual QA.
- Updated visual anchors priority to include current-range textbook explicitly.

## 1.1.1-dev — 2026-09-18
- Added verified visual skill stack: draw.io base, concept diagrams, chemistry visuals, and timeline visuals.
- Upgraded `arc-visual-renderer` into a router skill.
- Added `ARC_VISUAL_SKILL_STACK_V1.0.md` for subject/type-based routing.

## 1.1.0-dev — 2026-09-18
- Added on-demand ARC skill layer with 13 project-specific skills.
- Added source ingest for PDF/HWP/HWPX/Office-style structured materials.
- Added research grounding and claim-ledger workflow.
- Added item generation, distractor design, factual audit, item naturalness audit, item QA, set editorial, visual rendering, bank curation, regression evaluation, skill orchestration and governance.
- Added `ARC_SKILL_ORCHESTRATION_V1.0.md` and `SKILL_REGISTRY.yaml`.
- Explicitly disabled learner-adaptive wrong-answer regeneration and personal weakness tracking.
- External skill projects are design references only; no upstream scripts/code vendored.

## 1.0.0 — 2026-09-18
- GitHub-first engine architecture initialized.
- `SYSTEM_MANIFEST.yaml` added.
- `main` RELEASE / `dev` development workflow added.
- RUN_LOG JSONL + CSV initialized.
- ARC CORE detailed concept engine included.
- CONCEPT_ID → N° linkage enabled.
- School historical exams restricted to difficulty calibration.
- Teacher-style prediction disabled.
- Freeze mode intentionally not added.
