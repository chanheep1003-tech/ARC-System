---
name: arc-visual-drawio-base
description: 'draw.io 기반 편집형 시각자료 엔진. 흐름도, 비교도, 관계도, 표형 구조도, 지도 프레임, 시험지용 도식의 수정 가능한 원본(.drawio)과 SVG/PDF/PNG export를 담당한다.'
metadata:
  version: 1.0.0
  arc-role: visual-base
  upstream-inspiration:
    - github/awesome-copilot: draw-io-diagram-generator
    - jgraph/drawio-mcp
---
# ARC Visual Draw.io Base

## 역할
ARC 시각자료의 **기본 편집 캔버스** 역할을 한다. 결과물은 나중에 미세 수정 가능해야 하므로 editable source를 우선한다.

## 주 사용 대상
- 사회: 흐름도, 제도 관계도, 경제 순환, 정치 구조
- 한국사: 조직도, 비교표, 왕조/기관 관계도, 간단 지도 프레임
- 과학: 과정도, 장치도, 실험 순서도, 분류표
- CORE: 개념 구조도, 비교도, 요약 도식

## 기본 출력 우선순위
1. `.drawio` editable source
2. `.svg` for print-quality vector output
3. `.pdf` for page embedding
4. `.png` only when vector embedding is unavailable

## 강점
- 위치·화살표·박스·라벨을 직접 제어 가능
- 후편집이 쉽고 재사용성이 높음
- 여러 과목에 공통 디자인 시스템 적용 가능

## 사용 규칙
- 첫 선택지는 '예쁜' 인포그래픽이 아니라 **기능적 도식**이다.
- 시험지에 필요한 정보만 넣고 장식요소 최소화.
- 범례·라벨·화살표 방향을 명시한다.
- 흑백 인쇄 안정성을 확인한다.

## 호출 조건
- 사용자가 편집 가능한 원본을 원할 때
- 비교/흐름/구조/조직/지도 프레임처럼 도형 위주의 자산일 때
- 여러 자산 사이에 통일된 레이아웃이 필요할 때

## 비호출 조건
- 화학 구조식처럼 전문 분자 도구가 더 적합할 때
- 사건 배열 중심의 연표일 때(arc-visual-timeline 우선)
- 플랫 개념 설명 도식이 더 적합할 때(arc-visual-concept-diagrams 우선)
