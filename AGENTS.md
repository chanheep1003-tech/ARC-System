# ARC single entry point
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

## 2026-11-07 사용자 확정 기준 (충돌 시 우선)

`quality/korean/ARC_KOR_V1_V6_USER_CLARIFICATION_20261107.md`를 함께 읽는다. V1은 교과서 중심 전체 범위의 고른 출제, V2는 중요 부분 집중과 추론 강화, V3는 문법·문학·비문학의 다양한 새 지문, V4는 동북고 실제 시험의 상위 변별 수준까지, V5는 지정 범위 전체의 실제 시험 한 회, V6는 지정 범위 내 모든 문법 영역에 적용하는 낯선 표현 노출·판단 훈련이다. V6의 개별 어휘 뜻·품사·발음을 먼저 알려 주는 것은 필수 조건이 아니다. 기존 100문항/65문항/30문항 고정 배분은 폐기하고 요청별 범위에 맞게 배분한다.
