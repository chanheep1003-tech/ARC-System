---
name: arc-bank-curator
description: 'ARC 검증문항은행에 저장할 문항을 선별하고 메타데이터·사용이력·중복도를 관리한다. QA PASS 문항만 저장하며 문제은행이 범위나 출제 방향을 결정하지 못하게 한다.'
metadata:
  version: 1.0.0
  arc-role: bank-curation
---
# ARC Bank Curator

## 목적
문제은행을 “문항 창고”가 아니라 **검증된 재사용 자산**으로 유지한다.

## 저장 조건
`BANK_PASS`는 다음을 모두 만족해야 한다.
- scope 확인
- unique answer 독립 재검증
- 사실/데이터/자산 검증
- blocked/excluded scope 침입 없음
- 저작권 과복제 위험 없음
- 과목별 QA 통과

## 최소 메타데이터
- item_id
- subject
- concept ids
- item form
- reasoning form
- difficulty score + relative school level
- answer
- distractor axes
- asset spec/ref
- QA version
- generator/master version
- originality/similarity signature
- use_count
- last_used
- status

## 재사용 규칙
- 문제은행은 현재 시험범위를 결정하지 않는다.
- 최근 사용 문항은 우선순위를 낮춘다.
- 수정된 문항은 기존 PASS를 자동 상속하지 않고 새로 검증한다.
- 유사도가 높은 문항은 대표 1개만 활성화하거나 변형 필요 표시한다.

## 금지
- REVISE/DISCARD 문항 저장
- 답만 바꾼 사실상 중복 문항 다수 저장
- 출처/버전이 없는 문항 저장
