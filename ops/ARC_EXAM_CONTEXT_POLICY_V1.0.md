# ARC 시험별 범위·자료 수집 정책 V1.0
DATE: 2026-10-03
STATUS: ACTIVE-DEV

## 시험 설정의 우선순위

신규 출제는 runtime.active_exam_id와 runtime.exam_context_registry의 해당 시험·과목 설정을 사용한다. runtime.midterm_product_scope_lock은 과거 범위 기록이며 신규 시험의 기본값이 아니다. 기말 날짜·범위·제외 항목을 추정하여 확정 처리하지 않는다.

확정 범위는 scope_evidence_refs로 학교 안내·학습지 위치 등을 연결한다. 시험 전체 범위 미확정 중에도 개별 단원을 확인했다면 CONFIRMED_UNITS_ONLY로 N° 연습을 할 수 있다. ARC FINAL은 CONFIRMED인 시험 전체 범위와 과목·단원에 맞는 해시 고정 난도 기준을 모두 요구한다. 산화·환원 기준을 다른 과학 단원에 자동 적용하지 않는다.

## 기말 임시 범위 기본값

2026-10-03 최신 사용자 지시에 따라 기말 ARC 작업은 **과학·사회·국어 3과목에 집중**한다. `runtime.active_subjects`와 시험 설정의 `active_subjects`는 SCI·SOC·KOR로 일치시킨다. 한국사·AI는 `DEFERRED_BY_USER`로 보관하고 제품 목록을 비운다. 두 과목의 신규 자료 수집·출제·품질 개선은 이번 기말 작업에서 제외하며 기존 원본·범위 기록은 삭제하지 않는다. 공용 엔진 호환성 검사에는 과거 자료를 사용할 수 있다.

3과목의 준비·자료 수집 범위는 **이번 학기 과목별 전체 학습 내용에서 실제 중간고사에 포함된 범위를 뺀 나머지 전부**로 설정한다. 남은 교과서 단원과 학교 보충자료를 모두 포함하고, 세부 페이지·작품·제외 항목은 학교의 기말 범위 공지가 나오면 정한다. 이는 `PROVISIONAL_REMAINDER` 상태이며 학교 확정 범위는 아니다.

`provisional_scope_policy`에 공통 기준과 사용자 지시를 기록한다. 중간 범위를 빼는 근거는 실제 중간 범위 기록이다. 과학 산화·환원 집중, 한국사 N° 우선, AI 제작 보류 같은 `midterm_product_scope_lock`의 제작 우선순위를 실제 중간 범위로 간주하지 않는다. 기존 범위 장부와 과목 MASTER는 대조 대상이며, 서로 다른 기록을 임의로 확정하지 않는다. 확인 전 단원·원문 ID는 빈 목록으로 두되 자료 수집은 이 나머지 전체를 대상으로 진행한다.

학교 공지가 나오면 해당 과목의 임시 기준을 공지의 포함·제외 범위로 교체하고 `scope_evidence_refs`와 단원·원문 ID를 갱신한다. 학교가 중간 내용을 기말에 다시 포함하면 그 내용도 포함한다. 범위 변경은 profile 해시를 바꾸므로 기존 원고도 새 범위로 재확인한다. 임시 수집 기준만으로 최종 출판을 승인하지 않는다.

## 출제 전 검사

원고의 exam_context에는 exam_id, profile_sha256, unit_ids, source_ids를 넣는다. profile_sha256은 시험 설정 객체를 canonical JSON으로 직렬화한 SHA-256이다. 범위 설정이 수정되면 기존 원고는 EXAM_PROFILE_STALE로 보류된다. 이를 통과하려면 실제 변경 범위와 원고를 다시 확인해야 한다. 해시만 바꾸어 검토를 대체하지 않는다.

python tooling/exams/exam_scope_gate.py <items.yaml>로 확인한다. 운영 production_pipeline.py는 동일 검사를 자동 실행하며, 불합격이면 독립 재풀이 파일 읽기·원문 로딩·PDF 생성 전에 보고서를 쓰고 멈춘다. content bundle→handoff→QA 파일에도 같은 context를 남기고 Typesetter에서 서로 대조한다. Context는 내부 메타데이터이며 학생용 본문에는 넣지 않는다.

정답·사실·문학 해석의 진실성은 범위 검사로 확인되지 않는다. 기존 전 선지 근거 검수·원문 고정·블라인드 1회·중복 검사·인간 최종 검토를 유지한다.

## 과거 자료의 재실행

--archived-replay는 이전 번들과 합성 canary의 회귀 검사 전용이다. 현재 시험 context에는 사용 금지다. 시험 context가 없는 예전 자료의 진단 PDF는 만들 수 있지만 EXAM_SCOPE=ARCHIVED_REPLAY이고 release_allowed=false이며 최종 출판 가능 상태로 표시하지 않는다. 이 옵션으로 생성한 출력물을 기말 FINAL 완성본으로 취급하지 않는다.

## 자료 수집

발견(METADATA_ONLY), 시험명 확인(HEADER_REVIEWED), 공식 링크 확인(LINK_REVIEWED), 내용 검토(CONTENT_REVIEWED)를 구분한다. 읽지 않은 자료를 분석 완료로 표시하지 않는다. 검색 결과·유료 참고서·기출·생성 문제집은 학교의 원문 자료와 다른 역할을 가진다.

현재 시험에 직접 사용할 RAW_SCHOOL_SOURCE는 2022 개정 적합성·범위 증거·단원 연결·내용 검토·원문 무결성 확인을 모두 기록해야 한다. 참고자료와 과거 기출은 후보·검토용이며 현재 범위를 자동 확정하지 않는다. 교사가 다른 기출에서 스타일을 예측하지 않고 기존 teacher_style_prediction=disabled를 유지한다.

Google Drive에는 원본을 유지하고 GitHub에는 목록·검수 기록만 남긴다. 교과서·기출·유료 문제집 PDF를 저장소에 업로드하지 않는다. 제목·크기가 같은 파일은 중복 후보이며 내용 해시 비교 전에 삭제하지 않는다.

## 실행·승격

기말은 PROVISIONAL_REMAINDER 기준으로 준비·자료 수집을 진행한다. 학교 근거가 확인된 단원은 별도 등록하고, 최종 출판은 확정 범위 검사를 통과해야 한다. 파일 그래프 점검·자료 수집·합성 회귀 검사는 계속 가능하다. dev에서 구현과 검증을 마친 뒤 기존 BRANCH_POLICY에 따라 승격한다. 모든 과목·실제 모델 호출·운영 사이트·PDF 시각 검토까지 끝난 것으로 확대 보고하지 않는다.
