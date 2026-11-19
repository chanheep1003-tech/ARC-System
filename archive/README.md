# archive/ — superseded ARC rule files

이 폴더는 `SYSTEM_MANIFEST.yaml`이 더 이상 고르지 않는 구버전 규칙 파일을 원래 경로 그대로 보관한다.
예: `engine/common/COMMON_GENERATION_ENGINE_V4.8_ARC.md` → `archive/engine/common/COMMON_GENERATION_ENGINE_V4.8_ARC.md`

- 제작·검수·조판에서 이 폴더의 파일을 읽지 않는다. 유효한 파일은 manifest가 고른 것뿐이다.
- 이 폴더의 파일에 규칙을 덧붙이지 않는다. 바꿀 규칙은 새 버전 파일로 만들고 manifest를 갱신한다.
- 왜 폐기됐는지와 대체 파일은 `quality/governance/DEPRECATION_REGISTRY_V1.1.yaml`에 있다.
- 과거 실행 기록(`ops/RUN_LOG.*`, `CHANGELOG.md`, `quality/production/*`)은 당시 경로를 그대로 둔다.
  그 기록의 경로는 이 폴더 아래 같은 상대 경로에서 찾는다.

이동: 2026-11-19, 125개 파일.
