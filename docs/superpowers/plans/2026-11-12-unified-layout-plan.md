# ARC Unified Layout & Multi-Model Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unify ARC_N and ARC_FINAL PDF layout design (Pure B&W N° cover/body, Dongbuk exam-style FINAL header, difficulty-only tags, spacious 4-question target pacing, and separate `*_SOLUTIONS.pdf` booklet) and lock multi-model consistency across Gemini, Claude, and ChatGPT.

**Architecture:** Enhance `tooling/typeset/kor_renderer.py` to support user-space font fallback (`~/.local/share/fonts`), Pure B&W minimalist N° covers, Dongbuk-style FINAL page-3 exam headers, `[D#]` difficulty markers on stems, spacious question spacing, and a dedicated `render_solutions()` PDF generator. Wire `solutions_pdf` into `draft_preview.py` and `production_pipeline.py`, and add `scaffold` subcommand to `tooling/arc.py`.

**Tech Stack:** Python 3, PyMuPDF (`fitz`), PyYAML.

**Spec:** `docs/superpowers/specs/2026-11-12-unified-layout-design.md`

## Global Constraints
- `ARC_N` page order invariant: Cover (p1) → Blank verso (p2) → Problem pages (p3..N) → Blank separator (pN+1) → Quick Answer Key (pN+2).
- `pdf_preflight.py` checks `STUDENT_METADATA_LEAK` and `KOR_QUESTION_MARKER_RE`: difficulty display on student pages must not trigger `STUDENT_METADATA_LEAK` and must preserve `01` / `1.` question number extraction.
- All existing CI tests (`python tooling/run_ci_local.py`) must pass with 0 failures.

---

### Task 1: User-Space Font Resolution (`arc.py`, `kor_renderer.py`, `install.sh`)
- [ ] Update font lookup in `tooling/typeset/kor_renderer.py` and `tooling/arc.py` to check `/usr/share/fonts/truetype/nanum` first, then `~/.local/share/fonts/nanum` (and `~/.local/share/fonts/arc-fallback/NotoSerifKR.ttf`).
- [ ] Update `tools/oss/install.sh` so non-root environments install Python deps with `--user --break-system-packages` and download Nanum/Noto fonts into `~/.local/share/fonts/`.

### Task 2: Upgraded Layout & Solutions Booklet PDF in `kor_renderer.py`
- [ ] Write failing test in `tooling/production/test_layout_and_solutions.py` verifying:
  1. Pure B&W `ARC_N` cover with title, school name, and no passage list clutter.
  2. `ARC_FINAL` first problem page includes Dongbuk High School exam banner (`동북고등학교`, `기말고사`).
  3. Separate `*_SOLUTIONS.pdf` is generated and contains per-option explanations (`①`..`⑤`) and difficulty tags.
- [ ] Implement in `tooling/typeset/kor_renderer.py`, `tooling/production/draft_preview.py`, and `tooling/production/production_pipeline.py`.
- [ ] Verify test passes and existing `test_production_pipeline.py` and `test_subject_production.py` remain green.

### Task 3: Multi-Model Bundle Scaffolder (`arc.py scaffold`) & Universal Entry Sync
- [ ] Add `scaffold` command to `tooling/arc.py` that creates a canonical `items.yaml` template with plan metadata, archetype slots, and 5-option judgment skeletons.
- [ ] Add `GEMINI.md` and update `AGENTS.md` with the strict multi-model consistency rule.
- [ ] Run `python tooling/arc.py checksums` and `python tooling/run_ci_local.py`.
