# bank/ — ARC REFERENCE 기출 문항은행 (통합과학2·통합사회2)

수집한 기출·공식 문항 색인을 **출제에 쓸 수 있는 후보**로 정리한 레지스트리다.
상태: **Phase 1(메타데이터) + Phase 2(본문 검토) 완료.** 후보 풀 1,158건의 본문을 읽고 판정했다.
- `READY` 83건(중간 트랙, 범위 확정) + `READY_PENDING_RANGE` 538건(기말 후보 트랙, 학교 범위 공지만 기다림) = **출제 후보 621건**
  (과학 중간 26·기말 78, 사회 중간 57·기말 460). 난도는 D1 85 / D2 354 / D3 170 / D4 12, **D5는 0건**.
- 나머지: `HOLD` 902, `EXCLUDED` 232, 정답 없음 165, 본문 미검토 160. 전체 2,080건.

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

## Phase 2 검토 방식과 한계 (읽기 전에 확인)
- **본문 열람**: EBSi·KICE 공식 PDF를 내려받아 문항이 있는 쪽을 텍스트(좌우 단 분리)와 이미지로 읽었다. 본문은 저장소에 없다. 판정값만 `review/p1.jsonl`에 있다.
- **정답**: 해설지 정답표에서 읽은 공식 정답(`review/official_answers.csv`, 기존 공식 정답 364건과 전수 일치로 파서 검증)을 쓴다. 검토자는 정답을 **보지 못한 채** 독립으로 풀었고, 공식 정답과 일치한 문항만 `READY*`가 된다.
  전체 일치율 **92.1%(991/1076)**, 확신도 H에서도 95.4%였다. 불일치 85건은 `KEY_DISPUTE`로 `HOLD`다. 공식 정답이 틀렸거나 검토가 틀린 쪽을 가리지 않았다.
- **독립 풀이는 1회뿐**이다(`review_pass=P1`). 계획했던 2회 풀이가 아니라 "공식 정답과 일치하는 1회 풀이"를 검증으로 쓴다. 정답이 공식 정답표 값이므로 공식 정답과 어긋난 문항만 걸러 낸다는 의미다.
- **난도(`difficulty_score`)는 AI 구조 점수**(`ARC_DIFFICULTY_ENGINE` R5 단계)다. 학교 앵커(동북고 2025 중간)와 비교하지 않았고, 실제 정답률로 보정하지 않았다. 학교 실물 시험과 같은 척도라고 가정하면 안 된다.
- **고2·3 문항 502건이 출제 후보에 포함**된다(`EXTENDED_SOLVABLE`). "통합과학/통합사회 1·2와 중학 지식만으로 풀리는가"를 검토자가 판단했고, 필요 지식 밖이면 `ADVANCED_BLOCKED`(395건)로 뺐다. 이 판단은 AI 판정이라 출제 전 교사 확인이 필요하다.
- **개념 재배정 79건**: 수집 단계 키워드 매핑이 틀렸다고 검토자가 판단한 문항을 `REVIEW_REASSIGNED`로 옮겼다. 무관(`MISFIT`) 판정은 224건이었지만 대체할 개념을 지정한 경우만 옮겼고, 나머지는 원 배정을 유지했다(트랙 개념이 없다고 한 문항은 제외). 수집 단계 매핑의 정확도는 부족 분석에 영향을 주는 한계다.
- 본문을 못 읽은 문항: 도표 판독 불가 25건(`FIGURE_UNREADABLE`), 쪽 못 찾음 2건 등. `NEEDS_*`/`HOLD`로 남았다.
- **본문 미검토 풀**(160건 + 정답 없음 일부): 외부 접근 불가 출처(경기도교육청·네이버 파일, 41건), 가야고 시험지·Drive 원본(121건, 이 환경에서 아직 열람하지 않음).

## 알려진 한계
- (Phase 1 시점 기록) 수집 색인의 요지·출제의도·정답만으로 만든 판정이 `review_pass`가 빈 문항에 남아 있다(`INDEX_TEXT_REVIEW_ONLY_NOT_PDF_VISUAL`).
- 개념 배정은 대부분 수집 단계의 키워드 범위다(`mapping_basis=KEYWORD_COLLECTOR_UNIT`). 성취기준 코드·수동 배정은 소수다.
- 기말 범위는 학교 공지 확정 전이라 `FINAL_REMAINDER` 개념은 `range_confirmed=N`이다. 확정되면 `concepts.csv`·`scope_crosswalk.csv`만 고쳐 다시 빌드한다.
- 통합사회 C 파트(인권·기본권) 문항은 학습지 손글씨 X 영역과 겹치는지 **시각 확인**이 필요하다(`SOCIAL_MASTER` §2-1). 레지스트리 `notes`에 표시했다.
- 수집 단계에서 `EXCLUDED_SUBJECT1_OR_ADVANCED`로 제외한 판정은 승계했다(`HOLD`).
- `body_access=EXTERNAL_PDF_REACHABLE`은 2026-10-04 세션에서 도메인별 HEAD 요청이 200이었다는 뜻이다. 재확인이 필요하다.
