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
When a needed capability is not sufficiently covered by the current ARC skill registry, the maintainer may search public GitHub skills and apply `skills/ARC_EXTERNAL_SKILL_INTAKE_POLICY_V1.0.md`. External skills remain below ARC authority and are loaded/adapted only on demand.

## 2. Load policy
Read `skills/SKILL_REGISTRY.yaml`, then load only skills required by the task. If a specialized external tool is needed, read `mcp/SERVER_REGISTRY.yaml` and `mcp/MCP_POLICY.yaml`; do not preload all MCP servers.
Scheduled generation additionally follows `ops/ARC_AUTOMATION_RUNTIME_V1.0.md`, `ops/ARC_DRIVE_WRITE_ADAPTER_V1.0.md`, and `ops/ARC_RUNTIME_PRIORITY_POLICY_V1.0.md`: write preflight, connection-aware native-Docs persistence, per-subject JIT loading, checkpointing, subject priority, resource budgeting, and resume-on-failure.
For N°/FINAL generation and item QA, the subject-specific `quality/gold/*_GOLD_ANCHORS_V1.0.md` is a required JIT input.
When a claim is source-sensitive, `quality/ARC_SOURCE_LEDGER_V1.0.md` is also mandatory.

## 3. N° / FINAL generation route
- Always: `arc-item-generator`, `arc-distractor-engine`, `arc-fact-audit`, `arc-item-naturalness-audit`, `arc-item-qa`, `arc-set-editor`
- QA authority: `ARC_ITEM_QUALITY_RUBRIC_V1.1` + `ARC_QA_BENCH_V1.2` + subject GOLD anchor pack + active executable-tool policies
- Conditional source: `arc-source-ingest` when raw/unparsed files enter; `arc-research-grounding` when external information is needed.
- Conditional visuals: `arc-visual-renderer` applies Reference-First → VISUAL_SPEC → deterministic renderer when supported → Visual PASS A/B → authenticity rubric. Unsupported deterministic types route to specialized visual skills. If a specialized MCP is available, route to draw.io / ChemCP / Timeline MCP according to `mcp/MCP_ORCHESTRATION_V1.0.md`; otherwise use the ARC visual skill fallback.
- Repository context: GitHub official MCP may be used read-only; native GitHub connector remains a fallback.
- Gold calibration: compare every candidate to nearest GOOD/BAD anchor before final QA score.
- Source verification: SOURCE_REQUIRED claims receive SOURCE_ID and PASS B re-opens the original source before BANK_PASS.
- Similarity: local/CI host가 지원하면 sentence-transformers + local Qdrant quantitative layer를 실행한다. CALIBRATION_REQUIRED면 raw score는 advisory.
- PDF release: PyMuPDF preflight를 실행 가능한 host에서 수행하고 결과를 Human Review에 전달한다.
- Social C: X-mark detector를 실행 가능한 host에서 먼저 사용하고 ambiguous region은 HUMAN_CHECK로 보류한다.
- Bank: `arc-bank-curator` only for PASS candidates.
- Engine/Master/QA/source/bank-rule changes: add `arc-eval-regression` and run all 30 frozen fixtures before promotion.

## 4. Product behavior
### ARC N°
Prioritize high-quality individual items plus set diversity. Student PDF does not expose internal IDs, difficulty labels, skill traces, MCP traces, or QA notes.

### ARC FINAL
Prioritize actual-test flow, mixed difficulty, authentic density, timing plausibility, and final answer-key independence.

### ARC CORE
Required JIT stack:
- manifest-selected ARC CORE content engine
- ARC CORE depth engine
- ARC CORE editorial-naturalness policy
- ARC CORE QA bench
- active subject MASTER for scope/source/factual constraints
- current-range source materials

Skill/MCP layers may assist source ingest, grounding, fact audit, visuals and QA, but no learner-adaptive retry feature is enabled.
Do not load N° distractor/answer-position/set-editor skills for a pure CORE task.
For document editorial structure, source extraction, typography/PDF QA, and skill-design gaps, vetted external GitHub skills may be used as REFERENCE_ONLY or ADAPT inputs under the external-skill intake policy.

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

## 7. Executable tooling truthfulness
실행기가 없는 connector-only runtime에서는 TOOLING_UNAVAILABLE을 기록한다.
promptfoo / local Qdrant / PyMuPDF preflight / OpenCV X-detection / deterministic visual verifier를 실제 실행하지 않고 PASS했다고 주장하지 않는다.

## 8. Runtime priority
Default subject order is KOR → SOC → SCI → HIS → AI.
Normal 100-item runs keep 20 items per subject; priority changes processing order and extra resource allocation, not required item count.
P0–P2 are non-skippable. Under resource pressure defer P5, then nonessential P4, then nonessential P3.

## 9. Release rule
Skill/MCP/QA changes live on `dev` until structural validation and representative regression checks pass. Promote to `main` only with zero new hard-fail classes.
