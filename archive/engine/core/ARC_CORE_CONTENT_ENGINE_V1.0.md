# ARC CORE CONTENT ENGINE V1.0

## 0. PURPOSE
ARC CORE는 단순 요약노트가 아니라 시험 직전까지 반복 사용할 수 있는 `개념 설명 + 시각자료 + 함정 정리 + N° 연결`형 개념서다.
현재 학교 시험범위의 교과서와 학습지를 내신 대비 관점에서 다시 구조화한다.

핵심 목표:
- 얕은 1~2문장 요약 금지
- 개념의 원리/관계/조건을 이해 가능하게 설명
- 자주 혼동되는 개념 분리
- 실제 평가에서 어떻게 묻는지 연결
- N° 문항군과 concept-level 연결

## 1. SOURCE PRIORITY
1. 현재 학교 학습지/교사자료
2. 현재 교과서 시험범위
3. 학교 보충자료
4. 공식 외부자료(필요한 경우)
5. 일반 설명자료

학교자료에 없는 범위를 자동 확장하지 않는다.
사회 C파트 사용자 X 표시 영역은 최상위 OUT OF SCOPE다.

## 2. CONCEPT GRANULARITY
기존 `개념당 4~8줄`, `페이지당 2~4개 개념` 같은 고정 규칙을 폐기한다.

기본:
- 단순 개념: 2~3개/페이지 가능
- 일반 중요 개념: 1~2개/페이지
- 복합/고난도 개념: 1개가 1~1.5페이지 사용 가능

페이지 절약을 위해 필요한 설명/조건/시각자료를 삭제하지 않는다.

## 3. CONCEPT_ID
모든 핵심 개념에 영구 식별자를 부여한다.
형식:
`ARC-{SUBJECT}-{UNIT}-{NNN}`

예:
- ARC-SCI-EV-001
- ARC-SCI-OR-004
- ARC-SOC-B-012
- ARC-HIS-IL-007
- ARC-KOR-LIT-003
- ARC-AI-ML-005

SUBJECT CODE:
SCI / SOC / HIS / KOR / AI

CONCEPT_ID는 제목이 약간 바뀌어도 동일 개념이면 유지한다.

## 4. CONCEPT METADATA
각 concept에는 내부적으로 다음을 보유한다.

CONCEPT_ID
TITLE
SCOPE_SOURCE
PRIORITY = R | S | C
N_LINK = FOUNDATION | APPLICATION | HIGH
VISUAL_IDS
CONFUSING_WITH
PREREQUISITE_IDS
NEXT_IDS

PRIORITY 의미:
R = 시험범위 핵심
S = 핵심 이해를 보조
C = 학교자료에 직접 있을 때만 사용

## 5. CORE BLOCK
학생용 CORE에는 다음 구조를 기본으로 한다.

### 1. CONCEPT_ID + TITLE
작고 깔끔하게 표시.

### 2. ONE-LINE DEFINITION
개념을 한 문장으로 고정.

### 3. CORE EXPLANATION
개념을 충분히 설명한다.
단순 정의 복사 금지.
원인/과정/조건/결과를 필요한 만큼 풀어쓴다.

### 4. RELATION / PROCESS
원인→과정→결과, A↔B 비교, 전/후 상태 등 관계를 명시.

### 5. VISUAL
그래프/도식/표/지도/입자모형/연표/실험도 등.
장식이 아니라 이해에 필요한 경우 우선 배치.

### 6. MUST
반드시 기억해야 할 핵심 1~3개.
지나친 개수 금지.

### 7. CONFUSING
실제로 혼동 가능성이 있는 개념만 비교.
억지 함정 생성 금지.

### 8. EXAM CONNECTION
`선생님이 반드시 낸다` 같은 예측형 문장을 쓰지 않는다.
대신 평가 사고과정을 설명한다.
예:
- 결과 자료에서 원인을 역추론할 수 있음
- 두 조건을 동시에 만족하는지 판단
- 그래프 기울기/구간을 해석
- 비슷한 권리구제 절차를 구분
- 연대/사건 선후관계를 결합

### 9. N° LINK
학생용 표시:
`N° 연결 → 기본 / 적용 / 고난도`

내부적으로는 N° 문항 ID/CONCEPT_ID와 직접 연결 가능.

## 6. N° CONNECTION
N° 문항 metadata:
PRIMARY_CONCEPT_ID
SECONDARY_CONCEPT_IDS[]

학생용 N° 문제지에는 CONCEPT_ID를 굳이 노출하지 않아도 된다.
편집/분석용 metadata에서 유지한다.

CORE concept → N°:
FOUNDATION = 개념 직접 확인/기본 자료
APPLICATION = 조건/자료 적용
HIGH = 복수조건/통합/고난도

## 7. DETAILED EXPLANATION RULE
학교 난도가 높은 과목에서는 설명을 충분히 유지한다.

금지:
- 정의만 쓰고 종료
- 예시 하나만 주고 원리 생략
- 비슷한 개념의 차이를 설명하지 않음
- 시각자료가 필요한데 텍스트만 사용
- 지나친 카드 쪼개기로 흐름 단절

본문 권장:
8.5~9.2pt
line-height 1.60~1.72

## 8. SUBJECT BEHAVIOR
### SCIENCE
실험/그래프/과정/입자모형을 우선.
수치·단위·조건 오류 금지.

### SOCIAL
개념→사례→판단 기준 구조.
학교 학습지 범위가 교과서보다 우선.
C파트 X 표시 금지.

### HISTORY
연표/지도/단체관계/정책 비교를 적극 사용.
현재 교사 스타일 예측 금지.

### KOREAN
작품 핵심구절 전체 복제 대신 표현/정서/관계/비교 구조 중심.
현대문학 저작권에 유의.

### AI
알고리즘 흐름/탐색/데이터 전처리/표·간단 코드 출력 중심.

## 9. LAYOUT INTERACTION
콘텐츠 엔진은 내용 밀도를 우선하고 조판 엔진이 페이지를 결정한다.

원칙:
- 1 concept = 1 page 강제 금지
- 1 page = 4 concepts 강제 금지
- 내용 길이에 따라 동적 페이지 구성
- concept block 중간 분할은 가능한 피함
- VISUAL + 해당 설명은 함께 유지

## 10. ERROR FEEDBACK LOOP
같은 CONCEPT_ID에서 반복 오류가 나면 다음 중 어디 문제인지 분류한다.

A. 문제풀이 오류
B. CORE 설명 부족
C. CONFUSING 누락
D. VISUAL 부족/부정확

B/C/D이면 해당 concept block만 패치한다.
전체 CORE를 불필요하게 재작성하지 않는다.

## 11. QUALITY GATE
CORE concept별 검사:
- 현재 범위인가
- 설명이 충분한가
- 학교자료와 충돌 없는가
- 중요 조건이 누락되지 않았는가
- 시각자료가 실제 이해에 도움 되는가
- CONFUSING이 실제 혼동 포인트인가
- EXAM CONNECTION이 평가 추론과 연결되는가
- N° 연결이 가능한가

## 12. OUTPUT CONTRACT
ARC CORE 생성 요청 시 출력은 다음 구조를 따른다.

CORE_META
SUBJECT
TARGET_RANGE
SOURCE_SCOPE
CONCEPT_COUNT

CONCEPT_BLOCKS
각 concept의 학생용 본문

CORE_LINK_INDEX
CONCEPT_ID → N° FOUNDATION/APPLICATION/HIGH 연결 가능 상태

QC_STATUS
SCOPE
SOURCE_GROUNDED
CONCEPT_ID
VISUAL_COMPLETE
CONFUSING_CHECK
N_LINK_READY
PDF_HANDOFF

상세 검수 사고과정은 출력하지 않는다.
