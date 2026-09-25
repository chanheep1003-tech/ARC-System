# ARC_ERROR_DATABASE_V1.0
VERSION: 1.0
DATE: 2026-09-17
ROLE: 출제·검증·시각자료·조판 오류의 재발 방지
STATUS: ACTIVE

## 0. PURPOSE
한 번 발견한 오류를 “그 문항만 고치고 끝내지 않기” 위한 데이터베이스다.

오류 처리 흐름:
DETECT → CLASSIFY → FIX → REGRESSION TEST → PREVENTION RULE → CLOSE

실제 발생한 오류와 단순 위험요소를 구분한다.
초기 V1.0에는 확인되지 않은 사고를 실제 오류처럼 기록하지 않는다.

## 1. SEVERITY
- S0 CRITICAL: 학생에게 배포하면 정답/범위/사실이 틀리는 수준. 즉시 출제 중단.
- S1 MAJOR: 문항 타당도·변별력·자료 해석을 크게 훼손.
- S2 MODERATE: 품질 저하이나 정답 자체는 유지.
- S3 MINOR: 표현/메타데이터/조판 경미 문제.

## 2. ERROR CODES

### COMMON
- ERR-SCOPE-001 범위 밖 필수지식
- ERR-SCOPE-002 제외범위 재유입
- ERR-ANS-001 복수정답
- ERR-ANS-002 정답 없음
- ERR-ANS-003 ANSWER_KEY 불일치
- ERR-COND-001 조건 부족
- ERR-DATA-001 표/그래프/수치 불일치
- ERR-SOURCE-001 출처 사실과 생성 아이디어 혼동
- ERR-COPY-001 문항/원문 과도 복제
- ERR-DUP-001 기존 ARC 문항과 과도한 구조 반복
- ERR-ASSET-001 필수 시각자료 누락
- ERR-ASSET-002 ASSET_CLASS 오분류
- ERR-ASSET-003 placeholder
- ERR-HANDOFF-001 필수 handoff 필드 누락
- ERR-PDF-001 문항/선지 분리
- ERR-PDF-002 clipping/overlap/glyph 오류
- ERR-PDF-003 PRODUCT_MODE 레이아웃 혼합
- ERR-PDF-004 ARC CORE 2단 본문 flow 오염
- ERR-PDF-005 의미 단위가 깨지는 페이지 분할 / heading orphan
- ERR-PDF-006 본문 폰트·weight·크기·대비로 인한 인쇄 가독성 저하
- ERR-PDF-007 PART/장/절/보조 블록 시각 계층 불명확

### KOREAN
- ERR-KOR-001 관찰 사실과 화자 추론 혼동
- ERR-KOR-002 화자/작품 지식 과잉추론
- ERR-KOR-003 표현효과 과잉해석
- ERR-KOR-004 현대문학 장문 복제
- ERR-KOR-005 매력도 낮은 오답 / 정답 즉시 노출
- ERR-KOR-006 핵심 내신 포인트 누락 / 변별형 과잉

### SCIENCE
- ERR-SCI-REDOX-001 전자수 보존 오류
- ERR-SCI-REDOX-002 전체 이온수/양이온수 혼동
- ERR-SCI-REDOX-003 spectator ion 조건 부족
- ERR-SCI-REACT-001 반응성 서열 비유일
- ERR-SCI-MASS-001 금속판 질량변화 근거 부족
- ERR-SCI-VIS-001 입자모형 개수/레이블 오류
- ERR-SCI-ADV-001 상위학년 공식/개념 누출

### SOCIAL
- ERR-SOC-X-001 C파트 사용자 X 영역 출제
- ERR-SOC-RIGHT-001 권리구제 기관/절차/효과 오류
- ERR-SOC-RIGHT-002 기본권 제한 판단 점프
- ERR-SOC-DATA-001 비율/수/증가율 혼동
- ERR-SOC-FACT-001 판례·공식자료 사실 왜곡

### HISTORY
- ERR-HIS-TIME-001 사건 선후 오류
- ERR-HIS-SOURCE-001 사료 주체/시기 오식별
- ERR-HIS-PERSON-001 인물-단체 연결 오류
- ERR-HIS-LINE-001 계열/활동 혼동
- ERR-HIS-REGION-001 지역 오류

### AI
- ERR-AI-DFS-001 DFS 순서/방문규칙 오류
- ERR-AI-BFS-001 BFS 순서/방문규칙 오류
- ERR-AI-DATA-001 전처리/EDA 해석 오류
- ERR-AI-CORR-001 상관관계를 인과관계로 해석
- ERR-AI-CODE-001 코드 실행 결과 불일치
- ERR-AI-SCOPE-001 범위 밖 알고리즘/문법 의존

## 3. ERROR RECORD
실제 오류가 확인되면 아래 형식으로 기록한다.

```yaml
ERROR_ID: ERR-YYYYMMDD-SUBJECT-NNN
DATE:
SUBJECT:
SET_ID:
ITEM_ID:
CONCEPT_ID:
ERROR_CODE:
SEVERITY:
DETECTED_STAGE: GENERATION / VERIFY_A / VERIFY_B / QA_BENCH / PDF_QC / USER_FEEDBACK
DESCRIPTION:
EXPECTED:
ACTUAL:
ROOT_CAUSE:
FIX_APPLIED:
PREVENTION_RULE:
REGRESSION_BENCH_ID:
REGRESSION_STATUS: PENDING / PASS / FAIL
MASTER_CHANGE:
COMMON_ENGINE_CHANGE:
STATUS: OPEN / FIXED / REGRESSION_PENDING / CLOSED / RECURRED
RECURRENCE_COUNT:
```

## 4. CLOSE RULE
오류를 CLOSED로 바꾸려면:
1. 해당 문항 수정 또는 폐기
2. 원인 분류 완료
3. 예방 규칙 필요 여부 판단
4. 관련 QA BENCH 또는 최소 재현 테스트 실행
5. regression PASS

수정만 했고 테스트하지 않았으면 `REGRESSION_PENDING`.

## 5. ESCALATION RULE
- S0: 1회만 발생해도 관련 MASTER에 즉시 방지규칙 검토
- 같은 ERROR_CODE S1 이상이 2회 재발: 과목 MASTER에 명문화
- 3개 이상 과목에서 같은 공통 오류가 발생: COMMON ENGINE 규칙으로 승격
- 동일 ERROR_CODE 3회 재발: 해당 BENCH를 RELEASE 필수 벤치로 승격
- 사용자에게서 발견된 S0/S1 오류: HUMAN_FOUND=true로 표시하고 우선 회귀검사

## 6. PREVENTION RISK REGISTRY
아래는 “실제 오류 발생 이력”이 아니라 현재 MASTER가 이미 방지하고 있는 고위험 패턴이다.

|RISK_ID|과목|위험|현재 방어|
|---|---|---|---|
|RISK-SCI-01|과학|전자수/이온수 정량 오류|REDOX_LEDGER + 독립검증|
|RISK-SCI-02|과학|반응성 서열이 하나로 결정되지 않음|transitive closure + 비유일 시 문항형 변경|
|RISK-SCI-03|과학|질량 변화 근거 부족|상대질량/실제질량/입자수 조건 확인|
|RISK-SOC-01|사회|C파트 X 영역 유입|C_X_MARK_FILTER|
|RISK-SOC-02|사회|SOURCE_FACT/GENERATION_IDEA 혼동|내부 Blueprint 분리|
|RISK-KOR-01|국어|관찰과 화자 추론 혼동|OBSERVED_FACT / SPEAKER_INFERENCE 분리|
|RISK-KOR-02|국어|현대문학 장문 복제|최소 인용 + 학교원문 범위|
|RISK-KOR-03|국어|정답이 즉시 보이고 오답이 경쟁하지 못함|ATTRACTIVE_DISTRACTOR + OBVIOUS_ANSWER + SECOND_BEST gate|
|RISK-KOR-04|국어|핵심 주제·표현법·소재 기능보다 변별형 미세분석이 과다|CORE_EXAM_POINT_COVERAGE + DIFFICULTY_BALANCE + RARE_TASK_BUDGET|
|RISK-HIS-01|한국사|사료 시기/주체 오류|FACT CHECK MATRIX|
|RISK-HIS-02|한국사|민족주의/사회주의 계열 혼동|IDEOLOGICAL_LINE_SWAP 검수|
|RISK-AI-01|AI|DFS/BFS 탐색 순서 오류|방문규칙·탐색구조 독립검증|
|RISK-AI-02|AI|상관↔인과 혼동|AI verification gate|
|RISK-PDF-01|공통|정답이 ARC N° 학생 PDF에 노출|ANSWER_KEY 편집자용 분리|
|RISK-PDF-02|공통|TRUE_VISUAL을 표로 대체|ARC PDF TRUE_VISUAL gate|
|RISK-PDF-03|CORE|N° 2단 규칙이 CORE에 침투|PRODUCT_MODE namespace + CORE ONE_COLUMN hard lock|
|RISK-PDF-04|CORE|제목/문단/표/도식 의미 단위 절단|SEMANTIC_PAGINATION + source overflow + render preflight|
|RISK-PDF-05|CORE|가벼운 폰트/작은 글씨로 인쇄 가독성 저하|typography tokens + font audit|
|RISK-PDF-06|CORE|PART/장/절 계층 평탄화|four-level hierarchy gate|
|RISK-N-CORE-BALANCE|ARC_N COMMON|심화/변별 문항이 핵심 시험포인트를 밀어내는 세트 드리프트|ARC_N_BALANCE_GATE 70~80% CORE + 20~30% ADVANCED|

## 7. ERROR → SYSTEM FEEDBACK
오류 종료 시 다음 파일을 검토한다.
- ARC_SCOPE_LEDGER: 범위/개념 관리 문제였는가?
- ARC_QA_BENCH: 재발 테스트가 필요한가?
- 과목 ACTIVE MASTER: 과목 특수 규칙이 필요한가?
- COMMON ENGINE: 여러 과목에 공통인가?
- ARC PDF MASTER: 조판/시각자료 문제인가?

모든 오류를 무조건 프롬프트에 추가하지 않는다.
중복 지시가 늘어나면 토큰과 충돌 위험이 커지므로
재발 가능성이 높고 일반화 가능한 규칙만 MASTER로 승격한다.

## 8. INCIDENT LOG
현재 V1.0 초기화 시점에는 검증된 실제 incident를 소급 생성하지 않는다.

|ERROR_ID|SUBJECT|ERROR_CODE|SEVERITY|STATUS|REGRESSION|
|---|---|---|---|---|---|
|ERR-20260919-HIS-PDF-001|HISTORY CORE|ERR-PDF-004|S1|REGRESSION_PENDING|PENDING|
|ERR-20260919-SOC-PDF-001|SOCIAL CORE|ERR-PDF-005|S2|REGRESSION_PENDING|PENDING|
|ERR-20260919-CORE-PDF-001|CORE COMMON|ERR-PDF-006|S2|REGRESSION_PENDING|PENDING|
|ERR-20260919-CORE-PDF-002|CORE COMMON|ERR-PDF-007|S2|REGRESSION_PENDING|PENDING|
|ERR-20260920-CORE-HANDOFF-001|CORE COMMON|ERR-PIPE-STALE-HANDOFF|S1|FIXED_DEV|HANDOFF-SMOKE-STALE|
|ERR-20260920-SOC-PDF-001|SOCIAL CORE|ERR-PDF-MAJOR-BOUNDARY|S2|FIXED_DEV|PDF-SMOKE-MAJOR-BOUNDARY|

첫 실제 오류부터 순차적으로 기록한다.


### ERR-20260919-HIS-PDF-001
```yaml
ERROR_ID: ERR-20260919-HIS-PDF-001
DATE: 2026-09-19
SUBJECT: HISTORY CORE
SET_ID: ARC_CORE_한국사2_일제식민통치와민족운동_V1.0_REVIEW
ERROR_CODE: ERR-PDF-004
SEVERITY: S1
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: ARC CORE 한국사 본문이 ARC N°형 좌우 2단 reading flow로 렌더됨.
EXPECTED: CORE main reading flow는 1단이어야 함.
ACTUAL: 장/절 제목과 본문이 두 개의 독립 열로 흘러가며 긴 제목까지 좁은 열에서 분절됨.
ROOT_CAUSE: CORE는 1단이 권장 수준이었고 N° 2단은 hard rule이어서 PRODUCT_MODE/CSS 격리 실패 시 N° layout이 우세할 수 있었음.
FIX_APPLIED: PDF MASTER V2.4 + CORE PATCH v0.8 + TYPESETTER V1.6에 ONE_COLUMN hard lock/namespace/preflight gate 추가.
PREVENTION_RULE: CORE_TWO_COLUMN_FLOW=0
REGRESSION_BENCH_ID: PDF-SMOKE-CORE-COLUMN
REGRESSION_STATUS: PENDING
MASTER_CHANGE: templates/ARC_PDF_LAYOUT_MASTER_V2.4.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```

### ERR-20260920-CORE-HANDOFF-001
```yaml
ERROR_ID: ERR-20260920-CORE-HANDOFF-001
DATE: 2026-09-20
SUBJECT: CORE COMMON
ERROR_CODE: ERR-PIPE-STALE-HANDOFF
SEVERITY: S1
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: 구형 handoff MD가 CORE 2단, 구형 PDF MASTER, 작은 본문 크기 같은 조판 지시를 최신 Typesetter에 재주입함.
EXPECTED: handoff는 잠긴 내용과 의미 구조만 전달하고 조판 규칙은 현재 SYSTEM_MANIFEST에서 해석해야 함.
ACTUAL: 한국사 handoff의 2단 지시와 사회 handoff의 구형 master/font 지시가 최신 CORE hard lock보다 우선될 수 있었음.
ROOT_CAUSE: handoff acceptance에 stale ruleset/layout-directive executable gate가 없었음.
FIX_APPLIED: tooling/handoff/handoff_preflight.py와 CI smoke 추가; Generator/Content Bundle/Typesetter 계약에서 layout authority 제거.
PREVENTION_RULE: STALE_HANDOFF_GATE=PASS; HANDOFF_LAYOUT_DIRECTIVES=0
REGRESSION_BENCH_ID: HANDOFF-SMOKE-STALE
REGRESSION_STATUS: PASS_LOCAL
MASTER_CHANGE: ops/ARC_TYPESETTER_CONTRACT_V1.6.md
STATUS: FIXED_DEV
RECURRENCE_COUNT: 1
```

### ERR-20260920-SOC-PDF-001
```yaml
ERROR_ID: ERR-20260920-SOC-PDF-001
DATE: 2026-09-20
SUBJECT: SOCIAL CORE
ERROR_CODE: ERR-PDF-MAJOR-BOUNDARY
SEVERITY: S2
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: A/B/C 파트나 독립 대주제가 이전 내용과 같은 페이지 중간에서 시작해 구조 경계가 약해질 수 있음.
EXPECTED: PART/MAJOR_TOPIC은 항상 새 물리 페이지에서 시작하고 공백 페이지는 만들지 않음.
ACTUAL: 기존 v0.8은 파트 전환의 강제 page break 자체를 불필요한 것으로 취급했음.
ROOT_CAUSE: 밀도 최적화가 대경계 의미보다 우선하는 충돌 규칙.
FIX_APPLIED: level-1 boundary contract, HTML/ReportLab hard rule, PDF mid-page boundary detection, registered sparse remainder 예외 추가.
PREVENTION_RULE: CORE_MAJOR_BOUNDARY_PAGE_BREAK=PASS
REGRESSION_BENCH_ID: PDF-SMOKE-MAJOR-BOUNDARY
REGRESSION_STATUS: PASS_LOCAL
MASTER_CHANGE: templates/ARC_PDF_LAYOUT_MASTER_V2.4.md
STATUS: FIXED_DEV
RECURRENCE_COUNT: 1
```

### ERR-20260919-SOC-PDF-001
```yaml
ERROR_ID: ERR-20260919-SOC-PDF-001
DATE: 2026-09-19
SUBJECT: SOCIAL CORE
SET_ID: ARC_CORE_통합사회2_시험범위전체_V0.4_DRAFT
ERROR_CODE: ERR-PDF-005
SEVERITY: S2
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: 제목/도식/본문 또는 짧은 carry-over가 의미 단위와 맞지 않게 페이지 경계에서 분리됨.
EXPECTED: heading+첫 본문, 표 머리글+첫 행, 그림+직접 설명이 의미 단위로 유지되어야 함.
ACTUAL: 일부 절 시작이 페이지 하단에 고립되고 다음 페이지로 본문이 넘어가거나 짧은 잔여 문단이 새 페이지에 남음.
ROOT_CAUSE: 실제 렌더 높이 중심 분할은 존재했으나 semantic block taxonomy와 source-level overflow/reflow gate가 약했음.
FIX_APPLIED: semantic pagination, widows/orphans, heading orphan, table-row/figure keep rules 및 overflow audit 추가.
PREVENTION_RULE: SEMANTIC_PAGINATION=PASS; HEADING_ORPHAN=0
REGRESSION_BENCH_ID: PDF-SMOKE-SEMANTIC-PAGE
REGRESSION_STATUS: PENDING
MASTER_CHANGE: templates/ARC_PDF_LAYOUT_MASTER_V2.4.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```

### ERR-20260919-CORE-PDF-001
```yaml
ERROR_ID: ERR-20260919-CORE-PDF-001
DATE: 2026-09-19
SUBJECT: CORE COMMON
ERROR_CODE: ERR-PDF-006
SEVERITY: S2
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: 학생용 CORE 본문이 얇고 작게 느껴져 장시간 학습/인쇄 가독성이 낮음.
EXPECTED: Korean body는 Pretendard Regular(400) 중심의 print-first token을 일관 적용.
ACTUAL: 사용자 제공 Social/HISTORY CORE 두 PDF 모두 pdffonts와 독립 PDF inspect에서 NotoSansKR-Thin 임베딩이 확인됨.
ROOT_CAUSE: Thin 계열이 실제 학생용 본문에 임베딩되었고, 기존 권장 weight 규칙이 executable release gate로 강제되지 않았음.
FIX_APPLIED: body 9.9pt target, 1.54~1.58 line-height, dark neutral color, weight >=400 및 preflight font metrics 추가.
PREVENTION_RULE: FONT_TOKEN_COMPLIANCE=PASS; PRINT_LEGIBILITY=PASS
REGRESSION_BENCH_ID: PDF-SMOKE-TYPOGRAPHY
REGRESSION_STATUS: PENDING
MASTER_CHANGE: templates/core/ARC_TEMPLATE_SYSTEM_v0.8_CORE_PATCH.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```

### ERR-20260919-CORE-PDF-002
```yaml
ERROR_ID: ERR-20260919-CORE-PDF-002
DATE: 2026-09-19
SUBJECT: CORE COMMON
ERROR_CODE: ERR-PDF-007
SEVERITY: S2
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: PART/장/절/보조 블록의 시각적 위계가 충분히 분리되지 않아 빠른 스캔이 어려움.
EXPECTED: PART > CHAPTER > SECTION > FUNCTIONAL LABEL의 4단계 hierarchy가 size/weight/spacing으로 식별되어야 함.
ACTUAL: 일부 CORE 지면에서 제목 단계가 비슷한 톤과 크기로 이어져 단원 경계가 약함.
ROOT_CAUSE: 편집 자연스러움 규칙은 있었지만 hierarchy token과 QC field가 명시적 hard/required gate가 아니었음.
FIX_APPLIED: CORE PATCH v0.8에 four-level hierarchy와 QC gate 추가.
PREVENTION_RULE: PART_CHAPTER_SECTION_HIERARCHY=PASS
REGRESSION_BENCH_ID: PDF-VISUAL-HIERARCHY
REGRESSION_STATUS: PENDING
MASTER_CHANGE: templates/core/ARC_TEMPLATE_SYSTEM_v0.8_CORE_PATCH.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```

### ERR-20260921-E2E-001
```yaml
ERROR_ID: ERR-20260921-E2E-001
DATE: 2026-09-21
SUBJECT: KOR CORE CANARY
ERROR_CODE: ERR-PIPELINE-001
SEVERITY: S1
DETECTED_STAGE: NIGHTLY_SIMULATION
HUMAN_FOUND: false
DESCRIPTION: Production contracts described CONTENT_BUNDLE to handoff and PDF gates, but no executable canonical serializer or fixed full pipeline canary existed.
EXPECTED: A fixed bundle must run through serializer, handoff preflight, Typesetter, PDF and preflight with reproducible evidence.
ACTUAL: Individual handoff/PDF tools passed, but the boundary remained specification-only and ad hoc serialization could bypass filename/checksum locks.
ROOT_CAUSE: Executable ownership was implemented per-stage without a single deterministic cross-stage canary.
FIX_APPLIED: Added layout-blind serializer, filename/manuscript checksum verification, fixed KOR CORE 4-page canary, four fault injections, and CI artifact retention.
PREVENTION_RULE: HANDOFF_SERIALIZER=PASS; KOR_CORE_CANARY=CANARY_PASS
REGRESSION_BENCH_ID: KOR-CORE-CANARY-V1
REGRESSION_STATUS: PASS
STATUS: FIXED_CANARY_SCOPE
LIMITATION: Synthetic pipeline fixture only; production model generation, Korean exact source fidelity, and ARC_N remain separately gated.
RECURRENCE_COUNT: 0
```

### ERR-20260921-KOR-N-001
```yaml
ERROR_ID: ERR-20260921-KOR-N-001
DATE: 2026-09-21
SUBJECT: KOR ARC_N CANARY
ERROR_CODE: ERR-PDF-008
SEVERITY: S1
DETECTED_STAGE: NIGHTLY_SIMULATION
HUMAN_FOUND: false
DESCRIPTION: The fixed canary covered CORE only; ARC_N answer count and mandatory blank-page sequence had no executable cross-stage canary.
EXPECTED: A 10-item ARC_N fixture must pass QA, handoff, two-column typesetting, exact page order, answer-count and PDF preflight checks.
ACTUAL: Rules existed in the manifest, but the PDF runner did not prove cover-verso blank, separator blank or 10-to-10 question/answer integrity.
ROOT_CAUSE: Product-specific PDF sequence checks were not connected to the executable canary path.
FIX_APPLIED: Added KOR_N_CANARY_V1, handoff answer-key count validation and PDF page-order/item-count gates.
PREVENTION_RULE: KOR_N_CANARY=CANARY_PASS; ARC_N_QUESTION_COUNT=10; ARC_N_ANSWER_COUNT=10
REGRESSION_BENCH_ID: KOR-N-CANARY-V1
REGRESSION_STATUS: PASS
STATUS: FIXED_CANARY_SCOPE
LIMITATION: Synthetic content; exact school-source and semantic item-quality validation remain pending.
RECURRENCE_COUNT: 0
```

### ERR-20260921-PDF-AUTOFIX-001
```yaml
ERROR_ID: ERR-20260921-PDF-AUTOFIX-001
DATE: 2026-09-21
SUBJECT: PDF QC COMMON
ERROR_CODE: ERR-PIPELINE-002
SEVERITY: S1
DETECTED_STAGE: EVENING_INTEGRATION
HUMAN_FOUND: false
DESCRIPTION: PDF preflight detected defects but had no executable, bounded policy for safe automatic repair and retry.
EXPECTED: Eligible layout defects are mapped to Typesetter-owned profile changes, rerendered, and rechecked without touching locked content.
ACTUAL: A FAIL required ad hoc repair logic outside the executable pipeline.
ROOT_CAUSE: Preflight reporting and Typesetter repair ownership were specified but not connected by an allowlisted controller.
FIX_APPLIED: Added auto-fix classifier/profile mutator, two-attempt and no-progress guards, product isolation, CI smoke, and KOR CORE fail-to-pass exercise.
PREVENTION_RULE: PDF_AUTOFIX_CONTROLLER=PASS; LOCKED_CONTENT_MUTATION=0; MAX_ATTEMPTS=2
REGRESSION_BENCH_ID: KOR-CORE-CANARY-V1-AUTOFIX
REGRESSION_STATUS: PASS
STATUS: FIXED_CANARY_SCOPE
LIMITATION: Production renderer adapters beyond the fixed KOR canary remain to be connected.
RECURRENCE_COUNT: 0
```

### ERR-20260922-TYPESET-AUTH-001
```yaml
ERROR_ID: ERR-20260922-TYPESET-AUTH-001
DATE: 2026-09-22
SUBJECT: TYPESETTER COMMON
ERROR_CODE: ERR-PIPELINE-003
SEVERITY: S1
DETECTED_STAGE: NIGHTLY_SIMULATION
HUMAN_FOUND: false
DESCRIPTION: Executable KOR canaries selected product layout profiles inside each canary, so renderer paths could drift despite a shared written contract.
EXPECTED: Every HTML/ReportLab render resolves active assets and product invariants through one manifest-owned Typesetter admission point.
ACTUAL: Handoff and PDF gates were shared, but each canary directly chose columns, body size and blank-page behavior.
ROOT_CAUSE: Contract-level Typesetter authority was not represented by a shared executable gateway.
FIX_APPLIED: Added Typesetter gateway, route-invariant comparison, active-path resolution, inactive-product rejection, three-product isolation smoke, and routed CORE/N canaries through it.
PREVENTION_RULE: TYPESETTER_SINGLE_AUTHORITY=PASS; RENDERER_ROUTE_CONSISTENCY=PASS; PRODUCT_ISOLATION=PASS
REGRESSION_BENCH_ID: TYPESETTER-GATEWAY-SMOKE-V1
REGRESSION_STATUS: PASS_LOCAL
STATUS: FIXED_DEV
LIMITATION: Production model-authored source inputs and non-KOR subject render adapters remain separately gated.
RECURRENCE_COUNT: 0
```

### ERR-20260922-QA-PROOF-001
```yaml
ERROR_ID: ERR-20260922-QA-PROOF-001
DATE: 2026-09-22
SUBJECT: ARC_N/ARC_FINAL TYPESETTER ADMISSION
ERROR_CODE: ERR-QA-EVIDENCE-BYPASS
SEVERITY: S1
DETECTED_STAGE: TYPESETTER_GATEWAY_AUDIT
HUMAN_FOUND: false
DESCRIPTION: A handoff could declare QA_EVIDENCE_STATUS=PASS and name a QA file that did not exist or disagreed with the answer key.
EXPECTED: Open and rerun the sibling QA proof, then compare subject, count, and each locked answer before PDF production.
ACTUAL: Handoff preflight checked metadata fields and answer count but did not open the named proof or compare answer values.
ROOT_CAUSE: Admission treated producer-controlled QA status as authoritative without independent evidence readback.
FIX_APPLIED: Typesetter gateway opens and validates QA proof and blocks missing evidence, changed answers, and handoff/evidence mismatch.
PREVENTION_RULE: QA_EVIDENCE_READBACK=PASS; ANSWER_EVIDENCE_MATCH=PASS
REGRESSION_BENCH_ID: TYPESETTER-GATEWAY-SMOKE-V1-QA-PROOF
REGRESSION_STATUS: PASS_LOCAL
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```

### ERR-20260922-KOR-SCAN-001
```yaml
ERROR_ID: ERR-20260922-KOR-SCAN-001
DATE: 2026-09-22
SUBJECT: KOR SCHOOL SUPPLEMENT
ERROR_CODE: ERR-EXACT-SOURCE-NOT-READY
SEVERITY: S1
DETECTED_STAGE: SCHOOL_SOURCE_INTAKE
HUMAN_FOUND: false
DESCRIPTION: The canonical 3-page school Korean supplement PDF is image-only; no extractable text layer exists, while the local OCR install lacks Korean language data.
EXPECTED: An exactly verified transcription of all tested passages before user-facing CORE/N source-dependent claims and PDF rendering.
ACTUAL: Raw scan is accessible and visually identifiable, but a line-by-line checked exact text payload does not yet exist.
ROOT_CAUSE: School source was an image-only scan, while the synthetic KOR canary intentionally contained no school passage text.
FIX_APPLIED: Registered Drive ID, raw PDF SHA-256, page count and HOLD status in source inventory; refused to promote synthetic or derived text to raw source authority.
PREVENTION_RULE: KOR_EXACT_SOURCE_LOCK=HOLD_UNTIL_VERIFIED
REGRESSION_BENCH_ID: KOR-SCHOOL-SOURCE-INVENTORY-2026-V1
REGRESSION_STATUS: HOLD_SOURCE_TRANSCRIPTION
STATUS: OPEN
RECURRENCE_COUNT: 0
```

### ERR-20260922-SYNTHETIC-FONT-001
```yaml
ERROR_ID: ERR-20260922-SYNTHETIC-FONT-001
DATE: 2026-09-22
SUBJECT: KOR CORE/N SYNTHETIC CANARY
ERROR_CODE: PDF_VISUAL_GLYPH_SPACING
SEVERITY: S1
DETECTED_STAGE: RENDER_FIRST_VISUAL_QA
HUMAN_FOUND: false
DESCRIPTION: A rendered synthetic PDF showed distorted Latin glyph spacing while the automated PDF preflight reported zero failures and warnings.
EXPECTED: Legible glyph spacing and an embedded Unicode font in nonblank student pages.
ACTUAL: Base14 Helvetica/Helvetica-Bold substitutions caused visibly malformed spacing in the local rendered canary.
ROOT_CAUSE: Synthetic canary PDFs had not embedded their own regular/bold fonts; geometry-only preflight could not detect the visual substitution.
FIX_APPLIED: Embed DejaVu Sans regular/bold in both fixed canaries and verify the PDF font streams are embedded before PASS; re-rendered CORE/N canaries locally.
PREVENTION_RULE: SYNTHETIC_CANARY_EMBEDDED_FONT_AND_VISUAL_REVIEW
REGRESSION_BENCH_ID: KOR-CORE-AND-N-CANARY-EMBEDDED-FONT-V1
REGRESSION_STATUS: PASS_LOCAL_SYNTHETIC_LATIN_ONLY
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```

### ERR-20260922-QA-REPLAY-001
```yaml
ERROR_ID: ERR-20260922-QA-REPLAY-001
DATE: 2026-09-22
SUBJECT: ARC_N/ARC_FINAL QA EVIDENCE
ERROR_CODE: QA_PROOF_WRONG_MANUSCRIPT
SEVERITY: S1
DETECTED_STAGE: TYPESETTER_ADMISSION
HUMAN_FOUND: false
DESCRIPTION: A valid QA evidence file for a different manuscript with the same subject, item count, and ordered answers could be reused after handoff reserialization.
EXPECTED: The actual locked STUDENT MANUSCRIPT must be the one covered by the QA proof.
ACTUAL: The earlier gateway checked proof contents and answer key but did not bind proof to the manuscript bytes.
ROOT_CAUSE: QA evidence schema did not require a final manuscript digest at Typesetter admission.
FIX_APPLIED: Require SHA-256 of the final normalized manuscript in the proof, compare to locked handoff, and block swapped or unbound evidence.
PREVENTION_RULE: QA_EVIDENCE_MANUSCRIPT_BINDING_REQUIRED
REGRESSION_BENCH_ID: TYPESETTER-GATEWAY-SMOKE-V1-QA-MANUSCRIPT-BINDING
REGRESSION_STATUS: PASS_LOCAL_SYNTHETIC
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```

### ERR-20260923-SOC-HEADING-001
```yaml
ERROR_ID: ERR-20260923-SOC-HEADING-001
DATE: 2026-09-23
SUBJECT: SOC CORE SYNTHETIC CANARY
ERROR_CODE: PDF_HEADING_RIGHT_MARGIN_OVERFLOW
SEVERITY: S1
DETECTED_STAGE: PDF_PREFLIGHT
HUMAN_FOUND: false
DESCRIPTION: The long Social Part C heading extended into the right safety margin in the first four-page CORE render.
EXPECTED: Every major heading stays inside the safe frame, wraps without clipping, and remains attached to following content at the start of a new page.
ACTUAL: A single-line insertion method did not wrap the heading; geometry preflight returned TEXT_IN_MARGIN.
ROOT_CAUSE: The fixed canary renderer used a point insertion API for major headings and assumed all titles fit on one line.
FIX_APPLIED: Replaced point insertion with a bounded heading text box, moved body start below the two-line heading area, and fail closed when the text box reports overflow.
PREVENTION_RULE: MAJOR_HEADING_BOUNDED_WRAP_AND_OVERFLOW_CHECK
REGRESSION_BENCH_ID: SOC-CORE-CANARY-V1-LONG-HEADING
REGRESSION_STATUS: PASS_LOCAL_AFTER_SAME_FIXTURE_RETEST
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```

### ERR-20260923-XMARK-RUNTIME-001
```yaml
ERROR_ID: ERR-20260923-XMARK-RUNTIME-001
DATE: 2026-09-23
SUBJECT: SOC C SCHOOL WORKSHEET
ERROR_CODE: XMARK_DETECTOR_RUNTIME_AND_SHAPE_FAILURE
SEVERITY: S1
DETECTED_STAGE: SOURCE_SCOPE_FILTER
HUMAN_FOUND: false
DESCRIPTION: The X-mark detector could not complete its first real-source run because OpenCV was absent, then failed on a valid HoughLinesP result whose array shape differed from the hard-coded indexing assumption.
EXPECTED: The detector opens the canonical worksheet, emits conservative automatic/human-review candidates, and never changes scope without visual confirmation.
ACTUAL: The first run raised ModuleNotFoundError for cv2; after dependency installation the second run raised IndexError while iterating Hough line output.
ROOT_CAUSE: CI did not install the detector's declared runtime dependency, and the implementation assumed one OpenCV return shape.
FIX_APPLIED: Added OpenCV to CI, normalized Hough output to an N-by-4 array, added a raster-X-versus-blank smoke test, and reran the canonical Social C worksheet successfully.
PREVENTION_RULE: XMARK_DETECTOR_DEPENDENCY_AND_SHAPE_SMOKE_REQUIRED
REGRESSION_BENCH_ID: XMARK-DETECTOR-SMOKE-V1
REGRESSION_STATUS: PASS_LOCAL
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```

### ERR-20260923-SOC-XMARK-POLICY-001
```yaml
ERROR_ID: ERR-20260923-SOC-XMARK-POLICY-001
DATE: 2026-09-23
SUBJECT: SOC C SCHOOL WORKSHEET
ERROR_CODE: XMARK_SCOPE_FILTER_NON_BLOCKING
SEVERITY: S1
DETECTED_STAGE: MANIFEST_GOVERNANCE_REVIEW
HUMAN_FOUND: false
DESCRIPTION: The active manifest described Social C handwritten X marks as a non-blocking user filter, allowing excluded content to remain eligible for production evidence.
EXPECTED: Visually verified X-marked regions are hard exclusions for CORE, question stems, distractor knowledge, answer evidence and visual assets.
ACTUAL: The runtime token was NON_BLOCKING_USER_FILTER even though the school worksheet uses X marks to remove material from the tested scope.
ROOT_CAUSE: Source-ingest uncertainty was represented as permissive runtime behavior instead of a fail-closed review state.
FIX_APPLIED: Changed the active mode to BLOCKING_SCOPE_EXCLUSION, registered the verified exclusion index, and made synthetic Social CORE/N fixtures attest that excluded regions are unused.
PREVENTION_RULE: SOCIAL_C_XMARK_INDEX_AND_BLOCKING_SCOPE_GATE_REQUIRED
REGRESSION_BENCH_ID: SYSTEM-VALIDATOR-SOC-C-XMARK-V1
REGRESSION_STATUS: PASS_LOCAL
STATUS: FIXED_DEV
RECURRENCE_COUNT: 0
```


### ERR-20260923-KOR-N-002
```yaml
ERROR_ID: ERR-20260923-KOR-N-002
DATE: 2026-09-23
SUBJECT: KOR ARC_N
SET_ID: ARC_N02_공통국어2_보충자료4편_V1.0
ITEM_ID: SET_LEVEL
ERROR_CODE: ERR-KOR-005
SEVERITY: S1
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: 사용자가 실제 풀이 후 정답이 지나치게 명확하고 매력적인 오답이 부족하여 실제 시험 대비와 괴리가 크다고 보고함. accessible PDF text를 spot-audit한 결과 일부 문항에서 정답만 지문 핵심과 자연스럽게 연결되고 다수 오답은 관련 없는 행동·효과·직접 반대 진술로 즉시 제거 가능한 패턴이 확인됨.
EXPECTED: D3 이상 문항은 최소 2개의 source-grounded near-miss distractor가 실제 후보로 남고, 정답은 근거 비교 전 문체/관련성만으로 드러나지 않아야 함.
ACTUAL: 일부 문항에서 FIRST_PASS 후보가 사실상 1개이고, 표현효과/공통점/개념정의 문항의 오답이 정답과 같은 판단축에서 경쟁하지 못함.
ROOT_CAUSE: 기존 STRONG_DISTRACTOR_COUNT 규칙이 선언적이어서 TRUE_KERNEL·WHY_TEMPTING·DECISIVE_REFUTATION을 증명하지 않아도 strong으로 자체 판정할 수 있었고, key-hidden top-3/second-best/obviousness gate가 없었음.
FIX_APPLIED: ARC_KOREAN_ITEM_ENGINE_V1.2 및 ARC_KOREAN_ITEM_QA_V1.3에 attractive distractor proof, adversarial defense, first-pass candidate, second-best, immediate-elimination, obvious-answer gates 추가. 이전 세트를 regression fixture로 등록.
PREVENTION_RULE: KOR_ATTRACTIVE_DISTRACTOR_GATE=PASS; KOR_OBVIOUS_ANSWER_GATE=PASS; KOR_SECOND_BEST_GATE=PASS
REGRESSION_BENCH_ID: KOR-N-WEAK-DISTRACTOR-20260923-V1
REGRESSION_STATUS: PENDING
MASTER_CHANGE: engine/korean/ARC_KOREAN_ITEM_ENGINE_V1.2.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```


### ERR-20260924-KOR-N-003
```yaml
ERROR_ID: ERR-20260924-KOR-N-003
DATE: 2026-09-24
SUBJECT: KOR ARC_N
SET_ID: ARC_N03_공통국어2_보충자료4편_40Q_V1.0_DRAFT
ITEM_ID: SET_LEVEL
ERROR_CODE: ERR-KOR-006
SEVERITY: S1
DETECTED_STAGE: USER_FEEDBACK
HUMAN_FOUND: true
DESCRIPTION: 사용자가 세트가 지나치게 변별형·미세 추론형으로 구성되어 중요 표현 방법·주제·핵심 소재 기능 등 내신 핵심 포인트 점검이 부족하다고 보고함.
EXPECTED: ARC_N은 지문별 핵심 내신 포인트를 먼저 충분히 점검하고, 그 위에 표준 적용과 상위 변별을 단계적으로 배치.
ACTUAL: 일부 문학 지문군에서 삭제 가정, 단어 치환, 지칭어 미세 추적 등 discrimination-only task가 두드러지고 핵심층이 얇았음.
ROOT_CAUSE: COMMON V4.6의 ARC_N 난도 상향과 KOR V1.2의 integration-first 지표가 결합해 core exam-point coverage보다 변별 난도가 우선됨.
FIX_APPLIED: KOR ITEM ENGINE V1.3, KOR QA V1.4, KOREAN MASTER V4.3에 balanced profile, CORE_EXAM_POINT_COVERAGE, DIFFICULTY_BALANCE, RARE_TASK_BUDGET 추가. FINAL 고난도 정책은 유지.
PREVENTION_RULE: KOR_CORE_EXAM_POINT_COVERAGE=PASS; KOR_DIFFICULTY_BALANCE=PASS; KOR_RARE_TASK_BUDGET=PASS
REGRESSION_BENCH_ID: KOR-N03-OVERDISCRIMINATION-20260924-V1
REGRESSION_STATUS: PENDING
MASTER_CHANGE: subjects/KOREAN_MASTER_V4.3.md
COMMON_ENGINE_CHANGE: false
STATUS: REGRESSION_PENDING
RECURRENCE_COUNT: 1
```

## 9. MONTHLY REVIEW
시험기간 중 또는 10세트 생성마다:
- OPEN/RECURRED 오류 확인
- 동일 코드 반복 횟수 확인
- MASTER 승격 후보 확인
- 불필요하게 중복된 예방규칙 제거
- QA BENCH에 새 회귀케이스 추가 여부 결정


## ERR-2026-09-24-NFINAL-QUALITY-01
- CATEGORY: ITEM_QUALITY / DIFFICULTY_CALIBRATION
- PRODUCTS: ARC_N, ARC_FINAL
- SUBJECTS: KOR, SOC, HIS, SCI
- USER_OBSERVED:
  - overall item difficulty too low for Dongbuk High School exam preparation
  - attractive distractors frequently absent
  - correct answer often identifiable as the longest or most detailed option
  - nominal 5-choice items sometimes function as effective 2~3-choice items
- ROOT_CAUSE:
  - existing rules scored weak distractors but did not universally enforce first-pass candidate competition
  - answer-length audit was stronger in Korean-specific QA than in the cross-subject common stack
  - FINAL had layout assets but no dedicated mandatory difficulty/item-quality release gate
- FIX:
  - COMMON_GENERATION_ENGINE_V4.6
  - ARC_DIFFICULTY_ENGINE_V1.3
  - ARC_ITEM_QUALITY_RUBRIC_V1.5
  - ARC_FINAL_QUALITY_GATE_V1.0
- REGRESSION_REQUIREMENT:
  - inject longest-correct-option cue
  - inject three immediate-elimination distractors
  - inject fake-D4 one-step item
  - verify gate blocks all defects before FINAL release
- STATUS: CANARY_PASS


### CHECKSUM_REGISTRY_NOTE_20260924
The first CI run after N°/FINAL hardening failed only because ops/RUN_LOG.jsonl was newly added to CHECKSUMS.sha256 even though the legacy strict-checksum registry does not track that runtime log entry. Product canaries and behavioral smoke stages passed. The checksum entry was removed; no quality rule rollback was required. KOR ARC_FINAL executable canary subsequently passed after the new answer-length gate correctly rejected an initial baseline whose correct option was longest in 90% of items.


### KOR_FINAL_CANARY_PASS_20260924
- Commit under test: 374f397469148c814be31c851f20022f91ad276e
- GitHub Actions run: 35936878176
- Result: PASS
- Pipeline: Content QA -> FINAL Quality Gate -> Handoff -> Typesetter -> PDF -> PDF Preflight -> strict system validation
- FINAL difficulty profile: D2=1, D3=5, D4=3, D5=1; D4+D5=40%; D1+D2=10%
- Fault injection blocked: weak distractors, longest-correct cue, fake D4, too-easy set
- Initial baseline regression caught: LONGEST_OPTION_IS_KEY_RATE=0.90; fixture corrected and same canary rerun to PASS
- Student PDF answer isolation: PASS; separate answer artifact used
- STATUS: CLOSED_CANARY_PASS


### SCOPE_COMPRESSION_20260924
- TYPE: RUNTIME_PRIORITY / DEADLINE_RISK_REDUCTION
- USER_DECISION: science = oxidation-reduction only; history = ARC_N only
- RISK_BEFORE: remaining sprint still allocated work to HIS FINAL and potentially broad SCI scope, reducing probability of finishing meaningful exam-ready outputs by 2026-09-25.
- FIX: ARC_RUNTIME_PRIORITY_POLICY_V1.2 + SYSTEM_MANIFEST 1.8.22-dev product/scope lock.
- FAIL_CLOSED:
  - SCI non-redox current-sprint work rejected
  - HIS FINAL current-sprint work deferred
- STATUS: ACTIVE_SCOPE_LOCK


### READINESS_GOVERNANCE_20260924
- TYPE: DEADLINE / RELEASE_READINESS
- USER_REQUIREMENT: each active product must reach at least 80% preparation by 2026-09-25.
- RISK: subjective readiness percentages can hide unfinished subject/product combinations.
- FIX: ARC_PRODUCT_READINESS_GATE_V1.0 uses the minimum active subject/product score rather than an average.
- ARC_N MATRIX: KOR_N, SOC_N, HIS_N, SCI_REDOX_N.
- ARC_FINAL MATRIX: KOR_FINAL, SOC_FINAL, SCI_REDOX_FINAL.
- SCORING: five evidence-backed gates × 20 points.
- HARD_FAIL_OVERRIDE: readiness score cannot mask answer, scope, duplicate, difficulty, or PDF release failures.
- STATUS: ACTIVE
