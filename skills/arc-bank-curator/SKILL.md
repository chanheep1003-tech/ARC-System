---
name: arc-bank-curator
description: 'ARC 검증문항은행에 저장할 문항을 선별하고 메타데이터·출처검증·사용이력·중복도를 관리한다.'
metadata:
  version: 1.2.0
  arc-role: bank-curation
---
# ARC Bank Curator

## 목적
문제은행을 검증된 재사용 자산으로 유지한다.

## 권위 규칙
- quality/BANK_POLICY_V1.1.md
- quality/ARC_SOURCE_LEDGER_V1.0.md

## ACTIVE_BANK 저장 조건
다음을 모두 만족:
- scope 확인
- unique answer 독립 재검증
- 사실/데이터/자산 검증
- blocked/excluded scope 침입 없음
- 저작권 과복제 위험 없음
- 과목별 QA 통과
- ARC-IQR-V1.1 이상
- QUALITY_COMPONENTS 점수+근거
- SCORE_CEILINGS_APPLIED 기록
- SENTINEL_RECHECK PASS
- SOURCE_REQUIRED인 경우 모든 ANSWER_BASIS SOURCE_ID가 VERIFIED
- SOURCE_MISSING / SOURCE_CONFLICT 정답 근거 없음

## 최소 메타데이터
- item_id
- subject
- concept ids
- item form / reasoning form
- difficulty
- answer
- distractor axes
- asset spec/ref
- QA version
- item-quality version
- source_required
- source_ids
- source_status_summary
- source_ledger_version
- generator/master version
- originality/similarity signature
- use_count / last_used / status

## LEGACY BANK
기존 BANK는 삭제하지 않지만 현행 QA/Source 규칙 재검수 전 자동 승격하지 않는다.

## 금지
- REVISE/DISCARD 문항 저장
- SOURCE_REQUIRED인데 UNVERIFIED/SOURCE_MISSING인 문항 BANK_PASS
- 답만 바꾼 사실상 중복
- 출처/버전/QA 근거 없는 문항 저장
