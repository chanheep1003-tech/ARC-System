# ARC SKILL ORCHESTRATION V1.0

Status: DEV
Purpose: connect ARC's stable generation engines to the on-demand skill and MCP layers without bloating every prompt.

## 1. Authority order
1. User's current explicit scope/exclusion
2. Subject MASTER + ARC Scope Ledger
3. Common Generation Engine / product engine
4. Quality rules and school difficulty bench
5. ARC Skills selected for the current stage
6. MCP tools selected for the current stage
7. External reference material

Skills and MCP tools never override scope.

## 2. Load policy
Read `skills/SKILL_REGISTRY.yaml`, then load only skills required by the task. If a specialized external tool is needed, read `mcp/SERVER_REGISTRY.yaml` and `mcp/MCP_POLICY.yaml`; do not preload all MCP servers.
Scheduled generation additionally follows `ops/ARC_AUTOMATION_RUNTIME_V1.0.md`: per-subject JIT loading, checkpointing, native-Docs persistence, and resume-on-failure.

## 3. N° / FINAL generation route
- Always: `arc-item-generator`, `arc-distractor-engine`, `arc-fact-audit`, `arc-item-naturalness-audit`, `arc-item-qa`, `arc-set-editor`
- QA authority: `ARC_ITEM_QUALITY_RUBRIC_V1.1` + `ARC_QA_BENCH_V1.1`
- Conditional source: `arc-source-ingest` when raw/unparsed files enter; `arc-research-grounding` when external information is needed.
- Conditional visuals: `arc-visual-renderer` first applies `ARC_VISUAL_REFERENCE_FIRST_V1.0`, then selects the ARC visual skill. If a specialized MCP is available, route to draw.io / ChemCP / Timeline MCP according to `mcp/MCP_ORCHESTRATION_V1.0.md`; otherwise use the ARC visual skill fallback.
- Repository context: GitHub official MCP may be used read-only; native GitHub connector remains a fallback.
- Bank: `arc-bank-curator` only for PASS candidates.
- Engine/Master changes: add `arc-eval-regression`.

## 4. Product behavior
### ARC N°
Prioritize high-quality individual items plus set diversity. Student PDF does not expose internal IDs, difficulty labels, skill traces, MCP traces, or QA notes.

### ARC FINAL
Prioritize actual-test flow, mixed difficulty, authentic density, timing plausibility, and final answer-key independence.

### ARC CORE
Skill/MCP layers may assist source ingest, grounding, fact audit, visuals and QA, but no learner-adaptive retry feature is enabled.

## 5. MCP discipline
- MCP is a Tool Layer, not an authority layer.
- Question-generation runtime uses minimum privileges; GitHub is read-only by default.
- Google Drive continues through the existing connector; third-party Drive MCP is disabled.
- MCP failure triggers documented fallback and must not silently expand scope or invent missing source content.
- MCP-produced visuals still require ARC Visual QA.

## 6. Non-goals
- personal weakness modeling
- wrong-answer-based regeneration
- teacher-style prediction from different-teacher historical exams
- scope expansion driven by bank, MCP, or web sources
- autonomous repository mutation during ordinary question generation

## 7. Release rule
Skill/MCP/QA changes live on `dev` until structural validation and representative regression checks pass. Promote to `main` only with zero new hard-fail classes.
