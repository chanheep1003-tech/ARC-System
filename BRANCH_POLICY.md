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
