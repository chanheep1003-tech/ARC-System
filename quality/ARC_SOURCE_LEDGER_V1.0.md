# ARC SOURCE LEDGER V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: hallucination-resistant source trace and re-open verification

## 0. PURPOSE
ARC가 '읽었다', '출처가 있다', '자료가 말한다'고 주장한 핵심 근거는 실제로 다시 열 수 있어야 한다.
모든 기본 개념에 출처 태그를 남기는 것이 아니라, 틀리면 문항이 깨지는 핵심 사실·수치·사료·외부자료만 추적한다.

## 1. SOURCE_REQUIRED
다음 중 하나면 SOURCE_ID가 필수다.
- 한국사: 연도, 인물, 단체, 사료, 정책 주체, 선후관계
- 통합사회: 철학자 입장, 판례/헌법기관/법·제도, 외부 통계, 고난도 제시문 근거
- 통합과학: 외부 실험자료, 실제 수치/그래프 데이터, 학교자료에 특화된 조건
- 인공지능기초: 외부 코드/데이터, 학교자료의 알고리즘 조건, 실제 데이터 해석
- 공통국어: 작품 원문 근거, 학교 학습활동에 특화된 해석, 외부 비문학 자료
- 모든 과목: 웹·논문·EBS·교육청·공식기관 자료를 정답 근거로 사용
- 모든 과목: 특정 학교 학습지/교과서 페이지가 범위 또는 정답의 직접 근거

SOURCE_ID가 보통 불필요:
- 교과과정의 매우 기본적인 정의를 단독 확인하는 저위험 문항
- ARC가 직접 만든 가상 수치/상황으로서 GENERATED_DATA임이 명확한 자료
단, GENERATED_DATA도 실제 데이터처럼 보이게 제시하면 생성 근거/규칙을 내부 메타데이터에 남긴다.

## 2. STATUS
SOURCE_STATUS는 정확히 세 개만 사용한다.
- VERIFIED: 원출처를 실제로 다시 열어 핵심 근거와 위치를 확인함
- UNVERIFIED: 후보 근거는 있으나 PASS B 재열람이 끝나지 않음
- SOURCE_MISSING: 출처를 다시 열 수 없거나, 주장한 위치/근거를 찾지 못함

출처끼리 충돌하면 UNVERIFIED로 두고 SOURCE_CONFLICT=true를 기록한다.
임의로 한쪽을 선택해 VERIFIED로 만들지 않는다.

## 3. SOURCE RECORD
필수 필드:
SOURCE_ID:
SUBJECT:
SOURCE_TYPE: DRIVE | WEB | OFFICIAL | PAPER | GENERATED_DATA
TITLE:
ROLE: SCOPE | ANSWER_BASIS | DISTRACTOR_CHECK | FACT_CHECK | VISUAL_DATA | CONTEXT
STATUS: VERIFIED | UNVERIFIED | SOURCE_MISSING
LOCATION:
ACCESSED_AT:
CLAIM_SUMMARY:
ITEM_IDS:
SOURCE_CONFLICT: false
NOTES:

### DRIVE LOCATION
가능하면 FILE_ID / PAGE / SECTION_OR_HEADING을 기록하고, 필요 시 VISUAL_REGION 설명을 남긴다.

### WEB LOCATION
URL / PAGE_TITLE / SECTION_OR_HEADING / PARAGRAPH_OR_ANCHOR / PUBLISHED_DATE(optional) / ACCESSED_AT을 기록한다.

### PAPER/OFFICIAL
기관/저자, 문서명, 연도, 페이지/표/그림 번호를 기록한다.

### GENERATED_DATA
GENERATION_RULE / UNITS / CONSTRAINTS / DERIVATION_CHECK를 기록한다.
실제 조사자료처럼 오인시키지 않는다.

## 4. PASS A / PASS B
PASS A:
- 문항 자체 정답 검증
- SOURCE_REQUIRED 여부 판정
- 필요한 SOURCE_ID 연결

PASS B:
- 정답을 독립 재풀이
- SOURCE_REQUIRED인 SOURCE_ID를 실제로 다시 연다
- CLAIM_SUMMARY와 원출처 위치가 일치하는지 확인
- 수치/연도/인물/조건/사료/철학자 입장을 대조
- 일치하면 VERIFIED
- 위치가 모호하거나 재열람 못 하면 UNVERIFIED 또는 SOURCE_MISSING

PASS B는 검색결과 스니펫, 파일명, 이전 AI 요약만 보고 VERIFIED 처리할 수 없다.

## 5. ITEM GATE
문항에 SOURCE_REQUIRED=true가 하나라도 있으면:
- 모든 ANSWER_BASIS SOURCE_ID가 VERIFIED여야 BANK_PASS 가능
- FACT_CHECK 핵심 SOURCE_ID가 UNVERIFIED면 최대 STUDY_DRAFT
- SOURCE_MISSING이면 RELEASE/BANK 금지
- SOURCE_CONFLICT=true이면 정답 근거로 사용 금지

단순 기본개념 문항은 SOURCE_LEDGER가 비어 있어도 그 사실만으로 FAIL하지 않는다.

## 6. SOURCE CLAIM SAFETY
금지:
- 실제로 열지 않은 파일을 읽었다고 주장
- 페이지/문단 위치 추정해서 기입
- 검색 스니펫만으로 VERIFIED
- 2차 요약을 1차 원문처럼 표시
- GENERATION_IDEA를 원출처 주장으로 표시
- 링크가 있다는 이유만으로 내용 검증 완료 처리
- Drive의 X표시/시각표식을 OCR 텍스트만으로 확인했다고 주장

## 7. AUTOMATION STORAGE
Scheduled run ledger root:
Google Drive /N제 시스템/92_자동화실행/04_SOURCE_LEDGER
FOLDER_ID: 1CmiPOP_Ma9FIuoyLOTEhjFpX7-tYwYwZ

권장 파일: SOURCE_LEDGER_<RUN_ID>_<SUBJECT>
자동화는 과목별 checkpoint 직후 native Google Doc으로 ledger를 저장한다.
SOURCE_REQUIRED 레코드가 0개면 문서에 SOURCE_REQUIRED_RECORDS=0과 이유를 기록한다.
파일이 필요한데 ledger 저장에 실패하면 해당 과목 BANK write를 중단한다.

## 8. BANK METADATA
BANK item에:
SOURCE_REQUIRED:
SOURCE_IDS:
SOURCE_STATUS_SUMMARY:
SOURCE_LEDGER_VERSION: ARC-SOURCE-V1.0

V1.0 이전 BANK는 기존 BANK_POLICY의 legacy 재검수 규칙을 따른다.

## 9. COPYRIGHT
SOURCE_LEDGER는 위치와 근거 요약을 저장하는 추적 장치다.
저작권 자료의 장문 원문을 복제하는 저장소로 사용하지 않는다.
필요 최소한의 claim summary와 위치만 남긴다.

END ARC SOURCE LEDGER V1.0