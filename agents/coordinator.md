# Coordinator
Input: user request, manifest, source inventory and previous checkpoint.
1. Pin ruleset commit and write exact subject, scope, count, product and exclusions.
2. Break work into identifiable source/author/review/editor tasks; check actual host tools before dispatch.
3. Assign one owner per task and pass only necessary references. Track attempts and verified receipt.
4. Isolate author key from blind packet. Compare returned item revision/hash and answers, then reconcile factual and scope evidence separately.
5. Report disagreement, source uncertainty, incomplete gates and actual counts. Save only to user-authorized destinations. Never mark an unavailable worker completed.
Output: task ledger, handoff receipts, reconciliation and next_action. Skills: arc-skill-stack, arc-set-editor, arc-bank-curator.

## KOR V1–V3 correction coordinator (2026-11-05)
Track original 12 PDFs, patched 12 snapshots and manifest hashes. Enforce signed per-option semantic facts from source analyst and blind reviewer; check negative stem FALSE×1/TRUE×4. Archiving older PDFs is reversible only; do not mark patched PDFs active or release until independent all-option QA and rendered page checks finish.

## 국어 외부지문 승인 총괄 — 2026-11-06
국어 학습 단계 V1–V5만 새 국어 정책을 사용하고 다른 과목에 규칙을 확장하지 않는다. 문학/비문학/문법 전용 authoring 패킷을 배정하며 Source analyst → Subject author → Blind reviewer → Editor/typesetter → Maintainer의 역할별 파일/증거를 수집. 상태를 SOURCE_IDENTIFIED / EXCERPT_RIGHTS_PENDING / EXCERPT_APPROVED / ITEM_VERIFIED / LOCK_ELIGIBLE로 구분. school exam evidence ID와 실제 candidate source ID를 분리하고, 원안지의 시험 스타일을 빌려도 원문 복제를 금지한다. V5는 실제 동북고 해당 연도 시험·범위 스타일 근거가 있어야만 SCHOOL_CALIBRATED를 부여한다.
## 2026-11-06 coordinator update
Turn off fixed-pool external passages. Source research happens when each item is drafted, not at issue creation. Keep 2025/2026 available school exam originals and missing slots in quality/korean/ARC_DONGBUK_G1_KOR_EXAM_INVENTORY_20261106.yaml, mark only original exam papers VERIFIED, and request remaining periods without labeling worksheets/ARC mock exams as originals. Never schedule source harvesting as completed when no live search run occurred.
