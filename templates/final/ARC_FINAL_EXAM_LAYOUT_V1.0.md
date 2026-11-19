# ARC FINAL — 실전 시험지 레이아웃 명세 V1.0
VERSION: 1.0
DATE: 2026-11-19
STATUS: ACTIVE
PRODUCT: ARC_FINAL only (ARC N°는 `templates/n/ARC_N_BW_LAYOUT_V1.1.md`, CORE는 `templates/core/ARC_CORE_BW_OPEN_EDITORIAL_V1.0.md`)
RENDERER (single authority): `tooling/typeset/kor_renderer.py` via `tooling/production/production_pipeline.py`
PREFLIGHT: `tooling/pdf_qc/pdf_preflight.py --product ARC_FINAL --expected-item-count N --expected-cr-count M --answer-key-pdf <KEY>`
DESIGN REFERENCE (not rendered by code): `templates/final/ARC_FINAL_master_v0.2.html`

이 문서의 수치는 렌더러 실측값이다. 명세·HTML·렌더러가 다르면 렌더러와 이 문서를 기준으로 맞추고, 바꿀 때는 셋을 함께 고친다.

## 1. 산출물
| 파일 | 내용 |
|---|---|
| `<BATCH_ID>_DRAFT.pdf` | 학생 시험지 (표지 → 백지 → 문제) |
| `<BATCH_ID>_ANSWER_KEY.pdf` | 선택형 전 문항 정답 + 서술형 모범답안·채점 기준·허용 답 |
| `<BATCH_ID>_SOLUTIONS.pdf` | 문항별 상세 해설 |

## 2. 물리 페이지 순서 (사용자 지시 2026-11-19: 표지 뒤 백지 유지)
1. 표지
2. 완전 백지 1쪽 — 로고·머리말·꼬리말·쪽 번호·워터마크 없음 (양면 인쇄 시 문제 1쪽이 앞면에서 시작)
3. 문제 쪽 (3쪽부터)

학생 시험지 안에는 정답표·정답 줄·해설이 없다 (`FINAL_ANSWER_ON_PROBLEM_SHEET`).

## 3. 판형과 여백
| 항목 | 값 |
|---|---|
| 판형 | A4 세로 595.28 × 841.89pt |
| 여백 | 좌우 46pt(16.2mm), 위 64pt, 아래 58pt |
| 단 | 2단, 단 간격 20pt, 중앙 세로선 0.55pt 회색(0.76) |
| 본문 | 9.8pt, 행간 1.62배 (번들 `layout.body_pt`로 조정 가능, 줄이는 것보다 재배치 우선) |
| 서체 | 국어 HCR Dotum(HANDotum R/B, 옛한글·방점 공용), 그 밖 나눔고딕 R/B |
| 쪽 번호 | 하단 중앙 `- n -`, 8.8pt Bold |

## 4. 첫 문제 쪽 머리 (시험지 정보)
- 1행: `{exam_title} | 동북고등학교 | {course}` 10.5pt Bold. `exam_title`은 번들 값을 쓴다(없으면 현재 시험명). 다른 시험명을 하드코딩하지 않는다.
- 우측: `{set_label} · 배점 문항별 표시` 8.4pt
- 정보 칸(0.8pt 테두리, 가운데 세로선): `대상: 동북고등학교 1학년` | `범위: …`
- 범위 문구가 칸보다 길면 6.8pt까지 줄이고, 그래도 길면 말줄임표(…)로 끝낸다. 단어 중간에서 잘라내지 않는다.
- 머리 아래 1.1pt 검은 선.
- 둘째 쪽부터: 좌측 머리말 8.5pt Bold + 우측 문서 코드 7.8pt 회색, 0.7pt 선.

## 5. 문항
- 번호: 선택형 `1.`, 서술형 `[서술형 n]`
- 발문 끝에 배점 `(n점)` — **모든 문항 필수** (`FINAL_POINTS_NOT_PRINTED`). 선택형·서술형 배점 합계는 학교 공지와 같아야 한다(생산 파이프라인 `POINTS_GATE`).
- 난도 배지 `[n]`: 사용자 승인 통합 레이아웃 명세(2026-11-12) §2.3에 따라 배점 뒤에 표시한다.
- 선지 ①~⑤: 폭이 허락하면 한 줄 5개/3개 배열, 아니면 한 줄에 하나.
- `<보기>`·<조건>·표·그림은 문항 블록 안에서 쪼개지 않는다. 블록이 단 높이보다 길면 다음 단/쪽으로 블록째 넘긴다.
- 지문 묶음은 `※ 다음 글을 읽고 물음에 답하시오. (선택형 a~b번, 서술형 n번)` 머리로 시작한다.

## 6. 서술형 답안란
- `<조건>` 상자 다음에 `답:` 표지와 가로 쓰기 줄.
- 줄 수 = 번들 `answer_lines`, 없으면 모범답안 길이 × 1.4 / 한 줄 글자 수 + 여유 1줄, 3~10줄.
- 모든 서술형에 같은 높이를 쓰지 않는다.

## 7. 정답지 PDF
- 첫 줄 `정답  ANSWER KEY`
- 선택형: `번호  ①~⑤` 한 줄씩, 1~N 빠짐없이 (`FINAL_ANSWER_KEY_COUNT_MISMATCH`)
- 서술형: `[서술형 n] 모범답안 (n점)` + `답:` + `채점 기준:` + `유사 정답:` (`FINAL_ANSWER_KEY_CR_MISSING`)

## 8. 표지
- 시험명·과목·문항 수(`선택형 a문항 · 서술형 b문항`)·일러두기
- 일러두기 셋째 줄(FINAL): "정답표와 해설은 별도 파일로 제공됩니다. 시험지에는 정답을 싣지 않습니다."
- 브랜드 로고는 등록 자산만 (`templates/brand/ARC_BRAND_ASSET_REGISTRY_V1.0.md`)

## 9. 자동 검사 (preflight V1.3)
| 코드 | 조건 |
|---|---|
| FINAL_COVER_VERSO_NOT_BLANK | 2쪽이 완전 백지가 아님 |
| FINAL_ANSWER_ON_PROBLEM_SHEET | 문제지에 `정답`/`ANSWER KEY` 머리 또는 `번호 ①` 정답 줄 |
| FINAL_QUESTION_COUNT_MISMATCH | `1.`~`N.` 번호 누락 |
| FINAL_CR_COUNT_MISMATCH | `[서술형 1]`~`[서술형 M]` 불일치 |
| FINAL_POINTS_NOT_PRINTED | `(n점)` 표기 수 < 전체 문항 수 |
| FINAL_ANSWER_KEY_PDF_MISSING / _COUNT_MISMATCH / _CR_MISSING | 정답지 PDF 누락·불일치 |
| COLUMN_GUTTER_CROSSING | 본문 줄이 단 경계를 넘음 |

## 10. 골드 샘플
- 등록 대기: 기말 범위 FINAL 번들이 사용자 검수를 1회 통과하면 그 PDF를 `templates/gold/samples/ARC_FINAL_*_SAMPLE_V1.0.pdf`로 등록한다.
- 그 전까지 회귀 기준은 `quality/production/KOR_SEMIFINAL_FINAL_20260925`(보관 재생 모드) 렌더 결과다.

END ARC_FINAL_EXAM_LAYOUT_V1.0
