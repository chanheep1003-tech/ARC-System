# ARC Promptfoo Regression Runner

This directory makes the 30 frozen regression fixtures executable with promptfoo.

## 1. Candidate adapter
Provide one of:

- `ARC_CANDIDATE_CMD`: executable command reading JSON on stdin and returning JSON on stdout.
- `ARC_CANDIDATE_RESULTS_DIR`: directory containing `<FIXTURE_ID>.json` results for offline comparison.

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
