# ARC Deterministic Visual Tooling

## Supported directly
- SCI-GRAPH
- SCI-PARTICLE
- SCI-PROCESS
- SOC-DATA / SOC-STAT
- SOC-FLOW
- SOC-INSTITUTION
- SOC-COMPARE
- SOC-CASEBOX
- SOC-MAP with explicit verified vector regions

Other types route to draw.io, ChemCP, or timeline tooling according to policy.

## Render
```bash
python tooling/visual/arc_visual_render.py \
  --spec visual.yaml \
  --out visual.svg \
  --manifest visual.render.json
```

## Independent PASS B
```bash
python tooling/visual/visual_verify.py \
  --spec visual.yaml \
  --manifest visual.render.json \
  --asset visual.svg \
  --report visual.verify.json
```

Optional `--question-check` accepts a JSON file containing the question-side expected visual data/counts. This enables QUESTION_VISUAL_CROSSCHECK.

For redox particle models, generate the question-check data from the independently verified REDOX_LEDGER, not from the renderer output.
