# ARC 사용자 결정 기록 — 2026-11-08
이 문서는 규칙 정비 세션에서 사용자가 직접 내린 결정과 그 반영 위치를 기록한다. 규칙의 권위는 SYSTEM_MANIFEST가 가리키는 각 규칙 파일에 있고,
이 문서는 감사 추적용이다. 값이 PROVISIONAL인 항목은 사용자 확인 전까지 바뀔 수 있다.

| ID | 결정 | 반영 위치 |
|---|---|---|
| D-01 | ARC_N 문항 메타 스트립에 추정 난이도를 표시한다. 표기는 D1~D5 그대로(D-10). 본문·선지·정답표에는 표시하지 않고 ARC_FINAL에는 표시하지 않는다. | 공통 엔진 §11, 난이도 엔진 §0, V2.4 §2·§16, N 레이아웃, manifest arc_n_metadata_strip_difficulty |
| D-02 | ARC_FINAL 조판 기준은 FINAL HTML 마스터의 확대 흑백 2단(12.8mm, 발문 9.5pt, 선택지 9.1pt). | V2.4 §6·§7, manifest arc_final_layout_basis |
| D-03/D-12 | ARC_N 표지에 승인 로고를 넣되 흑백 로고 자산(ARC_N_LOCKUP_MASTER_BW.png)을 신규 등록해 쓴다. 등록 전에는 BRAND_ASSET_MISSING. | V2.4 §5·§23, N 레이아웃, 조판 계약 §1-A, 브랜드 자산 등록부, manifest arc_n_cover_logo_variant |
| D-04 | ARC_N은 페이지당 4문항을 기본으로 하되, 4개를 놓고도 다음 문항이 통째로 들어갈 여백이 있으면 5·6문항으로 늘린다(상한 없음, 문항 분할·축소 금지). 지문 세트는 지문 1회 + 문항군을 이어 배치. (같은 날 후속 정정: 처음엔 "4문항 고정, 지문 구간만 해제"로 기록했다가 사용자가 "4는 기본이지 상한이 아니다"라고 정정) | V2.4 §6, N 레이아웃, manifest arc_n_question_packing |
| D-05 | 기말 범위는 학교 공지 전까지 "2학기 전체 − 2학기 중간 실제 범위"로 확정(임시). MASTER의 SCOPE LOCK은 중간고사 스냅샷(참고용)으로 표시하고 범위 기준은 EXAM_CONTEXTS 하나로 일원화. | 국어·사회·과학 MASTER, EXAM_CONTEXTS |
| D-06 | 사회 CORE에서도 C파트 X표시 제외는 막는 규칙(BLOCKING). | CORE 엔진 V1.3 §8-A |
| D-07 | 기출 70% / 창작 30%는 과목마다 다르게 적용. 초기값(PROVISIONAL): SOC·SCI=PAST_70_AI_30, KOR=STRUCTURE_REFERENCE_ONLY(기출 문항 미사용), 부족 시 사용자 허용 하에 ORIGINAL_TRIAL. | 기출·창작 정책 §10, tooling/sources/generation_source_gate.py |
| D-08 | 사회 C학습지 손글씨 X표 영역은 기말에서도 계속 제외(복원하지 않음). | 기출·창작 정책 §5, 사회 MASTER §2-1 |
| D-09 | FINAL 난이도는 "동북고 평균보다 조금 더 어렵게". 과목 앵커 평균 +0.1~+0.3(PROVISIONAL). 공통 하한(D4+D5 30%)은 폐지. | 공통 엔진 §21.4, 난이도 엔진, FINAL 품질 게이트 §2, EXAM_CONTEXTS |
| D-11 | 초안은 임시 폴더 저장 허용, 제품 폴더 이동·중복 이력·BANK 등록은 사용자 내용 승인 후. | 중복·승인 정책 §6-A, 오케스트레이터, 사람 검토 게이트 §8, manifest |
| D-13 | 기말 ARC_FINAL은 학교 공지 없이 사용자 임시 확정만으로 출시 허용. 공지로 범위가 바뀌면 프로필 해시가 달라져 재검토. | EXAM_CONTEXTS release_on_user_provisional_lock |
| D-14 | 마감 2026-12-07(사용자 입력 "12 7일"). 시험일인지 준비 마감일인지 미확인. | 준비도 게이트, EXAM_CONTEXTS target_date, manifest readiness_deadline |
| D-15 | 사회·과학 ARC_N 은 4단계(S1~S4), 기준은 사고 동작. 국어 V1~V6 과 별개. | quality/ARC_N_STAGE_LADDER_V1.1.md, manifest arc_n_stage_ladder |
| D-16 | 기출/변형/창작 구성은 단계가 아니라 문제은행 재고로 결정: 재고 충분 → 사용자가 변형 요청, 부족 → 창작 위주(ORIGINAL_TRIAL, 상시 허용). D-07 의 과목별 고정 프로필 중 SOC·SCI 는 이 규칙이 보완. | ARC_GENERATION_SOURCE_POLICY §10, 사다리 §4 |
| D-17 | ARC N° 흑백 로고는 컬러 마스터의 휘도 변환 파생본으로 등록(사용자 지시 예외). Drive 업로드·ID 기록 대기. | brand registry |
| D-18 | KOR·SOC·SCI ARC_N 에 D1 문항 금지(모든 단계 D2~D5, 국어의 D1 10% 허용 폐지). ARC_FINAL 은 영향 없음. | 사다리 §1-A, manifest arc_n_forbid_difficulty, production_pipeline PROFILES(BALANCE_D1_OUT_OF_RANGE) |
| D-19 | 국어도 사회·과학과 같은 4단계(S1~S4)로 통일. 국어 V5 는 ARC_FINAL 과 겹쳐 FINAL 로 통일(V5 명칭 폐지), V6 별도 모듈 단계 제거. | quality/ARC_N_STAGE_LADDER_V1.1.md, manifest korean_stage_ladder, AGENTS.md |
| D-20 | 단계·세트 문항 수·난이도 분포·국어 기출/창작 구성은 기본값 없이 요청마다 사용자가 정한다. 비어 있으면 생성 전에 사용자에게 묻는다(코드 게이트 REQUEST_SPEC_*, SOURCE_PROFILE_UNDECLARED=FAIL). 앞서 제안한 단계별 분포 수치는 참고 예시로 강등. | 사다리 §0, production_pipeline.request_spec_findings, generation_source_gate |
| D-21 | ARC N° 문항은 교과서 개념·예문·표를 그대로 옮겨 만들지 않는다. 교과서는 '출제 개념의 범위'일 뿐이고, 자료·사례·제시문·수치는 새것(미공개 소재)으로 구성해 개념을 전이 적용하게 한다. 실제 시험이 교과서 문장 대응 수준으로 나오지 않으므로(사용자 2026-11-08). 교과서 문장을 선지에 그대로 쓰면 불합격. | 사다리 §2 S2 비고, 생성 전 점검 |
| D-22 | 난이도 조절(게이트)이 실패하면 반복 재생성 전에 문제은행·기출·모의 자료와 `quality/exam_style` 종합 노트를 참고해 해당 난이도의 실제 출제 구조로 재설계한다(사용자 2026-11-08). 이번 사회 S2 요청은 선택형 20문항만 만든다(서술형 제외). | 사다리 §2, quality/exam_style/README_EXAM_STYLE_SUMMARY_20261108.md |
| D-23 | S2 20문항 실험 불합격 후 시스템 수정(사용자 지시): ①출제 구조 라이브러리·template 코드 필수 ②풀이자 눈금 보정용 기준 문항 레지스트리 ③요청 전 범위 대비 D4+ 가능성 점검(feasibility, 사용자에게 묻기) ④정답 길이·절대 표현·정답 분포·교과서 복제 자동 검사. 임계값은 모두 잠정. | quality/ARC_ITEM_STRUCTURE_AND_CALIBRATION_V1.0.md, tooling/production/item_structure_gate.py, difficulty_calibration.py |
| D-24 | ARC N 은 자료 제시형 추론 문항을 기본으로 한다: 교과서 밖 개념은 문항 안(view)에서 정의를 주고 적용·추론하게 하며, 정의 없이 교과서 밖 용어를 이름으로 쓰면 FAIL(사용자 2026-11-08 "이런 추론식 문제 만들도록 저장"). 범위(소단원)는 그대로. | quality/ARC_ITEM_STRUCTURE_AND_CALIBRATION_V1.0.md §6, EXAM_STRUCTURE_LIBRARY supplied_concept_rule, item_structure_gate.py |

## 이 정비로 해결되지 않은 것 (후속 과제)
1. 흑백 로고 자산 파일이 없다. 등록(Drive ID, 해시) 전까지 ARC_N 표지는 생성되지 않는다.
2. N 레이아웃 코드 강제 일부 완료(난이도 스트립 렌더·검사, BW 로고 release_blocker). 배치: kor_renderer(국어 N·FINAL 렌더러)는 문항을 쪼개지 않고 통째로 단에 이어 채우며 들어가지 않으면 다음 단/페이지로 넘기므로(코드 확인) 새 규칙의 동작과 일치한다. 다만 기준 샘플 PDF와 눈으로 비교하지는 않았다. 아직 없음: 선택지 가로 3열 배치 확인, 렌더러가 아닌 다른 경로(과학·사회 N)의 배치.
3. 과학 기말용 앵커가 없다(현재 FINAL 앵커는 중간고사 산화·환원 전용). 과학 전체 코퍼스 앙상블 앵커 파일을 새로 만들어야 한다.
4. D-07 과목별 값, D-09 오프셋 수치, D-14 날짜의 의미는 사용자 확인이 필요하다.
5. 국어 V1~V6 레벨별 난이도·CORE/심화 비율 수치가 정의돼 있지 않다.
6. 학교가 기말 범위를 공지하면 EXAM_CONTEXTS의 단원·원문 ID와 scope_evidence_refs를 채워야 한다(현재 비어 있음).
7. CORE 카나리 2종은 PDF 마스터 V2.1을 고정 참조하고, 동결 회귀 fixture·오류 DB·폐기 레지스트리의 옛 버전 표기는 이력이라 그대로 두었다.
8. 정독하지 못한 파일: 오류 DB 본문 사건 기록, 국어 V6 전문 2종·교정 정책·미지 지문 분석, CONTENT_BUNDLE V1.6, CLAUDE_HANDOFF V1.4, DRIVE_WRITE_ADAPTER V1.2, EXTERNAL_TOOLS, agents/*.
