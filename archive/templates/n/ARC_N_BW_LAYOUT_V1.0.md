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
- Body (stems, passages, tables, choices, rubrics):
  - **SOC / SCI / ENG / Master**: **HanSantteutDotum Regular / Bold** (`B_R` / `B_B`); **HANDotum** (`G_R`) fallback only for missing glyphs (lazy-embedded and subsetted).
  - **KOR (국어 — 현대국어·중세국어 단일 서체 표준)**: **함초롬돋움 Regular / Bold (`HANDotum.ttf` / `HANDotumB.ttf`)** (`B_R` / `B_B`, `R` / `B`). 현대국어·한자와 중세국어(옛한글 자모 조합 `나랏말ᄊᆞ미`·어두자음군 `ᄠᅳ들`/`ᄡᅳ메`·옛자모 `ㆍ`/`ㅿ`/`ㆁ`/`ㆆ`·방점 `〮`/`〯`·PUA)를 위화감이나 서체 혼용 없이 단일 고딕 패밀리로 조판한다. 제목·문항번호(`G_B`)에 옛한글·방점이 포함되면 해당 어절을 자동으로 `HANDotumB` (`B_B`)로 승격해 방점과 음절 분리를 방지한다(방점 `U+302E`/`U+302F`는 유니코드 결합 순서에 따라 해당 음절 **뒤**에 배치한다).
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

## 6. 별도 해설지 (`*_SOLUTIONS.pdf`) 2단 모던 고딕 표준
- 마스터 해설 샘플: `templates/gold/samples/ARC_N_ALL_IN_ONE_SOLUTIONS_SAMPLE_V1.0.pdf` (`master_sample_p5_solutions.png`).
- **2단 편집 레이아웃**: 문제지와 동일한 A4 2단 그리드(`COL_W`, `0.55pt` `#C2C2C2` 중앙 세로 구분선, `0.7pt` 상단 러닝 헤더, `0.55pt` `#B8B8B8` 하단 푸터선)를 사용한다. `ARC_N`과 `ARC_FINAL` 모두 문제/해설 타이포그래피와 2단 해설 구조를 공유하며, `ARC_FINAL`만 정답표를 별도 파일(`*_ANSWER_KEY.pdf`)로 분리한다.
- **문항별 해설 블록**: `#F1F1F1` 소프트 그레이 헤더 바 + `2.8pt` 좌측 검정 강조선 + 검정 캡슐 문항 배지(`01`, `[서답형 1]`) + `정답 ①` 배지 + `[난이도 · 유형]` 메타 표기를 상단에 배치한다.
- **선지별·채점기준 서술**: 핵심 풀이에 이어 ①~⑤ 각 선지별 정·오답 판별 근거를 내어쓰기(hanging indent)로 정리하며, 서답형 문항은 모범답안과 채점 기준(%)을 제시한다. 헤더에는 반드시 `"정답 및 상세 해설"` 문자열을 포함한다.

## 7. Verification Gate
- Every generated `ARC_N` PDF must pass `tooling/pdf_qc/pdf_preflight.py` (`product="ARC_N"`, `fail_count=0`, `light_body_ratio=0.0`, blank cover verso & answer separator, exact item & key count) and visual comparison against `ARC_N_ALL_IN_ONE_MASTER_SAMPLE_V1.0.pdf`.
- Production renderer changes must also pass `test_layout_and_solutions.py` (`*_SOLUTIONS.pdf` + `ARC_CORE` + `ARC_FINAL`), `test_subject_production.py`, `test_production_pipeline.py`, and `test_semifinal_bundle.py`.
