# ARC-System 작업 규칙 (Claude Code 자동 적용)

## 시작 순서
`README.md`의 Start order를 따른다: SYSTEM_MANIFEST.yaml → 해당 과목 MASTER → 필요한 엔진/quality → 현재 시험범위 자료 → 생성 → QA → `ops/RUN_LOG` 기록.
사용자가 이미 준 정보는 다시 묻지 않는다. 결과가 크게 달라질 때만 최소 질문 1회.

## 요청 → 제품 라우팅
- N제/문제집/유형별 → ARC_N (공통 엔진 → 조판 `templates/n/ARC_N_BW_LAYOUT_V1.0.md`)
- 파이널/모의고사/실전 → ARC_FINAL
- 개념서/CORE/압축본 → ARC_CORE (`engine/core/`, 에디션 DETAIL 기본 / COMPACT)
- ARC_N은 문제 본문 뒤 **권말 빠른 정답표 1쪽만** 허용(번호→정답만). 해설·난도·유형 태그 금지.

## 플러그인/도구 사용 규칙
- 계획·구현·리뷰가 여러 단계인 작업: superpowers (계획 → 검증 순서).
- 조판/템플릿/CORE 디자인(HTML·CSS) 작업: impeccable 로 디자인 점검.
- PDF·DOCX·PPTX 등 자료 읽기: `markitdown <파일>` 로 Markdown 변환 후 범위 확인.
- 저장소/자료 구조 파악이 필요하면: graphify.
- 긴 명령 출력(로그·빌드): rtk 로 압축해서 읽기.
- 역할 전문가가 필요하면 `~/.claude/agents` 의 agency-agents 사용.
- 응답 스타일: i-have-adhd 방식 — 결론 먼저, 번호 단계, 짧게. 단 **문항·지문 등 산출물 본문에는 스타일 규칙을 적용하지 않는다**(caveman/축약 금지).
- claude-mem, caveman 은 비활성. 켜지 않는다.

## 절대 규칙
- 과거 다른 교사 기출은 난이도 보정에만 사용. 스타일 예측 금지.
- Drive의 교과서/기출/유료 문제집 PDF를 GitHub에 올리지 않는다.
- 자료를 실제로 열지 못했으면 읽었다고 하지 않는다. 렌더 검증 없이 조판 "완료" 금지.
- `main`에서 실험성 수정 금지 — 변경은 브랜치/`dev`에서 하고 승격 조건(BRANCH_POLICY)을 따른다.
- 토큰이나 대용량 캐시를 크게 쓰는 작업은 중간에 한 번 사용자에게 묻는다.

## 환경
- 앱류(DeepTutor/Orkas/heretic)는 필요할 때만 `./tools/oss/install.sh --full`.
- GPU 없음 → 이미지 생성은 연결된 외부 도구 사용.
