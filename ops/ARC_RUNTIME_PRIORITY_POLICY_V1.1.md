# ARC RUNTIME PRIORITY POLICY V1.1
VERSION: 1.1
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: runtime scheduling and resource allocation

## 0. PURPOSE
When time, context, or tool budget is constrained, preserve accuracy and required QA while allocating extra review according to subject priority.

## 1. SUBJECT PRIORITY
Default order:
1. KOR — 공통국어2
2. SOC — 통합사회2
3. HIS — 한국사2
4. SCI — 통합과학2
5. AI — 인공지능기초

Normal 100-item QA still keeps equal base item counts unless the user requests otherwise.
Priority controls:
- processing order
- retry order
- additional review
- research effort
- context allocation
- optimization budget

Recommended extra-resource weights:
- KOR 30
- SOC 25
- HIS 20
- SCI 15
- AI 10

## 2. REQUIRED STAGES
P0 SCOPE / ACCURACY / UNIQUE ANSWER
P1 ACTUAL ITEM PRODUCTION
P2 REQUIRED QA
P3 REQUIRED VISUALS
P4 BANK / SET EDITORIAL
P5 RESEARCH / OPTIMIZATION

P0-P2 may not be skipped.
P3 may not be skipped when the visual is answer-bearing.

## 3. DEGRADATION
If resources are constrained, defer in this order:
1. optional P5
2. nonessential P4 polish
3. nonessential P3 visuals

Never trade required QA for item count.

## 4. SUBJECT FAILURE ISOLATION
A failed subject does not terminate the whole run.
Persist failure state, continue to the next subject, then resume failures in:
KOR → SOC → HIS → SCI → AI order.

## 5. RETRY
Default automatic retry budget: one retry per failed subject/stage.
Do not bypass hard-fail rules to make a retry pass.

## 6. USER OVERRIDE
An explicit user request for another subject order overrides this policy for that run only.

END ARC RUNTIME PRIORITY POLICY V1.1
