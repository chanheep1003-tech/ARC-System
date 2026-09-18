# ARC Executable Tooling Layer

Policy files define what must be true. This directory contains deterministic tools that can actually test or render parts of that policy.

## Install Python tooling
```bash
python -m pip install -r tooling/requirements.txt
```

## Components
- `promptfoo/`: executable 30-fixture regression runner
- `similarity/`: sentence-transformers + local Qdrant similarity engine
- `pdf_qc/`: PyMuPDF PDF preflight + Social C-part X-mark detector
- `visual/`: deterministic visual renderer + independent PASS B verifier

## Trust model
Tool output is evidence, not authority over scope.
User scope, subject MASTER, Source Ledger, QA hard gates, and Human Review remain authoritative.

## Runtime availability
Connector-only scheduled ChatGPT runs may not have a local command runtime. Such runs must record `TOOLING_UNAVAILABLE` rather than pretending these scripts executed.
Local/CI/Work/Codex hosts with Python/Node should run the tooling and persist its reports.
