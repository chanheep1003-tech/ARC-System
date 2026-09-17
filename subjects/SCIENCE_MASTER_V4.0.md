# 00_ACTIVE_통합과학2_동북고_MASTER_V4.0
# BASE: ARC COMMON GENERATION ENGINE V4.0
# PRODUCT_MODE: ARC_N / ARC_FINAL inherited
# MODE: CONTENT GENERATION ONLY

## 0. DRIVE FIRST
ROOT: `/Google Drive/N제 시스템/02_통합과학`
우선순위:
1) 학교자료/현재 학습지
2) 교과서
3) 2025 동북고 실제 중간고사 `1hq43RSKzn2kqDqMI7HsrrLyDSiHkR3cB`
4) 요청 단원 최신 BANK/외부자료 색인
5) 그래프·이미지·실험자료 색인
6) 문제집·참고자료
7) 오류사례·금지패턴
8) 우수문항·벤치마크

요청 단원과 직접 관련 없는 단원은 불필요하게 읽지 않는다.

## 1. SCOPE LOCK
GT p14~19 지질 시대
EV p20~35 진화·생물다양성
OR p38~45 산화·환원
EE p82~91 지구 환경 변화
EM p102~109 전자기 유도·발전

특정 단원 요청 시 그 단원 밖 지식으로 정답을 결정하지 않는다.
상위학년 자료는 구조만 참고한다.

## 2. DONGBOOK SCIENCE DNA
- 그림/실험/표/그래프 비중 높음
- ㄱㄴㄷ 적극 사용하되 전 문항 강제 금지
- 조건 변화/미지 대상/전후 비교
- 결과→원인 역추론
- 정량+정성 결합
- 생활·탐구 맥락
- 쉬운 문항과 고난도 문항 혼합

20문항 이상이면 가능한 범위에서 최소 8종 이상의 문항 구조를 사용한다.
초반 1~6번을 정의·암기 문제로만 채우지 않고 4번 이내부터 자료형을 섞는다.

## 3. VISUAL QUOTA
20문항 기준 권장 최소:
- MATERIAL_BASED_COUNT ≥ 10
- TRUE_VISUAL_PLANNED ≥ 6
- TRUE_VISUAL_ESSENTIAL ≥ 4

TRUE_VISUAL 6개에는 가능하면:
- graph ≥ 1
- particle_model ≥ 1
- experiment_diagram 또는 reaction_before_after ≥ 1
- flowchart/process/composite ≥ 1

DATA_TABLE은 TRUE_VISUAL로 집계하지 않는다.
SPEC_ONLY를 RENDERED로 표기하지 않는다.

## 4. UNIT STRUCTURE ROTATION
### OR 산화·환원
산소 이동 / 전자 이동 / 금속-금속이온 / 반응성 서열 / 미지 금속 / 양이온 수 / 전체 이온 수 / 입자모형 / 순차 투입 / 그래프 / 금속판 질량 변화 / 색 변화·석출 / 반응 전후 / 변인 통제 / 가설 검증 / 생활·제련 맥락.

20문항이면 최소 8종 구조 사용.
권장: DIRECT_BASIC 3~4 / REACTION_OBSERVATION 2~3 / REACTIVITY_INFERENCE 3~4 / ION_COUNT_OR_PARTICLE 3~4 / GRAPH_OR_SEQUENCE 2~3 / EXPERIMENT_HYPOTHESIS 2 / INTEGRATED_HIGH 1~2.

### EV
변이 / 자연선택 / 내성 / 비율그래프 / 종다양성 / 유전적다양성 / 단편화 / 생태통로 / 외래종.

### GT
표준화석 / 시상화석 / 연대표 / 환산 / 대멸종 / 생물다양성 그래프 / 화석 생성 / 회복구간.

### EE
복사평형 / 열수지 / 알베도 / 온실효과 / 대기대순환 / 무역풍 / 용승 / 엘니뇨·라니냐 / SST 편차 / 시계열.

### EM
자석·코일 이동 / 감은 수 / 속력 / 방향 / 세기 / 복수코일 / 발전기 / 에너지전환 / 개회로-폐회로 / 시간그래프.

## 5. ADVANCED LEAK BLOCK
정답에 필요하도록 만들지 말 것:
자기선속·유도기전력 공식 / 토크·회로방정식 / 몰·원자량 화학량론 / 한계반응물 / 전지전위 / 복잡한 산화수·반쪽반응 계산 / 하디-바인베르크 / 전사·번역 / 개체군 증가방정식 / 방사성동위원소 절대연령 계산 / 지구과학 심화공식.

## 6. REDOX QUANTITATIVE AUDIT
산화·환원 정량 문항은 내부 `REDOX_LEDGER` 필수:
OXIDIZED_SPECIES / REDUCED_SPECIES / ELECTRONS_LOST / ELECTRONS_GAINED / INTEGER_RATIO / INITIAL_CATIONS / FINAL_CATIONS / SPECTATOR_IONS / TOTAL_IONS_BEFORE / TOTAL_IONS_AFTER / MASS_CHANGE_BASIS / COMPLETION_CONDITION.

전자수 보존을 먼저 맞춘 뒤 이온 수·입자 수·질량 변화를 판단한다.

## 7. REACTIVITY ORDER AUDIT
실험 결과를 방향관계로 바꿔 transitive closure를 수행한다.
전체 순서를 묻는 경우 모든 대상의 순서가 하나로 결정될 때만 출제한다.
부분 관계만 결정되면 ‘반드시 옳은 것/알 수 있는 관계’형으로 바꾼다.

## 8. MASS / COMPLETION / SPECTATOR SAFETY
금속판 질량 변화는 반응성만으로 단정 금지. 상대질량/질량비/실제 질량/입자 수 근거가 있어야 한다.
정량 문항은 충분한 양/제한 시약/완결 여부/남은 물질을 명시한다.
전체 이온 수를 물으면 spectator ion의 종류·수 또는 계산에 필요한 조건을 명확히 한다.
전체 양이온 수와 전체 이온 수를 혼동하지 않는다.

## 9. INDEPENDENT VERIFICATION
공통 PASS A/B에 더해 검사:
- REDOX_LEDGER 정확성
- 반응성 관계 유일성
- 질량 변화 근거 충분
- 반응 완결 조건 충분
- spectator ion 조건 충분
- 그래프/표/입자모형 수치 일치

불일치 문항은 폐기 또는 재작성.

## 10. QC_STATUS ADDITIONS
REDOX_LEDGER: PASS/N.A.
REACTIVITY_ORDER_AUDIT: PASS/N.A.
MATERIAL_BASED_COUNT: x/n
TRUE_VISUAL_PLANNED: x/n
TRUE_VISUAL_ESSENTIAL: x/n
GRAPH_COUNT: x
PARTICLE_MODEL_COUNT: x
EXPERIMENT_DIAGRAM_COUNT: x
DATA_TABLE_COUNT: x
VISUAL_RENDER: PENDING_PDF (SPEC_ONLY일 때)

## 11. ARC HANDOFF
공통 엔진 V4.0의 HANDOFF_META + SECTION A~D를 그대로 따른다.
ANSWER_KEY는 검증용이며 ARC_N 학생 PDF에는 넣지 않는다.
FINAL 요청은 PRODUCT_MODE=ARC_FINAL로 처리하고 별도 FINAL 프롬프트를 사용하지 않는다.
