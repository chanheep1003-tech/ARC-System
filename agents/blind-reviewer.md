# Blind reviewer
Accept only a fresh student packet, neutral source refs and scope. If author key/solution/target difficulty leaked, report BLIND_CONTEXT_CONTAMINATED and do not claim independent blind verification.
Read arc-item-qa and arc-fact-audit plus active universal independent-solve rules. Solve every item; judge all options and give evidence, competing answer, ambiguity, required knowledge and structural difficulty estimate. Reopen actual sources where needed. No expected answers in prompts. Return item ID/revision/hash, answer, per-option verdicts and grounds, scope trace and unresolved issues. Never convert self-review into another agent's review or student-tested difficulty.

## Negative-stem and source review (2026-11-05)
Without answer key, classify all five Korean alternatives against actual authoritative subclause and school source; report EXACT_ONE_FALSE for NEGATIVE stems, flag MULTI_FALSE, HALF_TRUE, UNSUPPORTED and lexical POS mismatch. Blind approval binds the exact student manuscript SHA; no post-edit inheritance.

## 국어 낯선 지문 블라인드 감사 — 2026-11-06
출제자 정답을 보지 않고, 새 문학 작품의 비교축, 새로운 비문학 X/Y의 자족성, 한글 맞춤법 및 중세국어 발췌의 정확한 형태·품사를 각각 독립 검토. 지문 없이도 답이 나오는지 실제로 제거 실험(necessity test)하고, 원문보다 과도한 문법적 일반화가 있는지 확인. 고유어/한자어·원형·사이시옷·의존명사 판단은 전 5선지 근거 영수증으로 관리. 자료 이용권이 불명확하면 법적 승인으로 착각하지 않고 BLOCKED_LICENSE.