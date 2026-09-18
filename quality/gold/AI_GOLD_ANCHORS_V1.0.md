# AI GOLD ANCHORS V1.0
SUBJECT: 인공지능기초
SCOPE: AI_MASTER_V4.0
ANCHOR_POLICY: ARC_GOLD_ANCHOR_POLICY_V1.0

## GOOD

### AI-G-001 — DFS/BFS 규칙 명시
EXPECTED_ITEM: 93~96
EXPECTED_COMMERCIAL: 92~95
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

그래프의 인접 관계가 다음과 같고, 같은 깊이/인접 후보가 여러 개면 알파벳 순으로 방문한다.
S: A, B
A: C, D
B: D
C: 없음
D: 없음
이미 방문한 노드는 다시 방문하지 않는다.

S에서 시작한 BFS의 방문 순서는?
1. S-A-C-D-B
2. S-A-B-C-D
3. S-B-A-D-C
4. A-B-C-D-S
5. S-A-B-D-C
ANSWER: 2
WHY_GOOD:
- ADJACENCY_ORDER/visited rule 명시.
- 공유 노드 D 때문에 규칙 추적 필요.
- 단순 트리 암기보다 실제 traversal 수행.

### AI-G-002 — 전처리/EDA/학습 구분
EXPECTED_ITEM: 92~95
EXPECTED_COMMERCIAL: 92~94
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

어떤 학생이 데이터 분석을 다음 순서로 수행했다.
(가) 결측치와 중복 행을 확인해 처리했다.
(나) 변수별 분포와 두 변수 사이의 관계를 그래프로 살펴보았다.
(다) 입력과 정답 데이터를 이용해 모델의 규칙을 학습시켰다.

(가)~(다)에 대한 설명으로 가장 적절한 것은?
1. (가)는 전처리, (나)는 탐색적 데이터 분석, (다)는 모델 학습에 해당한다.
2. (가)와 (나)는 모두 모델 학습이므로 구분할 필요가 없다.
3. (나)는 결측치를 제거하는 과정만을 의미한다.
4. (다)는 데이터 수집 이전에 수행되어야 한다.
5. (가)는 학습된 모델의 정확도를 계산하는 단계이다.
ANSWER: 1
WHY_GOOD:
- 세 단계의 기능을 비교.
- 용어 암기보다 과정 순서와 역할을 구분.

### AI-G-003 — 상관과 인과
EXPECTED_ITEM: 92~94
EXPECTED_COMMERCIAL: 92~94
EXPECTED_DECISION: BANK_A
DIFFICULTY: D3~D4

학교 데이터에서 하루 평균 운동 시간과 심폐 지구력 점수 사이에 양의 상관관계가 관찰되었다.
이 결과만으로 말할 수 있는 것으로 가장 적절한 것은?
1. 운동 시간이 늘어나면 다른 조건과 무관하게 모든 학생의 점수가 반드시 오른다.
2. 두 변수 사이에 함께 증가하는 경향이 관찰되었지만, 이것만으로 운동 시간이 점수 상승의 유일한 원인이라고 확정할 수는 없다.
3. 상관관계가 있으므로 두 변수는 같은 데이터를 의미한다.
4. 양의 상관이면 두 변수의 측정 단위도 같아야 한다.
5. 상관관계가 관찰되면 추가 분석은 필요 없다.
ANSWER: 2
WHY_GOOD:
- 상관 해석 범위를 판단.
- 1, 5는 실제 과잉추론 함정.
- 현재 범위의 데이터 해석 역량을 측정.

## BAD

### AI-B-001 — 너무 단순한 트리 DFS
EXPECTED_MAX_ITEM: 83
EXPECTED_DECISION: REVISE
DEFECT: DIRECT_TRAVERSAL_RECALL
문제: S의 자식 A,B, A의 자식 C,D인 단순 트리에서 "왼쪽 우선 DFS 순서"를 한 번 추적하게 함.
WHY_BAD:
- 기초 연습용으로는 가능하나 PREMIUM 근거 없음.
- 분기/재방문/조건 판단이 거의 없음.

### AI-B-002 — 방문순서 조건 누락
EXPECTED_DECISION: DISCARD
DEFECT: DFS_BFS_UNDERSPECIFIED
문제: 한 노드에서 여러 인접 노드가 가능한 그래프를 주고 인접 방문 우선순위를 지정하지 않은 채 유일한 DFS 순서를 요구.
WHY_BAD:
- 복수정답 가능.
- AI_MASTER hard fail.

### AI-B-003 — 상관=인과
EXPECTED_DECISION: DISCARD
DEFECT: CORRELATION_CAUSATION
문제: 두 변수 사이 상관계수가 양수라는 사실만으로 한 변수가 다른 변수의 원인임을 정답으로 처리.
WHY_BAD:
- DATA SAFETY 위반.
- 자료가 허용하는 결론 범위를 초과.
