---
name: arc-skill-governance
description: 'ARC skill의 추가·수정·중복·충돌을 관리하고 Agent Skills 형식, 버전, 의존성, 토큰 예산, release 승격 조건을 검토한다. skill 자체를 관리할 때 사용한다.'
metadata:
  version: 1.0.0
  arc-role: skill-governance
---
# ARC Skill Governance

## 목적
skill 수가 늘어도 시스템이 프롬프트 묶음처럼 비대해지지 않도록 관리한다.

## 규칙
- 각 skill은 한 가지 전문 책임을 가진다.
- `SKILL.md`에는 무엇을 하는지와 언제 쓰는지를 frontmatter description에 명시한다.
- 본문은 기본 200줄 안쪽을 목표로 하고, 큰 참고자료는 `references/`로 분리한다.
- secret, credential, copyrighted source document를 skill 폴더에 넣지 않는다.
- Drive 원자료와 GitHub skill/engine을 혼합하지 않는다.
- 동일 기능이 70% 이상 겹치면 새 skill보다 기존 skill 확장을 우선한다.
- 새로운 skill은 `SKILL_REGISTRY.yaml`에 등록한다.
- main 승격 전 최소 구조검사 + 회귀평가를 거친다.

## 토큰 예산
문항 생성 런타임에서는 모든 skill을 preload하지 않는다. `arc-skill-stack`이 작업별 최소 조합만 선택한다.

## 폐기/통합 기준
- 3회 이상 호출되지 않고 다른 skill로 완전히 대체됨
- 독립 출력이 없고 다른 skill의 한 단계에 불과함
- 반복적으로 conflicting instruction을 발생시킴
