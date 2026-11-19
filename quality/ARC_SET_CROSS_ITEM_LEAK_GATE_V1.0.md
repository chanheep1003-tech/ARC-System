# ARC_SET_CROSS_ITEM_LEAK_GATE_V1.0 — 한 시험지 안의 답 유출 차단
VERSION: 1.0
DATE: 2026-11-19
STATUS: ACTIVE
SCOPE: 모든 과목 · ARC N° / ARC FINAL
EXECUTABLE: `tooling/content_qa/content_qa_gate.py` → `lint_bundle_text` (`CROSS_ITEM_ANSWER_LEAK`, `CROSS_ITEM_EXAMPLE_REUSE`), 생산 파이프라인 `PRINT_INTEGRITY_GATE`
ORIGIN: 2026-11 한글 맞춤법 실전 세트 검증. 선택형에 나온 핵심 어휘·예문이 서답형에 다시 나와 서답형 답을 선택형에서 베낄 수 있었음.

## 1. 원칙
한 시험지의 어떤 문항도 다른 문항의 답을 알려 주면 안 된다. 특히 서답형의 답(바른 표기, 고쳐 쓴 문장, 핵심 개념어)이 선택형 선지·`<보기>`에 그대로 실리면 서답형은 '찾아 베끼기'가 된다.

## 2. 서답형 답 표지
서답형 문항은 답의 핵심 문자열을 `answer_targets`에 적는다.
```yaml
- item_id: C1
  format: CR
  answer_targets: [깨끗이]      # 학생이 써야 할 핵심 표기
  model_answer: "'깨끗이'"
```
`answer_targets`가 없으면 `model_answer`의 따옴표 안 문자열과 `accepted_variants`에서 3자 이상 문자열을 자동으로 뽑는다.

## 3. 판정
| 코드 | 조건 | 심각도 |
|---|---|---|
| CROSS_ITEM_ANSWER_LEAK | 서답형 답 표지가 다른 문항의 발문·`<보기>`·선지에 공백 무시하고 그대로 있음 | 규범 문항 또는 `answer_targets` 명시 → FAIL / 그 밖(문학 등에서 자동 추출) → WARN |
| CROSS_ITEM_EXAMPLE_REUSE | 규범 서답형의 발문·`<보기>`·조건이 선택형 선지·`<보기>` 예문과 6자 이상 연속 일치 | FAIL |

문학 세트처럼 지문이 공유되는 경우 지문 속 시어가 답이 되는 것은 정상이다. 이때 WARN은 검수자가 "지문에서 찾는 과업인지, 선지가 답을 대신 보여 주는지"를 판단해 기록한다.

## 4. 출제 절차
1. 세트 설계 단계에서 선택형과 서답형의 표제어·예문 목록을 따로 만들고 겹치지 않게 한다.
2. 같은 규정을 서답형에서 다시 묻는다면 **다른 낱말·다른 문장**으로 묻는다.
3. 선택형 해설·정답표는 학생 시험지와 분리되어 있으므로 검사 대상이 아니다.

## 5. 한계
정적 검사는 문자열 일치만 본다. 뜻은 같지만 표기가 다른 유출(동의어, 활용형)은 독립 재풀이 검수자가 `BLIND_REVIEW`에서 확인한다.

END ARC_SET_CROSS_ITEM_LEAK_GATE_V1.0
