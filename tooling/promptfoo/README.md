# ARC Promptfoo Regression Runner

This directory makes the 30 frozen regression fixtures executable with promptfoo.

## 1. Candidate adapter
Promptfoo runs two providers over the same frozen fixture set.

Baseline:
- `ARC_BASELINE_CMD` or
- `ARC_BASELINE_RESULTS_DIR`

Candidate:
- `ARC_CANDIDATE_CMD` or
- `ARC_CANDIDATE_RESULTS_DIR`

Each command reads JSON on stdin and returns JSON on stdout. Result directories contain `<FIXTURE_ID>.json` files.

Candidate result schema:

```json
{
  "decision": "BANK_A",
  "item_score": 94,
  "hard_fail": false,
  "reasons": ["..."]
}
```

## 2. Run
From this directory:

```bash
python -m pip install -r ../requirements.txt
npx promptfoo@latest eval -c promptfooconfig.yaml -o ../results/promptfoo-regression.json
```

The runner loads `REGRESSION_FIXTURES_V1.0.yaml`, resolves the referenced GOLD anchor text, and applies frozen expected-decision/score/hard-fail assertions.

Do not edit fixture expectations to make a candidate pass.


The promptfoo matrix therefore shows baseline and candidate side by side under identical frozen expectations.
