# ARC_DIFFICULTY_ANCHORS_V1.0
VERSION: 1.0
DATE: 2026-09-17
ROLE: 난이도 비교용 대표 기준문항 레지스트리
STATUS: ACTIVE

## 원칙
Anchor는 문제를 복제하기 위한 저장소가 아니다.
새 문항의 상대 난도를 비교하기 위한 기준점이다.

원본 문장·선지·그림을 그대로 재사용하지 않는다.
각 Anchor에는 구조 정보와 난도 특성만 기록한다.

## Anchor 등급
- SCHOOL_STANDARD: 실제 동북고의 보통 난도
- SCHOOL_UPPER: 실제 동북고의 변별 난도
- WORKBOOK_MID: 문제집/외부자료 중간 난도
- WORKBOOK_HIGH: 문제집/고난도자료 상위 난도
- ARC_BANK: 누적된 검증문항은행 내부 기준

## 초기 참조 소스

### 공통국어2
- 2025-2학기 동북고 중간 공통국어2 실제 시험
- 현재 학교 보충자료/학습지
- 국어 문제집·참고자료 중 현재 시험범위와 직접 맞는 자료
상태: ANCHOR_SELECTION_PENDING

### 통합과학2
- 2025-2학기 동북고 중간 통합과학2 실제 시험
- `정합_통합과학_고난도20제_문제지.pdf`
- `통합과학2_고난도N제_40문항.pdf`
- 현재 범위 교과서/학습지/외부자료은행
상태: ANCHOR_SELECTION_PENDING

### 통합사회2
- 2025-2학기 동북고 중간 통합사회2 실제 시험
- A/B/C 학교 학습지
- 통합사회 문제집·참고자료 중 현재 범위와 직접 맞는 자료
- C파트 손글씨 X 영역은 Anchor 후보에서도 제외
상태: ANCHOR_SELECTION_PENDING

### 한국사2
- 2025-2학기 동북고 중간 한국사2 실제 시험
- 현재 교과서/학교자료
- 한국사 문제집·참고자료 중 현재 범위와 직접 맞는 자료
상태: ANCHOR_SELECTION_PENDING

### 인공지능기초
- 2025 기출/학교자료 중 현재 범위와 일치하는 문항
- 길벗 현재 범위
- 문제집·참고자료가 있으면 범위 일치 자료만 사용
상태: ANCHOR_SELECTION_PENDING

## 과목별 목표 Anchor 수
처음에는 과목별 최소:
- SCHOOL_STANDARD 5
- SCHOOL_UPPER 3
- WORKBOOK_MID 3
- WORKBOOK_HIGH 3

자료 부족 시 억지로 채우지 않는다.
그 경우 DIFFICULTY_CONFIDENCE=LOW 또는 MEDIUM.

## RECORD TEMPLATE
```yaml
ANCHOR_ID:
SUBJECT:
SOURCE_TYPE:
SOURCE_FILE_ID:
SOURCE_FILE_TITLE:
SOURCE_ITEM:
CONCEPT_ID:
QUESTION_FORM:
REFERENCE_LEVEL:
STRUCTURAL_SCORE:
SCHOOL_RELATIVE:
KEY_DIFFICULTY_FACTORS:
  concept_load:
  reasoning_depth:
  data_load:
  distractor_strength:
  condition_load:
  transfer_novelty:
COPY_ALLOWED: false
NOTES:
```

## 선택 기준
1. 실제 학교 기출에서는 쉬운 문항만 고르지 말고 분포를 대표하도록 선택.
2. 문제집은 난도표시가 있더라도 구조를 직접 평가.
3. 범위 밖 지식이 필요한 문항은 Anchor에서 제외.
4. 오류/복수정답/조건부족 문항은 제외.
5. 비슷한 구조만 여러 개 고르지 않는다.
6. 같은 Anchor를 장기간 사용하되 실제 시험이나 자료가 갱신되면 교체 검토.

## 3시간 QA 사용
- 신규 문항의 같은 CONCEPT_ID 또는 유사 QUESTION_FORM Anchor를 우선 찾는다.
- 가능하면 LOW/HIGH 두 기준 사이에서 상대 위치를 판단.
- Anchor가 없으면 검증문항은행의 기존 PASS 문항을 보조 Anchor로 사용.
- 비교가 억지이면 구조점수만 사용하고 LOW_CONFIDENCE로 기록.

## 업데이트
처음 실제 Anchor 선정이 완료되면 `ANCHOR_SELECTION_PENDING`을 `READY`로 변경한다.
학교 시험이 새로 생기면 이전 시험 Anchor를 삭제하지 않고 연도 태그를 추가해 비교한다.
