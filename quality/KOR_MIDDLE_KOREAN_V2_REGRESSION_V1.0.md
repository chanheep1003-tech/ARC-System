# ARC KOR Middle Korean — V2 Regression Suite V1.0
VERSION: 1.0-dev
DATE: 2026-11-07
STATUS: DEFINED_NOT_EXECUTED
TARGET: 2022 개정 공통국어2 중세 국어 ARC_N / ARC_FINAL
SOURCE_SET: ARC_N_공통국어2_중세국어_100Q_V2.0_REVIEW_PATCH_20261105.pdf
SOURCE_LOCATION: Google Drive (original PDF remains in Drive; source is not copied to GitHub)
RULES: subjects/KOREAN_MIDDLE_KOREAN_QUALITY_RULES_V1.0.md

## TEST MATRIX
| BENCH | 재현 조건 | 기대 판정 | 자동/독립 검증 지표 |
|---|---|---|---|
| KOR-MID-001 | V2 #05 D3, 훈민정음 28자와 구성 수치가 정답을 노출하는 선지 | REVISE/REJECT as D3; OBVIOUS_ANSWER flag | 표면 산술·보기 직접 대조만으로 특정 선택지 배제 가능 여부 |
| KOR-MID-002 | V2 #07 D4, 8종성의 보기와 선지가 직접 충돌 | REVISE/REJECT as D4; GIVEN_AWAY_BY_SOURCE | 3개 이상 독립 추론단계 및 경쟁 오답 2개가 있는지 |
| KOR-MID-003 | V2 #20, 해설의 단일 답 ④와 선지별 분석 충돌 의혹 | HOLD until 5-option independent truth table and primary sources confirm unique answer | 원문/문법 근거 + PASS A/B + 5개 선지 TRUE/FALSE/UNDETERMINED |
| KOR-MID-004 | 신규 D4 후보: 정답/오답이 모두 같은 판정축을 갖고 두 문헌 비교·환경 분석을 요구 | PASS only if evidence and 3 effective steps verified | 판단 단계 기록·첫 독해 제거 가능 오답 수·출처 |
| KOR-MID-005 | 신규 D5 후보: ㄱㄴㄷㄹ 조합/장문만 늘린 변형 | FAIL/DEMOTE if no actual transfer+counterexample reasoning | 새 자료 전이, 예외, 독립 추론, 난도 과장 여부 |

## BENCH INPUT CONTRACT
- 사용자 요청: 학교 범위 내 중세국어 객관식 20문항, D3/D4 중심 D5 일부.
- 동일 학교 학습지/교과서/원문을 실제로 읽었는지 기록. 확인 불가한 자료를 읽었다고 가정하지 않음.
- 신규 생성 20문항의 모든 5지 선지에 독립 진리표/근거/오답의 경쟁력 기록.
- 기존 V2 문항은 '오류 재현 사례'이며 원문을 복사하여 새 문제로 출제하지 않음.
- 비교할 두 실행 모두 동일 자료/요청/문항수/허용 범위로 수행.
- 출제와 검증 역할을 분리; blind recheck 수행 여부를 명시.
- 사용자 체감난도는 중요한 품질 피드백이지만 집단 정답률과 동일한 데이터로 간주하지 않음.

## PASS / RELEASE
- HARD FAIL 0; 모든 문항 SOURCE_VERIFIED, UNIQUE_ANSWER, INDEPENDENT_RECHECK 통과.
- D3는 독립 조건 2개 이상, D4는 실질 3단계 이상, D5는 자료 간 전이 및 반례/예외 확인.
- D4/D5는 오답 최소 2개가 실제 판단 근거를 확인하기 전까지 경쟁 후보가 될 것.
- D4/D5에서 자료를 가리거나 숫자/단정어만으로 답을 찾을 수 있으면 재출제.
- 비교 결과는 accuracy / distractor / reasoning / school_match / set_diversity / repeated_stem / source_uncertainty의 수치 및 문항 ID로 보고.
- BENCH 실행 없이 `REGRESSION_STATUS=PASS` 또는 `RELEASE_READY=true`로 기록 금지.
- 특정 유형의 결과가 나쁘면 FAIL 문항을 BANK에 저장하지 않고 문항 ID 및 오류 원인만 보존.

## REPORT TEMPLATE
```yaml
BENCH_RUN_ID:
BENCH_VERSION: 1.0
RULESET_BRANCH: dev
SOURCE_CHECKED:
ITEMS_GENERATED:
ITEMS_WITH_INDEPENDENT_TRUTH_TABLE:
D3_FALSE_DIFFICULTY_COUNT:
D4_FALSE_DIFFICULTY_COUNT:
D5_FALSE_DIFFICULTY_COUNT:
WEAK_DISTRACTOR_COUNT:
NON_UNIQUE_OR_UNDETERMINED_COUNT:
SOURCE_UNVERIFIED_COUNT:
KOR_MID_001_005: {001: PENDING, 002: PENDING, 003: PENDING, 004: PENDING, 005: PENDING}
REGRESSION_STATUS: PENDING
RELEASE_READY: false
```

## QA BENCH ENTRIES (moved 2026-11-10)
아래 두 벤치는 폐기된 `quality/ARC_QA_BENCH_V1.0.md`에 추가되어 있던 것을 내용 변경 없이 옮긴 것이다.
manifest-selected QA BENCH(`active.quality.qa_bench`)의 국어 벤치와 함께 실행한다.

**KOR-B04 — D3/D4 선지·난도 위장 검사**
- 요청: `학교 확정 중세국어 범위에서 D3 10문항 + D4 10문항, 5지선다`.
- 검사: 보기 단순대조, 산술/극단표현 단서, 교과서 재진술, 독립 판단 단계, 오답 2개 이상 경쟁 가능성.
- 고정 재현 항목: V2 #05(D3) / #07(D4); `quality/KOR_MIDDLE_KOREAN_V2_REGRESSION_V1.0.md`.

**KOR-B05 — 형태소 분석·정답 유일성**
- 요청: `중세국어 연철·조사·어미·높임법을 원문에 근거하여 출제하는 객관식 20문항`.
- 검사: 원문/판본/표기, 형태소 분석 기록, 5지 진리표, 불확정/복수정답, PASS A/B 블라인드 재풀이.
- 고정 재현 항목: V2 #20 — 출처와 전 선지 검수 전에는 HOLD; 문항 오류 확정 여부를 추정하지 않음.
- 중세 국어 규칙 변경 후 dev→main 승격 시 KOR-B04와 KOR-B05를 모두 실제 실행해 HARD FAIL 0 및 품질 변화 기록을 확보한다. 정의만 추가한 단계는 PENDING.

