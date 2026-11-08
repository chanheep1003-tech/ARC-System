# ARC 사용자 결정 기록 — 2026-11-08
이 문서는 규칙 정비 세션에서 사용자가 직접 내린 결정과 그 반영 위치를 기록한다. 규칙의 권위는 SYSTEM_MANIFEST가 가리키는 각 규칙 파일에 있고,
이 문서는 감사 추적용이다. 값이 PROVISIONAL인 항목은 사용자 확인 전까지 바뀔 수 있다.

| ID | 결정 | 반영 위치 |
|---|---|---|
| D-01 | ARC_N 문항 메타 스트립에 추정 난이도를 표시한다. 표기는 D1~D5 그대로(D-10). 본문·선지·정답표에는 표시하지 않고 ARC_FINAL에는 표시하지 않는다. | 공통 엔진 §11, 난이도 엔진 §0, V2.4 §2·§16, N 레이아웃, manifest arc_n_metadata_strip_difficulty |
| D-02 | ARC_FINAL 조판 기준은 FINAL HTML 마스터의 확대 흑백 2단(12.8mm, 발문 9.5pt, 선택지 9.1pt). | V2.4 §6·§7, manifest arc_final_layout_basis |
| D-03/D-12 | ARC_N 표지에 승인 로고를 넣되 흑백 로고 자산(ARC_N_LOCKUP_MASTER_BW.png)을 신규 등록해 쓴다. 등록 전에는 BRAND_ASSET_MISSING. | V2.4 §5·§23, N 레이아웃, 조판 계약 §1-A, 브랜드 자산 등록부, manifest arc_n_cover_logo_variant |
| D-04 | 지문 세트는 지문 구간만 4문항 고정 슬롯을 해제한다. | V2.4 §6, N 레이아웃, manifest arc_n_passage_set_slots |
| D-05 | 기말 범위는 학교 공지 전까지 "2학기 전체 − 2학기 중간 실제 범위"로 확정(임시). MASTER의 SCOPE LOCK은 중간고사 스냅샷(참고용)으로 표시하고 범위 기준은 EXAM_CONTEXTS 하나로 일원화. | 국어·사회·과학 MASTER, EXAM_CONTEXTS |
| D-06 | 사회 CORE에서도 C파트 X표시 제외는 막는 규칙(BLOCKING). | CORE 엔진 V1.3 §8-A |
| D-07 | 기출 70% / 창작 30%는 과목마다 다르게 적용. 초기값(PROVISIONAL): SOC·SCI=PAST_70_AI_30, KOR=STRUCTURE_REFERENCE_ONLY(기출 문항 미사용), 부족 시 사용자 허용 하에 ORIGINAL_TRIAL. | 기출·창작 정책 §10, tooling/sources/generation_source_gate.py |
| D-08 | 사회 C학습지 손글씨 X표 영역은 기말에서도 계속 제외(복원하지 않음). | 기출·창작 정책 §5, 사회 MASTER §2-1 |
| D-09 | FINAL 난이도는 "동북고 평균보다 조금 더 어렵게". 과목 앵커 평균 +0.1~+0.3(PROVISIONAL). 공통 하한(D4+D5 30%)은 폐지. | 공통 엔진 §21.4, 난이도 엔진, FINAL 품질 게이트 §2, EXAM_CONTEXTS |
| D-11 | 초안은 임시 폴더 저장 허용, 제품 폴더 이동·중복 이력·BANK 등록은 사용자 내용 승인 후. | 중복·승인 정책 §6-A, 오케스트레이터, 사람 검토 게이트 §8, manifest |
| D-13 | 기말 ARC_FINAL은 학교 공지 없이 사용자 임시 확정만으로 출시 허용. 공지로 범위가 바뀌면 프로필 해시가 달라져 재검토. | EXAM_CONTEXTS release_on_user_provisional_lock |
| D-14 | 마감 2026-12-07(사용자 입력 "12 7일"). 시험일인지 준비 마감일인지 미확인. | 준비도 게이트, EXAM_CONTEXTS target_date, manifest readiness_deadline |

## 이 정비로 해결되지 않은 것 (후속 과제)
1. 흑백 로고 자산 파일이 없다. 등록(Drive ID, 해시) 전까지 ARC_N 표지는 생성되지 않는다.
2. 코드가 새 N 레이아웃을 강제하지 않는다: 4문항 슬롯 배치, 지문 구간 예외, 메타 스트립 난이도, BW 로고 해시 게이트는 typesetter_gateway·pdf_preflight에 구현이 없다.
3. 과학 기말용 앵커가 없다(현재 FINAL 앵커는 중간고사 산화·환원 전용). 과학 전체 코퍼스 앙상블 앵커 파일을 새로 만들어야 한다.
4. D-07 과목별 값, D-09 오프셋 수치, D-14 날짜의 의미는 사용자 확인이 필요하다.
5. 국어 V1~V6 레벨별 난이도·CORE/심화 비율 수치가 정의돼 있지 않다.
6. 학교가 기말 범위를 공지하면 EXAM_CONTEXTS의 단원·원문 ID와 scope_evidence_refs를 채워야 한다(현재 비어 있음).
7. CORE 카나리 2종은 PDF 마스터 V2.1을 고정 참조하고, 동결 회귀 fixture·오류 DB·폐기 레지스트리의 옛 버전 표기는 이력이라 그대로 두었다.
8. 정독하지 못한 파일: 오류 DB 본문 사건 기록, 국어 V6 전문 2종·교정 정책·미지 지문 분석, CONTENT_BUNDLE V1.6, CLAUDE_HANDOFF V1.4, DRIVE_WRITE_ADAPTER V1.2, EXTERNAL_TOOLS, agents/*.
