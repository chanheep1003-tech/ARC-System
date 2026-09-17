---
name: arc-visual-concept-diagrams
description: '교육용 flat SVG 개념도 엔진. 교과서형 과정도, 개념관계도, 설명 그림, 과학·사회·역사 개념도에 적합한 통일 디자인 시스템을 제공한다.'
metadata:
  version: 1.0.0
  arc-role: visual-educational
  upstream-inspiration:
    - NousResearch/hermes-agent: concept-diagrams
---
# ARC Visual Concept Diagrams

## 역할
교과서/개념서 스타일의 **flat, minimal, educational SVG** 자산을 만든다.

## 주 사용 대상
- 과학: 개념도, 물리 세팅, 화학 과정도, 생물 구조/관계도
- 사회: 개념 관계도, 사상 비교도, 인과 구조도
- 한국사: 제도 구조도, 사건 흐름 개요도
- CORE: 자세한 설명용 보조 그림

## 강점
- 생성형 이미지보다 AI 티가 적음
- 벡터 중심이라 인쇄에 강함
- 한 장 안에 원리와 구조를 명확히 보여주기 좋음

## 설계 규칙
- flat style, minimal palette, textbook-like spacing
- 그림보다 라벨과 정보 구조를 우선
- 한 장면에 너무 많은 시각 효과 금지
- 물리·화학·생물·사회에서 공통되는 ARC 브랜드 질서를 유지

## 호출 조건
- 설명형/개념형 그림이 필요할 때
- 정답 추론에 필요한 관계를 한 눈에 복원시켜야 할 때
- CORE나 과학/사회 N제에서 '설명용 그림'이 중심일 때

## 비호출 조건
- 정교한 화학 구조식(arc-visual-chem 우선)
- 순수 연대표/사건선(arc-visual-timeline 우선)
- 정교한 editable layout 요구가 강할 때(arc-visual-drawio-base 우선)
