# ARC MCP Layer

ARC의 MCP 계층은 엔진을 대체하지 않는다. 외부 전문 도구를 안전하게 호출하는 Tool Layer다.

## 역할
- GitHub MCP: ARC-System 엔진/MASTER/규칙 조회 및 유지보수
- draw.io MCP: 편집 가능한 도식/흐름도/구조도 제작
- ChemCP: 화학 구조식·분자 2D 렌더링
- Timeline MCP: 한국사·사회·과학사 연표 제작
- Google Drive: 현재 MCP로 전환하지 않고 기존 ChatGPT/Drive connector 유지

## 기본 원칙
1. Scope와 출제 규칙은 GitHub `main`/`dev`의 ARC 엔진이 결정한다.
2. MCP는 읽기·렌더링·변환·저장 같은 도구 실행만 담당한다.
3. 문제 출제 런타임에서는 GitHub MCP를 기본 read-only로 취급한다.
4. secret/PAT/API key는 repo에 커밋하지 않는다.
5. MCP 실패 시 기존 connector/skill 기반 fallback이 있어야 한다.
6. 외부 MCP 결과도 ARC QA와 Visual QA를 통과해야 최종 산출물에 들어간다.

세부 정책은 `MCP_POLICY.yaml`, 서버 정의는 `SERVER_REGISTRY.yaml`, 라우팅은 `MCP_ORCHESTRATION_V1.0.md`를 따른다.
