# ARC_QA_BENCH_V1.0
VERSION: 1.0
DATE: 2026-09-17
ROLE: 출제 프롬프트 회귀검사·품질 비교
STATUS: ACTIVE

## 0. PURPOSE
출제 MASTER 또는 COMMON ENGINE을 업데이트할 때
“문구가 좋아 보이는가”가 아니라 “실제 생성 품질이 좋아졌는가”를 동일 조건에서 비교한다.

이 파일은 프롬프트 업데이트의 RELEASE GATE다.

## 1. WHEN TO RUN
다음 변경 시 최소 관련 BENCH를 실행한다.
- COMMON GENERATION ENGINE 변경
- 과목 MASTER의 범위/난도/오답/검증 규칙 변경
- 시각자료 분류 규칙 변경
- ANSWER_KEY/HANDOFF 구조 변경
- 새로운 HARD FAIL 추가
- 오류 재발 방지 규칙 추가

사소한 파일명 변경·주석 수정은 생략 가능하다.

## 2. BENCH PRINCIPLES
- BENCH_ID와 요청 조건은 고정한다.
- 이전 버전과 새 버전은 같은 입력자료/범위/문항수로 비교한다.
- 정답이나 특정 문항 문장을 ‘외워서’ 맞추는 벤치가 아니라 품질 특성을 검사한다.
- 벤치 실행 결과는 학생용 문제집으로 배포하지 않는다.
- 벤치 자체를 자주 바꾸지 않는다. 바꿀 경우 BENCH_VERSION을 올린다.

## 3. HARD FAIL
하나라도 발생하면 점수와 무관하게 FAIL:
- 범위 밖 지식이 정답에 필수
- 복수정답/정답 없음
- 정답키와 문항 불일치
- 필수 자료 누락
- placeholder
- 사용 금지 범위 유입
- C파트 X 표시 영역 출제
- 저작권 원문/문항의 과도한 복제
- 데이터·그래프·입자모형 수치 불일치
- 역사 사료 주체/시기 오류
- DFS/BFS 탐색 순서 오류
- 조판 handoff 필수 필드 누락

## 4. QUALITY SCORE — 100
|평가축|점수|판정 기준|
|---|---:|---|
|정확성/유일정답|25|PASS A/B, 계산·사실·자료 일치|
|범위 충실도|15|SCOPE LOCK, 제외범위 0|
|학교 DNA 적합도|15|동북고 기출의 자료형·발문·추론 스타일 반영|
|오답 품질|10|HALF_TRUE/조건오류 등 판단축이 명확|
|문항 구조 다양성|10|동일 패턴 반복 억제|
|자료·시각 무결성|10|ASSET_CLASS 정확, TRUE_VISUAL 과장 없음|
|난도/변별 균형|5|단순암기 편중·과도한 선행지식 없음|
|원작성/저작권|5|복제 위험 없음|
|출력·HANDOFF 무결성|5|A~D + HANDOFF_META 정상|

권장 판정:
- 92~100 + HARD FAIL 0 = RELEASE PASS
- 87~91 + HARD FAIL 0 = RC / 수동검토
- 86 이하 = FAIL
- 전 버전보다 총점이 하락하면 원인 분석 필수

점수는 절대적 진실이 아니라 버전 간 비교 지표다.
정확성·범위·유일정답은 점수보다 HARD GATE가 우선한다.

## 5. FIXED BENCH SET

### KOR — 공통국어2
**KOR-B01**
- 요청: `탄궁가 객관식 20문항`
- 검사: 직접확인 편중 여부, 표현효과, HALF_TRUE, 원문 복제 위험

**KOR-B02**
- 요청: `팔원 고난도 객관식 15문항`
- 검사: OBSERVED_FACT vs SPEAKER_INFERENCE, 화자 지식 과잉, 문맥 근거

**KOR-B03**
- 요청: `칸트-헤겔 자율성 객관식 15문항`
- 검사: 공통점/차이, 범위 밖 철학사 지식 의존 여부

### SCI — 통합과학2
**SCI-B01**
- 요청: `산화환원 객관식 20문항`
- 검사: REDOX_LEDGER, 반응성 유일성, 이온수/입자수, 질량변화 근거, TRUE_VISUAL

**SCI-B02**
- 요청: `진화·생물다양성 객관식 20문항`
- 검사: 개체 변화 vs 집단 비율 변화, 자연선택, 다양성 구분, 자료형 비중

**SCI-B03**
- 요청: `전자기 유도·발전 객관식 15문항`
- 검사: 방향/세기/속력/감은수 조건, 선행공식 누출, 시간그래프

### SOC — 통합사회2
**SOC-B01**
- 요청: `C파트 학습지 기반 객관식 20문항`
- 검사: C_X_MARK_FILTER, 권리구제/기관, 기본권 충돌, 범위 누출

**SOC-B02**
- 요청: `B파트 학습지 기반 객관식 20문항`
- 검사: 학교자료 직접 근거 ≥ 60%, 지도/인구피라미드/변천자료, TRUE_VISUAL 분류

**SOC-B03**
- 요청: `기본권·권리구제 객관식 20문항`
- 검사: 기관/절차/효과, PURPOSE_ONLY_CONSTITUTIONALITY, SOURCE_FACT/GENERATION_IDEA

### HIS — 한국사2
**HIS-B01**
- 요청: `시험범위 종합 객관식 20문항`
- 검사: 사료/지도/연표 등 ≥ 7, 시기·인물·단체·계열 정확성

**HIS-B02**
- 요청: `민족주의계·사회주의계·민족협동전선 중심 15문항`
- 검사: IDEOLOGICAL_LINE_SWAP, PERSON_ORGANIZATION_SWAP, 전후관계

**HIS-B03**
- 요청: `사료·연표형 고난도 15문항`
- 검사: 사료 주체·시기, 사건 선후관계 유일성

### AI — 인공지능기초
**AI-B01**
- 요청: `DFS/BFS 객관식 15문항`
- 검사: 탐색 순서, 방문 규칙, 트리/그래프 구조와 답 일치

**AI-B02**
- 요청: `데이터 전처리·시각화 객관식 15문항`
- 검사: 전처리/EDA, 그래프 해석, 상관↔인과 혼동

**AI-B03**
- 요청: `시험범위 종합 객관식 20문항`
- 검사: 실제 자료해석형 ≥ 6, 올해 범위만 사용, 코드 출력 논리

## 6. INTEGRATION BENCH
출제→조판 전체 파이프라인을 확인한다.

**INT-B01 ARC_N**
- 대상: 과학 자료형 20문항
- 기대: 학생 PDF에는 문제만
- ANSWER_KEY는 편집/검증용으로 분리
- 2단 + FULL_WIDTH 자동 전환
- 필수 시각자료 누락 0

**INT-B02 ARC_FINAL**
- 대상: 사회 또는 한국사 20문항
- 기대: 시험지형 출력
- 힌트/난도/유형 태그 0
- 정답 노출 0
- 시험지 메타데이터 정상

## 7. BENCH REPORT TEMPLATE
```yaml
BENCH_RUN_ID:
DATE:
BENCH_VERSION: 1.0
BENCH_ID:
SUBJECT:
OLD_ENGINE:
NEW_ENGINE:
MASTER_VERSION:
PRODUCT_MODE:

HARD_FAILS: []

SCORES:
  correctness: /25
  scope_fidelity: /15
  school_dna: /15
  distractor_quality: /10
  structure_diversity: /10
  asset_integrity: /10
  difficulty_balance: /5
  originality: /5
  handoff_integrity: /5
TOTAL: /100

OLD_TOTAL:
DELTA:

KEY_IMPROVEMENTS: []
REGRESSIONS: []
ERROR_IDS: []
RELEASE_DECISION: PASS / RC / FAIL
```

## 8. RELEASE GATE
COMMON ENGINE:
- 관련 5과목에서 최소 1개 BENCH씩 실행
- HARD FAIL 0
- 새 규칙과 직접 관련된 BENCH는 반드시 실행
- 회귀가 있으면 ACTIVE 승격 금지

SUBJECT MASTER:
- 해당 과목 BENCH 2개 이상
- 범위 변경 시 SCOPE BENCH 필수
- 오류 수정 시 관련 ERROR_ID의 regression test PASS 필수

## 9. BENCH HISTORY
초기 상태:
- V1.0 기준 벤치 정의 완료
- 실제 BASELINE 점수는 아직 `UNMEASURED`
- 다음 실제 세트 생성부터 BENCH_RUN_ID를 부여하여 누적한다.
