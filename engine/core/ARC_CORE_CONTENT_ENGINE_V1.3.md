# ARC CORE CONTENT ENGINE V1.3
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: 상세 내신 개념서 콘텐츠 생성
BASE_RULESET: ARC 1.7.7-dev

## 0. PURPOSE
ARC CORE는 단순 요약노트가 아니라 시험범위를 반복 학습할 수 있는 상세 내신 개념서다.
현재 학교 학습지·교과서·보충자료를 가장 높은 근거로 삼아 개념의 원리, 관계, 조건, 혼동 포인트를 다시 구조화한다.

CORE의 학생용 결과물은 'AI가 항목을 자동 정리한 카드 모음'이 아니라 실제 편집자가 만든 참고서처럼 읽혀야 한다.

핵심 목표:
- 얕은 1~2문장 요약 금지
- 개념의 원리/관계/조건을 이해 가능하게 설명
- 실제 혼동 포인트를 구분
- 문제에서 틀리기 쉬운 판단 함정을 근거 있게 정리
- 필요한 시각자료를 기능적으로 사용
- N° 출제를 위한 concept-level metadata는 내부에만 유지
- 학생용에는 내부 ID/QC/N° 링크를 노출하지 않음
- 동일 템플릿 반복보다 내용에 맞는 자연스러운 편집 흐름 우선

필수 편집 규칙:
engine/core/ARC_CORE_EDITORIAL_ARCHITECTURE_V2.0.md
quality/ARC_CORE_EDITORIAL_NATURALNESS_V1.2.md
quality/ARC_CORE_QA_BENCH_V1.2.md
engine/core/ARC_CORE_DEPTH_ENGINE_V1.1.md

## 1. SOURCE PRIORITY
1. 현재 학교 학습지/교사자료
2. 현재 교과서 시험범위
3. 학교 보충자료
4. 사용자가 직접 제공·업로드한 시험범위 자료
5. 공식 외부자료(필요한 경우)
6. 일반 설명자료

학교자료에 없는 범위를 자동 확장하지 않는다.
사회 C파트 사용자 X 표시 영역은 최상위 OUT OF SCOPE다.
과목 ACTIVE MASTER의 범위 제외 규칙은 CORE에도 그대로 적용한다.

학교자료와 일반 설명이 충돌하면 학교자료의 현재 시험범위 해석을 우선한다.
자료를 실제로 읽지 못했으면 읽었다고 간주하지 않는다.

## 2. MACRO EDITORIAL ARCHITECTURE — REQUIRED BEFORE CONCEPT WRITING
ARC CORE는 concept를 하나씩 잘 쓰는 것만으로 PASS하지 않는다.
학생용 원고를 쓰기 전에 engine/core/ARC_CORE_EDITORIAL_ARCHITECTURE_V2.0.md에 따라 chapter/cluster 수준 구조를 먼저 만든다.

Required internal fields:
CENTRAL_QUESTION
CHAPTER_THESIS
DOMINANT_ORGANIZATION
BACKBONE_NODES[]
ESSENTIAL_RELATIONS[]
SUPPORTING_DETAILS[]
END_SYNTHESIS_MODE

핵심:
- chapter당 하나의 중심 질문
- 3~6개의 backbone node
- 하나의 지배적 조직 원리(시간/인과/비교/문제-해결/구조/작품 흐름/기제-조건)
- concept는 backbone 안에 배치
- 본문 설명이 중심
- 표/박스/요약은 설명을 대체하지 않음
- 동일 사실의 본문→요약→표→도식 반복 금지
- chapter 마지막은 통합 문단/단일 구조도/판단 기준 중 하나를 기본으로 선택

CONTENT_LOCK 전 CORE_EDITORIAL_ARCHITECTURE=PASS가 필수다.

## 3. CONCEPT GRANULARITY
고정 분량 규칙을 두지 않는다.

기본:
- 단순 개념: 짧은 설명으로 종료 가능
- 일반 중요 개념: 충분한 본문 + 필요한 보조 블록
- 복합/고난도 개념: 한 개념이 1페이지 이상 사용 가능
- 서로 강하게 연결된 짧은 개념은 한 페이지 안에서 자연스럽게 묶을 수 있음

금지:
- 모든 concept를 같은 길이로 맞춤
- 모든 concept를 같은 수의 bullet로 맞춤
- 페이지를 채우기 위해 설명/예시/박스를 추가
- 페이지 절약을 위해 필요한 조건/예외/근거를 삭제

## 4. CONCEPT_ID — INTERNAL ONLY
모든 핵심 개념에 영구 식별자를 부여한다.

형식:
ARC-{SUBJECT}-{UNIT}-{NNN}

예:
ARC-SCI-OR-004
ARC-SOC-PUN-003
ARC-HIS-IL-007
ARC-KOR-LIT-003
ARC-AI-ML-005

SUBJECT CODE:
SCI / SOC / HIS / KOR / AI

CONCEPT_ID는 제목이 약간 바뀌어도 동일 개념이면 유지한다.

중요:
- CONCEPT_ID는 학생용 CORE PDF에 표시하지 않는다.
- 내부 CONTENT_BUNDLE / CORE_LINK_INDEX / 출제 metadata에서만 사용한다.
- 학생용 제목은 실제 개념명/작품명/소제목만 사용한다.

## 5. INTERNAL CONCEPT METADATA
각 concept에는 내부적으로 다음을 보유한다.

CONCEPT_ID
TITLE
SCOPE_SOURCE
SOURCE_IDS[]
PRIORITY = REQUIRED | SUPPORTING | CONDITIONAL
N_GENERATION_LINKS[]
VISUAL_IDS[]
CONFUSING_WITH[]
PREREQUISITE_IDS[]
RELATED_IDS[]
TRAP_EVIDENCE[]
SOURCE_TEXT_IDS[] (필요 시)
DEPTH_PRIORITY = STANDARD | ADVANCED | HIGH_DIFFICULTY
DEPTH_REASON[]
DEPTH_EVIDENCE[]
DEPTH_AXES[]
DEPTH_SOURCE_IDS[]

PRIORITY:
REQUIRED = 현재 시험범위 핵심
SUPPORTING = 핵심 이해를 보조
CONDITIONAL = 학교자료에 직접 있거나 요청 범위에서 필요할 때만

DEPTH_PRIORITY:
- 학생용 표시 금지
- engine/core/ARC_CORE_DEPTH_ENGINE_V1.1.md로 결정
- HIGH_DIFFICULTY는 범위 밖 내용을 추가하는 권한이 아니라 범위 안 판단축을 더 완전하게 설명하는 편집 우선순위
- 사용자 지정 고난도 영역은 source scope 안에서 우선 반영

N_GENERATION_LINKS:
- 학생용 표시 금지
- 향후 N° Generator가 문항 설계 시 참고하는 내부 인덱스
- 값은 관련 CONCEPT_ID 중심으로 저장
- 특정 N° 문제 번호를 CORE 학생용에 연결하지 않음
- 문제 생성 시 PRIMARY_CONCEPT_ID / SECONDARY_CONCEPT_IDS 설계에 활용

## 6. STUDENT-FACING CORE STRUCTURE
학생용은 고정 블록 템플릿을 강제하지 않는다.
chapter backbone과 연속 본문 흐름을 기본으로 하고, concept-level 요소는 필요한 경우에만 보조적으로 사용한다.

중요:
- concept card가 chapter structure를 대체하면 FAIL
- 한 소단원에 MUST/CONFUSING/TRAP/EXAM CONNECTION을 모두 강제하지 않음
- chapter마다 반복되는 "핵심 정리 → 주의 → 문제 적용" 순서를 만들지 않음
- summary는 재나열이 아니라 관계를 압축해야 함

### TITLE
실제 개념명 또는 작품/주제 소제목.
내부 ID를 붙이지 않는다.

### CORE EXPLANATION — 기본
핵심 설명.
정의만 복사하지 않고 원리/조건/관계/근거를 필요한 만큼 설명한다.
본문 자체가 충분하면 ONE-LINE DEFINITION을 따로 만들지 않아도 된다.

### RELATION / PROCESS — 선택
원인→과정→결과, 전/후 상태, 구조적 관계가 실제 이해에 필요할 때만.

### VISUAL — 선택
그래프/도식/표/지도/입자모형/연표/작품 구조도 등.
없어도 이해에 지장이 없으면 만들지 않는다.

### MUST — 선택
반드시 고정해야 할 핵심만 1~3개.
본문 문장을 그대로 복사하지 않는다.
모든 concept에 강제하지 않는다.

### CONFUSING — 선택
실제로 혼동 가능한 개념/판단축이 있을 때만.
차이가 한 축이면 문장으로 처리하고, 여러 축이면 비교표를 허용한다.

### TRAP — 선택
실제 평가에서 잘못 판단하기 쉬운 지점을 짚는다.
단순 '주의하세요' 박스가 아니라 왜 틀리는지 판단축이 보여야 한다.

TRAP 사용 조건:
- 학교자료/기출/검수 결과/일반적인 학습 오개념 중 하나 이상의 근거 존재
- 해당 개념 이해에 실제 도움이 됨
- 본문 또는 CONFUSING과 단순 중복 아님

TRAP 금지:
- 출제 가능성을 과장하기 위한 억지 함정
- 근거 없이 AI가 새로 만든 극단적 오답
- '무조건/반드시 시험에 나온다' 식 예측
- 모든 concept에 기계적으로 하나씩 배치
- 같은 '~가 아니다' 문형 반복

### EXAM CONNECTION — 선택
출제 예언이 아니라 이 개념을 문제에서 어떤 판단 과정으로 사용할 수 있는지를 짧게 설명한다.
예:
- 두 자료에서 같은 기준을 찾아 비교
- 결과에서 원인/조건을 역추론
- 비슷한 개념을 한 판단축에서 구분
- 작품 내부 근거와 화자의 추론을 분리

매 concept마다 강제하지 않는다.

## 7. N° GENERATION CONNECTION — INTERNAL ONLY
CORE는 학생에게 N° 링크를 보여 주지 않는다.

내부적으로:
CORE CONCEPT_ID
→ N_GENERATION_LINKS
→ 이후 N° SET_BLUEPRINT의 PRIMARY_CONCEPT_ID / SECONDARY_CONCEPT_IDS

활용:
- 시험범위 concept coverage 확인
- 동일 개념의 단순 중복 출제 방지
- 기본/적용/고난도 문항 설계 시 개념 조합 참고
- 미출제 concept 탐지
- CORE 설명과 N° 문항의 범위 일치 검증

학생용 CORE PDF에는 다음을 노출하지 않는다:
CONCEPT_ID
N_GENERATION_LINKS
FOUNDATION/APPLICATION/HIGH
BANK tier
QA score
priority
internal source ID

## 7-A. ADAPTIVE DEPTH
모든 concept를 같은 깊이로 설명하지 않는다.
engine/core/ARC_CORE_DEPTH_ENGINE_V1.1.md를 적용해 STANDARD / ADVANCED / HIGH_DIFFICULTY를 내부 분류한다.

학생용에는 DEPTH_PRIORITY, DEPTH_REASON, DEPTH_EVIDENCE를 노출하지 않는다.

HIGH_DIFFICULTY는 다음을 의미한다:
- 기본 원리를 다시 길게 반복하는 것이 아니라 판단을 갈라놓는 조건과 경계를 더 자세히 설명
- 실제 혼동 근거가 있으면 CONFUSING/TRAP을 강화
- 복수 자료·비교·조건 적용이 핵심이면 사고 흐름을 설명
- 필요한 표/도식/원문 근거를 충분히 사용
- 범위 밖 상위과정/배경지식으로 어려움을 부풀리지 않음

학생용 편집에서 FOUNDATION / CONDITIONS / BOUNDARIES / HIDDEN_ASSUMPTIONS / TRAP LOGIC / MULTI-STEP APPLICATION 같은 내부 depth 단계명을 고정 제목으로 출력하지 않는다.
내용에 맞게 본문과 필요한 보조 요소로 자연스럽게 흡수한다.

## 8. EDITORIAL NATURALNESS — HARD REQUIREMENT
quality/ARC_CORE_EDITORIAL_NATURALNESS_V1.2.md를 반드시 적용한다.

핵심:
- 모든 개념을 같은 구조로 찍어내지 않는다.
- 본문이 중심이고 박스는 보조다.
- 필요 없는 제목/표/박스는 만들지 않는다.
- 문장 길이와 문단 길이를 기계적으로 균일화하지 않는다.
- 같은 설명을 CORE EXPLANATION / MUST / TRAP에서 반복하지 않는다.
- 실제 교과서·학습지 용어를 우선한다.
- '쉽게 말하면', '핵심은', '즉', '따라서' 같은 연결어를 습관적으로 반복하지 않는다.
- 이모지, 마케팅 문구, 과도한 느낌표, AI 메타 문장을 쓰지 않는다.
- 근거 없는 '시험에 잘 나온다/선생님이 낸다' 표현 금지.
- 학생용에 내부 metadata가 보이면 HARD FAIL.

## 9. SUBJECT BEHAVIOR

### SCIENCE
원리 → 조건 → 과정/자료 → 결과 관계를 우선.
실험/그래프/과정/입자모형은 실제 이해에 필요한 경우 적극 사용.
수치·단위·조건 오류 금지.
TRAP은 산화제/환원제, 원인/결과, 입자 수, 그래프 축 해석 등 실제 오개념 근거가 있을 때 사용.

현재 사용자 지정 HIGH_DIFFICULTY:
- OR 산화·환원
- EM 전자기 유도

OR/EM은 ARC_CORE_DEPTH_ENGINE_V1.0의 과학 profile을 적용한다.
단, SCIENCE_MASTER의 ADVANCED LEAK BLOCK을 넘어서는 심화는 금지한다.
깊이는 공식 추가가 아니라 조건 해석·자료 읽기·개념 경계·복합 판단을 강화하는 방식으로 만든다.

### SOCIAL
개념 → 판단 기준 → 사례/비교 흐름.
학교 학습지 범위가 교과서보다 우선.
C파트 X 표시 금지.
사상가·이론은 실제 주장과 정당한 함의를 구분한다.
TRAP은 HALF_TRUE, 조건 누락, 권리/기관 혼동, 사상가 귀속 오류처럼 실제 판단축에 기반.

칸트·베카리아 형벌/사형 논쟁이 현재 범위에 포함되면 HIGH_DIFFICULTY 우선 대상.
단순 찬반 정리가 아니라 정당화 근거, 목적, 책임, 인간을 수단으로 대하는 문제, 비례성, 사회계약, 상대 비판 범위를 구분한다.
SOCIAL_MASTER의 CLAIM FIDELITY GATE를 그대로 적용한다.

### HISTORY
사건을 낱개 카드로 쪼개기보다 시기·원인·전개·관계를 연결해 서술.
연표/지도/단체 관계/정책 비교는 실제 필요할 때 사용.
현재 교사 스타일 예측 금지.
TRAP은 주체·시기·선후관계·비슷한 단체/정책 혼동에 근거.

한국사는 고난도 단원을 사전 고정하지 않는다.
현재 학교자료/교과서/기출에서 HISTORY_DIFFICULTY_SIGNAL을 탐지해 ADVANCED/HIGH_DIFFICULTY 후보를 정한다.
특히 단체의 결성·분화·통합, 세력 관계, 겹치는 시기, 사료 주체 추론, 정책·단체의 유사성이 한 cluster에 겹칠수록 깊이를 높인다.
evidence 없이 '이 단원은 어렵다'고 임의 승격하지 않는다.

### KOREAN
기본 규칙:
subjects/KOREAN_MASTER_V4.1.md의 SOURCE-BOUND ORIGINAL TEXT MODE를 그대로 적용한다.

국어 CORE는 작품을 '주제/정서/표현법' 카드 세트로 잘게 분해하는 방식을 기본으로 하지 않는다.
작품 전체의 흐름과 학교 보충자료의 해석 구조를 우선한다.

권장 흐름:
1. 작품/지문 SOURCE_TEXT_BLOCK — 실제 source에서 확보된 경우
2. 작품 전체 상황·구조를 이해하는 짧은 도입
3. 중요한 시어/장면/문단의 기능과 해석 근거
4. 표현과 효과의 연결
5. 화자/서술자/대상의 관계 또는 논지 구조
6. 필요한 CONFUSING / TRAP / 비교
7. 필요할 때만 EXAM CONNECTION

SOURCE_TEXT_BLOCK:
- 사용자 직접 제공/업로드 또는 연결 Drive의 학교자료·교과서·보충자료에서 실제 확보한 원문은 전문/시험범위 전체 수록 가능
- 시는 행·연·문장부호·순서를 보존
- 산문은 문단 순서를 보존
- 원문과 학교 해설을 섞어 하나의 원문처럼 만들지 않음
- 원문을 기억으로 복원하지 않음
- 동일 원문을 concept마다 반복하지 않고 작품 단위에서 1회 공유 가능

국어 CORE source emphasis:
1. 학교 보충자료/학교 학습지의 작품 해석·비교·강조점
2. 사용자가 직접 제공한 보충자료
3. 교과서/학습활동은 원문·기초 개념·빈틈 보완
4. 외부 해설은 검증 보조

교과서 기본 설명을 기계적으로 다시 길게 쓰지 않는다.
보충자료가 교과서 개념을 전제로 더 깊은 해석/비교축을 제공하면 그 구조를 CORE의 중심으로 삼는다.

국어 설명:
- 학교 보충자료·학습지의 용어와 해석 구조를 최우선
- 작품 밖 작가 생애/시대 지식을 정답 근거처럼 덧붙이지 않음
- 화자가 관찰한 사실과 화자의 추론을 구분
- 표현법 이름보다 '어떤 표현이 어떤 효과를 만드는가'를 근거와 연결
- 같은 작품의 정서·태도·주제를 한 문장 라벨로 과도하게 단순화하지 않음
- 보충자료가 강조한 비교 축이 있으면 그 축을 중심으로 정리

국어 TRAP 예시 원리:
- 관찰 사실 ↔ 화자의 추론 혼동
- 표현법은 맞지만 효과를 과장
- 부분 정서는 맞지만 작품 전체 태도로 일반화
- 공통점은 맞지만 차이의 근거가 다른 작품에만 존재
- 작품 밖 지식으로 화자/대상의 내면을 확정
단, 실제 source/검수 근거가 있을 때만 사용한다.

### AI
알고리즘 흐름/탐색/데이터 전처리/표·간단 코드 출력 중심.
단계가 중요한 개념은 흐름을 보존.
TRAP은 탐색 순서, 데이터 처리 순서, 용어 혼동처럼 실제 오류에 근거.

## 9. LAYOUT INTERACTION
콘텐츠 엔진은 내용 흐름과 정보 위계를 결정하고 조판 엔진이 페이지를 결정한다.

원칙:
- 1 concept = 1 page 강제 금지
- 페이지마다 같은 수의 concept 강제 금지
- concept block 중간 분할은 가능한 피함
- VISUAL + 해당 설명은 함께 유지
- 박스보다 본문이 시각적으로 우세해야 함
- 빈 공간을 장식으로 채우지 않음
- CORE는 단일 컬럼 본문을 기본으로 하되 비교/도식은 필요 시 내부 2단/전폭 사용 가능
- 국어 SOURCE_TEXT_BLOCK은 PDF MASTER V2.2의 fidelity 규칙 적용

## 10. ERROR FEEDBACK LOOP
같은 CONCEPT_ID에서 반복 오류가 나면 원인을 분류한다.

A. 문제풀이 오류
B. CORE 설명 부족
C. CONFUSING 누락
D. TRAP 누락/잘못된 함정
E. VISUAL 부족/부정확
F. SOURCE 해석/근거 문제

B/C/D/E이면 해당 concept block만 패치한다.
F이면 source를 다시 확인한 뒤 수정한다.
전체 CORE를 불필요하게 재작성하지 않는다.

N° 검수에서 반복적으로 발견된 오개념은 근거가 충분할 경우 TRAP_EVIDENCE로 CORE에 역반영할 수 있다.
단, 한 세트의 우연한 오답 구조를 곧바로 일반 TRAP으로 승격하지 않는다.

## 11. QUALITY GATE
concept별:
- 현재 범위인가
- 설명이 충분한가
- 학교자료와 충돌 없는가
- 중요 조건이 누락되지 않았는가
- 시각자료가 실제 이해에 도움 되는가
- CONFUSING이 실제 혼동 포인트인가
- TRAP에 근거가 있는가
- 학생용 내부 metadata 노출이 없는가

set-level:
- CORE_QA_STATUS = PASS
- DEPTH_ASSIGNMENT = PASS
- DEPTH_EVIDENCE = PASS
- DEPTH_SCOPE_SAFETY = PASS
- DEPTH_BUDGET = PASS
- CORE_EDITORIAL_NATURALNESS = PASS
- BLOCK_REPETITION = PASS
- LANGUAGE_RHYTHM = PASS
- SOURCE_TERMINOLOGY_MATCH = PASS
- STUDENT_METADATA_LEAK = PASS
- SOURCE_GROUNDED = PASS

국어 SOURCE_TEXT_BLOCK 사용 시 추가:
SOURCE_ACCESS = PASS
SOURCE_TEXT_FIDELITY = PASS
SOURCE_TEXT_COMPLETENESS = PASS
SOURCE_TEXT_LINKAGE = PASS

하나라도 필수 FAIL이면 READY_FOR_TYPESET 금지.

## 12. OUTPUT CONTRACT
ARC CORE 생성 요청 시:

CORE_META
SUBJECT
TARGET_RANGE
SOURCE_SCOPE
CONCEPT_COUNT

CORE_MANUSCRIPT
학생용 본문.
내부 ID/QC/N° linkage 노출 금지.

SOURCE_TEXT_BLOCKS
필요한 경우 Content Bundle Contract의 source-bound 구조 사용.
학생용에 실제 노출할 원문은 CORE_MANUSCRIPT에서 적절한 위치에 배치.

CORE_LINK_INDEX — INTERNAL
CONCEPT_ID
N_GENERATION_LINKS[]
PREREQUISITE_IDS[]
RELATED_IDS[]

QC_STATUS
CORE_QA_STATUS
CORE_QA_SCORE
CORE_QA_TIER
SCOPE
SOURCE_GROUNDED
CONCEPT_ID_INTEGRITY
VISUAL_COMPLETE
CONFUSING_CHECK
TRAP_EVIDENCE_CHECK
DEPTH_ASSIGNMENT
DEPTH_EVIDENCE
DEPTH_SCOPE_SAFETY
DEPTH_BUDGET
HIGH_DIFFICULTY_COMPLETENESS
CORE_EDITORIAL_NATURALNESS
STUDENT_METADATA_LEAK
N_LINK_READY
PDF_HANDOFF

상세 검수 사고과정은 출력하지 않는다.

END ARC CORE CONTENT ENGINE V1.3
