# ARC_CORE_BOOK_QA_V1.0
DATE: 2026-10-15
STATUS: ACTIVE (core_profile = BOOK)
RELATES: engine/core/ARC_CORE_BOOK_EDITORIAL_V1.0.md · templates/core/ARC_TEMPLATE_SYSTEM_v0.9_CORE_BOOK_PATCH.md
REPLACES (BOOK 한정): ARC_CORE_EDITORIAL_NATURALNESS_V1.2의 ‘박스 반복/블록 반복’ 항목 · ARC_CORE_QA_BENCH_V1.2의 anti-listing 항목

## 1. 통과 기준 (모두 충족해야 PUBLISH)
| ID | 검사 | 방법 | 기준 |
|---|---|---|---|
| B1 | 범위 잠금 | 개념 목록 ↔ 범위 문서 대조 | 범위 밖 개념 0 (인접 범위는 ‘이 책 범위 밖’ 한 줄) |
| B2 | 자료 충돌 | 학교 자료 ↔ 교과서 ↔ 원고 | 불일치는 ◇로 표시, 학교 자료 우선 병기 |
| B3 | 원문 충실도 | 인용 원문 대조 | 옛한글·한자 포함 EXACT. 자신 없는 형태는 ◇ |
| B4 | 구성요소 커버리지 | 개념별 체크 | 개념 머리·lead·소단락·중요 ≥1·확인 3~4 / 조작형은 예제 |
| B5 | 소단락 단위 | 원고 검사 | 한 소단락 한 생각, 연속 줄글 ≤ 4문장 |
| B6 | 용어 풀이 | 첫 등장 검사 | 풀이 없는 신규 용어 0 |
| B7 | 심화 분리 | 원고 검사 | ‘심화 포인트’는 건너뛰어도 본문이 이어짐, 학교 자료 밖은 † |
| B8 | 시험 포인트 근거 | 근거 칸 검사 | 실제 근거만. “반드시/무조건/100%” 0 |
| B9 | 기출 문장 복제 | 유사도 | 복제 0 (유형만 사용) |
| B10 | 정답 정확성 | 확인 문제·모의 문제 독립 재풀이 | 정답 일치, 단일 정답 |
| B11 | 내부 메타 비노출 | PDF 텍스트 검색 | CORE_LINK_INDEX/QC_STATUS/◇ 목록/제작 메모 0 |
| B12 | 흑백 | build_book.py | non_gray_source_colors = [] · gray max_channel_diff ≤ 8 |
| B13 | 차례 쪽수 | build_book.py 2-pass | 안정, missing 0 |
| B14 | PDF preflight | `pdf_preflight.py --core-profile BOOK` | FAIL 0 (WARN은 사람이 확인) |
| B15 | 시각 확인 | 대표 쪽 래스터 | 소단락 분할·태그 고립·옛한글 깨짐·표 잘림 0 |

## 2. 측정 기준선 (승인본 V2.0, 68쪽)
- 본문 평균 폰트(쪽별, 본문 180자 이상 67쪽): 최소 7.73 / 중앙 8.14 / 최대 8.94pt (표·옆 칸 포함 측정)
- preflight 점유율(측정값): 최소 0.119 / 중앙 0.33 / 최대 0.484 → BOOK 임계 FAIL < 0.10, WARN < 0.20
- BOOK 프로파일 결과: FAIL 0 / WARN 16 (희소 쪽 15 + 점검표 2열 grid 1)
- 위 기준선은 임계 설정의 근거이며, 새 책이 이 값과 같아야 한다는 뜻은 아니다.

## 3. 실패 처리
- 조판 결함(분할·고립·점유): Typesetter 자동 보정(허용 목록) → 재렌더 → 2회 초과 시 HOLD
- 내용 결함(B1~B3, B8~B10): Generator로 반송(CONTENT_RETURN). Typesetter가 내용을 고치지 않는다
- 내부 메타 노출(B11): FAIL, 원고에서 해당 섹션을 DO NOT PRINT로 이동

END ARC_CORE_BOOK_QA_V1.0
