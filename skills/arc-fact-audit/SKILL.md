---
name: arc-fact-audit
description: 'ARC 문항 생성과 분리된 두 번째 패스에서 사실·수치·연표·철학자 입장·과학 조건·DFS/BFS 등을 SOURCE_LEDGER와 함께 검증한다.'
metadata:
  version: 1.1.0
  arc-role: factual-verification
---
# ARC Fact Audit

## 핵심 원칙
생성과 검증을 같은 패스에서 완료했다고 간주하지 않는다.
핵심 사실이 외부 또는 특정 자료에 의존하면 quality/ARC_SOURCE_LEDGER_V1.0.md를 적용한다.

## 절차
1. 문항에서 검증 가능한 주장을 추출한다.
2. 각 주장에 SOURCE_REQUIRED 여부를 판정한다.
3. SOURCE_REQUIRED이면 SOURCE_ID를 연결한다.
4. PASS B에서 해당 SOURCE_ID의 원출처를 실제로 다시 연다.
5. 주장, 수치, 단위, 날짜, 고유명사, 정의, 인과, 선후 관계를 원출처 위치와 대조한다.
6. 정답뿐 아니라 핵심 오답의 틀린 이유도 사실적으로 검증한다.
7. ANSWER_BASIS SOURCE가 모두 VERIFIED일 때만 factual gate PASS.
8. SOURCE_CONFLICT가 있으면 임의로 한쪽을 선택하지 않는다.

## 상태
SOURCE 상태는 VERIFIED / UNVERIFIED / SOURCE_MISSING만 사용한다.
- UNVERIFIED: BANK_PASS 금지
- SOURCE_MISSING: RELEASE/BANK 금지
- SOURCE_CONFLICT=true: 정답 근거 사용 금지

## 과목별 중점
- 과학: 조건, 그래프 축, 수치, 단위, 실험 통제, 보존/변화 관계
- 사회: 사상가 입장, 판례·헌법기관, 통계 기준, 법·제도 표현
- 한국사: 연도, 전후관계, 단체·인물, 지역, 정책 주체, 사료
- 국어: 작품/지문 근거, 학교 학습활동, 자료 밖 작가론 남용 금지
- AI: 알고리즘 순서, DFS/BFS 조건, 코드 결과, 데이터 처리 단계

## Hard Fail
- 정답 근거의 SOURCE_REQUIRED 출처가 VERIFIED 아님
- 실제 원출처를 재열람하지 않았는데 VERIFIED 처리
- 오답이 사실은 맞는 문장임
- 자료 숫자와 선택지 숫자가 불일치
- 출처가 충돌하는데 임의로 확정
- 역사 사실/철학자 입장을 범위 밖 해석으로 확장
