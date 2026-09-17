# ARC Skills

ARC-System의 on-demand 전문 skill 레이어. 모든 skill을 매번 불러오지 않는다.

## Runtime principle
`COMMON_GENERATION_ENGINE + 과목 MASTER + 현재 범위`가 항상 중심이다. Skills는 자료 추출, 외부조사, 오답설계, 사실검증, 문체감사, QA, 세트편집, 시각자료, 회귀평가 등 특정 단계에만 개입한다.

## Default N° / FINAL flow
`item-generator → distractor-engine → visual(optional) → fact-audit → naturalness-audit → item-qa → set-editor → bank-curator(PASS only)`

원자료가 새로 들어오면 앞에 `source-ingest`, 외부 웹 자료가 필요하면 `research-grounding`, 엔진 변경을 평가할 때만 `eval-regression`을 추가한다.

개인 오답 기반 재출제·학습자 약점 추적 기능은 포함하지 않는다.
