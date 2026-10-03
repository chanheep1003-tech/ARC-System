# 자료 후보 목록 검사

목록: `quality/source/FINAL_COLLECTION_CANDIDATES_20261003_V1.yaml`.

```bash
python tooling/sources/source_collection_gate.py quality/source/FINAL_COLLECTION_CANDIDATES_20261003_V1.yaml
python tooling/sources/test_source_collection_gate.py
```

원본 자료를 복사하지 않고 출처·확인 단계·용도를 기록한다. 후보 발견과 현재 시험범위 편입을 구분하며 자동 승격하지 않는다. 과거 기출·공식 참고자료·연습 문제집은 RAW_SCHOOL_SOURCE로 승격할 수 없다.

같은 Drive ID 또는 추적 매개변수를 제거한 동일 URL은 중복 등록으로 차단한다. 제목과 크기만 같은 파일은 내용 미확인 중복 후보로 보고하며 원본을 삭제하지 않는다.

기말 신규 수집 대상은 과학·사회·국어(SCI·SOC·KOR)다. `collection_scope.active_subjects`는 현재 시험 설정과 일치해야 한다. 한국사·AI의 기존 후보는 `PARKED_BY_USER`로 보관하며 현재 시험 자료로 승격하지 않는다.
