# CHANGELOG

## 1.1.0 — 2026-11-07
- ARC_N: 권말 빠른 정답표(번호→정답만, 문제 본문 뒤 1쪽)를 허용하는 방향으로 조판 MASTER·엔진·과목 MASTER·오류 DB 문구 통일.
- ARC_CORE: 과목별 2에디션(DETAIL 상세 개념서 / COMPACT 시험 직전 압축본)으로 재구성. 순수 흑백, 1단 본문 + 전폭 시각자료.
- ARC_CORE 입구 연결: COMMON ENGINE MODE_MAP에 ARC_CORE 추가, 과목 MASTER 5종에 위임 문구 추가.
- CONCEPT_ID 통일: CORE `ARC-{SUBJ}-{UNIT}-{NNN}` ↔ SCOPE_LEDGER `SCOPE_CONCEPT_ID` 부모 연결.
- 조판 규칙 통일: ARC_PDF_LAYOUT_MASTER에 제품별 조판 기준 우선순위 명시, 구 CORE 규칙(2~4개/페이지·컬러) 삭제, CORE_PATCH v0.3 폐기 후 `templates/core/ARC_CORE_BW_LAYOUT_V1.0.md`로 대체, CORE HTML 템플릿에서 샘플 본문 제거(v0.3).
- COMMON ENGINE 복구: 438행 `[... ELLIPSIZATION ...]` 절단 흔적 제거 및 §17 제목 복원. 절단으로 사라진 원문은 복구하지 못함(원본 확인 필요). PDF_MASTER 파일명 불일치 수정.
- CHECKSUMS 재생성(기존 5개 불일치 해소).

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
