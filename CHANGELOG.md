# CHANGELOG

## 1.4.0-dev — 2026-09-18
- Added executable tooling layer instead of policy-only checks.
- Added promptfoo regression runner for the 30 frozen fixtures with custom candidate adapter and decision/score/hard-fail assertions.
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
