# ARC_SCOPE_LEDGER_V1.0
VERSION: 1.0
DATE: 2026-09-17
ROLE: 시험범위·개념·출제 커버리지 관리
STATUS: ACTIVE

## 0. PURPOSE
ARC N제 시스템에서 “무엇을 출제해야 하는가 / 무엇을 출제했는가 / 무엇이 비었는가”를 추적한다.
이 파일은 문제 생성 전 SCOPE PLAN과 생성 후 COVERAGE UPDATE의 기준이다.

핵심 목표:
- 시험범위 누락 방지
- 특정 개념 과다출제 방지
- 최근에 반복된 문항 구조의 재사용 억제
- ARC CORE → ARC N° → ARC FINAL 간 개념 ID 연결
- 제외 범위의 재유입 차단

## 1. SOURCE PRIORITY
범위 판정 우선순위:
1. 사용자·교사의 명시적 제외/포함 표시
2. 현재 학교 학습지·보충자료
3. 현재 시험범위 교과서
4. 해당 과목 ACTIVE MASTER
5. 공식 외부자료
6. 일반 참고자료

하위 자료는 상위 범위를 자동 확장할 수 없다.

## 2. STATUS CODES
PRIORITY:
- R = REQUIRED
- S = SUPPORTING
- C = CONDITIONAL
- X = EXCLUDED

COVERAGE:
- UNMEASURED = 아직 실출제 로그 없음
- UNDER = 목표보다 부족
- OK = 목표 범위 충족
- OVER = 최근 과다출제
- BLOCKED = 범위 제외/출제 금지

## 3. CONCEPT ID RULE
형식:
`SUBJECT-UNIT-CONCEPT`

예:
- SCI-OR-REACTIVITY
- SOC-C-RIGHTS
- KOR-PAL-INFERENCE
- HIS-COL-NATIONAL_MOVEMENT
- AI-SEARCH-BFS

같은 개념은 CORE/N°/FINAL에서 같은 CONCEPT_ID를 유지한다.

## 4. COVERAGE RECORD FIELDS
각 세트 생성 후 아래 값을 갱신한다.

|필드|의미|
|---|---|
|CONCEPT_ID|고유 개념 ID|
|PRIORITY|R/S/C/X|
|SOURCE_SCOPE|교과서/학습지/범위 근거|
|TARGET_MIN|한 종합세트에서 권장 최소|
|TARGET_MAX|권장 최대|
|GENERATED_COUNT|현재 세트 실제 출제수|
|RECENT_3SET_COUNT|최근 3세트 누적|
|QUESTION_FORMS|최근 사용 유형|
|ASSET_TYPES|최근 사용 자료형|
|LAST_USED_SET|마지막 사용 SET_ID|
|COVERAGE_STATUS|UNMEASURED/UNDER/OK/OVER/BLOCKED|
|NOTES|주의사항|

## 5. INITIAL SCOPE REGISTRY

### 5-1. 공통국어2

|CONCEPT_ID|PRIORITY|SOURCE_SCOPE|핵심 평가축|STATUS|
|---|---:|---|---|---|
|KOR-TAN-CORE|R|미래엔 p10~99 + 학교 보충 「탄궁가」|화자 처지, 빈궁 인식, 대응 태도, 시상 전개|UNMEASURED|
|KOR-TAN-EXPR|R|동일|가사 형식, 반복·열거·대조, 자조·해학|UNMEASURED|
|KOR-PAL-OBS|R|학교 보충 「팔원」|관찰 사실과 화자 추론 분리|UNMEASURED|
|KOR-PAL-CONTEXT|S|동일|인물 처지, 공간 이동, 시대·사회 맥락, 시어 의미|UNMEASURED|
|KOR-MEM-TIME|R|학교 보충 「기억할 만한 지나침」|과거 사건과 현재 회상, 시간 구조|UNMEASURED|
|KOR-MEM-DISTANCE|S|동일|화자-대상 거리, 타인의 고통에 대한 기억|UNMEASURED|
|KOR-AUT-CORE|R|칸트→헤겔 자율성 비문학|도덕적 자율성/인륜적 자율성의 공통점·차이|UNMEASURED|
|KOR-IZONDANG|X|박지원 「이존당기」|비상/참고 비교 전용|BLOCKED|

권장 종합세트 구조:
- 직접 확인 10~15%
- 문맥·표현 15~20%
- <보기> 적용 20~25%
- 비교 15~20%
- HALF_TRUE 15~20%
- 복수조건 10~15%

### 5-2. 통합과학2

|CONCEPT_ID|PRIORITY|SOURCE_SCOPE|핵심 평가축|STATUS|
|---|---:|---|---|---|
|SCI-GT-FOSSIL|R|p14~19 지질 시대|표준화석·시상화석·화석 생성|UNMEASURED|
|SCI-GT-TIME|R|동일|연대표·시기·대멸종·회복구간|UNMEASURED|
|SCI-EV-SELECTION|R|p20~35 진화·생물다양성|변이·자연선택·내성|UNMEASURED|
|SCI-EV-DIVERSITY|R|동일|종/유전적 다양성, 단편화, 생태통로, 외래종|UNMEASURED|
|SCI-OR-ELECTRON|R|p38~45 산화·환원|산소/전자 이동, 산화·환원 판정|UNMEASURED|
|SCI-OR-REACTIVITY|R|동일|금속-금속이온, 반응성 서열, 미지 금속|UNMEASURED|
|SCI-OR-QUANT|R|동일|양이온/전체 이온 수, 입자모형, 질량 변화|UNMEASURED|
|SCI-OR-EXPERIMENT|S|동일|순차 투입, 그래프, 변인 통제, 가설 검증|UNMEASURED|
|SCI-EE-ENERGY|R|p82~91 지구 환경 변화|복사평형, 열수지, 알베도, 온실효과|UNMEASURED|
|SCI-EE-CIRCULATION|R|동일|대기대순환, 무역풍, 용승, 엘니뇨·라니냐|UNMEASURED|
|SCI-EM-INDUCTION|R|p102~109 전자기 유도·발전|자석·코일 이동, 방향·세기, 감은 수·속력|UNMEASURED|
|SCI-EM-GENERATION|S|동일|발전기, 에너지전환, 복수코일, 시간그래프|UNMEASURED|

20문항 과학 권장:
- MATERIAL_BASED ≥ 10
- TRUE_VISUAL_PLANNED ≥ 6
- TRUE_VISUAL_ESSENTIAL ≥ 4
- 가능한 경우 문항 구조 8종 이상

### 5-3. 통합사회2

|CONCEPT_ID|PRIORITY|SOURCE_SCOPE|핵심 평가축|STATUS|
|---|---:|---|---|---|
|SOC-A-VIEW|R|A: 천재 p36~43 + A학습지|관점·정의·사례 적용|UNMEASURED|
|SOC-A-THOUGHT_MAP|R|『생각의 지도』 p156~233|동서양 사고, 속성/관계·맥락, 평균→개인 오류|UNMEASURED|
|SOC-C-RIGHTS|R|C: 천재 p8~23 + C학습지 비X 영역|인권·기본권·헌법 적용|UNMEASURED|
|SOC-C-REMEDY|R|동일|권리구제 기관·절차·효과|UNMEASURED|
|SOC-C-COLLISION|R|동일|권리충돌·조정, 기본권 제한|UNMEASURED|
|SOC-B-GLOBAL|R|B: p98~107 + B학습지|세계화·지역화, 세계도시, 다국적기업|UNMEASURED|
|SOC-B-POP|S|B: p124~133 + B학습지|인구분포, 피라미드, 변천, 이동|UNMEASURED|
|SOC-X-P44_49|X|천재 p44~49|현재 범위 제외|BLOCKED|
|SOC-X-P24_26|X|천재 p24~26|현재 범위 제외|BLOCKED|
|SOC-X-C_USER_MARK|X|C 학습지 손글씨 X 영역|정답근거/오답필수지식/<보기>/서답 채점요소 모두 금지|BLOCKED|

추가 규칙:
- `USER_X_EXCLUSION`이 모든 하위 범위보다 우선한다.
- 종합세트 인구 비중 기본 상한 20%.
- B 단독 세트는 B학습지 직접 근거 자료/문항 비중 최소 60%.

### 5-4. 한국사2

|CONCEPT_ID|PRIORITY|SOURCE_SCOPE|핵심 평가축|STATUS|
|---|---:|---|---|---|
|HIS-COL-CONTROL|R|미래엔 p10~63|일제 통치·정책·시기 식별|UNMEASURED|
|HIS-MOV-NATIONAL|R|동일|민족주의 계열 활동·단체·인물|UNMEASURED|
|HIS-MOV-SOCIAL|R|동일|사회주의 계열 활동·단체·인물|UNMEASURED|
|HIS-MOV-UNITY|R|동일|민족협동전선·연대·변화|UNMEASURED|
|HIS-RES-ARMED|R|동일|무장투쟁·지역·단체·전후관계|UNMEASURED|
|HIS-CULT-EDU|S|동일|교육·문화·언론·실력양성 관련 활동|UNMEASURED|
|HIS-LIBERATION|R|동일|광복, 건국 준비, 조직·강령·인물|UNMEASURED|
|HIS-SOURCE-ID|R|전 범위|법령·신문·사료·강령 식별|UNMEASURED|
|HIS-TIMELINE|R|전 범위|사건 선후관계·연표|UNMEASURED|

20문항 이상 권장:
- 사료/지도/연표/신문/사진/조직도 기반 ≥ 7문항

### 5-5. 인공지능기초

|CONCEPT_ID|PRIORITY|SOURCE_SCOPE|핵심 평가축|STATUS|
|---|---:|---|---|---|
|AI-CORE-CONCEPT|R|길벗 p10~53, p56~99|AI 기본 개념·사례 적용|UNMEASURED|
|AI-SEARCH-DFS|R|현재 학교 범위 내|DFS 탐색 순서·방문 규칙|UNMEASURED|
|AI-SEARCH-BFS|R|동일|BFS 탐색 순서·방문 규칙|UNMEASURED|
|AI-KR-REASON|S|동일|지식표현·추론|UNMEASURED|
|AI-ML-PROCESS|R|동일|기계학습 절차|UNMEASURED|
|AI-DATA-PREP|R|동일|수집·전처리·EDA|UNMEASURED|
|AI-DATA-VIZ|R|동일|그래프·상관계수표 해석|UNMEASURED|
|AI-CODE-INTERP|S|동일|코드 결과 해석|UNMEASURED|

20문항 기준:
- 범위상 가능하면 실제 자료해석형 ≥ 6문항

## 6. PRE-GENERATION RULE
새 세트를 만들기 전:
1. PRODUCT_MODE와 TARGET_RANGE를 확인한다.
2. X/BLOCKED 항목을 제거한다.
3. R 항목 중 `UNDER` 또는 `UNMEASURED`를 우선한다.
4. 최근 3세트에서 과다사용된 CONCEPT_ID/QUESTION_FORM에는 재사용 패널티를 준다.
5. 문항 청사진에 CONCEPT_ID를 반드시 부여한다.

## 7. POST-GENERATION UPDATE
세트 생성 후:
- GENERATED_COUNT 기록
- RECENT_3SET_COUNT 갱신
- QUESTION_FORMS 기록
- ASSET_TYPES 기록
- LAST_USED_SET 기록
- 오류가 있었으면 ERROR_ID 연결
- QA BENCH 대상 세트면 BENCH_ID 연결

## 8. COVERAGE JUDGEMENT
기본 판정:
- GENERATED_COUNT = 0 → UNDER
- TARGET_MIN 미만 → UNDER
- TARGET_MIN~TARGET_MAX → OK
- TARGET_MAX 초과 또는 최근 3세트 반복 과다 → OVER
- X 범위 → BLOCKED

종합세트의 목표는 모든 R 항목을 무조건 1문항씩 넣는 것이 아니라,
시험 비중·학교자료 강조·학교 기출 DNA에 따라 가중 배분하되 핵심 범위의 장기 공백을 만들지 않는 것이다.

## 9. SET LOG TEMPLATE
```yaml
SET_ID:
DATE:
SUBJECT:
PRODUCT_MODE:
TARGET_RANGE:
ITEM_COUNT:
CONCEPT_COVERAGE:
  - CONCEPT_ID:
    COUNT:
    QUESTION_FORMS:
    ASSET_TYPES:
ERROR_IDS: []
QA_BENCH_ID:
NOTES:
```

## 10. RELEASE RULE
이 Ledger의 범위 정보가 ACTIVE MASTER와 충돌하면 즉시 동기화한다.
단, 사용자·교사의 최신 명시적 범위 정보가 있으면 Ledger와 MASTER 모두 그 정보에 맞춰 수정한다.
