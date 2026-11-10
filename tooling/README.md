# ARC Executable Tooling Layer

Policy files define what must be true. This directory contains deterministic tools that can actually test or render parts of that policy.

## Start here
```bash
python -m pip install -r tooling/requirements-smoke.txt   # light: PyYAML, PyMuPDF, OpenCV
sudo apt-get install -y fonts-nanum fonts-wqy-zenhei       # required by the PDF renderer and canaries
python tooling/arc.py doctor
python tooling/arc.py status
```
`tooling/arc.py` is the single CLI: `doctor`, `status`, `start`, `scope`, `log`, `checksums`, `ci`. `tooling/run_ci_local.py` executes the same steps as `.github/workflows/arc-tooling-smoke.yml`.

E2E canary coverage (synthetic content; validates the pipeline, not model-authored quality):

| | CORE | N | FINAL |
|---|---|---|---|
| KOR | KOR_CORE | KOR_N | KOR_FINAL |
| SOC | SOC_CORE | SOC_N | SOC_FINAL |
| SCI | SCI_CORE | SCI_N | SCI_FINAL |

The real-bundle production pipeline (`tooling/production/`) and renderer (`tooling/typeset/kor_renderer.py`) are still Korean-only; SOC/SCI production bundles go through the canary typesetting path until a subject renderer exists.

## Install full Python tooling (similarity stack)
```bash
python -m pip install -r tooling/requirements.txt
```

## Components
- `promptfoo/`: executable 30-fixture regression runner
- `similarity/`: sentence-transformers + local Qdrant similarity engine
- `pdf_qc/`: PyMuPDF PDF preflight + Social C-part X-mark detector
- `visual/`: deterministic visual renderer + independent PASS B verifier
- `content_qa/`: Universal Independent Solve evidence, option semantics, scope/evidence and actual-difficulty gate

## Trust model
Tool output is evidence, not authority over scope.
User scope, subject MASTER, Source Ledger, QA hard gates, and Human Review remain authoritative.

## Runtime availability
Connector-only scheduled ChatGPT runs may not have a local command runtime. Such runs must record `TOOLING_UNAVAILABLE` rather than pretending these scripts executed.
Local/CI/Work/Codex hosts with Python/Node should run the tooling and persist its reports.
