# bank/ — ARC REFERENCE 기출 문항은행 (통합과학2·통합사회2)

수집한 기출·공식 문항 색인을 **출제에 쓸 수 있는 후보**로 정리한 레지스트리다.
상태: **Phase 1(메타데이터 단계) 완료.** 본문 검토가 끝난 문항(`READY`)은 아직 0건이다.

## 이 은행이 하는 일 / 하지 않는 일
- 하는 일: 문항별 출처·번호·개념·정답(공식 정답표 값)·범위 상태 기록, 중복·원형 묶음, 개념별 부족 분석.
- 하지 않는 일: 문제 본문·선지·자료 원문을 저장하지 않는다(저작물 복제 방지, `ERR-COPY-001`). 정답·난도를 추정해서 채우지 않는다.
- `91_검증문항은행`(BANK_POLICY, QA PASS 전용)과 **별개 계층**이다. 여기 있는 문항은 `QA_STATUS=PASS`가 아니므로 ARC N°/FINAL의 직접 재사용 후보가 아니다. 승격하려면 BANK_POLICY의 ACCEPTANCE를 처음부터 통과해야 한다.
- 타 학교 정기고사(`CALIBRATION_ONLY`)는 난이도 보정 전용이다(`SYSTEM_MANIFEST` `historical_exam_usage`).

## 파일
|파일|내용|
|---|---|
|`items_SCI.csv`, `items_SOC.csv`|문항 레지스트리. 컬럼·허용값·하드 규칙은 `schema.yaml`|
|`clusters_*.csv`|원형 묶음(평가목표 문구가 같은 것끼리). 대표 1건 + 변형|
|`concepts.csv`|개념 ID 목록. `phase`=MIDTERM(Ledger, 범위 확정) / FINAL_REMAINDER(중간 제외 나머지, 범위 미확정)|
|`scope_crosswalk.csv`|성취기준 코드·수집 키워드 → 개념(또는 그룹)|
|`concept_rules.csv`|그룹 안에서 키워드로 세부 개념을 정하는 순서 규칙|
|`blocked_knowledge.csv`|고2·3 문항 보류 키워드(SCIENCE_MASTER §5 ADVANCED LEAK BLOCK)|
|`manual_topic_map.csv`|가야고 시험지 주제→개념 수동 매핑|
|`COVERAGE_GAP_SCI.md`, `COVERAGE_GAP_SOC.md`|트랙·개념별 부족 분석(생성 파일)|
|`SOURCES_MANIFEST.md`|입력 파일 이름·행 수·sha256|
|`tools/`|`build_register.py`(빌드), `validate.py`(검증), `coverage.py`(부족 분석)|

## 재생성
입력 CSV는 저장소에 두지 않는다(Drive `N제 시스템` 수집 결과, `SOURCES_MANIFEST.md` 참조).
```
python3 bank/tools/build_register.py --judge <ARC_추가분_전체판정.csv> --gaya <ARC_학교기출_정답교정.csv> --sources <SCI SOURCES.csv> <SOC SOURCES.csv>
python3 bank/tools/validate.py
python3 bank/tools/coverage.py
```
표준 라이브러리만 쓴다. 입력과 규칙 파일이 같으면 결과도 같다.

## 상태 사다리
`status`: `READY`(본문 검토·정답 확인·난도 평가·범위 확정 모두 끝남) > `NEEDS_BODY_REVIEW`(공식 정답 있음, 본문 미검토) > `NEEDS_ANSWER`(정답 없음) > `HOLD`(범위 경계·상위학년 지식 의심·중복) > `EXCLUDED`(범위 밖·비문항).
`scope_status`: `IN_SCOPE`, `EXTENDED_CANDIDATE`(고2·3 문항, 보류 키워드 없음, **풀이 가능성 미검증**), `ADVANCED_BLOCKED`(키워드·원 과목 근거 보류, 본문 확인 시 해제 가능), `NEEDS_SCOPE_CHECK`, `OUT_OF_SCOPE`, `BLOCKED_USER_X`.
`READY`가 되려면 `body_reviewed=Y`, 정답 출처 확인, 난도 평가, `range_confirmed=Y`가 모두 필요하다(`validate.py`가 강제).

## 알려진 한계
- 본문을 본 문항이 없다. 수집 색인의 요지·출제의도·정답만 있다(수집 단계 `INDEX_TEXT_REVIEW_ONLY_NOT_PDF_VISUAL`).
- 개념 배정은 대부분 수집 단계의 키워드 범위다(`mapping_basis=KEYWORD_COLLECTOR_UNIT`). 성취기준 코드·수동 배정은 소수다.
- 기말 범위는 학교 공지 확정 전이라 `FINAL_REMAINDER` 개념은 `range_confirmed=N`이다. 확정되면 `concepts.csv`·`scope_crosswalk.csv`만 고쳐 다시 빌드한다.
- 통합사회 C 파트(인권·기본권) 문항은 학습지 손글씨 X 영역과 겹치는지 **시각 확인**이 필요하다(`SOCIAL_MASTER` §2-1). 레지스트리 `notes`에 표시했다.
- 수집 단계에서 `EXCLUDED_SUBJECT1_OR_ADVANCED`로 제외한 판정은 승계했다(`HOLD`).
- `body_access=EXTERNAL_PDF_REACHABLE`은 2026-10-04 세션에서 도메인별 HEAD 요청이 200이었다는 뜻이다. 재확인이 필요하다.
