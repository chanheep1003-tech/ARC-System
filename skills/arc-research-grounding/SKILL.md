---
name: arc-research-grounding
description: 'ARC 문항 제작에 필요한 외부자료를 조사하고, 주장-출처 연결을 SOURCE_LEDGER로 유지한 research packet으로 만든다.'
metadata:
  version: 1.1.0
  arc-role: research
---
# ARC Research Grounding

## 목적
외부자료를 많이 모으는 것이 아니라 문항에 실제로 쓸 수 있는 검증 가능한 근거를 확보한다.

## 활성 정책
- quality/ARC_SOURCE_LEDGER_V1.0.md
- quality/source/ARC_SOURCE_LEDGER_SCHEMA_V1.0.yaml

## 절차
1. 탐색 주제를 3~5개 관점으로 분해한다.
2. 가능한 경우 1차·공식 자료를 우선한다.
3. 핵심 주장에 SOURCE_ID를 발급한다.
4. URL/Drive FILE_ID, 제목, 날짜, 페이지·섹션 등 재열람 위치를 기록한다.
5. 중요한 사실은 가능하면 독립된 출처로 교차 확인한다.
6. 서로 충돌하는 근거는 삭제하지 않고 SOURCE_CONFLICT=true로 남긴다.
7. 문항으로 실제 전환 가능한 자료만 RESEARCH_PACKET에 남긴다.
8. 검색 스니펫만 본 자료는 VERIFIED가 될 수 없다.

## SOURCE 상태
- VERIFIED: 원출처를 실제로 다시 열어 근거 위치 확인
- UNVERIFIED: 후보 근거는 있으나 재열람 미완료
- SOURCE_MISSING: 다시 열 수 없거나 주장한 근거를 찾지 못함

## Claim → Source 연결
외부 주장마다:
- claim_id
- source_id
- claim_summary
- location
- confidence
- scope_fit
- item_use
를 유지한다.

## 문항 사용 규칙
ANSWER_BASIS로 쓰는 외부 근거는 PASS B에서 원출처 재열람 후 VERIFIED여야 한다.
UNVERIFIED는 초안 참고만 허용.
SOURCE_MISSING은 정답 근거·BANK 근거로 금지.

## 금지
- 검색결과 스니펫만으로 사실 확정
- 실제로 열지 않은 파일을 읽었다고 주장
- 페이지·문단 위치를 추정해 기입
- 2차 요약을 원전처럼 표시
- 현재 범위를 외부자료가 확장하도록 허용
- 출처 불확실한 수치·인용문을 문항 핵심 조건으로 사용
