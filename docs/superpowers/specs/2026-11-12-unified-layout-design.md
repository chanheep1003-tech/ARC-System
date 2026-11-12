# ARC Unified Layout & Multi-Model Consistency Design Spec

**Date:** 2026-11-12
**Status:** Approved

## 1. Intent & Why
Eliminate formatting and item-structure divergence when dispatching tasks across Gemini, Claude, and ChatGPT. All models must author only canonical `items.yaml` bundles (via `arc.py scaffold`), and all PDFs must be rendered exclusively through `tooling/typeset/kor_renderer.py`.

## 2. Design Decisions (User-Approved)
1. **Font Resolution in Non-Root Environments:**
   - `tooling/typeset/kor_renderer.py`, `tooling/arc.py`, and `tooling/canary/canary_fonts.py` resolve Nanum fonts and CJK fallback fonts from both `/usr/share/fonts/...` and `~/.local/share/fonts/...` so cloud VMs without `sudo` render identical Korean PDFs.
2. **ARC N° Layout (Pure B&W, Simple & Spacious):**
   - **Cover:** Pure black & white (`#000000`). Top logo (if provided), bold `set_label` & `course` title, `cover_subtitle`, clean horizontal rule, and bottom `school_line` (`동북고등학교`). No cluttered passage-title lists on the cover.
   - **Body:** Two-column B&W layout. Spacious pacing targeting ~2 questions per column (4 per page) when items are standard length, while smoothly flowing across columns/pages when passages or `<보기>` boxes are long.
   - **Question Header:** Displays difficulty badge (`[D3]`) cleanly beside the question stem/number without bulky metadata boxes.
   - **Quick Answer Key:** Placed at the end of the student PDF (after the mandatory blank separator page) as a clean number + answer grid.
3. **ARC FINAL Layout (Dongbuk High School Actual Exam Style):**
   - **First Problem Page Banner:** Authentic Dongbuk High School exam header block (`2026학년도 2학기 기말고사`, course title, info table with 과목코드 / 문항수 / 배점 안내, and double top rule) above the two-column exam body.
   - **Question Header:** Exam numbering (`1.`, `[서답형 1]`) with points (`(3.8점)`) and difficulty tag (`[D3]`).
   - **Answer Key:** Separated into `*_ANSWER_KEY.pdf`.
4. **Separate Detailed Solutions Booklet (`*_SOLUTIONS.pdf`):**
   - Both `draft_preview.py` and `production_pipeline.py` automatically generate `<BATCH_ID>_SOLUTIONS.pdf` alongside the student PDF.
   - Contains: Question number, correct answer, difficulty & task family/archetype, per-option (`①`–`⑤`) truth verdict and explanation (`why`), attractive distractor (`2순위`) tag, and constructed-response (`CR`) model answer + grading rubric.
5. **Multi-Model Consistency (`arc.py scaffold` & Entry Rules):**
   - Add `python tooling/arc.py scaffold --subject <KOR|SOC|SCI> --product <ARC_N|ARC_FINAL> --scope "..." --out <dir>` to generate a ready-to-fill `items.yaml` skeleton with registered archetypes and 5-option judgment slots.
   - Sync `GEMINI.md` and `AGENTS.md` so Gemini, Claude, and ChatGPT follow the exact same CLI-first workflow.
