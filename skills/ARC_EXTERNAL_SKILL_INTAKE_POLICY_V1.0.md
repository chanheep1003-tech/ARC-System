# ARC EXTERNAL SKILL INTAKE POLICY V1.0
VERSION: 1.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: 외부 GitHub skill 탐색·검증·흡수 정책

## 0. PURPOSE
ARC가 필요한 기능을 이미 잘 구현한 공개 skill/agent pattern이 GitHub에 존재할 경우, 이를 참고해 중복 개발을 줄인다.
외부 skill은 ARC의 권위 규칙을 대체하지 않고, 검증된 설계 패턴·워크플로·도구 사용법을 선택적으로 흡수한다.

## 1. SOURCE PRIORITY
1. OpenAI 공식 공개 skill/repository
2. Anthropic 등 모델 제공사 공식 repository
3. 신뢰 가능한 오픈소스 프로젝트
4. 기타 공개 GitHub repository

공식이라고 해서 자동 채택하지 않는다.

## 2. INTAKE MODES
REFERENCE_ONLY
- 구조, 트리거 설계, JIT loading, validation pattern만 참고
- 원문/코드 복사 없음

ADAPT
- 라이선스가 허용하는 범위에서 일반적 아이디어·워크플로를 ARC 구조에 맞게 재작성
- ARC naming, authority, QA, source policy에 맞춰 독립 구현

VENDOR
- 기본 비활성
- 라이선스가 명확히 허용되고, 실제 코드 의존성이 필요한 경우에만 별도 검토 후 사용
- 사용자 명시 승인 없이는 외부 실행 코드 자동 vendor 금지

## 3. LICENSE / SAFETY GATE
흡수 전 확인:
- repository owner
- license
- source file license/notice
- executable code 여부
- network/credential 요구 여부
- destructive/write capability 여부
- 외부 source/document를 포함하는지 여부

다음은 VENDOR 금지:
- proprietary/source-available only
- license 불명확
- credential 수집/전송
- 자동 repo mutation
- 범위 밖 웹 수집을 강제
- ARC source hierarchy를 우회

Proprietary/source-available skill은 REFERENCE_ONLY로만 사용한다.

## 4. AUTHORITY
외부 skill은 다음을 절대 override하지 않는다:
1. 사용자 현재 범위/제외
2. SYSTEM_MANIFEST
3. subject MASTER
4. ARC engine
5. ARC quality/source/copyright policy
6. ARC product contracts

외부 skill의 지침이 충돌하면 해당 부분을 버린다.

## 5. TOKEN / CONTEXT
- 외부 skill 전체를 preload하지 않는다.
- 필요한 기능이 생긴 순간에만 탐색한다.
- 먼저 README/SKILL frontmatter와 필요한 부분만 읽는다.
- 큰 repository 전체를 context에 넣지 않는다.
- 동일 기능이 ARC 내부 skill에 이미 있으면 기존 skill 확장을 우선한다.

## 6. CORE PRIORITY USE CASES
ARC CORE에서는 다음 기능이 부족할 때 외부 skill 탐색을 우선 고려한다:
- 문서/참고서 편집 구조
- 자연스러운 정보 위계와 중복 제거
- source ingest / structured extraction
- PDF render/preflight
- typography/layout QA
- 표·도식 생성
- skill 자체의 설계/검증

단, 교과 내용 판단과 시험범위 결정은 외부 skill에 위임하지 않는다.

## 7. N° / FINAL PRIORITY USE CASES
- deterministic visual rendering
- PDF preflight
- item/set editorial tooling
- data/table validation
- structured source extraction

문항 정답/범위/난도 authority는 ARC가 유지한다.

## 8. PROVENANCE
외부 skill을 실제로 흡수해 ARC rule/skill을 변경하면 CHANGELOG에 최소:
- source repository
- source path/name
- intake mode
- adopted pattern
- copied code 여부
- license note
를 기록한다.

외부 코드/문구를 실제 복사하지 않았다면 'design reference only'로 기록한다.

## 9. PROMOTION
외부 skill 기반 변경도 일반 ARC 변경과 동일하게:
dev
→ structural validation
→ relevant regression
→ no new hard-fail
→ main promotion

외부 repository의 주장만으로 PASS를 선언하지 않는다.

END ARC EXTERNAL SKILL INTAKE POLICY V1.0
