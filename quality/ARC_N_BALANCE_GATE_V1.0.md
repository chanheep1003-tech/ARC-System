# ARC N BALANCE GATE V1.0
VERSION: 1.0
DATE: 2026-09-25
STATUS: ACTIVE-DEV
ROLE: 모든 과목 ARC_N의 핵심문제 70~80% / 심화문제 20~30% 균형 게이트

## 0. PURPOSE
ARC_N은 실전 FINAL과 목적이 다르다.

ARC_N의 기본 목적:
1. 시험범위의 핵심 출제포인트를 빠짐없이 반복·점검
2. 학교에서 자주 묻는 대표 문제를 충분히 연습
3. 표준 적용·실수 방지
4. 마지막 20~30%에서 상위권 변별 연습

따라서 기본 세트는:
CORE_EXAM_POINT = 70~80%
ADVANCED_DISCRIMINATION = 20~30%
로 구성한다.

이 비율은 난도 D등급과 동일하지 않다.
CORE 문제도 강한 오답·대표 자료 적용으로 D3 또는 필요한 경우 D4가 될 수 있다.

ARC_FINAL에는 본 게이트의 70/30 비율을 강제하지 않는다.

## 1. CLASSIFICATION

### CORE_EXAM_POINT
다음 중 하나 이상을 직접 점검:
- 학교 학습지/보충자료의 명시 핵심
- 교과서 핵심 개념·원리·관계
- 학교 기출에서 반복되는 대표 판단축
- 학습활동의 주요 표현/자료/사례
- 시험 전 반드시 알아야 하는 기본 비교·인과·절차·해석

CORE는 단순 암기 문제만을 뜻하지 않는다.

권장 CORE 난도:
- D1~D3 중심
- 학교 특성에 따라 일부 D4 가능

### ADVANCED_DISCRIMINATION
다음과 같은 추가 변별 부담이 주된 평가목표:
- 2개 이상 자료/조건 통합
- 낯선 사례 전이
- 고매력 HALF_TRUE
- 정교한 비교·비판
- 조건 변경
- 복수 사료/그래프/도표 연결
- 다단계 정량 추론
- 반사실적/고난도 구조 조작

ADVANCED도 반드시 현재 시험범위 안에서 해결 가능해야 한다.

## 2. SET RATIO

권장:
- 10문항: CORE 7~8 / ADVANCED 2~3
- 20문항: CORE 14~16 / ADVANCED 4~6
- 24문항: CORE 17~19 / ADVANCED 5~7
- 25문항: CORE 18~20 / ADVANCED 5~7
- 30문항: CORE 21~24 / ADVANCED 6~9
- 40문항: CORE 28~32 / ADVANCED 8~12

문항수가 작아 정확한 비율이 불가능하면 가장 가까운 정수 배분을 사용한다.

기본 gate:
ARC_N_CORE_RATE >= 0.70
ARC_N_CORE_RATE <= 0.80
ARC_N_ADVANCED_RATE >= 0.20
ARC_N_ADVANCED_RATE <= 0.30

허용 예외:
- 사용자가 명시적으로 고난도/최상위/변별 전용 N제를 요청
- 실제 학교 앵커가 더 높은 변별 비율을 명확히 요구

예외여도 CORE_EXAM_AXIS coverage는 선행한다.

## 3. UNIVERSAL BLUEPRINT FIELDS
모든 ARC_N 문항:
ARC_N_LAYER:
CORE_EXAM_AXIS:
CORE_EXAM_EVIDENCE:
ADVANCED_REASONING_MECHANISM:
SCHOOL_FREQUENCY_CLASS = HIGH | MEDIUM | LOW
TARGET_DIFFICULTY:
ACTUAL_DIFFICULTY:

CORE_EXAM_POINT이면 CORE_EXAM_AXIS와 CORE_EXAM_EVIDENCE가 비어 있으면 안 된다.
ADVANCED_DISCRIMINATION이면 ADVANCED_REASONING_MECHANISM을 명시한다.

## 4. SUBJECT CORE AXES

### KOR
최소 coverage 후보:
- 주제/중심 의미
- 화자·서술자 정서/태도
- 중요 표현법과 효과
- 핵심 시어·소재·이미지 기능
- 시상/시간/서술 구조
- 비문학 중심 주장·핵심 개념
- 글의 구조/서술 방식
- 핵심 개념 관계
- 내용 일치
- 대표 사례 적용

Korean Item Engine의 더 구체적인 coverage gate가 우선한다.

### SOC
현재 요청범위 안에서 가능한 핵심축을 우선:
- 핵심 개념/정의/원칙
- 학교 학습지 명시 내용
- 사상가·관점의 핵심 주장과 차이
- 기본권/헌법/권리구제의 대표 원리·기관·절차
- 세계화/지역화의 핵심 개념과 대표 사례
- 인구 자료의 기본 판독: 비율/수/증감/연령구조/이동
- 대표 지도·그래프·표의 기본 기능
- 원인-결과/목적-수단/주장-근거의 기본 연결

심화는 위 핵심축을 낯선 사례·복수자료·HALF_TRUE로 확장한다.
C파트 X표시 제외 규칙은 항상 우선한다.

### HIS
현재 범위 안에서:
- 핵심 사건/정책의 의미
- 인물·단체·활동 연결
- 사건 선후관계
- 배경/원인
- 결과/영향
- 핵심 사료의 주체·시기·맥락
- 대표 지도/연표/신문/사진 해석
- 유사 사건·단체의 기본 구분

심화:
- 복수 사료 연결
- 연표+인물+단체 교차
- 원인과 결과 복합 연결
- 비슷한 계열/정책의 HALF_TRUE 구분

### SCI
현재 잠긴 시험범위 안에서:
- 핵심 개념/정의
- 핵심 원리·보존관계
- 대표 반응/현상
- 기본 실험·관찰 결과
- 대표 그래프/표/입자모형 판독
- 정성적 변화 방향
- 범위 내 기본 정량관계
- 원인/결과 및 조건 변화

현재 midterm sprint에서는 산화환원만 사용한다.
비산화환원 내용은 본 gate를 이유로 재유입하지 않는다.

심화:
- 복수조건 변화
- 실험+입자/그래프 연결
- 정성+정량 통합
- 순차 투입/전후 상태 비교
- 고매력 수치·보존 HALF_TRUE

### AI
현재 범위 안에서:
- 핵심 용어/개념
- 알고리즘/절차의 기본 순서
- 코드·의사코드 기본 해석
- 데이터 전처리/시각화의 목적
- 출력 결과 해석
- 상관/인과 등 핵심 구분
- 대표 사례 적용

심화:
- 다단계 실행 추적
- 조건 변경
- 데이터→시각화→해석 연결
- 코드 결과와 개념의 복합 판단

현재 sprint에서 AI가 비활성화되어 있으면 활성 제품 우선순위를 변경하지 않는다.

## 5. CORE QUALITY RULE
CORE 70~80%를 쉬운 문제로 채워 비율만 맞추는 것을 금지한다.

CORE 문항도:
- 정답 유일
- 범위 근거 명확
- 오답 최소 1~2개가 실제 혼동축 기반
- D3 이상은 universal distractor gate 적용
- 학교자료/교과서의 핵심을 정확히 점검
- 같은 개념의 단순 반복 금지

다음은 CORE로 카운트하지 않는다:
- 작품명/용어만 알아도 푸는 라벨 문제의 반복
- 선지가 너무 명백해 실질 1~2지선다인 문항
- 같은 정의를 문장만 바꿔 반복
- 핵심축과 무관한 지엽 사실

## 6. ADVANCED QUALITY RULE
ADVANCED는 어렵게 보이기 위한 문항이 아니다.

금지:
- 범위 밖 필수지식
- 불필요한 장문
- 조건 부족
- 지나친 계산노동
- 애매한 표현
- 절대어 하나로 제거되는 오답
- 낯선 소재만 넣고 추론 부담은 없는 가짜 고난도

ADVANCED는 최소 하나:
- 2단계 이상 추론
- 복수 근거/조건 통합
- strong distractor 2개 이상
- 실제 비교/적용/자료통합

을 가져야 한다.

## 7. SET RELEASE GATE
ARC_N_BALANCE_GATE=PASS 조건:
- CORE/ADVANCED 비율 기본 범위 충족
- 과목별 CORE_EXAM_AXIS coverage 누락 없음
- CORE를 단순암기형으로만 채우지 않음
- ADVANCED가 범위 밖 지식에 의존하지 않음
- 정답/오답 품질 gate 통과
- 학교자료 우선순위 유지
- semantic duplicate 없음

REVISE:
- CORE 65~69% 또는 81~85%
- 핵심축 한두 개가 비었지만 재설계 가능
- ADVANCED 과다/부족이 소수 문항 교체로 수정 가능

FAIL:
- CORE <65% without explicit high-difficulty override
- 핵심 범위가 반복적으로 누락
- 심화문제가 세트의 주력을 차지
- 비율을 맞추기 위해 약한 기본문항을 대량 생성
- 범위 밖 지식이 심화 난도의 원인

## 8. REPORT
세트마다 내부 기록:
ARC_N_CORE_COUNT
ARC_N_ADVANCED_COUNT
ARC_N_CORE_RATE
ARC_N_ADVANCED_RATE
CORE_AXIS_DISTRIBUTION
CORE_AXIS_MISSING
ADVANCED_MECHANISM_DISTRIBUTION
DIFFICULTY_DISTRIBUTION
BALANCE_OVERRIDE_REASON
ARC_N_BALANCE_GATE

학생 PDF에는 노출하지 않는다.

END ARC N BALANCE GATE V1.0
