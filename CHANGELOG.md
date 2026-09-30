# CHANGELOG

## 1.3.0 — 2026-09-30
- **N°13 심화 변별 시범(V0.1)**: 1등급 변별용. 시험 범위 11편 × 2문항 = 22문항(외부 지문·외부 <보기> 없음). 실수 빈발 지점(화자·청자 대응, 서술자 논평 vs 발화, 관찰/전해 들음/추측, 개수 계산, 이유 vs 근거, 양보 가정절)만 겨냥. 해설 각 문항에 '함정' 명시. `outputs/KOR/ARC_N13_심화변별_시범/`.

## 1.2.0 — 2026-09-30
- **N°11 V1.2 · N°12 V1.2 난도 상향(2차)**: 사용자 피드백("답이 너무 명확") 반영. 오답을 같은 방향의 HALF_TRUE로, 유형을 ㄱ~ㅁ·개수형·표·순서·<보기>·사례로 다변화, 표 오답을 사실 관계 칸에 배치. 보고 `quality/reports/N11_N12_REVISION_V1.2_20260930.md`, 원고 `revise_f/g.py`(N°11), `revise_n12b.py`(N°12).
- **FINAL N°01 V1.2 · N°02 V1.1**: 2025 동북고 기출(R0) 대비 상위 문항 보강(외부 <보기>·사례 적용), 선지 단서 제거, 선지 린트 PASS. 평균 구조점수 60.7 / 61.0 (R0 58.3). 보고 `quality/reports/FINAL_DIFFICULTY_RECHECK_V2_20260930.md`, 재현 스크립트 `quality/tools/final_difficulty_recheck.py`, 원고 `src/revise_final.py`.
- **문제지·답지 동시 조판 규칙**: `quality/ARC_PAIRED_DELIVERY_V1.0.md`, 도구 `quality/tools/bundle_pdf.py`, 세트별 `src/make.sh`. 모든 세트는 `…_문제지+답지.pdf`(문제지+정답표) 합본이 기본 산출물이고 해설은 별도 PDF. 기존 N06~N10·FINAL N01/N02도 합본 추가. QA Bench RELEASE GATE·PDF 조판 MASTER·CLAUDE.md 연결.
- **N°11·N°12 V1.1**: 전 문항 선지 재구성(EVOLVE, COPY 0), D2 배제, 선지 린트 PASS. 보고 `quality/reports/N11_N12_REVISION_V1.1_20260930.md`.
- 선지 린트 도구: 동률 편향 제거(유일 최장·유일 최대 중복만 단서로 계산), 개정 원고(`apply_rev.py`) 자동 반영.

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
