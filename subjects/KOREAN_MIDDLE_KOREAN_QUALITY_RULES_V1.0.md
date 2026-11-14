# ARC KOREAN — MIDDLE KOREAN ITEM QUALITY RULES V1.0
VERSION: 1.0-dev
DATE: 2026-11-07
STATUS: ACTIVE-DEV / MANIFEST_REGISTERED (runtime.korean_middle_korean_policy) / REGRESSION_NOT_EXECUTED
PRODUCT: ARC_N / ARC_FINAL
CURRICULUM: 2022 개정 공통국어2
CONTEXT: ARC_N 중세국어 V2 난도·선지 품질·정답 유일성 개선

## 0. ACTIVATION & SCOPE SAFETY
- 이 모듈은 사용자가 중세 국어, 「국어의 어제와 오늘」, 「변화하는 국어의 모습」 또는 이에 대응하는 특정 교과서 페이지·학습지 범위를 명시해 SCOPE_LOCK이 확인될 때만 활성화한다.
- manifest-selected 국어 MASTER(`active.subjects.korean`)의 기본 범위를 중세 국어로 자동 확장하지 않는다. 요청한 단원/문헌/학교 학습지만을 이번 요청의 SCOPE_LOCK에 기재한다.
- 범위 근거 순서: 현재 학교 학습지/시험범위 → 해당 교과서 원문 → 원문 확인된 실제 학교 기출 → 공신력 있는 문법·국어사 해설 → 검증된 참고문항의 구조.
- 학교 기출은 독립적인 '정답의 진리'가 아니다. 기출의 해설 및 오류 가능성도 검토하고, 원문을 재복제하지 않는다.
- 사용자 제공 Scribd·유료 문제집은 합법적으로 접근 가능한 문서의 구성/판단축/난도 보정에만 사용한다. 원문·선지의 대량 복제, 접근 제한 우회 금지.
- 학교수업의 단순화된 설명과 언어사 연구의 견해가 다르면 출제에 필요한 판단 조건과 자료 출처를 명시한다. 합의되지 않은 이견으로 정답을 가르지 않는다.

## 1. V2 진단 — 확정과 미검증 분리
- 2026-11-07 검토: V2 D3 05번은 '초성 17 + 중성 11 = 28'이라는 문항 내부 산술 힌트만으로 정답 후보를 좁힐 수 있음 → FAKE_DIFFICULTY / WEAK_DISTRACTOR 유형.
- V2 D4 07번은 보기의 8종성 관련 설명과 특정 선지가 직접 충돌하여, 별도 음운 분석 없이 제거될 수 있음 → GIVEN_AWAY_BY_SOURCE.
- V2 20번은 정답표의 단일 정답 주장과 여러 선지의 형태소 분석 간에 충돌 가능성이 확인됨 → SUSPECTED_NON_UNIQUE; 정답 유일성을 독립 검수하기 전에는 BANK/출판으로 승격 금지. 정확한 형태소 근거가 확보되기 전에는 수정 완료나 복수정답을 확정했다고 기록하지 않는다.
- 위 사례는 현재 조사한 문항 수준의 진단이다. 미검수 전체 V2 100문항을 모두 오류 확정으로 기재하지 않는다.
- 원본 V2는 QC_STATUS=REVIEW_REQUIRED (아직 전체 정답 유일성·문헌 근거 재검증이 끝나지 않음). 기존 PDF가 자동 변경된 것으로 간주하지 않는다.

## 2. 난도: 문제 길이/전문용어가 아닌 판단 단계
D2 — 단일 개념 확인 및 한 번의 근거 연결.
D3 — 문헌 속 실제 어절에 최소 2개의 독립 조건을 적용(예: 형태소 경계 + 조사/어미 기능). 보기에 답이 노출되면 D3 불가.
D4 — 최소 3개의 실질 판단 단계, 또는 2개 이상의 용례를 비교하여 예외·환경 조건까지 통합. 정답 후보에 남는 경쟁 오답 최소 2개를 설명할 수 있어야 함. 단순 암기·상호 배타적 단정어 제거·보기 그대로 베끼기는 D4 불가.
D5 — 자료 A와 B 비교 + 낯선 용례로 원리 전이 + 반례/예외 검토가 모두 필요하며, 높은 난도의 원인이 정확한 추론이어야 함. ㄱㄴㄷㄹ 조합 개수·문장 길이만 늘리는 방법 금지.
- 위 D단계는 설계/구조적 목표이고 실제 정답률 검증이 없다면 '예상 난도'로만 표기한다.
- manifest-selected 난도 엔진(`active.quality.difficulty_engine`)의 구성요소 점수를 기록하되, 과장 난도 발견 시 점수와 라벨을 하향 조정하거나 재출제한다.
- D4/D5 판정 전 '보기 제거 테스트': 보기 없이 불가능한지, 보기 내용을 단순 대조하기만 하면 답이 나오는지, 상식/수량/극단 표현만으로 3개 이상 제거되는지 점검한다.
- 핵심 과정의 단계 수는 '직접 근거 확인/형태 분석/음운·문법 적용/반례 검증/문헌 비교' 같은 서로 다른 연산으로만 센다. 똑같은 연산의 반복은 단계 수로 부풀리지 않는다.

## 3. 오답 설계 — '틀린 이유가 정확한' 매력적인 선지
- 모든 선지에 같은 판단축을 적용한다. 가능하면 정답을 포함한 후보들이 동일 형태소·동일 문헌·동일 음운 환경을 서로 다른 방식으로 해석하도록 만든다.
- 최소 2개 경쟁 오답은 참인 관찰 + 잘못된 기능 분류, 조건의 미세 전도, 인접 이형태 혼동, 시기·문헌 혼동 등 실제 학생 오개념으로 설계한다.
- 선지마다 내부 기록: `CLAIM`, `TEXT_EVIDENCE`, `GRAMMAR_RULE`, `TRUE_FALSE`, `WHY_PLAUSIBLE`, `EXACT_REFUTATION`.
- '모두/항상/오직/전혀/반드시/예외 없이' 같은 극단 표현은 일괄 금지가 아니나, 이 단어만 보고 답을 고를 수 있으면 표면 힌트 FAIL. 정답 길이·문체·구체성·기호 배치를 이용해 정답을 드러내지 않는다.
- 허술한 반대말 선지, 시대착오가 노골적인 선지, 세부 문법과 무관한 선지 3개 이상이면 선택지 세트를 전면 재설계한다.
- 선지의 복잡한 접속 표현(AND/OR)은 원자 주장별 진리값과 전체 명제를 따로 평가한다. 전제 하나만 참이라도 전체가 거짓이면 반박 가능해야 한다.

## 4. 중세 국어 전용 SOURCE + MORPHEME GATE
모든 형태소/음운·표기 판단 문항은 다음을 수행한다.
1. 원문 출전 및 판본·행/장/교과서 쪽수와 표기된 철자·방점을 확인한다. 가공·현대화·정규화 표기라면 표시한다. 읽지 않은 원문을 읽었다고 주장하지 않는다.
2. 어절 전체를 체언/용언 어간, 접사, 선어말 어미, 종결/연결/전성 어미, 조사로 분리해 적는다.
3. 연철/분철/중철, 음운 환경(모음 조화·종성 유무), 조사 이형태, ㅎ 종성 체언, 사동/피동, 높임법의 적용 조건을 근거와 대조한다.
4. 동일한 철자에 대하여 기능이 다른 해석이 가능한지 앞뒤 문맥으로 반증한다. 원문이 불충분하면 해당 선지/문항 폐기.
5. 중세 국어의 표기/음가/현대어 대응을 혼동하지 않는다. ㅇ/ㆁ/ㆆ, 어두 자음군/된소리, 문법 요소와 어절 표기를 별도로 검증한다.
6. 2회 독립 검증: PASS A는 원문/문법 근거로 각 선지의 진리값 평가, PASS B는 정답 번호·출제 의도를 가린 채 5개 선지를 각각 참/거짓/불확정으로 평가한다.
7. 5지선다 '옳은 것'은 TRUE=1, '적절하지 않은 것'은 FALSE=1이어야 하며 나머지 4개도 모두 확정적으로 판정 가능해야 한다. 불확정 1개라도 있으면 HOLD.
- 추정·쟁점·음가/표기 불명확성은 난이도가 아니라 QC 오류다.
- 검수 근거는 문헌 원문과 학교 수업 기준의 페이지/인용 위치를 기록하며 출처 불확정 시 `SOURCE_VERIFIED=false`로 막는다.

## 5. SET EDITORIAL GATE — 20/50/100문항
- ㄱㄴㄷㄹ 조합, 형태 분석 5지 선택, 교과서 지문 단순 재진술, '적절하지 않은 것은' 발문 등 한 종류가 과밀하지 않은지 확인.
- 동일 조건·근거·오답 함정이 3문항 연속 반복되면 REVISE. 표/장문 자료가 실제 판단에 필요하지 않으면 제거한다.
- 새 자료를 읽어야 답이 바뀌는 적용형, 두 문헌 비교형, 미세 이형태 판단형, 오류 수정·반례 제시형 등을 균형 있게 배치하되 학교 내신 및 요청 범위를 우선한다.
- 교과서·학교 학습지 핵심 출제포인트가 심화/지엽 문항에 밀리지 않도록 COVERAGE와 D-분포를 동시에 확인한다.
- 정답 번호 균형을 맞추려고 정답을 바꾸거나 약한 선지를 선택하지 않는다.
- 실제 고난도 학생 테스트/정답률 데이터가 없으면 `ACTUAL_DIFFICULTY=UNMEASURED`로 기록한다.

## 6. HARD GATES + BANK RULE
다음 하나라도 해당하면 QC_STATUS=HOLD, BANK_PASS 금지, CONTENT_LOCK 금지, TYPESET_HANDOFF 금지:
- TRUE/FALSE/UNDETERMINED 진리표에서 유일 정답 불성립
- 원문과 형태소 분석의 불일치 또는 객관적으로 출처가 확인되지 않음
- 5지선다 중 다수 선지의 즉시 배제 / 정답 표면 힌트
- 근거 문헌의 범위 외 필수 지식 의존, 방점/문자 깨짐, 다른 판본 무고지 혼용
- 출제 의도와 독립 풀이의 불일치 또는 자료·정답표와 선지 불일치
- D4/D5가 장문/ㄱㄴㄷㄹ 조합 숫자로만 어려워진 경우
- 학교 실제 기출과 무단복제 또는 기존 ARC 문제와 실질 중복
- 오류 확정 문항은 ERROR_DATABASE에 오류 코드·원인·회귀 상태를 남기고 새 ID로만 재검증한다.

## 7. INTERNAL METADATA & RESULT STATES
```yaml
ITEM_ID: # set+version+item number; no duplicate IDs
SOURCE_REFERENCE:
SOURCE_VERIFIED: true|false
MORPHEME_LEDGER: [] # 각 형태소/기능/음운 환경/출전
OPTION_TRUTH_TABLE: # ①~⑤ 각각 TRUE/FALSE/UNDETERMINED+근거
  A: {verdict: null, evidence: null}
  B: {verdict: null, evidence: null}
  C: {verdict: null, evidence: null}
  D: {verdict: null, evidence: null}
  E: {verdict: null, evidence: null}
DISTRACTOR_EVIDENCE: [] # 오답별 그럴듯함과 정확한 반박
REASONING_STEPS: [] # 서로 다른 판단 과정
OBVIOUS_ELIMINATION_COUNT:
SECOND_BEST_CANDIDATES: []
EXPECTED_DIFFICULTY: D2|D3|D4|D5
ACTUAL_DIFFICULTY: UNMEASURED
DIFFICULTY_CONFIDENCE: LOW|MEDIUM|HIGH
INDEPENDENT_RECHECK: PASS|FAIL|PENDING
KOR_MID_SOURCE_QA: PASS|FAIL|PENDING
KOR_MID_UNIQUE_ANSWER: PASS|FAIL|PENDING
KOR_MID_DISTRACTOR_QA: PASS|FAIL|PENDING
KOR_MID_DIFFICULTY_QA: PASS|FAIL|PENDING
QC_STATUS: PASS|REVISE|HOLD|DISCARD
```
- 내부 검수 기록은 학생 PDF에서 숨기고, 검증된 ANSWER_KEY는 별도 유지.
- 모든 필수 게이트가 PASS이고 기존 공통 엔진/품질 루브릭도 PASS일 때만 BANK 후보. 반례/정답 충돌이 발견되면 배포를 막고 재검증.

## 8. REGRESSION SUITE
- 필수 테스트: `quality/KOR_MIDDLE_KOREAN_V2_REGRESSION_V1.0.md`의 KOR-MID-001~005.
- 이 파일은 규칙 정의일 뿐 실제 V2 100문항을 검수 완료했다는 뜻이 아니다.
- 교정 뒤 동일 자료/조건으로 이전 규칙 vs 새 규칙을 비교하며 결과표에 실제 판정을 남긴다.

## 9. MASTER ROUTING (moved 2026-11-10)
이 절은 폐기된 `archive/subjects/KOREAN_MASTER_V4.0.md` 13절에 있던 라우팅 규칙이다. 현행 국어 MASTER와 함께 적용한다.
- 트리거: 사용자가 중세 국어/국어의 어제와 오늘/변화하는 국어의 모습을 명시하거나 해당 학교 학습지·교과서 범위를 직접 지정한 경우에만.
- 국어 MASTER의 기본 SCOPE를 자동 확장하지 않는다. 명시적 요청 범위를 별도 SCOPE_LOCK으로 고정하고 해당 원문·학교자료의 실열람을 선행한다.
- 강제 게이트: `KOR_MID_SOURCE_QA`, `KOR_MID_UNIQUE_ANSWER`, `KOR_MID_DISTRACTOR_QA`, `KOR_MID_DIFFICULTY_QA` 전부 PASS. 하나라도 FAIL/PENDING이면 BANK_PASS/학생용 배포/CONTENT_LOCK/TYPESET_HANDOFF 금지.
- D3는 형태소/음운/문법 등 독립 조건 2개 이상; D4는 3개 실질 추론 단계와 근거로 경쟁하는 오답 2개 이상; D5는 새로운 문헌 자료의 전이 + 반례/예외 검토를 확인한다. 긴 문장·극단 단정어·ㄱㄴㄷㄹ 조합으로 난도 부풀리기 금지.
- 형태소 경계/조사·어미 기능/음운 환경/문헌 표기를 선지 5개 각각 원문 근거에 대조하는 TRUTH TABLE 및 독립 PASS A/B를 의무화한다.
- `quality/KOR_MIDDLE_KOREAN_V2_REGRESSION_V1.0.md`의 회귀검사 상태는 실측 결과만 기록한다. 테스트를 실행하지 않았다면 PENDING으로 유지한다.
- ARC_N° 중세국어 V2 원본 전체는 재검증 전까지 검증 완료 은행으로 취급하지 않는다. 기존 PDF를 자동 수정한 것으로 보고하지 않는다.
- 전 과목 공통 보조 게이트: `quality/ARC_FALSE_DIFFICULTY_GATE_V1.0.md`.

