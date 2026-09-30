# CHANGELOG

## 1.1.0 — 2026-09-30
- **선지 경쟁력 엔진 추가**: `quality/ARC_DISTRACTOR_ENGINEERING_V1.0.md` (오답 유형 DT1~DT8, 단일 변이 규칙, CDI, D등급 상한, 린트 게이트).
- **선지 린트 도구**: `quality/tools/option_cue_lint.py` — 최장=정답·어휘중복·길이비·과잉 단정어 점검(R0=2025 기출로 기준 보정).
- 난이도 엔진: DISTRACTOR 축을 CDI로 채점, LEVEL CAP·LABEL INTEGRITY(배점 역산 라벨 금지) 추가.
- 품질 루브릭/QA Bench/공통 엔진 HARD FAIL/국어 MASTER에 게이트 연결.
- 지문 라이브러리 `sources/KOR/공통국어2/` (교과서 1·2단원 + 보충 4편 원문, md 사본은 Drive 동기화).
- 산출물 세트 파이프라인 정리: `outputs/README.md`.
- **핵심 문항 진화 재사용 정책**: 세트 간 겹침 허용, 이전 문항을 선지 재구성·발문 변경으로 개선해 재사용(EVOLVE), 무개선 복붙(COPY)만 10% 이하 제한. SIMILARITY_GUARD V1.1, BANK_POLICY, 공통 엔진 개정.
- 점검 보고: `quality/reports/DIFFICULTY_SYSTEM_AUDIT_20260930.md`, `CUE_LINT_BASELINE_20260930.md`.

## 1.0.0 — 2026-09-18
- GitHub-first engine architecture initialized.
- `SYSTEM_MANIFEST.yaml` added.
- `main` RELEASE / `dev` development workflow added.
- RUN_LOG JSONL + CSV initialized.
- ARC CORE detailed concept engine included.
- CONCEPT_ID → N° linkage enabled.
- School historical exams restricted to difficulty calibration.
- Teacher-style prediction disabled.
- Freeze mode intentionally not added.
