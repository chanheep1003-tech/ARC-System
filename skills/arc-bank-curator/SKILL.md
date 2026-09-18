---
name: arc-bank-curator
description: 'ARC 검증문항은행에 저장할 문항을 선별하고 메타데이터·사용이력·중복도를 관리한다. QA PASS 문항만 저장하며 문제은행이 범위나 출제 방향을 결정하지 못하게 한다.'
metadata:
  version: 1.1.0
  arc-role: bank-curation
---
# ARC Bank Curator

## 목적
문제은행을 “문항 창고”가 아니라 검증된 재사용 자산으로 유지한다.

## 권위 규칙
현재 활성 정책은 `quality/BANK_POLICY_V1.1.md`.
문제은행은 현재 시험범위나 출제 방향을 결정하지 못한다.

## ACTIVE_BANK 저장 조건
다음을 모두 만족해야 한다.
- scope 확인
- unique answer 독립 재검증
- 사실/데이터/자산 검증
- blocked/excluded scope 침입 없음
- 저작권 과복제 위험 없음
- 과목별 QA 통과
- ARC-IQR-V1.1 이상
- QA BENCH 1.1 이상
- QUALITY_COMPONENTS에 항목별 점수+근거
- SCORE_CEILINGS_APPLIED 기록
- SENTINEL_RECHECK PASS

## LEGACY BANK
V1.1 이전 BANK는 삭제하지 않지만 ACTIVE_BANK로 직접 재사용하지 않는다.
V1.1 재검수 PASS 전에는 구조 참고용으로만 취급한다.
이전 PREMIUM/A/B 라벨을 신뢰하여 자동 승격하지 않는다.

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
- item-quality version
- score ceilings
- sentinel recheck
- generator/master version
- originality/similarity signature
- use_count
- last_used
- status

## 재사용 규칙
- 최근 사용 문항은 우선순위를 낮춘다.
- 수정된 문항은 기존 PASS를 자동 상속하지 않고 새로 검증한다.
- 유사도가 높은 문항은 대표 1개만 활성화하거나 변형 필요 표시한다.
- scheduled automation은 native Google Docs BANK batch를 허용한다.

## 금지
- REVISE/DISCARD 문항의 ACTIVE_BANK 저장
- 답만 바꾼 사실상 중복 문항 다수 저장
- 출처/버전/QA 근거가 없는 문항 저장
- V1.1 재검수 없는 legacy 문항 직접 재사용
