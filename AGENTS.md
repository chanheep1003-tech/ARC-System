# ARC 홈 — 에이전트 진입점

항상 한국어로 답한다. 이 파일은 **길 안내만** 한다. 세부 규칙은 아래 포인터가 가리키는 파일에 있고, 유효한 버전은 `SYSTEM_MANIFEST.yaml`이 정한다.

## 세션 시작
```bash
python tooling/arc.py doctor && python tooling/arc.py status
```

## 먼저 읽기 (순서대로)
1. `ARC_MAP.md` — 저장소 지도, 제품·버전 표, 제작 흐름
2. `SYSTEM_MANIFEST.yaml` — 활성 규칙 경로 (한 커밋에 고정해서 읽는다; 최신 파일명을 추측하지 않는다)
3. 맡은 과목의 진입 파일 **하나만**:
   - 국어: `entry/KOR.md`
   - 영어: `entry/ENG.md`
   - 사회·과학: `entry/SOC_SCI.md`
4. 팀 작업이면 `agents/TEAM.md`와 맡은 역할 파일

## 항상 지키는 규칙
- 제작 요청은 계획 카드부터: `python tooling/arc.py plan …` → 단원 세트 1개 → 사용자 검토 → 나머지.
- 문항은 **내신 출제자 순서**로 만든다: 출제 계획표 → 수업 근거 → 학생 오개념별 오답 → 이의 제기 검토 → 동료 교사 검토. 변별 문항은 배운 개념에 **새 보기·예문·조항·자료**를 주어 추론·심화하게 하고, **어려운 문항일수록 추론·심화로** 낸다(D4 추론·심화, D5 심화) (`quality/ARC_EXAMINER_LENS_V1.3.md`, 게이트 `python tooling/content_qa/examiner_lens_gate.py <번들>/items.yaml`).
- 문항은 등록된 학교 원형으로 만든다 (`quality/ARC_SCHOOL_ARCHETYPE_GATE_V1.0.md`). 모든 과목에서 `active.quality.false_difficulty_gate`와 문항 품질 루브릭을 함께 적용한다.
- 활성 과목: KOR, ENG, SOC, SCI. 기말 범위는 `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml`이 과목 MASTER의 중간고사 SCOPE LOCK보다 우선한다.
- 사용자 검수를 1번 통과한 산출물은 반드시 Google Drive에 저장한다. 통과 전에는 저장하지 않는다 (`ops/ARC_DRIVE_SAVE_RULE_V1.0.md`).
- 규칙은 manifest가 고른 파일에만 넣는다. 지난 버전은 `archive/`에 있으며 읽지도 고치지도 않는다. 새 규칙은 새 파일·새 버전으로 만들고 manifest를 갱신한다.
- 파일을 고친 뒤 `python tooling/arc.py checksums`, 푸시 전 `python tooling/arc.py ci`.
- 시스템 변경은 유지보수 브랜치에서 한다. PR #6은 활성 규칙이 아닌 별도 후보다.
- 실제 위임은 지원되는 호스트나 API 어댑터가 있을 때만 일어난다. 없으면 검증된 파일 핸드오프를 쓰고 WAITING_FOR_WORKER로 기록한다. 일어나지 않은 모델 간 호출을 했다고 말하지 않는다.
- 사용자의 현재 명시적 지시가 이 파일보다 우선한다.

## 다른 곳
| 무엇 | 어디 |
|---|---|
| 최근 인수인계 (2026-11-14 출제자 시선 V1.3 · 국어 단계 통합) | `ops/HANDOFF_20261114_EXAMINER_LENS.md` |
| 운영 절차 | `ops/ARC_RUNBOOK.md` · 한 요청 = 한 상태: `tooling/workflow/arc_workflow.py` |
| 프로젝트 스킬 | `skills/` (목록: `skills/SKILL_REGISTRY.yaml`) |
| 외부 플러그인·도구 | `.claude/settings.json`, `tools/oss/README.md` |
| 지난 버전 규칙 | `archive/` (참고용, 비활성) |
| 원본 자료·생성 PDF | Google Drive (저장소에 올리지 않음) |
