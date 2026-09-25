# ARC VISUAL SKILL STACK V1.0

Status: DEV
Purpose: 검증된 4개 visual skill을 ARC 시각자료 체계에 통합하기 위한 호출 규칙.

## 0. Reference-first prerequisite
모든 skill routing 이전에 `ARC_VISUAL_REFERENCE_FIRST_V1.0`을 수행한다. actual visual reference가 존재하면 먼저 스타일 문법을 추출하고, 그 후 적합한 renderer를 선택한다.

## 1. Deterministic renderer first
정확한 수치/개수/방향이 핵심이면 specialized skill보다 먼저 deterministic renderer를 선택한다.
- SCI-GRAPH / SOC-DATA / SOC-STAT → matplotlib
- SCI-PARTICLE → ARC deterministic SVG
- SOC-FLOW / SOC-INSTITUTION / SOC-COMPARE / SOC-CASEBOX → structured SVG
- SOC-MAP → verified vector base + structured SVG overlay
실행 코드: `tooling/visual/`

## 2. Stack
1. arc-visual-drawio-base
2. arc-visual-concept-diagrams
3. arc-visual-chem
4. arc-visual-timeline

## 3. Default by subject
### 통합과학
- 기본: arc-visual-concept-diagrams
- 보조: arc-visual-drawio-base
- 화학 구조식: arc-visual-chem
- 순서/발견사: arc-visual-timeline

### 통합사회
- 기본: arc-visual-drawio-base
- 보조: arc-visual-concept-diagrams
- 연표/변화과정: arc-visual-timeline

### 한국사
- 기본: arc-visual-timeline
- 보조: arc-visual-drawio-base
- 구조 설명: arc-visual-concept-diagrams

### 공통국어/AI
- 필요한 경우에만 arc-visual-drawio-base 또는 arc-visual-concept-diagrams

## 4. Asset-type routing
- 흐름도 / 비교도 / 조직도 / 지도 프레임 → drawio-base
- 개념도 / 과정도 / 원리도 / flat educational SVG → concept-diagrams
- 화학 구조식 / 분자 그림 → visual-chem
- 사건 배열 / 연표 / 시기 변화 → visual-timeline

## 5. Non-goals
- 손그림풍 whiteboard aesthetics
- 브랜딩 중심 infographic
- 장식형 포스터
- 개인 맞춤 약점 시각화

## 6. QA gate
모든 ESSENTIAL 시각자료는 VISUAL PASS A/B + QUESTION_VISUAL_CROSSCHECK + ARC_VISUAL_AUTHENTICITY_RUBRIC_V1.1을 통과해야 하며, 아래는 즉시 FAIL:
- 기능 없는 장식
- 과목 사실 오류
- 인쇄 시 판독 불가
- AI 그림 티가 심한 pseudo-illustration
- 수정 불가능한 닫힌 포맷만 남는 경우
