# ARC SKILL ORCHESTRATION V1.0

Status: DEV
Purpose: connect ARC's stable generation engines to the on-demand skill layer without bloating every prompt.

## 1. Authority order
1. User's current explicit scope/exclusion
2. Subject MASTER + ARC Scope Ledger
3. Common Generation Engine / product engine
4. Quality rules and school difficulty bench
5. ARC Skills selected for the current stage
6. External reference material

Skills never override scope.

## 2. Load policy
Read `skills/SKILL_REGISTRY.yaml`, then load only skills required by the task. Do not preload all skill bodies.

## 3. N° / FINAL generation route
- Always: `arc-item-generator`, `arc-distractor-engine`, `arc-fact-audit`, `arc-item-naturalness-audit`, `arc-item-qa`, `arc-set-editor`
- Conditional: `arc-source-ingest` when raw/unparsed files enter; `arc-research-grounding` when external information is needed; `arc-visual-renderer` when the item needs a functional asset. Visual routing first applies `ARC_VISUAL_REFERENCE_FIRST_V1.0`, then chooses among `arc-visual-drawio-base`, `arc-visual-concept-diagrams`, `arc-visual-chem`, and `arc-visual-timeline`; `arc-bank-curator` only for PASS candidates.
- Engine/Master changes: add `arc-eval-regression`.

## 4. Product behavior
### ARC N°
Prioritize high-quality individual items plus set diversity. Student PDF does not expose internal IDs, difficulty labels, skill traces, or QA notes.

### ARC FINAL
Prioritize actual-test flow, mixed difficulty, authentic density, timing plausibility, and final answer-key independence.

### ARC CORE
This skill layer may assist source ingest, grounding, fact audit, visuals and QA, but no learner-adaptive retry feature is enabled.

## 5. Non-goals
- personal weakness modeling
- wrong-answer-based regeneration
- teacher-style prediction from different-teacher historical exams
- scope expansion driven by bank or web sources

## 6. Release rule
Skill changes live on `dev` until structural validation and representative regression checks pass. Promote to `main` only with zero new hard-fail classes.
