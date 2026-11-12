# ARC single entry point
**Read `ARC_MAP.md` first.** It is the map of this repository: what lives where, the product/version table, and the rule that every production request starts with a plan card (`python tooling/arc.py plan …`) before any item is written. Build items from registered school archetypes (`quality/ARC_SCHOOL_ARCHETYPE_GATE_V1.0.md`), one unit set at a time.
First command on any host with a shell: `python tooling/arc.py doctor && python tooling/arc.py status`. `status` prints the KOR/SOC/SCI × CORE/N/FINAL matrix with the exact blocker per cell. `python tooling/arc.py start --subject … --product … --count … --scope …` creates the request/state and lists the manifest-selected files to read, in order. After editing any tracked file run `python tooling/arc.py checksums`; before pushing run `python tooling/arc.py ci`.
Start with ops/ARC_RUNBOOK.md. Use tooling/workflow/arc_workflow.py for one request and one resumable state when a local runtime is available; connector-only hosts follow the same JSON contract without claiming CLI execution.
# ARC expert team entry point
Read SYSTEM_MANIFEST.yaml at one pinned commit, then agents/TEAM.md and the assigned role file. Resolve active subject/engine/QA paths from that manifest instead of guessing the newest filename. Current explicit user instructions take precedence.
Production reads GitHub rules and Drive sources. Work on a maintenance branch for system changes. PR #6 is a separate unmerged candidate, not an active ruleset.
No file creates a running agent by itself. Actual delegation needs a supported host or API adapter. Otherwise use verified file handoffs and record WAITING_FOR_WORKER. Never claim a cross-provider call that did not happen.

## KOR 2026-11-05 correction patch
When reviewing KOR N° spelling/medieval corpora, additionally read quality/korean/ARC_KOR_NORM_20261105_CORRECTION_POLICY.md. A negative stem requires exactly one FALSE answer. Static PDF PASS does not confer content lock; preserve original source, pending patches and review receipts separately.


## KOR-only V1–V6 learning levels (corrected 2026-11-06)
For subject=KOR ONLY, load quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md, verified exam inventory and quality/korean/ARC_KOR_DYNAMIC_SOURCE_SELECTION_V1.0.yaml (NO preselected source titles). Other subjects do not inherit this ladder. Korean V3 unseen materials vary by genre: literature compares a new literary text, nonfiction explains and compares new concepts, grammar uses authentic new examples (including song lyrics, poems and fiction when licensing allows). V1–V4=ARC_N, V5=ARC_FINAL, V6=ARC_N specialist. Unverified source text or licensing remains BLOCKED.

## KOR V6 emergency specialist (2026-11-06)
NEW KOR policy is `quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md`; treat old V1–V5 document as archived. For modern Korean orthography V6, read `quality/korean/ARC_KOR_V6_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY_V1.0.md`. ARC N° V6 chooses unfamiliar lexemes/idioms/sentences per item after locking the target grammar rule; distinguishes POS vs dictionary fact vs formal rule, and requires key-blind independent solving, all-option truth audits, novelty/rights receipts. V5 remains ARC FINAL. This applies to KOR only; SCI/SOC unaffected. NEVER claim 100-question V6 produced from policy existence.

## KOR Middle Korean module + false-difficulty gate (registered 2026-11-10)
Only when the user explicitly requests Middle Korean scope, load `runtime.korean_middle_korean_policy` and its regression file. For all subjects load `active.quality.false_difficulty_gate` together with the item quality rubric. Never patch a rule into a file the manifest no longer selects (e.g. `*_V4.0`, `*_V1.0` superseded versions): add a new registered file or a new version and update SYSTEM_MANIFEST.yaml.
