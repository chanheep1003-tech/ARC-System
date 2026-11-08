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


## Item structure gate and calibration (D-22/D-23)

`item_structure_gate.py` checks template codes, structure score bands, scope feasibility and length/absolute-word/answer-position/textbook-copy cues; `difficulty_calibration.py` measures the blind solver's scale against anchor items. Rules: `quality/ARC_ITEM_STRUCTURE_AND_CALIBRATION_V1.0.md`.
