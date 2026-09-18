# ARC Similarity Engine

## Input item JSONL
Each item should contain:

```json
{
  "item_id": "SCI-001",
  "stem": "...",
  "choices": ["...", "..."],
  "full_text": "...",
  "concept_id": "ARC-SCI-...",
  "question_form": "...",
  "reasoning_form": "...",
  "condition_pattern": "...",
  "answer_path": "...",
  "visual_template": "SCI-GRAPH"
}
```

## Index BANK
```bash
python tooling/similarity/arc_similarity.py index --input bank.jsonl
```

## Query new items
```bash
python tooling/similarity/arc_similarity.py query --input new.jsonl
```

Until thresholds are calibrated, raw cosine scores are advisory and risk is `UNCALIBRATED`.

## Calibrate
Create labeled pair JSONL with `a`, `b`, and `label` in `LOW|MEDIUM|HIGH|DUPLICATE`, then:

```bash
python tooling/similarity/calibrate_similarity.py --pairs labeled_pairs.jsonl
```

Thresholds are model- and BANK-distribution-specific.
