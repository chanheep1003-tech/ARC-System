# ARC_TEMPLATE_SYSTEM_v0.3_CORE_PATCH
DATE: 2026-09-18
STATUS: ACTIVE PATCH

## ARC CORE 변경사항
기존 v0.2의 다음 규칙을 폐기:
- '한 페이지 2~4개 개념 목표'
- '개념 본문 4~8줄 원칙'
- '중간 밀도 압축본'

새 원칙:
- ARC CORE = 상세 시험대비 개념서
- 1페이지 1~2개 핵심 개념 기본
- 복잡한 개념 1~1.5페이지 허용
- CONCEPT_ID를 학생용에 작게 표시
- CORE → N° 연결 블록 추가
- 시각자료 적극 사용
- 시각자료는 ARC_VISUAL_AUTHENTICITY_RUBRIC 통과 필수
- 상세 설명은 [필수]/[이해]/[보충] 위계 사용
- MUST 최대 3개
- CONFUSING은 실제 혼동 항목만
- EXAM CONNECTION 추가
- 페이지 압축보다 내용 완결성을 우선

## NEW CORE BLOCK
1. CONCEPT_ID + TITLE
2. ONE-LINE DEFINITION
3. CORE EXPLANATION
4. RELATION / PROCESS
5. VISUAL
6. MUST
7. CONFUSING
8. EXAM CONNECTION
9. N° LINK

## DESIGN
- `templates/brand/ARC_BRAND_LOCKUP_SPEC_V1.0.md`의 ARC CORE lockup을 표지/브랜드 헤더에 적용
- ARC master wordmark와 burgundy arc symbol은 N°/FINAL과 완전히 동일한 크기·기하 사용
- CORE는 secondary label/divider만 warm-gray dark #8A877F 사용
- divider 길이/위치, label baseline, 전체 lockup 비율은 N°/FINAL과 동일
- 브랜드 Deep Navy / Warm Gray / Burgundy 유지
- 개념 본문 폭은 읽기 편한 단일 컬럼 우선
- 비교/도식은 2단 내부 배치 가능
- 큰 그림/그래프는 전폭
- 카드 UI처럼 과도하게 조각내지 않음
- 교과서+상위권 내신 개념서의 중간 편집 밀도 지향

END PATCH
