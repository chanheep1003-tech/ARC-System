# ARC VISUAL REFERENCE-FIRST PROTOCOL V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: DEV
ROLE: 실제 교재·학교 자료를 기준으로 ARC 시각자료의 자연스러움과 과목별 편집 문법을 맞추는 사전 절차

## 1. CORE PRINCIPLE
ARC 시각자료는 백지에서 스타일을 상상해 그리지 않는다.
가능한 경우, 같은 과목·같은 자료형의 실제 교과서/학교 학습지/실제 시험/사용자 제공 문제집을 먼저 보고 편집 문법을 추출한 뒤 새 자산을 설계한다.

목표는 원본 복제가 아니라 다음을 학습하는 것이다.
- 정보 밀도
- 선 굵기와 도형 단순화 수준
- 라벨 위치와 길이
- 축/범례/단위 처리
- 화살표·괄호·패널 사용 방식
- 여백과 비율
- 흑백 인쇄 대비
- 과목별로 통용되는 '문제집다운' 시각 문법

## 2. REFERENCE PRIORITY
R0 현재 동북고 실제 시험지/기출의 동일 또는 유사 ASSET_TYPE
R1 현재 학교 학습지·보충자료
R2 현재 시험범위 교과서
R3 사용자 제공 시중 문제집·N제
R4 EBS/교육청/평가원/공식 교육자료
R5 ARC 검증 Visual Anchor

현재 범위 및 사용자 X-제외 규칙은 모든 reference보다 우선한다.

## 3. MINIMUM REFERENCE RULE
새 visual을 만들기 전 가능한 경우:
- 같은 TEMPLATE_ID/ASSET_TYPE reference 2개 이상 확인
- 그중 최소 1개는 R0~R3 권장
- reference가 1개뿐이면 해당 한계를 기록
- reference가 없으면 `REFERENCE_GAP=true`로 기록하고, 가장 보수적인 교과서형 template 사용

## 4. REFERENCE EXTRACTION
원본에서 다음만 추출한다.
- geometry grammar: 박스/선/축/화살표/패널 구조
- density grammar: 한 그림당 정보량
- label grammar: 라벨 위치·길이·정렬
- hierarchy grammar: 제목/범례/주석 단계
- print grammar: 회색조, 선굵기, 패턴
- subject grammar: 과목별 관습적 표현

원본의 독창적 그림·문구·수치·배치를 그대로 복제하지 않는다.

## 5. COPYRIGHT / ORIGINALITY GUARD
금지:
- 시중 문제집/교과서 시각자료를 픽셀 단위로 복제
- 고유한 캐릭터/일러스트/레이아웃을 그대로 모방
- 출처 표기를 제거한 채 원본 그림 재사용
- 원본 수치·문구를 그대로 가져와 새 문항처럼 위장

허용:
- 일반적인 그래프/표/연표/실험 선화의 관습적 형식 참고
- 정보 구조·여백·선굵기·라벨 관습 참고
- 사실/데이터를 별도 검증한 뒤 ARC 방식으로 재구성

## 6. SUBJECT-SPECIFIC REFERENCE CHECK
### SCIENCE
확인: 장치 단순화 수준, 입자 표기, 그래프 축/범례, before/after 패널, 화살표 관습.
실험장치는 물리적 연결과 관찰 지점을 실제 교재 수준으로 맞춘다.

### SOCIAL
확인: 지도 단순화, 통계 그래프 밀도, 사례박스, 인구피라미드, 흐름도 박스 비율.
마케팅 인포그래픽 스타일로 변형하지 않는다.

### HISTORY
확인: 연표 사건 밀도, 지도 범위, 사료박스/조직도, 시대 구분선, 경로 화살표.
역사적 위치·연대 정확성을 스타일보다 우선한다.

## 7. PRE-RENDER VISUAL BRIEF
각 visual은 렌더 전에 아래 최소 메타데이터를 가진다.
- VISUAL_ID
- SUBJECT
- ASSET_TYPE / TEMPLATE_ID
- REFERENCE_ANCHOR_IDS[]
- REFERENCE_SOURCE_LEVELS[]
- OBSERVED_VISUAL_GRAMMAR
- ARC_TRANSFORMATION_PLAN
- COPY_RISK=LOW/MEDIUM/HIGH
- REFERENCE_GAP=true/false

## 8. POST-RENDER COMPARISON
새 visual을 reference와 다시 비교한다.
- 너무 화려하거나 너무 단순하지 않은가
- 정보밀도 차이가 과도하지 않은가
- 라벨/선/도형 비율이 문제집답게 보이는가
- 원본을 너무 닮아 COPY_RISK가 올라가지는 않았는가
- 실제 A4 시험지에 들어갔을 때 이질감이 없는가

## 9. RELEASE GATE
다음 중 하나면 REVISE:
- REFERENCE_GAP인데 새로운/복잡한 시각 문법을 임의 창작함
- R0~R3 reference와 현저히 다른 정보 밀도/비율
- 생성형 일러스트 느낌이 강함
- 원본을 과도하게 닮음
- 실제 시험지/교재 옆에 두었을 때 명백히 이질적임

END ARC VISUAL REFERENCE-FIRST PROTOCOL V1.0
