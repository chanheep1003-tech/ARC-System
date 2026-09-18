# ARC_VISUAL_ANCHORS_V1.1
VERSION: 1.1
DATE: 2026-09-18
STATUS: ACTIVE
ROLE: 시각자료 품질 비교 기준 레지스트리

## PURPOSE
사용자 제공 학교 기출·학습지·문제집에서 좋은 시각자료의 편집 구조만 추출해 Anchor로 사용한다.
원본 이미지/도표 자체를 복제하지 않는다. 원본 시각물의 고유 표현을 복제하지 않고 일반적인 편집 문법만 추출한다.

## PRIORITY
V0 실제 동북고 시험지 시각자료
V1 현재 학교 학습지/보충자료
V2 현재 시험범위 교과서
V3 사용자 제공 시중 문제집/고난도 N제
V4 공식 평가자료
V5 기존 ARC PREMIUM_BANK_A 시각자료

## SCIENCE TARGET
- SCI-GRAPH 5
- SCI-PARTICLE 5
- SCI-EXPERIMENT 5
- SCI-PROCESS 3
메모: 축 구성, 선굵기, 입자 배치, 장치 단순화, 라벨 밀도, 흑백 안정성

## SOCIAL TARGET
- SOC-MAP 5
- SOC-STAT 5
- SOC-FLOW 4
- SOC-CASEBOX 4
- SOC-COMPARE 4
- SOC-INSTITUTION 4
메모: 지도 단순화, 통계 밀도, 범례, 분모/기준연도, 자료박스 문체, 기관·권리구제 절차 방향, 비교 기준 일치, 인포그래픽 과장 여부

## HISTORY TARGET
- HIS-TIMELINE 5
- HIS-MAP 4
- HIS-SOURCEBOX 5
- HIS-ORG 3
- HIS-NEWSPAPER 2
메모: 문서성, 시간축 밀도, 지도 정보량, 사료 박스 구조, 조직도 관계표현

## RECORD
VISUAL_ANCHOR_ID
SUBJECT
SOURCE_TYPE
SOURCE_FILE_ID
SOURCE_TITLE
SOURCE_ITEM
TEMPLATE_ID
VISUAL_LEVEL
STRUCTURE_NOTES
VISUAL_GRAMMAR_NOTES
DENSITY_NOTES
LABEL_NOTES
PRINT_NOTES
AI_AVOID_NOTES
COPY_ALLOWED=false
STATUS=READY/PENDING

## COMPARISON
새 시각자료는 가능한 경우 같은 TEMPLATE_ID Anchor 2개 이상과 비교:
- 너무 화려한가
- 너무 단순한가
- 정보밀도가 비슷한가
- 글자/선/도형 비율이 자연스러운가
- 실제 문제집처럼 기능 중심인가

## RELEASE
Visual Anchor는 스타일/편집 문법 기준일 뿐 정확성 검증을 대체하지 않는다.
필수 visual은 VISUAL_PASS_A/B와 QUESTION_VISUAL_CROSSCHECK가 선행되어야 한다.
VISUAL_A/B만 BANK_PASS 가능.
PREMIUM_BANK_A는 VISUAL_A 권장.
D4/D5에서 TRUE_VISUAL이 핵심이면 VISUAL_A 없이는 FINAL 우선 후보로 승격하지 않는다.

END ARC VISUAL ANCHORS V1.0
