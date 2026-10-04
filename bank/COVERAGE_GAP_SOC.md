# COVERAGE_GAP_SOC — 통합사회2 기출 후보 부족 분석 (잠정)

> `bank/tools/coverage.py` 가 생성한 파일이다. 직접 고치지 말고 레지스트리를 고친 뒤 재생성한다.

**읽는 법.** 본문 검토가 끝난 문항(READY)은 현재 **14건**이다. 아래 숫자는 모두 "후보 풀"(본문·정답 미검토, HOLD·EXCLUDED 제외) 기준의 **잠정치**다. 판정 기준(가정): 개념당 후보 원형 ≥ 6이면 OK, 3~5이면 LOW, < 3이면 CRITICAL.
**엄격**은 고2·3 선택과목 문항을 뺀 풀(현재 교육과정 문항·학교 시험지), **확장**은 그 문항을 포함한 풀이다. 확장은 "현재 지식으로 풀리는가"를 아직 검증하지 못해 낙관적이다.

## 1. 전체 현황

|구분|건수|
|---|---:|
|레지스트리 전체|1527|
|status=READY|14|
|status=READY_PENDING_RANGE|119|
|status=NEEDS_BODY_REVIEW|763|
|status=NEEDS_ANSWER|104|
|status=HOLD|446|
|status=EXCLUDED|81|

후보 풀 1000건 중 본문을 지금 도구로 열 수 있는 것: **981건** (`DRIVE_ORIGINAL`·`EXTERNAL_PDF_REACHABLE`·`SCHOOL_SEPARATED_PDF`).

## 2. 중간 트랙 (SCOPE_LEDGER, 범위 확정)

|개념|우선순위|전체|후보 풀|원형(엄격)|원형(확장)|풀 중 정답 보유|HOLD|판정(엄격)|판정(확장)|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|SOC-A-VIEW|R|50|43|24|33|32|6|OK|OK|
|SOC-A-THOUGHT_MAP|R|0|0|0|0|0|0|CRITICAL|CRITICAL|
|SOC-C-RIGHTS|R|75|65|54|56|38|9|OK|OK|
|SOC-C-REMEDY|R|6|4|4|4|2|2|LOW|LOW|
|SOC-C-COLLISION|R|3|3|3|3|2|0|LOW|LOW|
|SOC-B-GLOBAL|R|14|8|7|8|6|4|OK|OK|
|SOC-B-POP|S|11|8|8|8|8|3|OK|OK|

부족 개념(엄격 기준, 적은 순): SOC-A-THOUGHT_MAP(0, CRITICAL), SOC-C-COLLISION(3, LOW), SOC-C-REMEDY(4, LOW)

## 2. 기말 후보 트랙 (중간 제외 나머지, 범위 미확정 — READY 불가)

|개념|우선순위|전체|후보 풀|원형(엄격)|원형(확장)|풀 중 정답 보유|HOLD|판정(엄격)|판정(확장)|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|SOC-F-MINORITY|P|4|0|0|0|0|4|CRITICAL|CRITICAL|
|SOC-F-INEQUALITY|P|204|10|3|4|10|194|LOW|LOW|
|SOC-F-CAPITALISM|P|8|7|4|7|6|0|LOW|OK|
|SOC-F-MARKET|P|376|307|8|199|292|59|OK|OK|
|SOC-F-FINANCE|P|103|87|5|63|84|16|LOW|OK|
|SOC-F-TRADE_SD|P|148|107|6|76|103|39|OK|OK|
|SOC-F-PEACE|P|65|50|10|44|45|13|OK|OK|
|SOC-F-KOREA_EASTASIA|P|5|3|3|3|2|2|LOW|LOW|
|SOC-F-ENERGY_CLIMATE|P|352|284|27|191|252|53|OK|OK|
|SOC-F-FUTURE|P|0|0|0|0|0|0|CRITICAL|CRITICAL|
|SOC-F-PEACE_SD_UNSPEC|P|59|14|2|10|14|42|CRITICAL|OK|

부족 개념(엄격 기준, 적은 순): SOC-F-FUTURE(0, CRITICAL), SOC-F-MINORITY(0, CRITICAL), SOC-F-PEACE_SD_UNSPEC(2, CRITICAL), SOC-F-INEQUALITY(3, LOW), SOC-F-KOREA_EASTASIA(3, LOW), SOC-F-CAPITALISM(4, LOW), SOC-F-FINANCE(5, LOW)

확장 기준에서만 부족이 가려지는 개념(고2·3 문항 풀이 가능성 검증이 해결의 열쇠): SOC-F-CAPITALISM(LOW→OK), SOC-F-FINANCE(LOW→OK), SOC-F-PEACE_SD_UNSPEC(CRITICAL→OK)

## 3. 후보 풀 구성

|origin_level|건수|
|---|---:|
|UPPER|805|
|LEGACY_G1|142|
|CURRENT|40|
|SCHOOL|13|

|reuse_mode|건수|
|---|---:|
|ADAPT_ONLY|947|
|DIRECT_OK|40|
|CALIBRATION_ONLY|13|

|asset_type (기준)|건수|
|---|---:|
|unknown (NONE)|798|
|passage (REVIEW)|66|
|table (REVIEW)|33|
|unknown (VISUAL_REQUIRED_FIELD)|24|
|graph (REVIEW)|23|
|composite (REVIEW)|16|
|map (KEYWORD_GUESS)|14|
|none (VISUAL_REQUIRED_FIELD)|8|
|flowchart (REVIEW)|7|
|graph (KEYWORD_GUESS)|5|
|map (REVIEW)|3|
|table (KEYWORD_GUESS)|3|

|question_form|건수|
|---|---:|
|UNKNOWN|565|
|선택형|428|
|서술형|7|

난도(D1~D5) 분포는 **산출 불가**: 후보 풀 1000건 모두 `UNRATED`다. 본문 검토(Phase 2) 후에 채운다.

## 4. 해석상 한계

- 개념 배정은 대부분 수집 단계의 키워드 범위(`KEYWORD_COLLECTOR_UNIT`)에서 나왔다. 성취기준 코드 기반(`CODE_*`)·수동(`TOPIC_MANUAL`) 배정은 소수다. 고2·3 선택과목 문항(`UPPER`)은 요지·출제의도 텍스트만 본 판정이라 실제로 현재 지식으로 풀리는지는 본문을 봐야 안다.
- 중간 트랙의 후보가 적은 것은 수집 지시가 "중간 제외 나머지"였기 때문이다. 중간 트랙 보강은 학교 시험지·교재(Drive에 있으나 아직 문항 단위로 색인되지 않은 자료)가 필요하다.
- 후보 원형은 평가목표 문구가 같은 것끼리 묶은 값이다. 구조 수준 묶음은 본문 확보 후 다시 한다.
- 자료형(그래프·입자모형 등)은 대부분 `unknown`이라 자료형별 부족은 아직 판단할 수 없다.
