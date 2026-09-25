# ARC-System

ARC CORE / N° / FINAL 제작을 위한 엔진·규칙 저장소.

## Source of truth
- GitHub: 엔진, 과목 MASTER, QA/난이도/시각자료 규칙, 조판 템플릿, MCP 정책
- Google Drive: 교과서, 학습지, 학교 기출, 외부 참고자료, 검증문항은행, 생성 PDF

## Branches
- `main`: RELEASE
- `dev`: 개발/실험

## Start order
1. `SYSTEM_MANIFEST.yaml`
2. manifest-selected pipeline integrity contract
3. manifest-selected 해당 과목 MASTER
4. `skills/SKILL_REGISTRY.yaml`에서 필요한 skill만 선택
5. 필요한 엔진/quality 규칙
6. Drive에서 현재 시험범위 자료
7. 필요 시 `mcp/SERVER_REGISTRY.yaml`에 따라 전문 도구 호출
8. 생성 → 사실감사 → 자연스러움 감사 → QA → 세트편집
9. PASS 문항만 문제은행 후보
10. `ops/RUN_LOG.jsonl` 기록

## Important
과거 다른 교사 기출은 현재 출제 스타일 예측에 사용하지 않는다.
난이도 calibration anchor로만 사용한다.

## Skill layer
- On-demand only: 모든 skill을 한 번에 로드하지 않음
- 문항 중심: generator / distractor / fact audit / naturalness / QA / set editor / visual / bank
- 자료 입력: PDF·HWP/HWPX·Office 구조 보존형 ingest
- 엔진 변경: golden benchmark 기반 regression
- 개인 오답 기반 재출제와 약점 추적은 비활성화

## Visual stack
- `arc-visual-renderer`: top-level router
- `arc-visual-drawio-base`: editable diagram base
- `arc-visual-concept-diagrams`: educational flat SVG
- `arc-visual-chem`: chemistry structure visuals
- `arc-visual-timeline`: history/social/science timelines
- Reference-First: 실제 교과서·학교자료·문제집의 시각 문법을 먼저 분석하고 새로 설계

## MCP layer (v1.2 dev)
- GitHub official MCP: repo context / maintenance, generation runtime read-only 우선
- draw.io official MCP: editable diagram rendering
- ChemCP: chemistry-only molecular/structure rendering
- Timeline MCP: history/social/science timeline rendering
- Google Drive: 기존 connector 유지, third-party Drive MCP 비활성화
- 모든 MCP는 on-demand 호출, 실패 시 fallback 필수
- MCP가 범위·정답·난도·출제 원칙을 결정하지 않음


## Executable tooling layer
Policy-only checks now have concrete runners under `tooling/`:
- promptfoo frozen regression runner
- sentence-transformers + local Qdrant similarity
- PyMuPDF PDF preflight
- PDF annotation/vector/OpenCV X-mark detector
- deterministic visual renderer + independent visual verifier

Install:
```bash
python -m pip install -r tooling/requirements.txt
```

See `tooling/README.md`.
