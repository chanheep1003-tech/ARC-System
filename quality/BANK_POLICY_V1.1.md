# ARC VERIFIED ITEM BANK POLICY V1.1
VERSION_DATE: 2026-09-18
STATUS: ACTIVE
ROOT: /Google Drive/N제 시스템/91_검증문항은행

## PURPOSE
검증을 실제로 통과한 문항만 ARC N°/FINAL의 활성 재사용 후보로 사용한다.
V1.1은 QA 점수 인플레이션이 확인된 legacy BANK를 자동 활성 후보에서 제외한다.

## ACTIVE ELIGIBILITY
ACTIVE_BANK 후보는 문항 단위로 아래를 모두 만족해야 한다.
- SCOPE_LOCK PASS
- UNIQUE_ANSWER PASS
- INDEPENDENT_RECHECK PASS
- BLOCKED_SCOPE_CHECK PASS
- 자료/수치/사실 검증 PASS
- 필요한 ASSET_SPEC 완전
- COPY_RISK 허용 범위
- 해당 과목 특수 QC PASS
- ITEM_QUALITY_RUBRIC_VERSION = ARC-IQR-V1.1 이상
- QA_BENCH_VERSION = 1.1 이상
- SCORE_CEILINGS_APPLIED 기록 존재
- QUALITY_COMPONENTS에 항목별 숫자+근거 존재
- SENTINEL_RECHECK PASS
- QA_STATUS = PASS

## LEGACY BANK
2026-09-18 QA V1.1 활성화 이전에 생성된 BANK 문항은 삭제하지 않는다.
다만 다음 중 하나를 만족하기 전에는 ACTIVE_BANK로 사용하지 않는다.
1. V1.1로 재검수하여 PASS
2. 사용자 수동 승인 + V1.1 최소 정확성/오답/난도 재검수 PASS

LEGACY 문항은 구조 참고용으로만 사용할 수 있으며 정답·난도·PREMIUM 등급을 신뢰하지 않는다.

## PREMIUM
PREMIUM_BANK_A는 ARC_ITEM_QUALITY_RUBRIC_V1.1의 조건을 모두 충족해야 한다.
단순 직접개념 확인형, 약한 오답, generic context, 근거 없는 school-style 평가는 PREMIUM 금지.

## REJECT / REVISE
- HARD FAIL: DISCARD
- REVISE: 수정 후 처음부터 재검증
- FAIL 문항 본문은 활성 BANK에 저장하지 않는다.
- 오류/실패 메타데이터는 ERROR DB 또는 failure log에 기록한다.

## BANK ITEM FIELDS
- BANK_ITEM_ID
- SUBJECT
- SOURCE_SET_ID
- CONCEPT_ID
- TARGET_RANGE
- QUESTION_FORM
- DIFFICULTY
- ANSWER
- ASSET_CLASS / ASSET_TYPE
- ITEM_QUALITY_SCORE
- QUALITY_COMPONENTS with evidence
- QUALITY_FLAGS
- SCORE_CEILINGS_APPLIED
- QA_STATUS
- QA_DATE
- ITEM_QUALITY_RUBRIC_VERSION
- QA_BENCH_VERSION
- SENTINEL_RECHECK
- MASTER_VERSION
- COMMON_ENGINE_VERSION
- ERROR_HISTORY
- USE_COUNT_N
- USE_COUNT_FINAL
- LAST_USED_DATE

## FILE FORMAT
Scheduled automation: native Google Docs recommended.
Interactive/manual runs: Markdown or Docs allowed.
File format does not determine PASS status; metadata and QA evidence do.

## USE PRIORITY
1. 현재 범위·학습지·교과서
2. 현재 학교자료
3. ACTIVE_BANK V1.1+
4. LEGACY BANK structure-only reference
5. 외부 검증자료

과거 다른 교사 기출은 난이도 calibration에만 사용한다.

## HARD RULE
V1.1 재검수되지 않은 legacy BANK는 ARC N°/FINAL의 직접 재사용 후보가 아니다.

END BANK POLICY V1.1
