# ARC 국어 — 내신 실전 하이브리드 형식 (맞춤법·띄어쓰기·표준 발음)
VERSION: 1.0
DATE: 2026-11-19
STATUS: ACTIVE
SCOPE: KOR ONLY · ARC N°(V6 포함) / ARC FINAL의 문법 구간
ORIGIN: 2026-11 한글 맞춤법 실전 세트 비교. 3-DAY PACK(무힌트 조항 적용 + 실전 텍스트 복합 교정)과 내신형 V2(선택형 + 조건부 서답형, 채점 기준 포함)의 장점을 합친다.

## 1. 문항 수는 요청마다 정한다
사용자 지시(2026-11-19): ARC N°의 난도·문항 수는 그때그때 다르다. 이 문서는 **형식**을 정하고, 수량은 계획 카드가 정한다.
```bash
python tooling/arc.py plan --subject KOR --scope "한글 맞춤법" --count 50 --constructed 5 --save plan.yaml
```
- 예: 50문항 = 선택형 45 + 서답형 5, 26문항 = 선택형 22 + 서답형 4(실제 기말 구조).
- ARC FINAL은 학교 공지 구조(`ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml`)를 그대로 따른다.

## 2. 문항 구성 요소
| 요소 | 내용 | 근거 규칙 |
|---|---|---|
| A. 무힌트 조항 적용 | `<보기>`에는 조항 원문과 사실 자료만. 학생이 조항을 새 사례에 적용 | `quality/ARC_VIEW_EVIDENCE_POLICY_V1.0.md` |
| B. 실전 텍스트 복합 교정 | 칼럼·신문 기사·학교 안내문·단체 대화방 등 실제 글 속 ㉠~㉤ 교정. 표기와 띄어쓰기를 함께 판단 | 문법 원형 A2/A6 (`ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml`) |
| C. 조건부 서답형 | <조건> 2~3개, 모범답안, 허용 답, 부분점수 채점 기준 필수 | 원형 C1, `CR_RUBRIC_MISSING` |

권장 배합(계획이 따로 정하지 않을 때): A 40% · B 40% · 나머지 선택형 20% + 서답형은 계획 수만큼.

## 3. 필수 메타데이터
| 필드 | 쓰는 곳 | 목적 |
|---|---|---|
| `headwords` | 모든 문항 | 계획한 핵심 표제어. 학생 텍스트에 없으면 FAIL, 한 글자 다른 유사 표기 보고(`곗날`→`옛날` 오타 차단) |
| `intended_errors` | B형·띄어쓰기 선지 | 일부러 넣은 오류 조각. 여기 없고 판단 근거(`why`)에도 없는 붙여쓰기는 `UNINTENDED_SPACING_ERROR` |
| `answer_targets` | 서답형 | 서답형 핵심 답. 다른 문항에 실리면 `CROSS_ITEM_ANSWER_LEAK` |
| `view_clause_refs` | 조건 요약형 `<보기>` | 조항 요약을 쓸 때 근거 조항 명시 |

## 4. 표기·띄어쓰기 복합 문항의 복수정답 방지
- 각 선지에서 **판정 대상 조각**을 하나로 정하고, 나머지 부분은 표기·띄어쓰기가 완전히 바른 문장으로 쓴다.
- 판정 대상이 아닌 곳에 오류가 섞이면 그 선지도 '틀린 것'이 되어 복수정답이 된다. 정적 검사(`UNINTENDED_SPACING_ERROR`)와 독립 재풀이 전 선지 감사로 이중 확인한다.
- "'X'를 'X'로" 같은 자기동일 교정은 `OPTION_SELF_IDENTICAL_CORRECTION`으로 FAIL.

## 5. 세트 내 유출 방지
선택형에서 쓴 표제어·예문을 서답형에서 다시 쓰지 않는다. 같은 규정을 다시 물을 때는 다른 낱말·다른 문장을 쓴다 (`quality/ARC_SET_CROSS_ITEM_LEAK_GATE_V1.0.md`).

## 6. 실행
- 초안: `python tooling/production/draft_preview.py <번들> --output-dir <out>` → `print_integrity` 항목 확인
- 정식: `python tooling/production/production_pipeline.py <번들> --output-dir <out>` → `PRINT_INTEGRITY_GATE`

END ARC_KOR_SCHOOL_HYBRID_FORMAT_V1.0
