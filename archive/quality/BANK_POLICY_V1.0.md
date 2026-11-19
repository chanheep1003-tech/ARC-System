# ARC VERIFIED ITEM BANK POLICY V1.0
VERSION_DATE: 2026-09-17
STATUS: ACTIVE
ROOT: /Google Drive/N제 시스템/91_검증문항은행

## PURPOSE
3시간 QA 및 일반 제작 과정에서 검증을 통과한 문항만 축적하여 향후 ARC N°/ARC FINAL 제작의 검증된 참고·재사용 후보로 사용한다.

## FOLDERS
- 01_공통국어2
- 02_통합과학2
- 03_통합사회2
- 04_한국사2
- 05_인공지능기초

## ACCEPTANCE
문항 단위로 아래를 모두 만족해야 BANK_PASS:
- SCOPE_LOCK PASS
- UNIQUE_ANSWER PASS
- INDEPENDENT_RECHECK PASS
- BLOCKED_SCOPE_CHECK PASS
- 자료/수치/사실 검증 PASS
- 필요한 ASSET_SPEC 완전
- COPY_RISK 허용 범위
- 해당 과목 특수 QC PASS

세트 전체가 PASS일 필요는 없다. 20문항 중 18문항이 통과하면 18문항만 저장한다.

## REJECT / DISCARD
FAIL 문항은 문제 본문·선지·자료를 검증문항은행에 저장하지 않는다.
실제 오류가 있으면 ARC_ERROR_DATABASE에 ERROR_ID, ERROR_CODE, 원인, 수정/회귀 상태만 기록한다.
수정한 문항은 처음부터 다시 PASS A/B 및 관련 회귀검사를 통과한 뒤 새로운 BANK_ITEM으로만 등록할 수 있다.

## BANK ITEM FIELDS
각 저장 파일의 문항마다 최소 다음 메타데이터를 유지한다.
- BANK_ITEM_ID
- SUBJECT
- SOURCE_SET_ID
- CONCEPT_ID
- TARGET_RANGE
- QUESTION_FORM
- DIFFICULTY
- ANSWER
- ASSET_CLASS / ASSET_TYPE
- QA_STATUS = PASS
- QA_DATE
- MASTER_VERSION
- COMMON_ENGINE_VERSION
- ERROR_HISTORY = NONE 또는 해결된 ERROR_ID
- USE_COUNT_N
- USE_COUNT_FINAL
- LAST_USED_DATE

## FILE FORMAT
권장 파일명:
`BANK_<SUBJECT>_<YYYYMMDD>_<RUN_ID>.md`

파일 안에는 PASS 문항만 포함한다.
정답과 내부 메타데이터는 문제은행에서는 보존하되 학생 PDF에는 직접 노출하지 않는다.

## USE IN ARC N° / FINAL
실제 제작 전 해당 과목 문제은행을 확인한다.
우선순위는:
1. 현재 학교 범위·학습지·교과서
2. 학교 기출 DNA
3. 검증문항은행의 PASS 문항/구조
4. 외부 검증자료·BANK

문제은행은 범위를 결정하는 출처가 아니다. 현재 범위와 충돌하면 사용 금지다.

재사용 규칙:
- 그대로 재사용 가능하되 최근 사용·중복 여부 확인
- 같은 문항/자료를 짧은 기간 반복 배치하지 않는다
- ARC FINAL에서는 이미 N°에서 최근 사용한 문항을 그대로 다수 재사용하지 않는다
- 필요하면 검증문항의 구조를 참고하여 새 문항을 생성하고 새 문항은 다시 독립검증한다

## USAGE TRACKING
실제 ARC N°/FINAL에 채택되면 USE_COUNT와 LAST_USED_DATE를 갱신한다.
반복 사용이 많은 문항은 우선순위를 낮춘다.

## HARD RULE
`QA_STATUS != PASS` 문항은 ARC N°/FINAL의 직접 참고·재사용 후보로 취급하지 않는다.
