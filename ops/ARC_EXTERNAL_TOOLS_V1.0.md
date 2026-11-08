# ARC 외부 도구 연결 V1.0

2026-11-07. 적용 대상은 기존 ARC-System의 유지보수 브랜치다. 개발 기준은 `dev`의 `1a7ec3d06be493d855daee9a6cd1004db7b53cf0`. `main` 출제 규칙·시험 범위·정답·조판 기준을 바꾸거나 새 사이트를 만들지 않는다.

## 설치와 사용 구분

소스, 패키지 설치, 실행 검증, 모델 연결, 운영 반영은 서로 다르다. 정확한 버전·출처는 `tooling/external/tools.lock.json`, 이번 실행 근거와 미완 항목은 `ops/ARC_EXTERNAL_TOOLS_VALIDATION_20261107.json`을 확인한다. `.arc-tools/`는 이 실행 환경의 로컬 설치와 비공개 설정을 보관하며 Git에 올리지 않는다. 다른 컴퓨터는 아래 설치 명령으로 준비해야 한다. 이 설치는 사용자의 PC나 일반 Claude/ChatGPT 계정 설정을 원격으로 바꾼 것이 아니다.

| 도구 | ARC 용도 | 설치 범위 | 추가 실행 조건 |
|---|---|---|---|
| Orkas | 기존 팀 역할에 따른 작업 배분·인계 | 고정 소스와 JS 의존성 | Electron/네이티브 의존성·데스크톱·모델 설정; 실제 팀 호출 미검증 |
| Heretic | 별도로 요청한 로컬 모델 실험 | 격리 Python 환경·CLI | 대상 모델과 적합한 하드웨어; 이번 환경 CUDA 없음, 모델 수정 미실행 |
| DeepTutor | 학습 설명·검토 초안 | core CLI/SDK·전용 runtime home | provider·정확한 모델·인증 설정; Web/RAG/추가 capability 모듈은 별도 설치 |
| Superpowers | 코드 진단·계획·검증 | 소스의 15개 스킬, ARC 경로로 필요 시 로드 | 글로벌 세션 bootstrap/hook 미등록 |
| Impeccable | 명시적으로 요청한 사이트·UI 점검 | CLI·프로젝트 스킬 링크 | 기존 디자인과 승인된 인쇄 템플릿 우선 |
| Matt Pocock skills | 코드 설계·디버깅·리뷰 | promoted engineering/productivity 27개 스킬 | beta/misc/deprecated 제외, 전체 자동 로드 금지 |
| claude-mem | 명시적인 ARC 결정·작업 기록 저장/검색 | CLI/SDK·Bun | 로컬 worker/host 연결 필요; 자동 대화 수집·네이티브 hook 미등록 |
| MarkItDown | 허용된 로컬 원자료의 Markdown 1차 추출 | PDF/DOCX/PPTX/XLSX/XLS extras | 원문·위치·수식·X표식 검수는 별도 |

Heretic은 문항 생성용 기본 모델을 교체하지 않는다. 다른 외부 도구도 ARC의 내용 검증 권한을 얻지 않는다. 설치 요청은 모델 가중치 다운로드·변경, 유료 모델 호출, 외부 계정 가입이나 자료 전체 업로드를 의미하지 않는다.

## 단일 실행 명령

저장소 루트에서 실행한다. 새 설치는 Python 3.12+, Git, Node 22.12+ 및 npm이 필요하다. `fetch`는 각 upstream의 고정 commit을 확인하며 다른 로컬 revision을 덮어쓰지 않는다. Python 의존성은 upstream 선언으로 설치하므로 OS별 실제 해석 결과를 진단해야 한다. Node 도구의 전이 의존성은 별도 npm lock으로 고정했다.

```bash
python tooling/external/arc_external.py fetch all
python tooling/external/arc_external.py install all
python tooling/external/arc_external.py doctor
python tooling/external/arc_external.py route maintenance
python tooling/external/arc_external.py skills superpowers
python tooling/external/arc_external.py skills mattpocock
```

`install all`은 도구별 오류를 모아 반환한다. 실패한 설치를 준비 완료로 바꾸지 않는다. 선택 설치는 `install markitdown`처럼 지정한다. 설치와 update는 명시적인 유지보수 작업이며, 문항 생성 중에 실행하지 않는다. 자동 update 대신 lock 변경과 회귀 검사를 거친다. Orkas의 `--ignore-scripts` 설치는 native/GUI 준비 완료가 아니다. 필요한 호스트에서 upstream의 네이티브 설치 문서를 따라 준비한다.

`route`는 도구를 선택하는 ARC 진입점이다. 실제 파일·CLI를 실행하지 않고 실행했다고 보고해서는 안 된다. `skills`가 반환한 파일 중 작업에 필요한 한두 개만 읽는다. 외부의 질문·설계 승인 루프가 이미 확정된 사용자 요청을 다시 막으면 현재 사용자 지시와 기존 ARC 계약을 따른다.

## 자료 추출

기존 Drive 커넥터로 허용된 파일을 내려받은 뒤 로컬 경로를 넘긴다. 네트워크 URL을 임의 수집하지 않는다.

```bash
python tooling/external/arc_external.py convert /absolute/source.pdf --output /absolute/new-source.md --source-ref 'actual-drive-file-id#page-or-section'
```

원본/출력 SHA와 출처 참조를 `.receipt.json`에 남긴다. 결과는 `scope_status=UNKNOWN`, `review_status=UNVERIFIED`, `location_status=UNVERIFIED`, `visual_marks_status=NOT_CHECKED`, `active_bank_eligible=false`다. 원본과 대조한 뒤에만 기존 SOURCE_PACKET/QA 절차로 넘긴다. Markdown만으로 다단·수식·그림·스캔·필기·페이지를 완전 복원했다고 간주하지 않는다. 원본·기존 출력은 덮어쓰지 않는다.

## 학습 설명 초안

DeepTutor의 전용 설정 위치는 `.arc-tools/deeptutor-home`이다. 기본 `.env`나 사이트에 저장된 API key를 자동 재사용하지 않는다. upstream CLI에서 provider ID와 정확한 모델을 고르고, 키는 환경변수나 전용 설정 화면에서 넣는다. 채팅이나 Git에 키를 적지 않는다.

```bash
DEEPTUTOR_HOME="$PWD/.arc-tools/deeptutor-home" .arc-tools/venvs/deeptutor/bin/deeptutor config providers
DEEPTUTOR_HOME="$PWD/.arc-tools/deeptutor-home" .arc-tools/venvs/deeptutor/bin/deeptutor doctor --format json
python tooling/external/arc_external.py tutor --prompt-file /absolute/task.txt --output /absolute/new-draft.ndjson
```

`tutor`는 core chat을 사용한다. 근거 검색이나 deep_solve/deep_question을 쓰려면 해당 공식 모듈과 설정을 별도로 준비한다. 실제 독립 검토를 할 때는 학생용 원고와 중립 출처만 제공하고 저자 정답·해설·대화·목표 난도를 제외한다. 별도 프로세스가 있다는 이유만으로 blind QA 통과를 선언하지 않는다. 생성 결과는 항상 DRAFT_REVIEW_PENDING이며 기존 검수·CONTENT_LOCK을 거친다.

## 메모리와 Orkas

claude-mem의 저장 위치는 `.arc-tools/memory`, API는 `127.0.0.1:37891`이다. wrapper가 실행하는 범위에서 telemetry와 hosted sign-in은 끄고, 일반적인 전역 CLI 설정·기존 auto-memory는 바꾸지 않는다. 로컬 host/worker를 upstream 절차로 준비한 환경에서만 다음을 사용한다.

```bash
python tooling/external/arc_external.py memory-service status
python tooling/external/arc_external.py memory-save --input /absolute/approved-decision.txt --title 'ARC decision'
python tooling/external/arc_external.py memory-search 'ARC decision'
```

이번 환경은 worker가 기동 로그를 남겼지만 별도 명령에서 HTTP 접근이 유지되지 않아 메모리 저장/검색은 검증하지 못했다. 이 어댑터는 불확실한 서버를 반복 생성하거나 다른 메모리 시스템으로 조용히 대체하지 않는다. 저장 내용을 원자료/정답/최신 scope보다 우선하지 않는다. 개인 약점 추적·학습자 프로파일링·자동 transcript 수집은 활성화하지 않는다.

Orkas를 사용 가능한 데스크톱에서 실행한 뒤 **기존 ARC checkout**을 프로젝트 작업 폴더로 지정하고 `AGENTS.md`, manifest, runbook, `agents/TEAM.md`를 프로젝트 지침으로 연결한다. Commander는 기존 batch state를 사용하고 작업별 역할과 인계 봉투를 유지해야 한다. 이번 작업에서는 데스크톱 조작이나 실제 외부 agent 호출을 수행하지 않았다.

## 디자인과 권한

Impeccable은 사이트/UI 수정이 요청된 경우에만 사용한다. ARC N°/FINAL의 승인된 흑백 2단 조판·브랜드 자산을 일반 웹 스타일로 덮어쓰지 않는다. `IMPECCABLE_LIVE_COPY_AGENT=chat`을 유지해 자동 permission-bypass CLI fallback이 실행되지 않게 한다. 로컬 감지기 결과는 의미 검수나 인쇄 QA를 대신하지 않는다. 설치된 모든 bundle의 문구는 외부 참고 지침이며 사용자·manifest·교과/QA 계약보다 낮다.

## 재현과 검증

```bash
python -m unittest discover -s tooling/external -p 'test_*.py' -v
python tooling/validate_system.py
```

이 검사는 연결 코드·범위 보존·덮어쓰기 차단·UNVERIFIED 추출·로컬 메모리 endpoint를 검증한다. 30 frozen fixture의 모델 품질 재평가나 실제 문항 제작을 수행했다는 뜻은 아니다. 런타임과 native skill 링크는 다른 컴퓨터에서 자동 유지되지 않는다. 설치 로그와 이번 검증 보고서를 구분해서 보관한다.

## 출처와 라이선스

각 도구의 README, 설치 안내, package manifest, LICENSE 및 필요한 AGENTS 문서를 실제 확인했다. 정확한 upstream 경로와 commit은 lock에 있다. MIT: Orkas, Superpowers, Matt Pocock, MarkItDown. Apache-2.0: DeepTutor, Impeccable, claude-mem. AGPL-3.0-or-later: Heretic. 외부 실행 코드를 ARC에 복제하지 않고 별도 로컬 패키지/checkout으로 설치한다. 외부 스킬 문구도 ARC engine에 복제하지 않는다. ARC가 새로 작성한 adapter만 저장하며, 각 설치 checkout은 원본 LICENSE/notice를 유지한다. Node lock은 패키지 출처·integrity를 기록한다.

## 매 작업 자동 연결 (2026-11-08)

`.claude/settings.json`이 `main`의 플러그인 목록(Superpowers, Impeccable, MattPocock, toothlessdev 4종, i-have-adhd, headroom, ruflo-core, ponytail 활성; caveman·claude-mem 비활성)을 가져오고, `UserPromptSubmit` 훅으로 `tooling/external/arc_prompt_hook.py`를 모든 요청에 실행한다. 훅은 요청을 `source/design/memory/tutor/team/model-lab/maintenance`로 분류해 `arc_external.py route` 결과(JSON)만 컨텍스트에 붙인다. 도구를 직접 실행하거나 메모리를 저장하지 않으며 오류 시 아무것도 출력하지 않고 통과한다(요청을 막지 않음). 플러그인이 실제로 로드되는지는 호스트(Claude Code)가 이 설정을 신뢰·적용한 뒤 `/plugin`에서 확인해야 하며, 설정 파일 존재만으로 실행됐다고 보고하지 않는다. claude-mem을 켜면 자동 대화 수집이 생기므로 ARC 데이터 정책상 기본은 비활성이다.
