# 시험별 범위 검사

현재 설정: `ops/exams/EXAM_CONTEXTS_V1.yaml`.
기말 활성 과목은 과학·사회·국어(SCI·SOC·KOR)이며 한국사·AI는 사용자 요청으로 보류한다. 보류 과목의 현재 시험 출판은 범위가 확인되어도 과목 활성화 전에는 차단한다.
기말 준비·자료 수집의 기본값은 `PROVISIONAL_REMAINDER`: 이번 학기 전체 학습 내용에서 실제 중간고사 포함 범위를 뺀 나머지 전부다. 공통 기준은 `provisional_scope_policy`에 기록하며 제작 우선순위를 중간 범위 근거로 쓰지 않는다. 학교 공지가 나오면 과목별 확정 범위로 교체한다. 확인된 단원은 별도 증거와 함께 `CONFIRMED_UNITS_ONLY`로 등록하여 N° 연습에 사용할 수 있다. 임시 기준만으로 신규 출판을 승인하지 않는다.

원고 내부 메타데이터 예시:

```yaml
exam_context:
  exam_id: DONGBUK_2026_2_FINAL
  profile_sha256: <exam_scope_gate.digest(exam_profile)>
  unit_ids: [<confirmed-unit-id>]
  source_ids: [<confirmed-raw-source-id>]
```

검사: `python tooling/exams/exam_scope_gate.py path/to/items.yaml`.
회귀: `python tooling/exams/test_exam_scope_gate.py`.

`production_pipeline.run`의 기본 경로와 Typesetter admission은 이 검사를 수행한다. Sources used by passage/sets and QA source locks must match the declared source IDs. 시험 설정이 변경되면 해시가 달라져 이전 원고가 차단된다.

시험별 FINAL anchor는 subject, unit_ids, path, sha256을 등록한다. 본문 난도 검사는 기존 FINAL gate가 수행한다. 이 검사는 anchor의 단원 적용 범위와 파일 무결성을 추가 확인하며 학생 정답률을 측정하지 않는다.

`--archived-replay`는 과거·합성 회귀 전용이며 출판 가능한 상태가 아니다. 실제 기말 번들에서 사용하면 안 된다.
