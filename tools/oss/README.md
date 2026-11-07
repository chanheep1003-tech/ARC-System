# ARC 오픈소스 도구

소스는 저장소에 커밋하지 않는다(BRANCH_POLICY: 대용량/외부 자료 금지). 설치는 `install.sh`, 플러그인은 `.claude/settings.json`.

| 도구 | 종류 | ARC에서의 용도 | 상태 |
|---|---|---|---|
| microsoft/markitdown | CLI(pip) | 교과서·학습지·기출 PDF/DOCX/PPTX → Markdown 변환 후 범위 확인(`markitdown in.pdf -o out.md`) | 자동 설치(--quick) |
| rtk-ai/rtk | CLI(Rust, OSS판) | 긴 명령 출력 압축으로 토큰 절감 | 자동 설치(--quick) |
| obra/superpowers | 플러그인 | 계획·TDD·리뷰 워크플로 | 활성 |
| mattpocock/skills | 플러그인 | 엔지니어링 스킬 모음 | 활성 |
| pbakaus/impeccable | 플러그인 | HTML 조판 템플릿(`templates/`) 디자인 점검 | 활성 |
| toothlessdev-agent | 플러그인 4종 | daily-briefing, workflow-parallel, adhd, pr-review | 활성 |
| ayghri/i-have-adhd | 플러그인 | 결론 먼저·번호 단계 응답 스타일 | 활성 |
| JuliusBrussee/caveman | 플러그인 | 극단적 축약 응답 | **비활성**(문항 지문 품질 영향) |
| thedotmack/claude-mem | 플러그인 | 세션 간 기억(상주 워커) | **비활성**(ARC 데이터 정책상 임의 기억 저장 방지) |
| HKUDS/DeepTutor | 앱(Python+Node) | 학습 튜터/RAG 참고 | `--full` 설치 |
| Orkas-AI/Orkas | 앱(Node) | 멀티 에이전트 지휘 | `--full` 설치 |
| p-e-w/heretic | CLI(pip) | 모델 abliteration (**GPU 필요**, 이 클라우드엔 GPU 없음) | `--full` 설치만 |
| headroomlabs-ai/headroom | CLI(pip)+플러그인 | LLM 컨텍스트 압축 프록시(`headroom proxy`). skill+agent-hooks 플러그인 활성(세션 시작 시 프록시 자동 기동), 익명 전송(beacon)은 env로 끔 | skill 활성, CLI `--full`(`headroom proxy --port 8787`) |
| msitarzewski/agency-agents | 에이전트 모음 | 역할별 서브에이전트를 `~/.claude/agents`에 설치 | 자동 설치(--quick) |
| Graphify-Labs/graphify | CLI(pip `graphifyy`) | 저장소/문서 지식 그래프 생성 | 자동 설치(--quick) |
| ruvnet/ruflo | 플러그인(+npx) | 멀티 에이전트 스웜. `ruflo-core`만 활성(나머지 50여개는 필요 시 추가) | 활성 |
| DietrichGebert/ponytail | 플러그인 | 응답 레벨 조절 스킬 | 활성 |

활성/비활성은 `.claude/settings.json`의 `enabledPlugins`를 true/false로 바꾸면 된다.
세션 시작 시 `--quick`이 자동 실행되며, 앱류는 `./tools/oss/install.sh --full` (기본 위치 `~/.arc-oss`, `ARC_OSS_HOME`으로 변경).

## Headroom 사용법
- 프록시: `headroom proxy --port 8787` (헬스체크 `curl localhost:8787/health`), 절감량 `headroom savings`, 점검 `headroom doctor`.
- 실제로 압축을 거치려면 Claude Code를 프록시 경유로 실행: `ANTHROPIC_BASE_URL=http://localhost:8787 claude`. 클라우드 세션은 자체 API 경로를 쓰므로 기본 설정에서는 강제하지 않았다(세션이 끊길 수 있음).
