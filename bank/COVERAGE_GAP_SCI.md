# COVERAGE_GAP_SCI — 통합과학2 기출 후보 부족 분석 (잠정)

> `bank/tools/coverage.py` 가 생성한 파일이다. 직접 고치지 말고 레지스트리를 고친 뒤 재생성한다.

**읽는 법.** 본문 검토가 끝난 문항(READY)은 현재 **25건**이다. 아래 숫자는 모두 "후보 풀"(본문·정답 미검토, HOLD·EXCLUDED 제외) 기준의 **잠정치**다. 판정 기준(가정): 개념당 후보 원형 ≥ 6이면 OK, 3~5이면 LOW, < 3이면 CRITICAL.
**엄격**은 고2·3 선택과목 문항을 뺀 풀(현재 교육과정 문항·학교 시험지), **확장**은 그 문항을 포함한 풀이다. 확장은 "현재 지식으로 풀리는가"를 아직 검증하지 못해 낙관적이다.

## 1. 전체 현황

|구분|건수|
|---|---:|
|레지스트리 전체|553|
|status=READY|25|
|status=READY_PENDING_RANGE|73|
|status=NEEDS_BODY_REVIEW|64|
|status=NEEDS_ANSWER|67|
|status=HOLD|254|
|status=EXCLUDED|70|

후보 풀 229건 중 본문을 지금 도구로 열 수 있는 것: **207건** (`DRIVE_ORIGINAL`·`EXTERNAL_PDF_REACHABLE`·`SCHOOL_SEPARATED_PDF`).

## 2. 중간 트랙 (SCOPE_LEDGER, 범위 확정)

|개념|우선순위|전체|후보 풀|원형(엄격)|원형(확장)|풀 중 정답 보유|HOLD|판정(엄격)|판정(확장)|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|SCI-GT-FOSSIL|R|5|5|4|4|3|0|LOW|LOW|
|SCI-GT-TIME|R|6|4|4|4|2|2|LOW|LOW|
|SCI-GT-UNSPEC|R|1|0|0|0|0|0|CRITICAL|CRITICAL|
|SCI-EV-SELECTION|R|3|3|3|3|2|0|LOW|LOW|
|SCI-EV-DIVERSITY|R|5|1|1|1|0|4|CRITICAL|CRITICAL|
|SCI-EV-UNSPEC|R|1|0|0|0|0|1|CRITICAL|CRITICAL|
|SCI-OR-ELECTRON|R|12|11|10|11|4|1|OK|OK|
|SCI-OR-REACTIVITY|R|1|1|1|1|1|0|CRITICAL|CRITICAL|
|SCI-OR-QUANT|R|1|1|0|1|1|0|CRITICAL|CRITICAL|
|SCI-OR-EXPERIMENT|S|1|0|0|0|0|1|CRITICAL|CRITICAL|
|SCI-OR-UNSPEC|R|0|0|0|0|0|0|CRITICAL|CRITICAL|
|SCI-EE-ENERGY|R|10|10|9|10|8|0|OK|OK|
|SCI-EE-CIRCULATION|R|9|6|6|6|5|3|OK|OK|
|SCI-EE-UNSPEC|R|2|1|1|1|1|1|CRITICAL|CRITICAL|
|SCI-EM-INDUCTION|R|1|1|1|1|1|0|CRITICAL|CRITICAL|
|SCI-EM-GENERATION|S|28|19|2|14|18|8|CRITICAL|OK|

부족 개념(엄격 기준, 적은 순): SCI-EV-UNSPEC(0, CRITICAL), SCI-GT-UNSPEC(0, CRITICAL), SCI-OR-EXPERIMENT(0, CRITICAL), SCI-OR-QUANT(0, CRITICAL), SCI-OR-UNSPEC(0, CRITICAL), SCI-EE-UNSPEC(1, CRITICAL), SCI-EM-INDUCTION(1, CRITICAL), SCI-EV-DIVERSITY(1, CRITICAL), SCI-OR-REACTIVITY(1, CRITICAL), SCI-EM-GENERATION(2, CRITICAL), SCI-EV-SELECTION(3, LOW), SCI-GT-FOSSIL(4, LOW), SCI-GT-TIME(4, LOW)

확장 기준에서만 부족이 가려지는 개념(고2·3 문항 풀이 가능성 검증이 해결의 열쇠): SCI-EM-GENERATION(CRITICAL→OK)

## 2. 기말 후보 트랙 (중간 제외 나머지, 범위 미확정 — READY 불가)

|개념|우선순위|전체|후보 풀|원형(엄격)|원형(확장)|풀 중 정답 보유|HOLD|판정(엄격)|판정(확장)|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|SCI-F-ACIDBASE|P|156|76|14|59|40|79|OK|OK|
|SCI-F-HEAT_EXO|P|34|10|3|10|8|14|LOW|OK|
|SCI-F-ECOSYSTEM|P|67|5|5|5|4|61|LOW|LOW|
|SCI-F-FOODWEB|P|20|4|2|4|4|16|CRITICAL|LOW|
|SCI-F-SOLAR_ENERGY|P|17|8|1|8|8|7|CRITICAL|OK|
|SCI-F-ENERGY_RES|P|92|58|8|48|49|16|OK|OK|
|SCI-F-INFECTION|P|3|1|1|1|0|2|CRITICAL|CRITICAL|
|SCI-F-BIGDATA_AI|P|4|2|2|2|2|2|CRITICAL|CRITICAL|
|SCI-F-AI_ROBOT_IOT|P|2|2|2|2|1|0|CRITICAL|CRITICAL|
|SCI-F-SSI_ETHICS|P|1|0|0|0|0|1|CRITICAL|CRITICAL|
|SCI-F-SCI_TECH_LIFE|P|35|0|0|0|0|35|CRITICAL|CRITICAL|

부족 개념(엄격 기준, 적은 순): SCI-F-SCI_TECH_LIFE(0, CRITICAL), SCI-F-SSI_ETHICS(0, CRITICAL), SCI-F-INFECTION(1, CRITICAL), SCI-F-SOLAR_ENERGY(1, CRITICAL), SCI-F-AI_ROBOT_IOT(2, CRITICAL), SCI-F-BIGDATA_AI(2, CRITICAL), SCI-F-FOODWEB(2, CRITICAL), SCI-F-HEAT_EXO(3, LOW), SCI-F-ECOSYSTEM(5, LOW)

확장 기준에서만 부족이 가려지는 개념(고2·3 문항 풀이 가능성 검증이 해결의 열쇠): SCI-F-HEAT_EXO(LOW→OK), SCI-F-FOODWEB(CRITICAL→LOW), SCI-F-SOLAR_ENERGY(CRITICAL→OK)

## 3. 후보 풀 구성

|origin_level|건수|
|---|---:|
|UPPER|147|
|CURRENT|39|
|SCHOOL|22|
|LEGACY_G1|21|

|reuse_mode|건수|
|---|---:|
|ADAPT_ONLY|168|
|DIRECT_OK|39|
|CALIBRATION_ONLY|22|

|asset_type (기준)|건수|
|---|---:|
|unknown (NONE)|88|
|table (REVIEW)|20|
|passage (REVIEW)|19|
|composite (REVIEW)|19|
|experiment_diagram (REVIEW)|18|
|graph (REVIEW)|14|
|particle_model (REVIEW)|12|
|flowchart (REVIEW)|11|
|none (REVIEW)|10|
|experiment_diagram (KEYWORD_GUESS)|6|
|graph (KEYWORD_GUESS)|6|
|unknown (VISUAL_REQUIRED_FIELD)|5|
|map (REVIEW)|1|

|question_form|건수|
|---|---:|
|선택형|176|
|UNKNOWN|41|
|서술형|12|

난도(D1~D5) 분포는 **산출 불가**: 후보 풀 229건 모두 `UNRATED`다. 본문 검토(Phase 2) 후에 채운다.

## 4. 해석상 한계

- 개념 배정은 대부분 수집 단계의 키워드 범위(`KEYWORD_COLLECTOR_UNIT`)에서 나왔다. 성취기준 코드 기반(`CODE_*`)·수동(`TOPIC_MANUAL`) 배정은 소수다. 고2·3 선택과목 문항(`UPPER`)은 요지·출제의도 텍스트만 본 판정이라 실제로 현재 지식으로 풀리는지는 본문을 봐야 안다.
- 중간 트랙의 후보가 적은 것은 수집 지시가 "중간 제외 나머지"였기 때문이다. 중간 트랙 보강은 학교 시험지·교재(Drive에 있으나 아직 문항 단위로 색인되지 않은 자료)가 필요하다.
- 후보 원형은 평가목표 문구가 같은 것끼리 묶은 값이다. 구조 수준 묶음은 본문 확보 후 다시 한다.
- 자료형(그래프·입자모형 등)은 대부분 `unknown`이라 자료형별 부족은 아직 판단할 수 없다.
