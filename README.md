# ARC-System

ARC CORE / N° / FINAL 제작을 위한 엔진·규칙 저장소.

## Source of truth
- GitHub: 엔진, 과목 MASTER, QA/난이도/시각자료 규칙, 조판 템플릿
- Google Drive: 교과서, 학습지, 학교 기출, 외부 참고자료, 검증문항은행, 생성 PDF

## Branches
- `main`: RELEASE
- `dev`: 개발/실험

## Repository map
- `engine/` 생성 엔진 · `subjects/` 과목 MASTER · `quality/` QA·난이도·선지 규칙(+`tools/`, `reports/`)
- `templates/` 조판 템플릿 · `sources/` 지문 원문 라이브러리 · `outputs/` 산출물 세트(`outputs/README.md`)
- `ops/` 실행 로그 · `SYSTEM_MANIFEST.yaml` 활성 규칙 목록 · `CLAUDE.md` 작업 메모

## Start order
1. `SYSTEM_MANIFEST.yaml`
2. 해당 과목 `subjects/*_MASTER_V4.0.md`
3. 필요한 엔진/quality 규칙
4. 지문은 `sources/<과목>/` 라이브러리 먼저 확인 → 없을 때만 Drive에서 추출 후 라이브러리에 추가
5. 생성 (선지는 `quality/ARC_DISTRACTOR_ENGINEERING_V1.0.md` 규칙으로 작성)
6. QA + 선지 린트 (`python3 quality/tools/option_cue_lint.py`)
7. `ops/RUN_LOG.jsonl` 기록

## Important
과거 다른 교사 기출은 현재 출제 스타일 예측에 사용하지 않는다.
난이도 calibration anchor로만 사용한다.
