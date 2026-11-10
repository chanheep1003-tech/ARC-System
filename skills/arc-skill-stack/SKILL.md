---
name: arc-skill-stack
description: 'ARC 작업 목표에 맞춰 가장 작은 호환 skill 조합을 선택하고 실행 순서를 정한다. 모든 skill을 매번 불러 토큰을 낭비하지 않도록 orchestration할 때 사용한다.'
metadata:
  version: 1.0.0
  arc-role: orchestration
---
# ARC Skill Stack

## 핵심 원칙
**필요한 skill만 로드한다.** 기능이 겹치면 더 구체적인 ARC skill 하나를 선택하고 중복 검사를 피한다.

## 표준 조합
### 새 N°/FINAL 문항 생성
`arc-item-generator` → `arc-distractor-engine` → [필요 시 `arc-visual-renderer`] → `arc-fact-audit` → `arc-item-naturalness-audit` → `arc-item-qa` → `arc-set-editor` → [PASS만 `arc-bank-curator`]

### 새 자료 유입
`arc-source-ingest` → scope ledger 반영 → 이후 필요한 생성 skill

### 웹/외부자료 사용
`arc-research-grounding` → `arc-fact-audit` → 생성 workflow

### 엔진/MASTER 변경 검증
`arc-eval-regression` + 기존 QA 규칙

## 충돌 해결
- 범위: 사용자 exclusion > 현재 학습지/교사자료 > 현재 교과서 > 외부자료
- 사실: 원자료/공식근거가 생성 결과보다 우선
- 난도: 학교 difficulty bench가 일반 “수능 난도” 표현보다 우선
- 시각자료: 정확성/기능성이 미관보다 우선
- 자연스러움: 정확성/명료성을 절대 희생하지 않음

## 비활성 기능
개인 오답 기반 재출제, 학습자 프로파일링, 개인별 약점 추적은 ARC skill stack에 포함하지 않는다.
