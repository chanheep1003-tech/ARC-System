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

### KOREAN
- ERR-KOR-001 관찰 사실과 화자 추론 혼동
- ERR-KOR-002 화자/작품 지식 과잉추론
- ERR-KOR-003 표현효과 과잉해석
- ERR-KOR-004 현대문학 장문 복제

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
|RISK-HIS-01|한국사|사료 시기/주체 오류|FACT CHECK MATRIX|
|RISK-HIS-02|한국사|민족주의/사회주의 계열 혼동|IDEOLOGICAL_LINE_SWAP 검수|
|RISK-AI-01|AI|DFS/BFS 탐색 순서 오류|방문규칙·탐색구조 독립검증|
|RISK-AI-02|AI|상관↔인과 혼동|AI verification gate|
|RISK-PDF-01|공통|정답이 ARC N° 학생 PDF에 노출|ANSWER_KEY 편집자용 분리|
|RISK-PDF-02|공통|TRUE_VISUAL을 표로 대체|ARC PDF V2.0 TRUE_VISUAL gate|

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
|—|—|—|—|EMPTY|—|

첫 실제 오류부터 순차적으로 기록한다.

## 9. MONTHLY REVIEW
시험기간 중 또는 10세트 생성마다:
- OPEN/RECURRED 오류 확인
- 동일 코드 반복 횟수 확인
- MASTER 승격 후보 확인
- 불필요하게 중복된 예방규칙 제거
- QA BENCH에 새 회귀케이스 추가 여부 결정
