# System maintainer
Read arc-skill-governance and arc-eval-regression. Work in a dedicated branch from verified dev HEAD; keep production generation read-only on GitHub. Diagnose a concrete defect, make minimal change, update provenance/checksums/version where required and run applicable regression. Record baseline vs candidate evidence and unavailable tests. No main promotion without release gates. Do not change fixture expected outcomes to fit candidate results, or interpret static CI as model quality evaluation. Multiple providers share one ruleset; do not create model-specific engine forks.

## KOR regression maintenance (2026-11-05)
Maintain rule-subclause, negative-stem multi-false, wrong pronunciation, and stale cover-index regressions. Run existing tooling/content_qa/test_content_qa_gate.py and new tooling/content_qa/korean_norm_regression_gate.py when runtime is available; static PASS_STATIC_ONLY does not certify 600 item semantics. Do not forge CI receipts or edit gold answers to make tests green.

## 국어 장르별 새 지문 회귀 방지 — 2026-11-06
KOR에만 V1~V5 정책을 적용한다. CI/수동 QA에 두 가지 경고 추가: ① SCI/SOC에 quality/korean/ARC_KOR_V1_V5_LEVEL_POLICY_V1.1.md 자동 라우팅 금지 ② 노랫말/시/소설의 실제 발췌 텍스트가 미승인인데 PDF/GitHub에 장문 포함 시 HARD_FAIL. V3 새 지문 제거 후 동일 정답이 유지되어 문항풀이에 문맥이 불필요하면 DECORATIVE_PASSAGE로 반려. 기출 2025·2026 유형에 맞추되 '가사 빈도' 같은 확인 안 된 수치를 허위 근거로 기재하면 FAIL_PROVENANCE.
## 2026-11-06 maintainer update
Reject config with fixed preselected titles or hardcoded candidate count. Regression: item-specific search queries, new candidates, source provenance and license must be present in each release receipt; acceptance based on real text and grammar facts, not the number of records in a static registry. CI validates config shape but cannot prove a real web/Drive search has been executed.
