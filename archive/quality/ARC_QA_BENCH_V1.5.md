# ARC_QA_BENCH_V1.5
VERSION: 1.5
DATE: 2026-09-18
ROLE: 출제 프롬프트 회귀검사·품질 비교
STATUS: ACTIVE

## 0. PURPOSE
MASTER/ENGINE/QA 변경이 실제 생성 품질을 개선했는지 동일 조건에서 비교한다.
V1.5는 자동 점수 인플레이션, 정답 위치 편향, 사상가 귀속 오류에 더해 국어 SOURCE_TEXT_BLOCK의 원문 충실도와 완결성을 검출하며 frozen regression fixture로 규칙 변경의 회귀를 검출한다.

## 1. HARD FAIL
하나라도 발생하면 FAIL:
- 범위 밖 지식이 정답에 필수
- 복수정답/정답 없음
- 정답키 불일치
- 필수 자료 누락/placeholder
- 사용 금지 범위 유입, 통합사회 C파트 X 영역 침범
- 저작권 과복제
- 데이터·그래프·입자모형 오류
- 역사 사료 주체/시기 오류
- DFS/BFS 탐색 순서 오류
- 저장/조판 handoff 필수 필드 누락
- QA 근거 없이 점수만 기입
- 사상가 비판 문항의 정답이 상대의 실제 주장/정당한 함의가 아니라 허수아비 귀속에 의존
- 선지 재배열 뒤 ANSWER_KEY와 실제 정답 위치가 불일치
- SOURCE_TEXT_BLOCK을 기억/요약으로 복원하거나 source에 없는 행·문단을 삽입
- SOURCE_TEXT_BLOCK의 필수 행·문단 누락 또는 순서 변경
- 자동화 실행이 산출물 없이 SUCCESS 처리

## 2. RELEASE SCORE — 100
|평가축|점수|
|---|---:|
|정확성/유일정답|25|
|범위 충실도|15|
|현재 학교자료 적합도|15|
|오답 품질|10|
|문항 구조 다양성|10|
|자료·시각 무결성|10|
|난도/변별 균형|5|
|원작성/저작권|5|
|출력·HANDOFF 무결성|5|

- 92~100 + HARD FAIL 0 = RELEASE PASS
- 87~91 + HARD FAIL 0 = RC
- 86 이하 = FAIL

과거 다른 교사 기출은 학교자료 적합도 점수의 '스타일 근거'로 쓰지 않고 난이도 calibration에만 사용한다.

## 3. EVIDENCE-BASED QA
각 점수축에 최소 1개 관찰 근거를 남긴다.
'검토 완료', 'independently checked', '적절함'만으로는 근거가 아니다.

필수 예:
- distractor_quality: '②는 원인-결과 전도, ④는 조건 누락 HALF_TRUE'
- reasoning: '자료 A에서 시기 식별 → B와 선후관계 결합의 2단계'
- school_material_fit: '현재 학습지의 표 구조를 새 데이터로 재설계'

## 4. SENTINEL RECHECK
과목별 20문항 중 최소 4문항을 독립 재검수한다.
우선순위:
1) 최고 ITEM 점수 문항
2) 최고 난도 문항
3) 자료/시각 문항
4) 가장 낮은 점수의 PASS 문항

독립 재검수 점수 차이가 6점 이상이거나 PASS/REVISE 판정이 뒤집히면 그 과목 20문항 전체를 재채점한다.

## 5. SCORE DISTRIBUTION AUDIT
다음은 회귀 FAIL 사유:
- 점수가 88/89/90/91처럼 기계적 순환
- 70% 이상 문항이 5점 폭 안에 몰림
- 모든 QUALITY_FLAGS가 비어 있음
- PREMIUM 비율이 높지만 자료/추론 근거가 없음
- D3 이상인데 1단계 직접개념 문항이 반복

## 6. EXECUTABLE REGRESSION RUNNER
Runner: `tooling/promptfoo/promptfooconfig.yaml`
30개 fixture의 실제 결과 artifact 없이 REGRESSION_PASS를 주장하지 않는다.
candidate adapter는 `ARC_CANDIDATE_CMD` 또는 `ARC_CANDIDATE_RESULTS_DIR`를 사용한다.

## 7. FROZEN REGRESSION FIXTURES
활성 회귀셋:
- `quality/regression/ARC_REGRESSION_POLICY_V1.0.md`
- `quality/regression/REGRESSION_FIXTURES_V1.0.yaml`

총 30개: 5과목 × GOOD 3 + BAD 3.
COMMON ENGINE/MASTER/QA/난이도/Source/BANK 판정 규칙 변경 시 `arc-eval-regression`으로 전수 재평가한다.
- GOOD가 REVISE/DISCARD로 내려가면 FAIL
- BAD가 BANK_A/PREMIUM으로 올라가면 FAIL
- BAD-DISCARD가 PASS/BANK로 올라가면 FAIL
- 기대 점수 범위/상한을 3점 이상 벗어나면 drift를 기록하고 정책 기준에 따라 WARN/FAIL
- fixture 기대값을 변경하여 테스트를 통과시키는 행위 금지

## 8. GENERATIVE FIXED BENCH SET
KOR-B01 탄궁가 20: 직접확인 편중, 표현효과, HALF_TRUE
KOR-B02 팔원 15: 관찰 사실 vs 화자 추론
KOR-B03 칸트-헤겔 15: 공통점/차이, 범위 밖 철학사 금지
KOR-B04 보호 현대문학 20: user/Drive source 원문 완결성, shared passage linkage, 원문-선지 근거 대조
SCI-B01 산화환원 20: REDOX_LEDGER, 입자/질량/자료
SCI-B02 진화·생물다양성 20: 집단 변화, 자료형 비중
SCI-B03 전자기유도 15: 방향/세기/그래프
SOC-B01 C파트 20: X_MARK_FILTER
SOC-B02 B파트 20: 학습지 직접 근거, 지도/인구자료
SOC-B03 기본권·권리구제 20: 기관/절차/효과
SOC-B04 칸트·베카리아 형벌론 20: 주장/함의/비판 귀속, 절대표현, 정답위치 분포
HIS-B01 범위 종합 20: 사료/지도/연표 >=7
HIS-B02 민족주의·사회주의·민족협동전선 15
HIS-B03 사료·연표 고난도 15
AI-B01 DFS/BFS 15
AI-B02 전처리·시각화 15
AI-B03 범위 종합 20: 자료해석 >=6

## 8-1. ANSWER POSITION / CLAIM FIDELITY BENCH
5지선다 세트:
- EXPECTED = ITEM_COUNT / 5
- SOFT BAND = max(1, floor(EXPECTED)-1) ~ ceil(EXPECTED)+1
- ITEM_COUNT >= 10인데 ZERO_SLOT이면 WARN + 재편집 우선
- THREE_PLUS_STREAK / PERIODIC_SEQUENCE / ANSWER_KEY_DESYNC를 검사
- exact equal distribution은 단독 FAIL이 아니지만 기계적 순서와 결합되면 AI_SET_PATTERN FAIL
- 정답 분포 수정 뒤 shuffle된 문항은 UNIQUE_ANSWER와 PASS A/B를 다시 실행

사상가·이론 문항:
- PHILOSOPHY_ATTRIBUTION
- CRITIQUE_TARGET_FIDELITY
- ABSOLUTE_WORDING_AUDIT
를 검사한다.

STRAW_MAN_CRITIQUE 또는 정답 경로의 AMBIGUOUS_ABSOLUTE가 발견되면 RELEASE PASS 금지.

## 8-2. KOREAN SOURCE TEXT FIDELITY BENCH
SOURCE_TEXT_BLOCK을 사용하는 국어 세트는 다음을 검사한다.
- SOURCE_KIND가 USER_PASTED / USER_UPLOAD / CONNECTED_DRIVE / SCHOOL_WORKSHEET / TEXTBOOK 중 하나인가
- 실제 source를 현재 작업에서 다시 읽었는가
- 작품명/작가/범위가 source와 일치하는가
- 시의 행·연 순서 또는 산문의 문단 순서가 유지되는가
- source에서 확인되지 않은 텍스트가 추가되지 않았는가
- 필요한 범위가 누락되지 않았는가
- LINKED_ITEM_IDS의 문항 근거가 실제 source text에 존재하는가
- 같은 원문을 문항마다 불필요하게 반복하지 않는가

필수 QC:
SOURCE_ACCESS = PASS
SOURCE_TEXT_FIDELITY = PASS
SOURCE_TEXT_COMPLETENESS = PASS
SOURCE_TEXT_LINKAGE = PASS

하나라도 FAIL이면 READY_FOR_TYPESET 및 RELEASE PASS 금지.

## 9. AUTOMATION BENCH
자동화는 품질과 별도로 실행 내구성을 검사한다.
- RUN folder created
- SUBJECT checkpoint written after each subject
- RAW doc exists before QA starts
- QA report exists
- BANK write exists or explicit zero-pass explanation exists
- failure produces failure log
- partial completion can resume next run
- no self-optimization before item production completes

## 10. RELEASE GATE
COMMON ENGINE/QA 변경:
- 관련 5과목 최소 1 BENCH
- HARD FAIL 0
- SENTINEL RECHECK 통과
- SCORE DISTRIBUTION AUDIT 통과
- ANSWER POSITION AUDIT 통과
- 사상가·이론 문항이면 CLAIM FIDELITY AUDIT 통과
- SOURCE_TEXT_BLOCK 사용 국어 세트이면 SOURCE TEXT FIDELITY BENCH 통과
- AUTOMATION BENCH 통과
- REGRESSION_FIXTURES 30개 전수 실행
- REGRESSION_FAIL_COUNT = 0
- REGRESSION_EXECUTED = true

## 11. SELF-SCORING INFLATION AUDIT
20문항 이상 세트는 다음을 별도 점검한다.
- REVISE/DISCARD = 0
- BANK_A > 30%
- D4+D5 > 45%
- 90점 이상 비율 > 50%

하나라도 해당하면 SCORE_INFLATION_SUSPECT=true.
ARC_ITEM_QUALITY_RUBRIC_V1.3의 ZERO-REJECTION / PREMIUM-RATE AUDIT를 실행한다.
추가 blind recheck 완료 전 RELEASE PASS를 주지 않는다.

## 12. D4 ADVERSARIAL SENTINEL
기존 sentinel 4문항에 더해, D4/D5 비율이 30%를 넘는 세트는 다음 2문항을 추가 점검한다.
- <보기>가 정답 원리를 가장 직접적으로 제공하는 D4 후보
- 오답 중 즉시 제거 가능한 선지가 가장 많은 D4 후보

검사 질문:
1. <보기>를 한 문장으로 요약하면 정답이 바로 보이는가?
2. 실제 추론이 1단계인가?
3. 적어도 2개 오답이 마지막까지 경쟁하는가?

YES/NO 결과를 근거로 난도와 BANK tier를 재산정한다.

## 13. STORAGE INTEGRITY AUDIT
저장 성공은 생성/업로드 도구의 success 응답만으로 판정하지 않는다.

STORAGE_PLACEMENT=VERIFIED 조건:
- 실제 artifact FILE_ID가 존재
- 해당 FILE_ID의 parent_ids에 INTENDED_TARGET_FOLDER_ID가 포함되거나
- 대상 폴더 listing에서 동일 FILE_ID가 확인됨
- 파일이 non-empty

PDF/원고/QA 각각 독립 검증한다.

파일이 Drive root에만 있으면:
- STORAGE_PLACEMENT=ROOT_STAGED 또는 MOVE_PENDING
- VERIFIED 금지

로컬/Cowork에만 있으면:
- STORAGE_PLACEMENT=PENDING_MANUAL_UPLOAD

QA 리포트의 저장 상태와 실제 Drive 메타데이터가 다르면:
STORAGE_METADATA_MISMATCH = HARD FAIL
수정 전 FULL_STORAGE_SUCCESS / FINAL_RELEASED 금지.

END ARC QA BENCH V1.5
