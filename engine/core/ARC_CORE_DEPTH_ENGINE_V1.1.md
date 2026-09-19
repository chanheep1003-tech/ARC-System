# ARC CORE DEPTH ENGINE V1.1
VERSION: 1.1
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC CORE 개념별 설명 깊이·고난도 집중도 결정

## 0. PURPOSE
ARC CORE는 모든 시험범위를 같은 길이와 깊이로 다루지 않는다.
기본 개념은 빠르게 이해·복습할 수 있게 정리하고, 실제로 여러 판단축이 얽히거나 고난도 문항으로 변형되기 쉬운 부분은 더 깊게 설명한다.

중요:
HIGH_DIFFICULTY_DEPTH는 '내용을 많이 쓰는 모드'가 아니다.
범위 안에서 학생이 틀리는 이유와 문제에서 요구되는 판단 단계를 더 완전하게 설명하는 모드다.

## 1. DEPTH UNIT — CLUSTER FIRST
Depth is assigned to concept clusters before individual concept presentation.

CLUSTER_DEPTH_PRIORITY =
- STANDARD
- ADVANCED
- HIGH_DIFFICULTY

A cluster is a group of concepts that answer the same chapter question or belong to the same causal/comparative structure.

Why:
- concept-by-concept depth assignment can fragment CORE into many mini-cards
- a difficult chapter should be deep because relations are difficult, not because every concept receives a separate "advanced" block
- related facts should share one explanatory flow when possible

Individual DEPTH_PRIORITY may remain as internal metadata for N° linkage, but student-facing depth is expressed at cluster/chapter level.

## 2. DEPTH PRIORITY — INTERNAL ONLY
각 concept에 내부 메타데이터로 하나를 부여한다.

DEPTH_PRIORITY =
- STANDARD
- ADVANCED
- HIGH_DIFFICULTY

학생용 PDF에 이 라벨을 표시하지 않는다.

필수 metadata:
DEPTH_PRIORITY
DEPTH_REASON[]
DEPTH_EVIDENCE[]
DEPTH_AXES[]
DEPTH_SOURCE_IDS[]

## 3. DEPTH ASSIGNMENT

### STANDARD
다음에 해당:
- 정의/관계가 단순
- 조건이 적음
- 다른 개념과 혼동 위험이 낮음
- 학교자료에서 기본 확인 수준
- 반복 설명 없이도 이해 가능

처리:
- 짧고 정확한 본문
- 필요한 경우 MUST 1~2개
- 억지 CONFUSING/TRAP 금지
- 시각자료도 실제 기능이 있을 때만

### ADVANCED
다음 중 2개 이상:
- 두 개 이상의 개념을 연결해야 이해
- 비슷한 개념과 구분 필요
- 조건 변화에 따라 결과가 달라짐
- 자료/그래프/사료/작품 근거 해석이 필요
- 실제 학교자료에서 비교·적용이 강조됨
- N° 고난도 후보의 기반 개념

처리:
- 조건/관계 설명 강화
- 필요한 비교축 명시
- 근거 있는 CONFUSING/TRAP 가능
- 적용 사고과정 1회 정도 보여줄 수 있음

### HIGH_DIFFICULTY
다음 중 하나:
A. 사용자가 명시적으로 고난도 집중 대상으로 지정
B. 현재 학교자료/기출/N° QA에서 반복적으로 고난도 혼동이 확인
C. 3개 이상의 판단축이 동시에 필요
D. 같은 사실을 알아도 조건/관점/자료에 따라 정답이 달라질 수 있음
E. 유사 개념·단체·사상·과정의 경계가 핵심 평가요소

HIGH_DIFFICULTY는 반드시 DEPTH_REASON과 DEPTH_EVIDENCE를 가진다.
근거 없이 '어려워 보인다'는 이유로 승격 금지.

## 4. HIGH_DIFFICULTY DEPTH STACK
HIGH_DIFFICULTY cluster는 범위 안에서 필요한 판단축을 선택적으로 확장한다.
아래 stack은 student-facing 소제목 목록이 아니라 내부 검토축이다.
여러 관련 concept에 동일 stack을 반복하지 말고 chapter backbone 안에서 통합한다.

1. FOUNDATION
기본 정의/원리. 이미 아는 내용도 고난도 판단의 기준이 되는 최소 수준으로 고정.

2. CONDITIONS
결론이 달라지는 조건, 예외, 전제.

3. BOUNDARIES
비슷한 개념과 어디서 갈리는지.
공통점만이 아니라 차이를 만드는 판단축.

4. HIDDEN_ASSUMPTIONS
문제에서 생략되기 쉬우나 판단에 필요한 전제.
단, 학교자료/현재 교육과정 범위 안에서만.

5. TRAP LOGIC
학생이 왜 틀리는지.
'오답 문장'을 외우는 것이 아니라 잘못된 판단 경로를 설명.

6. MULTI-STEP APPLICATION
자료 → 개념 선택 → 조건 확인 → 결론처럼 실제 고난도 문제의 사고 흐름.
완성 문제를 매번 넣지는 않는다.

7. CROSS-LINK
관련 concept와의 연결.
학생용에 내부 ID는 보이지 않게 자연스러운 본문/비교로 처리.

모든 항목을 기계적으로 7블록으로 출력하지 않는다.
학생용에서는 필요한 부분을 본문·표·짧은 보조 블록으로 자연스럽게 편집한다.

## 5. DEPTH BUDGET
세트 전체를 HIGH_DIFFICULTY로 만들지 않는다.
또한 한 HIGH_DIFFICULTY cluster 안의 모든 concept를 별도 장문 설명으로 만들지 않는다.

기본 원칙:
- STANDARD가 가장 많아도 정상
- ADVANCED는 실제 비교/적용이 필요한 부분
- HIGH_DIFFICULTY는 시험에서 변별력이 생기는 핵심만
- 사용자가 특정 단원을 지정하면 해당 범위에서는 HIGH_DIFFICULTY 비중을 높일 수 있음

깊이 때문에 전체 CORE가 불필요하게 장문화되면 DEPTH_BUDGET_FAIL.
HIGH_DIFFICULTY가 아닌 concept까지 주변 설명이 늘어나지 않게 한다.

## 6. SUBJECT DEPTH PROFILE

### SOCIAL
사용자 지정 우선 HIGH_DIFFICULTY 후보:
- 칸트·베카리아 형벌/사형 논쟁

이 영역에서 우선 확인할 DEPTH_AXES:
- 형벌의 정당화 근거
- 형벌의 목적
- 범죄자 책임과 자유로운 행위
- 인간을 수단으로 대하는 문제
- 비례성의 의미와 근거
- 사형에 대한 논증
- 사회계약과 형벌권
- 상대 입장 비판의 정확한 범위
- 실제 주장 vs 정당한 함의 vs 허수아비 비판

금지:
- 범위 밖 철학사로 깊이를 가장함
- 베카리아를 unrestricted utilitarian으로 단순화
- 칸트를 '사회적 효과를 전혀 고려하지 않는 사람'처럼 과장
- 사형 찬반만 암기시키고 논증 구조를 생략

사회 다른 concept는 학교자료/기출/QA evidence가 있을 때 ADVANCED/HIGH_DIFFICULTY로 승격한다.

### SCIENCE
사용자 지정 HIGH_DIFFICULTY:
- OR 산화·환원
- EM 전자기 유도

#### OR 산화·환원
현재 SCIENCE_MASTER 범위 안에서 우선 DEPTH_AXES:
- 산소 이동과 전자 이동의 연결/구분
- 금속과 금속 이온 사이 전자 이동
- 산화되는 물질 / 환원되는 물질 판별
- 금속 반응성 관계 추론
- 실험 결과에서 미지 금속 관계 추론
- 양이온 수 vs 전체 이온 수
- spectator ion 조건
- 반응 전후 입자 수
- 순차 투입/완결 조건
- 그래프 해석
- 금속판 질량 변화의 조건 의존성
- 색 변화/석출과 실제 반응의 연결
- REDOX_LEDGER 기반 정량 일관성

ADVANCED LEAK BLOCK은 그대로 유지:
자기선속·유도기전력 공식, 몰/원자량 화학량론, 한계반응물, 전지전위, 복잡한 산화수·반쪽반응 계산 등은 깊이 확장을 이유로 정답 필수지식에 포함하지 않는다.

#### EM 전자기 유도
현재 SCIENCE_MASTER 범위 안에서 우선 DEPTH_AXES:
- 자석과 코일의 상대 운동
- 접근/이탈, 방향 변화에 따른 유도 현상 비교
- 이동 속력과 유도 효과의 세기 관계
- 코일 감은 수 변화
- 운동 방향과 전류 방향 판단
- 복수 조건 변화
- 개회로/폐회로에서 관찰되는 차이
- 발전기의 운동과 전기 에너지 전환
- 시간에 따른 운동/관찰량 그래프
- '움직인다' 자체가 아니라 자기적 상태 변화가 필요한 상황 구분

금지:
- 자기선속·패러데이 법칙 수식 계산을 고1 필수지식으로 요구
- 토크/회로방정식 등 ADVANCED LEAK
- 그림 방향이 불명확한 상태에서 오른손/렌츠 법칙 판단을 확정

과학 HIGH_DIFFICULTY는 시각자료/자료해석을 설명에 적극 포함하되 장식 visual은 금지.

### KOREAN
CORE source emphasis:
1. 학교 보충자료/학교 학습지의 작품 해석·비교·강조점
2. 사용자가 직접 제공한 보충자료
3. 교과서/학습활동은 기본 원문·기초 개념·빈틈 보완
4. 외부 해설은 검증 보조

교과서 내용을 기계적으로 재요약하지 않는다.
보충자료가 이미 교과서 기본 개념을 전제로 심화 해석을 제공하면 그 해석 구조를 CORE의 중심으로 삼는다.

HIGH_DIFFICULTY 후보:
- 보충자료에서 비교축이 여러 개인 작품
- 관찰 사실과 화자의 추론 구분
- 표현법과 실제 효과의 연결
- 부분 정서와 작품 전체 태도의 구분
- 두 작품 공통점/차이의 근거 범위
- <보기>를 통한 해석 적용
- 문학+비문학 비교 또는 복수 근거 통합

국어 HIGH_DIFFICULTY도 작품 밖 지식 확장으로 깊이를 만들지 않는다.
SOURCE_TEXT_BLOCK과 학교 보충자료의 실제 표현/해석을 근거로 한다.

### HISTORY
기본적으로 사전 HIGH_DIFFICULTY 단원을 고정하지 않는다.
현재 학교자료/교과서/기출을 읽고 혼동 밀도를 분석해 자동 승격한다.

HISTORY_DIFFICULTY_SIGNAL:
- 비슷한 이름/목표의 단체가 여러 개
- 단체의 결성·분화·통합이 연속
- 민족주의/사회주의/민족협동전선 등 세력 관계를 함께 봐야 함
- 같은 시기에 여러 운동/정책이 겹침
- 연도 암기보다 선후·동시성 판단이 중요
- 사료의 주체를 직접 말하지 않고 간접 단서로 식별
- 정책 이름/시기/주체/목표가 교차하기 쉬움
- 지도·지역과 사건을 함께 판단
- 인물의 활동이 여러 단체/시기에 걸침

3개 이상 signal이 한 concept cluster에 모이면 HIGH_DIFFICULTY 후보.
2개면 ADVANCED 후보.
단, 학교자료/시험범위 evidence가 있어야 확정한다.

HIGH_DIFFICULTY HISTORY 처리:
- 먼저 cluster의 CENTRAL_QUESTION을 정하고 시간축/인과/세력 관계 중 지배적 구조를 선택
- 사건을 개별 암기 카드로 쪼개지 않음
- 시간축 + 주체 + 목표 + 관계를 함께 설명
- 필요한 경우 비교표/연표/관계도
- '누가 언제 무엇을 왜 했는지'의 교차 혼동을 TRAP 근거로 사용

### AI
현재는 자동 depth assignment.
알고리즘 단계, 탐색 순서, 전처리 순서처럼 sequence/condition이 핵심이면 ADVANCED 후보.
사용자 지정이 없으면 HIGH_DIFFICULTY를 과도하게 만들지 않는다.

## 7. SOURCE-BASED DEPTH
깊이는 외부 일반지식의 양으로 결정하지 않는다.
DEPTH_EVIDENCE 우선순위:
1. 사용자 명시
2. 현재 학교자료/보충자료
3. 현재 교과서/학습활동
4. 실제 학교 기출/검수 결과
5. 검증된 N° 오류/오답 패턴
6. 공식 외부자료

외부 자료만으로 학교 범위를 확장하는 것은 금지.

## 8. N° CONNECTION
DEPTH_PRIORITY는 향후 N° Generator의 문항 설계 참고 metadata로 사용할 수 있다.

예:
STANDARD → foundation/application 후보
ADVANCED → application/integration 후보
HIGH_DIFFICULTY → high/integration 후보

하지만:
- CORE 학생용에 DEPTH_PRIORITY 노출 금지
- HIGH_DIFFICULTY라고 해서 N° 고난도 문항을 반드시 일정 수 생성할 필요 없음
- 실제 N° blueprint와 난도 엔진이 최종 결정

## 9. QA
필수:
CLUSTER_DEPTH_ASSIGNMENT = PASS
DEPTH_ASSIGNMENT = PASS
DEPTH_EVIDENCE = PASS
DEPTH_SCOPE_SAFETY = PASS
DEPTH_BUDGET = PASS
HIGH_DIFFICULTY_COMPLETENESS = PASS/NOT_APPLICABLE

HIGH_DIFFICULTY_COMPLETENESS:
- 기본 원리 누락 없음
- 조건/경계/함정 중 실제 필요한 축 반영
- 범위 밖 심화로 어려움을 가장하지 않음
- 설명만 길고 판단축이 늘지 않는 경우 FAIL
- student-facing 출력이 7개 고정 블록처럼 보이면 EDITORIAL_REVISE

END ARC CORE DEPTH ENGINE V1.1
