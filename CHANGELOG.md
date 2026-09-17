# CHANGELOG

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
