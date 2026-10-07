# archive/

Superseded versions of rule files. Not active, not loaded at runtime, kept for history and explicit replay only.
Paths mirror the original location (`archive/ops/...`, `archive/engine/...`, `archive/quality/...`, `archive/templates/...`, `archive/subjects/...`).

- Active files are resolved only through `SYSTEM_MANIFEST.yaml`.
- Moved on 2026-10-07: every file that was a non-latest version in its family and was not referenced by the manifest, exam registry, tooling, CI, skills, mcp, regression, canary, gold or source registries.
- Left in place (still referenced by `skills/`): `ops/ARC_AUTOMATION_RUNTIME_V1.0.md`, `quality/ARC_ITEM_QUALITY_RUBRIC_V1.1.md`, `quality/ARC_QA_BENCH_V1.2.md`, `quality/ARC_SET_EDITORIAL_ENGINE_V1.0.md`, `quality/ARC_SIMILARITY_GUARD_V1.0.md`, `quality/gold/KOR_GOLD_ANCHORS_V1.0.md`.
- `quality/governance/DEPRECATION_REGISTRY_V1.0.yaml` points at the archived paths.
