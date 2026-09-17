---
name: arc-visual-renderer
description: 'ARC 시각자료 라우터. 자료형을 판별해 draw.io base / concept diagrams / chem / timeline 중 적합한 visual skill로 보내고, 결과물을 authenticity rubric으로 검수한다.'
metadata:
  version: 1.1.0
  arc-role: visual-router
---
# ARC Visual Renderer

## Step 0 — Reference first
렌더링 전에 `ARC_VISUAL_REFERENCE_FIRST_V1.0`을 적용한다. 가능한 경우 실제 시험/학습지/교과서/사용자 제공 문제집의 같은 유형 visual 2개 이상을 보고 시각 문법을 추출한다. 원본 visual을 직접 복제하지 않는다.

## 역할
직접 모든 그림을 만드는 단일 엔진이 아니라, **시각자료 요구를 분류하고 적절한 하위 visual skill에 라우팅하는 상위 스킬**이다.

## 기본 원칙
시각자료는 장식이 아니라 **정답 추론에 기능적으로 필요한 정보 구조**다. 예쁘게 보이기보다 사실적 정확성, 판독성, 인쇄 안정성을 우선한다.

## 하위 스택
- `arc-visual-drawio-base`: editable `.drawio` + SVG/PDF/PNG export
- `arc-visual-concept-diagrams`: textbook-like educational SVG
- `arc-visual-chem`: chemical structure visuals
- `arc-visual-timeline`: timeline visuals

## 라우팅 규칙
### draw.io base 우선
- 흐름도, 비교도, 조직도, 구조도, 지도 프레임
- 후편집 필요
- 여러 시각자료 간 동일 레이아웃 유지 필요

### concept diagrams 우선
- 과학/사회/역사의 설명형 개념도
- 과정도, 원리도, 관계도
- 교과서형 flat educational style 필요

### chem 우선
- 구조식, 분자 그림, 화학 결합 구조
- 구조 정확성이 핵심

### timeline 우선
- 사건 순서, 제도 변화, 시대 구분, 과학사/역사 연표

## 공통 규칙
- 흰 배경, grayscale-first, 얇고 명확한 선
- 그림자, 광택, 불필요한 3D, 장식적 gradient 금지
- 축, 단위, 범례, 화살표 방향, 표 머리글 누락 금지
- 색만으로 범주를 구분하지 않는다. 선형/기호/패턴을 중복 사용한다.
- 실제 데이터는 미관을 위해 변경하지 않는다.
- 문항에 없는 정보를 그림이 몰래 제공하지 않게 한다.

## 검수
모든 결과물은 `ARC_VISUAL_AUTHENTICITY_RUBRIC`의 accuracy → functionality → print → naturalness 순으로 본다.

## Hard Fail
- 축/단위 오류
- 과학 구조나 역사 연표/지도 오류
- 색이 사라지면 의미가 붕괴
- 정답을 시각적으로 노출
- 보기용 장식에 불과함
- PDF에서 잘림/폰트 깨짐/저해상도
