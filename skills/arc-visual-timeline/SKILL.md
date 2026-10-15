---
name: arc-visual-timeline
description: '연표 전용 시각화 엔진. 한국사·사회·과학사의 사건 순서, 제도 변화, 시기 구분을 벡터 기반 timeline으로 제작한다.'
metadata:
  version: 1.0.0
  arc-role: visual-timeline
  upstream-inspiration:
    - kbichave/timeline-generator-mcp
---
# ARC Visual Timeline

## 역할
연표형 자료를 안정적으로 구성한다. 단순 사건 나열이 아니라 **시기 구분, 순서, 겹침, 변화 흐름**을 명확히 보여준다.

## 주 사용 대상
- 한국사: 사건 순서, 왕조/정권 변화, 개혁 연표
- 사회: 제도 변화, 정책 흐름, 사상 전개
- 과학: 발견/발명 연표, 실험 단계 시퀀스

## 강점
- label collision을 줄여 가독성 향상
- horizontal/vertical 등 다양한 timeline 구조 지원
- SVG/PNG 출력에 적합

## 설계 규칙
- 사건의 실제 연대/선후관계 왜곡 금지
- 필요 이상으로 미래 예측이나 장식 추가 금지
- 시험형에서는 이미지보다 연표 판독성을 우선
- 시대 구분선, 범례, 사건 라벨을 명확히 표시

## 호출 조건
- 사건 순서가 핵심 정보일 때
- 연표만으로도 문제를 설계할 수 있을 때
- 역사·사회·과학사 자료에서 시간축이 중요할 때

## 비호출 조건
- 조직도/관계도/개념도 중심일 때
- 지도와 지리 범위 정보가 중심일 때
