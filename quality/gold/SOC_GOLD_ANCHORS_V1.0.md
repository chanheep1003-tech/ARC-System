# SOC GOLD ANCHORS V1.0
SUBJECT: 통합사회2
SCOPE: SOCIAL_MASTER_V4.0
ANCHOR_POLICY: ARC_GOLD_ANCHOR_POLICY_V1.0
NOTE: C파트 USER_X_EXCLUSION은 모든 앵커보다 우선. X영역은 앵커로도 직접 사용하지 않음.

## GOOD

### SOC-G-001 — 평균 경향과 개인 일반화
EXPECTED_ITEM: 92~95
EXPECTED_COMMERCIAL: 92~95
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

두 집단에 동일한 분류 과제를 제시했다.
| 집단 | 개별 대상의 속성을 중심으로 분류 | 주변 대상과의 관계를 중심으로 분류 |
|---|---:|---:|
| X | 72% | 28% |
| Y | 39% | 61% |

이에 대한 해석으로 가장 적절한 것은?
1. X의 모든 사람은 반드시 속성 중심으로 사고한다.
2. Y의 모든 사람은 관계 중심 분류만 할 수 있다.
3. 집단 수준의 경향 차이는 말할 수 있지만 이를 각 개인에게 예외 없이 적용할 수는 없다.
4. X의 방식은 객관적이고 Y의 방식은 비합리적이라고 결론 내릴 수 있다.
5. 이 결과만으로 두 집단의 차이를 하나의 원인으로 확정할 수 있다.
ANSWER: 3
WHY_GOOD:
- 표 해석 + 평균→개인 일반화 오류 판별.
- 4, 5는 가치판단/단일원인 과잉추론 함정.
- 자료가 정답 경로에 필수.

### SOC-G-002 — 세계화 자료의 수준/비율 구분
EXPECTED_ITEM: 92~94
EXPECTED_COMMERCIAL: 92~94
EXPECTED_DECISION: BANK_A
DIFFICULTY: D4

어느 기업의 생산 구조 변화이다.
- 시기 A: 연구·설계, 부품 생산, 조립이 한 국가에 집중.
- 시기 B: 연구·설계는 본국, 부품 생산은 여러 국가, 조립은 임금이 낮은 국가들에 분산.

이에 대한 설명으로 가장 적절한 것은?
1. 시기 B에서는 생산 기능의 공간적 분업이 강화되었다고 볼 수 있다.
2. 시기 B에서는 모든 생산 기능이 본국으로 회귀하였다.
3. 시기 A와 B의 차이는 지역 간 상호의존과 무관하다.
4. 시기 B의 조립 지역은 반드시 세계도시의 최상위 계층이다.
5. 시기 B가 나타났다는 사실만으로 모든 국가의 소득 격차가 감소했다고 결론 낼 수 있다.
ANSWER: 1
WHY_GOOD:
- 공간적 분업 개념을 새 사례에 적용.
- 4, 5는 스케일/인과 과잉 일반화.
- 단순 용어 암기보다 구조 변화를 읽어야 함.

### SOC-G-003 — 복수 기준 판단
EXPECTED_ITEM: 91~94
EXPECTED_COMMERCIAL: 91~94
EXPECTED_DECISION: BANK_A
DIFFICULTY: D3~D4

어떤 정책을 평가하는 두 학생의 주장이다.
갑: "총비용 대비 편익이 커지는지를 먼저 보아야 한다."
을: "정책의 부담이 특정 집단에 과도하게 집중되는지도 보아야 한다."

이에 대한 설명으로 가장 적절한 것은?
1. 갑과 을은 서로 다른 평가 기준을 사용하므로 주장과 근거를 구분해 비교할 필요가 있다.
2. 서로 다른 기준을 사용하면 둘 중 하나는 반드시 사실을 왜곡한다.
3. 효율성을 고려하면 공정성은 판단할 수 없다.
4. 공정성을 고려하면 비용과 편익은 언제나 무의미하다.
5. 두 기준은 어떤 사례에서도 반드시 같은 결론을 낳는다.
ANSWER: 1
WHY_GOOD:
- 기준 차이를 인식한 뒤 주장-근거 관계를 판단.
- 결론 일치 여부와 근거 일치 여부를 구분.

## BAD

### SOC-B-001 — 평균을 개인에게 확정
EXPECTED_DECISION: DISCARD
DEFECT: AVERAGE_TO_INDIVIDUAL
문제: 집단 X의 관계 중심 응답 비율이 높다는 자료만으로 "X의 모든 개인은 관계 중심으로 사고한다"를 정답 처리.
WHY_BAD:
- 자료가 허용하는 추론 범위를 넘어감.
- 현재 MASTER의 명시적 금지 패턴.

### SOC-B-002 — 자료 없어도 풀리는 표
EXPECTED_MAX_ITEM: 82
EXPECTED_DECISION: REVISE
DEFECT: DECORATIVE_DATA
문제: 인구/세계화 표를 길게 제시하지만 정답은 '세계화는 상호의존을 높일 수 있다'라는 일반 정의만 알면 해결됨.
WHY_BAD:
- 자료가 기능하지 않음.
- 읽기 노동만 늘림.

### SOC-B-003 — C파트 X영역 사용
EXPECTED_DECISION: DISCARD
DEFECT: USER_X_EXCLUSION_VIOLATION
문제: C파트 학습지에서 사용자가 손으로 X 표시한 개념·사례를 정답 근거 또는 필수 오답 지식으로 사용.
WHY_BAD:
- 최상위 SCOPE hard fail.
- 점수와 무관하게 BANK 금지.
