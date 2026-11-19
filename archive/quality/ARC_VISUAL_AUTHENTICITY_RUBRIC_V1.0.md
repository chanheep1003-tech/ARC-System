# ARC_VISUAL_AUTHENTICITY_RUBRIC_V1.0
VERSION: 1.0
DATE: 2026-09-17
STATUS: ACTIVE
ROLE: 문제용 시각자료의 교재·시험지 수준 품질 검수

## PURPOSE
시각자료는 '예쁜 그림'이 아니라 '정확한 평가자료'다.
AI 장식성, 과도한 대칭, 비현실적 디테일, 정보 왜곡을 제거한다.

## HARD VISUAL FAIL
- 문제 조건/정답과 자료 내용 불일치
- 축·단위·범례·라벨 누락
- 입자 수·배치·실험장치 연결 등 과학 구조 오류
- 지도·연표·사료 배치의 사실관계 오류
- 없어도 풀 수 있는 장식용 자료
- 색상에만 의존하여 흑백 출력 불가
- 저해상도·글자 깨짐·한글 렌더 오류
- 과도한 3D·광택·일러스트풍·비정상 도형
- 실제 교재/시험지 톤과 현저히 동떨어짐
- 실제 reference를 확인할 수 있었는데도 무참조로 임의 스타일 생성
- 원본 교재/문제집 visual을 과도하게 모사하여 독창성/저작권 위험이 큼
- 자료가 정답을 노골적으로 암시

## SCORE 100
- INFORMATION_ACCURACY 25
- EDITORIAL_NATURALNESS 20
- FUNCTIONALITY 20
- SUBJECT_AUTHENTICITY 15
- PRINT_ROBUSTNESS 10
- VISUAL_CONSISTENCY 10

REFERENCE_AUTHENTICITY는 EDITORIAL_NATURALNESS와 SUBJECT_AUTHENTICITY에 포함하여 평가한다. reference-first protocol 미준수는 상한 VISUAL_B.

## PASS
92~100 VISUAL_A
86~91 VISUAL_B
80~85 REVISE
79 이하 DISCARD
HARD VISUAL FAIL은 점수 무관 DISCARD

## AI PATTERN FLAGS
AI_OVERDESIGNED
AI_3D_GLOSS
AI_DECORATIVE_GRAPH
AI_UNREALISTIC_LAYOUT
AI_SYMMETRY_OVERLOAD
AI_GENERIC_ICONOGRAPHY
AI_LABEL_NOISE
AI_COLOR_DEPENDENCE
AI_FAKE_PRECISION
AI_TEXT_RENDER_DEFECT
AI_VISUAL_NOT_NEEDED

## SCIENCE
- 그래프 축/단위/눈금/범례
- 입자모형 개수·상태·반응 전후 보존
- 실험장치 연결 방향과 물리적 가능성
- 방향성 화살표 정확성
- 3D 광택보다 선화/도형형 우선

## SOCIAL
- 지도 구역·경계·범례
- 통계축·단위·범주
- 인구피라미드 좌우/연령대
- 흐름도 단계와 방향
- 마케팅 인포그래픽 스타일 금지

## HISTORY
- 연표 선후관계
- 지도 지역·경로·활동범위
- 사료 박스의 문서성
- 조직도 관계 정확성
- 낡은 종이 질감 같은 장식 금지

## PRINT
A4 흑백 우선, 회색조 구분, 일관된 선굵기, 작은 글자 과사용 금지.

## METADATA
VISUAL_QUALITY_SCORE
VISUAL_TIER
VISUAL_FLAGS
BLACK_WHITE_SAFE
INFORMATION_COMPLETE
SUBJECT_AUTHENTICITY
REFERENCE_FIRST_CHECK=true/false
REFERENCE_GAP=true/false
COPY_RISK=LOW/MEDIUM/HIGH
VISUAL_RUBRIC_VERSION=ARC-VAR-V1.0

END ARC VISUAL AUTHENTICITY RUBRIC V1.0
