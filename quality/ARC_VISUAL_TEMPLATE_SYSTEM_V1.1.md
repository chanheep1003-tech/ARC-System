# ARC_VISUAL_TEMPLATE_SYSTEM_V1.1
VERSION: 1.1
DATE: 2026-09-18
STATUS: ACTIVE
ROLE: ARC N°/FINAL 시각자료 제작 규격

## CORE
시각자료는 이미지 생성물이 아니라 시험지용 정보 조판물로 제작한다.
정답에 영향을 주는 자료는 `VISUAL_SPEC → deterministic renderer → VISUAL PASS A/B`를 기본 경로로 한다.
생성형 일러스트 모델은 축·수치·입자개수·지도경계·실험연결·연표순서 같은 평가 핵심 자료의 기본 renderer로 사용하지 않는다.

필수 참조:
- quality/visual/ARC_VISUAL_RENDERER_POLICY_V1.0.md
- quality/visual/ARC_VISUAL_PASS_AB_V1.0.md
- 통합사회: quality/visual/SOC_VISUAL_SPEC_V1.0.md


## REFERENCE-FIRST
렌더링 전에 `ARC_VISUAL_REFERENCE_FIRST_V1.0`을 적용한다.
가능한 경우 같은 ASSET_TYPE/TEMPLATE_ID의 실제 교과서·학교 자료·기출·사용자 제공 문제집 visual 2개 이상을 먼저 보고, 정보밀도·선굵기·라벨·여백·패널 문법을 추출한다. 원본 자체는 복제하지 않는다.

## GLOBAL STYLE
- 흰 배경, 장식 최소, 흑백 우선
- 선굵기·글꼴·라벨 체계 일관
- 그림자·광택·그라데이션 원칙적 금지
- 아이콘 최소
- 자료 안 텍스트는 짧고 기능적으로
- 정보 계층 2~3단계 이내

## SCIENCE
### SCI-GRAPH
필수: x/y축, 단위, 눈금, 범례(필요 시), 정확한 데이터
금지: 장식 배경, 임의 곡선, 의미 없는 색

### SCI-PARTICLE
필수: 입자 종류·개수·반응 전후 대응
금지: 3D 광택, 원근감, 무작위 배치

### SCI-EXPERIMENT
필수: 핵심 장치, 연결 관계, 관찰 위치, 조건
권장: 교과서 선화 스타일
금지: 실제 사진풍 렌더, 실험실 배경

### SCI-PROCESS
필수: 단계·방향·조건
권장: 박스+화살표, 전후 비교 패널

## SOCIAL
사회 시각자료는 `SOC_VISUAL_SPEC_V1.0`을 필수 적용한다.

### SOC-MAP
verified vector base, region ID, highlight set, legend, label set 필수. 임의 행정경계 생성 금지.

### SOC-STAT / SOC-DATA
metric, unit, denominator(비율/비중/율), reference year/time, categories/series, values 필수.
비율↔절대수, 증가율↔증가량, 평균↔개인 일반화 오류를 검증한다.

### SOC-FLOW
node/edge/direction/relation 필수. 배치만으로 관계를 암시하지 않는다.

### SOC-CASEBOX
actor, situation, relevant condition, decision target을 분리한다.

### SOC-COMPARE
동일 기준으로 entities를 비교하며 criteria 누락 금지.

### SOC-INSTITUTION
actor → action/request → institution → power → remedy/effect를 방향 edge로 명시한다.

## HISTORY
### HIS-TIMELINE
단순 수평/수직 시간축 + 사건 라벨.
### HIS-MAP
지역/경로/활동범위만 필요한 만큼.
### HIS-SOURCEBOX
사료 본문과 출처/시기 단서 분리. 낡은 종이 질감 금지.
### HIS-ORG
박스+선, 위계/병렬 관계 정확.
### HIS-NEWSPAPER
제목·본문 일부·날짜·출처 단서만 시험지형으로 배치. 실제 신문 재현 금지.

## WIDTH
일반 자료는 단일 컬럼 폭.
복합 그래프·지도·다중패널은 전체 폭.
자료와 문항 본문 분리 금지.
다중패널은 A/B/C 라벨 사용 가능.

## SOURCE-TO-VISUAL
외부 원본 그림 복제 금지.
데이터/구조는 교육용으로 재구성 가능.
수치 변형 시 정답 검증 재수행.

## VISUAL SPEC
VISUAL_ID
SUBJECT
TEMPLATE_ID
ASSET_TYPE
SIZE
DATA
LABELS
AXES_OR_LAYOUT
LEGEND
BLACK_WHITE_MODE
ESSENTIAL
RENDER_NOTES
SOURCE_FACT(optional)
REFERENCE_ANCHOR_IDS(optional)
REFERENCE_SOURCE_LEVELS(optional)
OBSERVED_VISUAL_GRAMMAR(optional)
COPY_RISK(optional)
REFERENCE_GAP(optional)
GENERATION_TRANSFORM(optional)
RENDERER
RENDERER_VERSION
RENDER_MANIFEST_ID
VISUAL_PASS_A
VISUAL_PASS_B
QUESTION_VISUAL_CROSSCHECK

## TEMPLATE IDS
SCI-GRAPH
SCI-PARTICLE
SCI-EXPERIMENT
SCI-PROCESS
SOC-MAP
SOC-STAT
SOC-DATA
SOC-FLOW
SOC-CASEBOX
SOC-COMPARE
SOC-INSTITUTION
HIS-TIMELINE
HIS-MAP
HIS-SOURCEBOX
HIS-ORG
HIS-NEWSPAPER

END ARC VISUAL TEMPLATE SYSTEM V1.0
