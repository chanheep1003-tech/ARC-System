# ARC Release / Dev Policy

## main
실제 CORE / N° / FINAL 생성에 사용하는 RELEASE 브랜치다.
`SYSTEM_MANIFEST.yaml`에 등록된 파일만 활성 규칙으로 간주한다.

## dev
새 규칙, 실험적 난이도 보정, 템플릿 변경을 시험하는 브랜치다.
검증 전에는 실제 시험 대비 결과물 생성에 사용하지 않는다.

## 승격 규칙
dev 변경은 다음 조건을 만족한 뒤 main으로 옮긴다.
1. 범위/정답/자료 HARD FAIL 없음
2. 기존 QA Bench 회귀검사 통과
3. 기존 안정 규칙과 충돌 확인
4. SYSTEM_MANIFEST 버전 갱신
5. RUN_LOG에 변경 목적 기록

## 금지
- Drive의 교과서/기출/유료 문제집 PDF를 GitHub에 업로드하지 않는다.
- 서로 다른 교사의 기출을 Teacher DNA로 병합하지 않는다.
- main에서 실험성 수정을 바로 수행하지 않는다.

## 현재 상태 (2026-11-10)
- 실사용 ruleset은 `dev`(1.8.x)다. `main`은 1.0.x로 dev보다 500커밋 이상 뒤처져 있고 실행 도구·CI·시험 설정이 없다.
- 따라서 dev가 main으로 승격되기 전까지 실제 CORE / N° / FINAL 생성은 **dev의 고정 커밋**(`ruleset_commit`)을 기준으로 한다. main의 옛 규칙으로 생성하지 않는다.
- 승격은 위 승격 규칙 1~5와 `python tooling/arc.py ci` 전체 통과를 확인한 뒤 dev → main PR 한 번으로 수행한다. 승격 시 `system.version`을 release 계열로 올리고 `tooling/validate_system.py`의 버전 검사도 함께 갱신한다.

## 등록 파일 원칙
- 규칙은 `SYSTEM_MANIFEST.yaml`이 선택한 파일에서만 효력이 있다. 대체된 이전 버전 파일(`*_V4.0`, `*_V1.0` 등)에 규칙을 덧붙이지 않는다.
- 추적 파일을 고친 뒤에는 `python tooling/arc.py checksums`로 `CHECKSUMS.sha256`을 갱신한다. CI는 불일치를 실패로 처리한다.
