# ARC production pipeline

One bundle directory → every gate → PDF. Nothing is self-reported.

```
python tooling/production/production_pipeline.py <bundle_dir> --output-dir <out>
```

`<bundle_dir>` contains:

- `items.yaml`: set metadata, `passages` (each a `source_text_id` from
  `quality/source/KOR_SOURCE_TEXT_REGISTRY_2026_V1.0.yaml`, plus display-only
  `marks` that may add ⓐ/㉠ but never change a word), and items. Each item has
  its stem, options, answer, author second-best, per-option `judgments`
  (`v` statement truth, `c` competitiveness, `axis`, `claim`, `ev` = `P#S#`
  sentence refs, `why`), `family`, `balance`
  (CORE_EXAM_POINT / ADVANCED_DISCRIMINATION), `difficulty`,
  `reasoning_steps` and `immediate_elimination`.
- `blind_review.yaml`: output of an independent solver that saw only
  `student_manuscript.md`. For each item it records the answer, first-pass
  top-3, second-best, difficulty and flags a–e. Item `difficulty` must equal
  the blind difficulty; range estimates resolve to the lower bound.

What the pipeline computes and enforces:

- Source: registry lookup, SHA-256 verification, paragraph count, and a check
  that marks never change a word.
- Blind solve: every key must match the blind answer. Flags a/b/d block. Flag
  c blocks on D3+ items and only warns on core items.
- Answer-length cue: a key that is uniquely longest at ≥1.25× the median.
  Longest-option-is-key rate must be ≤ 0.30.
- Stem forms: "가장 적절한 것은?" ≤ 40%, "적절하지 않은" ≤ 20%, and the same
  stem ending may not run more than 2 items in a row.
- Answer positions: each position ≤ 30%, and no 3 identical keys in a row.
- Student-text leak: internal QA vocabulary. AI-style phrases.
- Strong distractors on D3+: an option counts if the author rated it STRONG or
  it appears in the blind solver's first-pass top-3.
- KOR ARC_N balance: D1 ≤ 10%, D4+D5 15–35%, ADVANCED 20–30%. Per-level bands
  only warn.
- QA evidence: PASS B comes from the blind review, and item/set gates are
  mapped from the failure codes. Then content QA, handoff serializer and
  preflight, typesetter admission, Korean renderer (`tooling/typeset/kor_renderer.py`)
  and PDF preflight.
- ARC_FINAL: the FINAL quality profile is built from the bundle and blind
  review and run through `final_quality_gate.py`. The answer key is written to
  a separate PDF.

The report status is `READY_FOR_USER_APPROVAL` or `BLOCKED`. Governance stays
`FINAL_USER_APPROVAL=PENDING` and `DRIVE_SAVE=BLOCKED` until the user approves
the exact artifact.


## Exam context admission (2026-10-03)
Normal production requires a current exam_context bound to the registered profile hash; pending scope is blocked before source loading and rendering. See tooling/exams/README.md. Archived bundles and synthetic canaries use --archived-replay explicitly; they remain release-blocked even when a diagnostic PDF is rendered. A failed normal Typesetter admission never renders a PDF.


## SOC / SCI bundles (2026-11-10)
SOC and SCI use this same pipeline and the same renderer as KOR. `subject: SOC|SCI` changes only what the content model allows; the page model, numbering, cover, ARC_N inline key and ARC_FINAL separate key PDF are identical.

What a SOC/SCI `items.yaml` may contain in addition to the KOR fields:

- **Standalone items**: omit `set`/`passage`. Items print in bundle order; a set's material prints once, before its first item.
- **Material sets**: `sets: [{id, prompt, works: [{material: {origin, paragraphs, title?, source_ref?, table?}, figure?}]}]`. `origin` is `GENERATED`, `SCHOOL_SOURCE` or `PUBLIC_DATA`; the last two require `source_ref`. `prompt` replaces the default "다음 글을 읽고 물음에 답하시오." KOR bundles are refused (`MATERIAL_FORBIDDEN_FOR_SUBJECT`): Korean passages must stay registry-locked raw text.
- **Figures**: `figure: {path, sha256, caption, width?}` on an item or a material work. `path` is inside the bundle directory; the bytes must match `sha256` or nothing is rendered. `caption` is the text description that goes to the blind solver in the manuscript. Render figures deterministically (`tooling/visual/arc_visual_render.py` or an equivalent script) and keep the PNG in the bundle.
- **Tables / <보기>**: `table: {header, rows, weights?}` and `view: [...]`, as for KOR.
- **Ion and formula notation**: write Unicode super/subscripts (`A²⁺`, `CO₂`); the renderer draws them as raised/lowered body-font glyphs.
- **Evidence refs** (`ev`): `P#S#` for sentences of the item's material set, or item-local `STEM`, `VIEW`, `TABLE`, `FIGURE`, `OPTION1`–`OPTION5`, `SCOPE:<id>`. Every option needs at least one.
- **Scope refs**: `scope_refs` on the bundle or the item states where the content sits in the confirmed range (worksheet/textbook location). Missing refs fail `SCOPE_REF_MISSING`.
- **Task families**: the shared school families plus subject families (`DATA_INTERPRETATION`, `GRAPH_READING`, `EXPERIMENT_ANALYSIS`, `RIGHTS_CONFLICT`, …; see `SUBJECT_FAMILIES`).
- **Balance**: SOC/SCI ARC_N enforce only the universal ADVANCED 20–30% target; no per-level band is registered for them.

Report gate names carry the subject (`SCI_EXAM_REALISM_GATE`, `SOC_SCHOOL_TASK_FAMILY_GATE`, …); KOR keeps `KOR_*`.

Fixtures `quality/production/SCI_N_REDOX_SAMPLE_20261110` and `SOC_FINAL_SAMPLE_20261110` are synthetic layout/gate regressions (`tooling/production/test_subject_production.py`). Their blind review is derived from the key and marked `synthetic`; they run only as archived replay and are not publishable content.

ARC_CORE for all three subjects goes through the handoff → typesetter gateway → CORE layout path covered by the CORE canaries; this pipeline is ARC_N / ARC_FINAL only.
