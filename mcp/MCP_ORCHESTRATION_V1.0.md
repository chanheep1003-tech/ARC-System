# ARC MCP ORCHESTRATION V1.0

Status: DEV

## 1. Purpose
MCP는 ARC 엔진이 전문 외부 도구를 호출하기 위한 Tool Layer다. MCP가 범위, 정답, 난도, 출제 원칙을 결정하지 않는다.

## 2. Question-generation route
1. GitHub에서 manifest / subject MASTER / engine / skill rules 로드
2. Google Drive connector에서 현재 범위 자료와 reference 확보
3. Scope Lock
4. 문항/세트 설계
5. 필요한 경우에만 MCP 호출
6. fact audit / item QA / visual QA / set editorial
7. PASS 결과만 최종 산출물에 사용

## 3. MCP routing
### GitHub official MCP
- 용도: 엔진·MASTER·규칙 조회, 유지보수
- 출제 런타임: read-only 우선
- repo write: 사용자가 시스템 수정/업데이트를 명시한 경우만

### draw.io official MCP
- 용도: 흐름도, 구조도, 조직도, 비교도, 편집형 시각자료
- reference-first 분석 후 호출
- 결과물은 editable source + vector export를 우선

### ChemCP
- 용도: 구조식/분자 그림이 실제 문항 판단에 필요한 경우만
- 일반 화학 개념도에는 호출하지 않음
- 교과 범위 밖 전문 descriptor는 문제에 자동 노출하지 않음

### Timeline MCP
- 용도: 사건 선후관계·시기 구분·제도 변화가 핵심일 때
- 한국사 우선, 사회/과학사 조건부
- 실제 연대/순서 검증 후 렌더링

## 4. Drive rule
Google Drive는 기존 native connector를 사용한다. 외부 third-party Drive MCP는 사용하지 않는다.

## 5. Visual rule
MCP 시각자료도 `ARC_VISUAL_REFERENCE_FIRST_V1.0` → `ARC_VISUAL_AUTHENTICITY_RUBRIC` 순으로 검수한다.

## 6. Failure handling
MCP 서버가 없거나 실패하면 생성 전체를 중단하지 않는다. `MCP_POLICY.yaml`의 fallback으로 전환하고 RUN_LOG에 도구 실패를 기록한다.

## 7. Token policy
서버와 스킬은 필요한 순간에만 호출한다. 모든 MCP/skill을 미리 로드하지 않는다.
