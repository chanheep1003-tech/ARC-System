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

활성/비활성은 `.claude/settings.json`의 `enabledPlugins`를 true/false로 바꾸면 된다.
세션 시작 시 `--quick`이 자동 실행되며, 앱류는 `./tools/oss/install.sh --full` (기본 위치 `~/.arc-oss`, `ARC_OSS_HOME`으로 변경).
