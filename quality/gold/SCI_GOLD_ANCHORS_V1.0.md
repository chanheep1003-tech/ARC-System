# SCI GOLD ANCHORS V1.0
SUBJECT: 통합과학2
SCOPE: SCIENCE_MASTER_V4.0
ANCHOR_POLICY: ARC_GOLD_ANCHOR_POLICY_V1.0
NOTE: 수치·자료는 ARC 생성 데이터이며 실제 교과서 도표를 복제하지 않음.

## GOOD

### SCI-G-001 — 반응성 관계 추론
EXPECTED_ITEM: 93~96
EXPECTED_COMMERCIAL: 93~95
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

금속 A, B, C와 각 금속 이온 수용액으로 다음 실험을 했다.
- A를 B 이온 수용액에 넣었더니 A 표면에 변화가 나타나며 반응하였다.
- C를 A 이온 수용액에 넣었더니 반응하지 않았다.
- B를 C 이온 수용액에 넣었더니 반응하였다.

이에 대한 판단으로 옳은 것만 고른 것은?
ㄱ. A는 B보다 반응성이 크다.
ㄴ. B는 C보다 반응성이 크다.
ㄷ. C는 A보다 반응성이 크다.
1. ㄱ
2. ㄴ
3. ㄱ, ㄴ
4. ㄱ, ㄷ
5. ㄱ, ㄴ, ㄷ
ANSWER: 3
WHY_GOOD:
- 세 실험을 방향관계로 바꾸는 과정 필요.
- 단일 관찰 암기가 아니라 transitive reasoning.
- ㄷ은 방향 역전 오답.

### SCI-G-002 — 자연선택 자료 해석
EXPECTED_ITEM: 92~95
EXPECTED_COMMERCIAL: 92~94
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

같은 종의 세균 집단을 두 환경에서 여러 세대 배양했다.
| 환경 | 처음 내성 개체 비율 | 여러 세대 뒤 |
|---|---:|---:|
| 항생제 없음 | 4% | 5% |
| 항생제 지속 | 4% | 68% |

이 자료로 설명할 수 있는 것으로 가장 적절한 것은?
1. 항생제가 모든 세균에 동일한 내성 유전자를 새로 만들었다.
2. 항생제가 있는 환경에서 기존 변이 중 내성 개체의 상대적 생존·번식이 유리했음을 추론할 수 있다.
3. 내성 비율 증가는 개별 세균이 필요에 따라 형질을 바꾼 결과임을 증명한다.
4. 두 환경의 결과가 다르므로 내성은 유전과 무관하다.
5. 항생제가 없는 환경에서도 내성 비율이 반드시 68%까지 증가해야 한다.
ANSWER: 2
WHY_GOOD:
- 두 조건 비교가 정답 경로에 필수.
- 개체 변화 vs 집단 비율 변화 오개념을 오답화.
- 단순 '자연선택 정의' 암기보다 자료 해석 요구.

### SCI-G-003 — 전자기 유도 조건 결합
EXPECTED_ITEM: 92~95
EXPECTED_COMMERCIAL: 92~95
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

같은 자석과 같은 코일을 사용한 세 실험이다.
| 실험 | 자석 이동 | 이동 속력 | 코일 감은 수 |
|---|---|---|---|
| I | 코일 쪽으로 | v | N |
| II | 코일 쪽으로 | 2v | N |
| III | 코일에서 멀어지게 | 2v | 2N |

전류계의 편향 방향과 크기를 비교할 때 옳은 설명은?
1. I과 II는 방향이 반대이고 크기는 같다.
2. I과 II는 방향이 같고, II의 효과가 더 크게 나타날 수 있다.
3. II와 III는 이동 속력이 같으므로 방향과 크기가 모두 반드시 같다.
4. III은 감은 수가 많으므로 자석 이동 방향과 무관하게 II와 같은 방향이다.
5. 감은 수는 유도 현상과 아무 관련이 없다.
ANSWER: 2
WHY_GOOD:
- 방향과 세기 변인을 분리해 판단.
- 3, 4가 조건 일부만 맞는 HALF_TRUE.
- 고급 자기선속 공식을 요구하지 않음.

## BAD

### SCI-B-001 — 정의 매칭
EXPECTED_MAX_ITEM: 83
EXPECTED_DECISION: REVISE
DEFECT: DIRECT_RECALL
문제: "표준화석의 특징으로 옳은 것은?"을 묻고 정답 외 선지를 절대연령 계산, 특정 환경만 서식 등 명백한 오답으로 구성.
WHY_BAD:
- 한 개념의 정의 재생만 요구.
- 자료/조건 없음.

### SCI-B-002 — 장식용 숫자
EXPECTED_MAX_ITEM: 82
EXPECTED_DECISION: REVISE
DEFECT: DECORATIVE_DATA
문제: 세균 내성 비율을 2%→70%로 제시하지만 실제 정답은 숫자를 보지 않아도 '자연선택은 기존 변이에 작용한다'를 고르면 됨.
WHY_BAD:
- 수치가 풀이에 기능하지 않음.
- 자료형처럼 보이는 직접개념 문제.

### SCI-B-003 — 근거 없는 질량 변화
EXPECTED_DECISION: DISCARD
DEFECT: MASS_CHANGE_UNDERCONDITIONED
문제: 금속 A가 B 이온을 석출시킨다는 사실만 주고 "금속판의 질량은 반드시 증가한다"를 정답으로 요구.
WHY_BAD:
- 상대 질량/반응량 조건이 없음.
- SCIENCE_MASTER의 MASS SAFETY 위반.
