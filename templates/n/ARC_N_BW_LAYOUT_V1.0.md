# ARC N° Fixed Master Layout Specification V2.0 (Canva Editorial Pure B&W Gothic Standard)
Date: 2026-11-14. Approved user master (`Canva DAHaz5b2kK0` + reduced item numbering) supersedes all prior Serif/tag-bar/9.1pt specs for `ARC_N`.
Visual & binary ground truth:
- Master All-in-One Sample: `templates/gold/samples/ARC_N_ALL_IN_ONE_MASTER_SAMPLE_V1.0.pdf` (`master_sample_p1_cover.png`, `master_sample_p2_body_passage.png`, `master_sample_p3_body_data_cr.png`, `master_sample_p4_answer_key.png`)
- Canonical Subject Samples: `templates/gold/samples/subjects/ARC_N_SAMPLE_{KOR,SOC,SCI,ENG}_V1.0.pdf`
- Deterministic Reference Renderer: `tooling/typeset/build_arc_n_master_sample.py` (`CanvaFontKit`, specs in `tooling/typeset/subject_sample_specs.py`)

## 1. Color System — 100% Pure B&W Monochrome
- Zero chromatic fills, strokes, badges, shadows, or accents anywhere on `ARC_N` pages.
- Fixed palette: Black `#000000`, Dark Body `#1F1F1F`, Secondary/Mid-Gray `#737373`, Column Gutter Grid `#C2C2C2` (`CANVA_GRID_GRAY`), Cell/Splitter Rule `#B8B8B8`, Notice Card `#F1F1F1` (`CANVA_BG_NOTICE`), Table Header `#E4E4E4` (`CANVA_BG_TH`), Paper `#FFFFFF`.
- Cover brand lockup uses desaturated monochrome asset (`templates/brand/assets/ARC_N_LOCKUP_MASTER.png` converted to grayscale / `ARC_N_LOCKUP_MASTER_BW.png`).

## 2. Physical Page Sequence & Isolation
- Mandatory order: `Page 1 Cover` -> `Page 2 Blank Verso (0 objects)` -> `2-Column Problem Body Pages (2 items per column max; vertical divider x=297.64pt)` -> `Blank Separator Page (0 objects before answer key)` -> `Quick Answer Key Page` (solutions remain in a separate booklet).
- `ARC_CORE` and `ARC_FINAL` retain their independent layouts; this rule applies strictly to `ARC_N`.

## 3. Unified Modern Gothic Typography (`CanvaFontKit`)
- Header, Question Numbers, `<보기>`/`<조건>` box headers, badge labels: **KoPub Dotum Bold** (`G_B`).
- Body (stems, passages, tables, choices, rubrics): **HanSantteutDotum Regular / Bold** (`B_R` / `B_B`); **HANDotum** (`G_R`) fallback only for missing Unicode/superscript/subscript/symbol/Hanja glyphs (lazy-embedded and subsetted).
- Never use `NotoSansKR-VF` (variable font registers as Thin weight and fails light-body preflight).
- Fixed Type Scale:
  - Running header: `8.4pt` Bold (`#1F1F1F`) + `0.7pt` black bottom rule (`y=46.5`).
  - Footer: `7.8pt` Regular left label (`#737373`) + `8.2pt` centered physical page number, top rule `0.55pt` (`#B8B8B8`, `y=792`).
  - **Question Numbers (reduced finalized size)**: `01~N` at **`13.2pt` Bold** (left hanging indent `23.0pt` in passage pages; stacked above stem in data/CR pages); **`[서답형 1]` at `11.6pt` Bold** stacked.
  - Stems: `8.8pt` Bold hanging (`lh 12.4pt`) or `8.7pt` Regular stacked (`lh 12.2pt`); passage body `8.0~8.1pt` (`lh 11.5~11.7pt`); choices `7.95~8.15pt` (`lh 11.1~11.5pt`).

## 4. Tag-Free 2-Column Grid & Cover Specification
- Body page size: A4 (`595.28 × 841.89 pt`), horizontal margins `12.8mm` (`36.3pt`), column width `250.3pt`, center divider `0.55pt` `#C2C2C2`, top/bottom horizontal splitter `0.55pt` `#B8B8B8`.
- **Zero Tag Bars**: Do not print black pill/tag-bar strips (`q-tagbar`), point values, or difficulty tags above or inside student questions.
- **Cover (`p1`)**:
  - Top bar (`y=38`) + single `0.75pt` black hairline; `4.5pt` left black vertical bar beside 3-line Gothic hero title (`23.5 / 23.5 / 21.5pt`); solid black pill + outlined pill directly **below** the hero title; borderless `#F1F1F1` `"일러두기 | ..."` notice card (`126pt` content start, zero orphan line-wraps); white-header Booktabs overview table (`0.45pt` row rules, `1.15pt` top/bottom); subtitle line; 4-column architectural footer grid (`A4 PORTRAIT` | `01-06 + 서답형 1` | `VERSION 1.0` | monochrome `ARC N°` lockup).

## 5. Passages, `<보 기>` / `<조 건>`, Tables, Diagrams & CR Answer Area
- **Common Passage Frame**: Title placed **outside** the box (`[01~02] ...`, `8.8pt` Bold); box uses `1.6pt` top black bar and `0.5pt` left/right/bottom hairline.
- **Material / Condition Boxes (`< 보 기 >` / `< 조 건 >`)**:
  - **Pill-tab (`_draw_pilltab_box`)**: Centered solid black tab straddling the top rule (standard prose/criterion `< 보 기 >`).
  - **Knockout (`_draw_knockout_box`)**: White knockout label centered on top hairline (compact statement sets such as ㄱ·ㄴ·ㄷ).
  - **Full-bar (`_draw_fullbar_box`)**: Full-width `16.0pt` solid black header bar with centered white label (deep/advanced `06` `< 보 기 >` and `[서답형 1]` `< 조 건 >`).
- **Tables & Vector Diagrams**: Data tables use `#E4E4E4` header fill with `1.0pt` outer horizontal rules and `0.4pt` gray cell gridlines. Diagrams distinguish series purely via stroke style and marker fill (`solid + ●` vs `dashed + □`).
- **Choices**: 5 choices stacked vertically with hanging indent, or 3-column grid (`grid3`) for ultra-short items.
- **Constructed Response (`[서답형 N]`)**: Open `답:` label followed by gray horizontal writing rules (`16.5pt` spacing, no closed border box).
- **Quick Answer Key (`p6`)**: 5-column Booktabs grid (`01~05` .. `21~25`) + borderless `#F1F1F1` CR model answer & rubric card with `3.0pt` solid black left accent bar.

## 6. Verification Gate
- Every generated `ARC_N` PDF must pass `tooling/pdf_qc/pdf_preflight.py` (`product="ARC_N"`, `fail_count=0`, `light_body_ratio=0.0`, blank cover verso & answer separator, exact item & key count) and visual comparison against `ARC_N_ALL_IN_ONE_MASTER_SAMPLE_V1.0.pdf`.
