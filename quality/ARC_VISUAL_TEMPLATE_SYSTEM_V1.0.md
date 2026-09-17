# ARC_VISUAL_TEMPLATE_SYSTEM_V1.0
VERSION: 1.0
DATE: 2026-09-17
STATUS: ACTIVE
ROLE: ARC N°/FINAL 시각자료 제작 규격

## CORE
시각자료는 이미지 생성물이 아니라 시험지용 정보 조판물로 제작한다.
가능하면 벡터·도형·차트·표 기반으로 만들고 생성형 일러스트 스타일은 지양한다.

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
### SOC-MAP
단순 경계+패턴/명도, 범례 명확. 위성지도풍 금지.
### SOC-STAT
막대/선/인구피라미드/표 중심. 마케팅 인포그래픽 금지.
### SOC-FLOW
사각형+화살표 중심.
### SOC-CASEBOX
짧은 사례+수치/표 조합의 시험지 자료박스.

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
GENERATION_TRANSFORM(optional)

## TEMPLATE IDS
SCI-GRAPH
SCI-PARTICLE
SCI-EXPERIMENT
SCI-PROCESS
SOC-MAP
SOC-STAT
SOC-FLOW
SOC-CASEBOX
HIS-TIMELINE
HIS-MAP
HIS-SOURCEBOX
HIS-ORG
HIS-NEWSPAPER

END ARC VISUAL TEMPLATE SYSTEM V1.0
