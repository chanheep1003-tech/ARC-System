# ARC single entry point
Start with ops/ARC_RUNBOOK.md. Use tooling/workflow/arc_workflow.py for one request and one resumable state when a local runtime is available; connector-only hosts follow the same JSON contract without claiming CLI execution.
# ARC expert team entry point
Read SYSTEM_MANIFEST.yaml at one pinned commit, then agents/TEAM.md and the assigned role file. Resolve active subject/engine/QA paths from that manifest instead of guessing the newest filename. Current explicit user instructions take precedence.
Production reads GitHub rules and Drive sources. Work on a maintenance branch for system changes. PR #6 is a separate unmerged candidate, not an active ruleset.
No file creates a running agent by itself. Actual delegation needs a supported host or API adapter. Otherwise use verified file handoffs and record WAITING_FOR_WORKER. Never claim a cross-provider call that did not happen.

## KOR 2026-11-05 correction patch
When reviewing KOR N° spelling/medieval corpora, additionally read quality/korean/ARC_KOR_NORM_20261105_CORRECTION_POLICY.md. A negative stem requires exactly one FALSE answer. Static PDF PASS does not confer content lock; preserve original source, pending patches and review receipts separately.
