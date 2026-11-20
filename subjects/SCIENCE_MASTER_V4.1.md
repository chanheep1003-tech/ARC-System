# 00_ACTIVE_통합과학2_동북고_MASTER_V4.1
# VERSION_DATE: 2026-11-19
# SUPERSEDES: archive/subjects/SCIENCE_MASTER_V4.0.md (archived)
# CHANGE: 기말 범위(A~D 파트 쪽수)로 SCOPE LOCK 교체, 서술형 규칙 신설, N° 수량·난도 요청별, FINAL 앵커 정책, 인쇄 무결성
# BASE: manifest-selected common generation engine
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

## 1. SCOPE LOCK — 2026학년도 2학기 기말 (학교 공지 2026-11-13)
범위의 유일한 근거: `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml` + `ops/exams/EXAM_CONTEXTS_V1.yaml` (SCI)
- A: 교과서 110~117쪽, 134~137쪽, 144~149쪽
- B: 교과서 46~62쪽
- C: 교과서 70~95쪽, 130~133쪽
- D: 교과서 98~101쪽, 150~154쪽
- 시험 구조: 선택형 24문항(80점) + 서술형 4문항(20점)

단원 주제 이름은 이 문서에서 추정하지 않는다. Drive의 교과서 해당 쪽을 열어 파트별 개념 목록을 source registry에 등록한 뒤 출제한다.
중간고사 단원 구조(§4의 GT p14~19, EV p20~35, OR p38~45, EE p82~91, EM p102~109)는 기말 범위와 **쪽수가 겹치는 부분만** 구조 참고로 쓴다.
현재 겹치는 쪽: EE p82~91 ⊂ C(70~95쪽). 나머지 중간고사 단원(GT·EV·OR·EM p102~109)은 `EXAM_SCOPE=ARCHIVED_REPLAY` 요청에서만 쓴다.
특정 파트 요청 시 그 파트 밖 지식으로 정답을 결정하지 않는다. 상위학년 자료는 구조만 참고한다.

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
20문항 기준 권장 최소 (문항 수가 다르면 비례 조정, 소수점 올림):
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

## 3A. 수량·난도 — V4.1
- ARC_N: 문항 수·난도 분포·서술형 수는 요청마다 계획 카드(`arc.py plan --subject SCI …`)가 정한다.
- ARC_FINAL: 선택형 24(80점) + 서술형 4(20점) 고정. 파트 배분은 학교 공지에 없으므로 쪽수 비중에 비례해 계획에 적고 사용자 확인을 받는다.
- ARC_FINAL 난도: 동북고 실제 기출과 같거나 살짝 더 어렵게. 기말 전 범위 앵커 `quality/anchors/SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml`(중심 평균 2.46, 목표 2.51~2.66, 2026-11-20 등록).
  난도는 전자기·산화환원식 정량 자료형, 양이온 수 변화, 그래프 해석에서 만든다. 지질·기후 단순 확인 문항만 늘려 쉬워지지 않게 한다.
  `SCI_REDOX_…` 앵커는 산화·환원 단원 전용이다.

## 3B. 서술형 — V4.1
- FINAL 4문항(합계 20점), N°는 계획 수만큼.
- 필수 필드: `conditions`, `model_answer`, `accepted_variants`, `rubric`(부분점수), `points`, `answer_targets`.
- 정량 서술형: 풀이 과정·단위·유효 조건을 채점 기준에 나눠 적는다(예: 관계식 1점, 대입 1점, 답과 단위 1점).
- 자료 해석 서술형: 자료에서 읽어야 할 근거 값/경향을 채점 요소로 명시한다.
- 서술형 답(핵심 용어·수치)이 같은 시험지 선택형 선지·자료에 그대로 나오면 `CROSS_ITEM_ANSWER_LEAK`.

## 4. UNIT STRUCTURE ROTATION (중간고사 단원 구조 — 기말과 겹치는 쪽만 참고)
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
manifest-selected 공통 엔진의 HANDOFF_META + SECTION A~D를 그대로 따른다.
ANSWER_KEY는 Generator/Publisher 검증용 잠금 데이터이며, ARC_N에서는 활성 PDF master에 따라 문제지 뒤의 필수 완전 공백 페이지 다음 compact answer section으로 정확히 삽입한다. 문제 페이지에는 노출하지 않는다.
FINAL 요청은 PRODUCT_MODE=ARC_FINAL로 처리하고 별도 FINAL 프롬프트를 사용하지 않는다.

## 12. GOLD STANDARD ANCHORS
필수 로드: `quality/gold/SCI_GOLD_ANCHORS_V1.0.md`
GOOD/BAD 앵커와 비교한 뒤 문항의 자료 기능, 추론 단계, 오답 강도를 판정한다.
직접개념형이 BAD 앵커와 가까우면 PREMIUM 금지 및 V1.1 점수 상한을 적용한다.


## EXECUTABLE VISUAL GATE — V1.0
필수 참조:
- quality/visual/ARC_VISUAL_RENDERER_POLICY_V1.0.md
- quality/visual/ARC_VISUAL_PASS_AB_V1.0.md
- quality/ARC_VISUAL_TEMPLATE_SYSTEM_V1.1.md
- quality/ARC_VISUAL_AUTHENTICITY_RUBRIC_V1.1.md

SCI-GRAPH는 수치 배열에서 deterministic chart로 렌더한다.
SCI-PARTICLE는 freehand/생성형 이미지로 만들지 않고 species/count 기반 deterministic SVG를 사용한다.
SCI-EXPERIMENT는 element/connection/direction spec이 완전해야 렌더한다.

산화·환원 입자모형:
- REDOX_LEDGER를 문항 검증에서 독립 생성
- visual spec의 before/after species count와 대조
- actual rendered element count와 다시 대조
- electron conservation / cation count / total ion count를 분리 확인
- REDOX_VISUAL_CROSSCHECK=PASS 필수

ESSENTIAL visual은 VISUAL_PASS_A, VISUAL_PASS_B, QUESTION_VISUAL_CROSSCHECK가 모두 PASS가 아니면 BANK/FINAL 후보가 아니다.


## 13. PRINT-EXAM INTEGRITY — V4.1
생산 파이프라인 `PRINT_INTEGRITY_GATE`(선지 문자 오류·세트 내 답 유출) FAIL이면 CONTENT_LOCK 금지.
