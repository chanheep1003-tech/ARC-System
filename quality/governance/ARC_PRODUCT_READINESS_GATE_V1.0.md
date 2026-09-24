# ARC PRODUCT READINESS GATE V1.0
VERSION: 1.0
DATE: 2026-09-24
STATUS: ACTIVE-DEV
ROLE: deadline readiness scoring and release prioritization

## 0. DEADLINE
HARD DEADLINE: 2026-09-25 23:59 KST

Current active subject/product matrix:
- KOR: ARC_N, ARC_FINAL
- SOC: ARC_N, ARC_FINAL
- HIS: ARC_N only
- SCI: ARC_N, ARC_FINAL, OXIDATION_REDUCTION_ONLY

CORE is maintenance-only and excluded from the 80% sprint target.

## 1. NON-GAMEABLE READINESS RULE
Readiness is evidence-based, not a subjective percentage.

A subject/product combination is scored from five gates, each worth 20 points:
1. SCOPE_SOURCE_READY
2. GENERATION_QUALITY_READY
3. QA_GOVERNANCE_READY
4. E2E_PDF_READY
5. REGRESSION_RELEASE_READY

Each gate is 0 / 10 / 20 only:
- 0 = missing, blocked, or unverified
- 10 = partially implemented or WARN with concrete evidence
- 20 = executable/verified PASS with evidence

SUBJECT_PRODUCT_READINESS = sum of the five gates, maximum 100.

Product readiness is the MINIMUM score among all currently active subject/product combinations for that product.
This prevents a strong subject from masking an unfinished subject.

ARC_N product readiness:
MIN(KOR_N, SOC_N, HIS_N, SCI_REDOX_N)

ARC_FINAL product readiness:
MIN(KOR_FINAL, SOC_FINAL, SCI_REDOX_FINAL)

## 2. HARD TARGET
By 2026-09-25 23:59 KST:
- ARC_N_PRODUCT_READINESS >= 80
- ARC_FINAL_PRODUCT_READINESS >= 80
- Every active subject/product combination should target >=80.
- RELEASE_READINESS cannot be PASS if either product is below 80.

If time is insufficient, always work on the lowest-scoring active subject/product combination first, except where a higher-priority blocker prevents multiple downstream combinations.

## 3. GATE DEFINITIONS

### G1 SCOPE_SOURCE_READY — 20
20:
- exact current sprint scope locked
- required school/textbook/source inventory accessible or verified enough for the intended canary/production path
- exclusions applied
- no unresolved scope ambiguity affecting answer basis

10:
- scope locked, but one non-critical source extraction/reference remains partial
- synthetic canary possible but production source path still WARN

0:
- scope unresolved
- required answer-basis source unavailable
- science outside redox or history FINAL requested in current sprint

### G2 GENERATION_QUALITY_READY — 20
20:
- subject/product generation path exists
- Dongbuk difficulty floor applied
- attractive distractor requirements applied
- answer-length/detail cue gate applied
- task/judgment-axis diversity applied
- no obvious-answer pattern in current verified canary

10:
- common engine exists but subject/product execution has not yet been verified
- quality rules present but model-backed or product-specific canary remains pending

0:
- no usable generation path or known quality regression remains open

### G3 QA_GOVERNANCE_READY — 20
20:
- unique answer / evidence / scope trace / independent solve PASS
- exact+semantic duplicate policy wired
- FINAL_USER_APPROVAL / DRIVE_SAVE governance correct
- FINAL additionally passes DIFFICULTY_PROFILE + ITEM_QUALITY_PROFILE

10:
- QA stack exists but one required active-product gate is WARN/pending

0:
- answer integrity, dedup, approval, or FINAL quality gate absent/bypassed

### G4 E2E_PDF_READY — 20
20:
- Generator -> QA -> Handoff -> Typesetter -> PDF -> Preflight executable path PASS
- question/answer count PASS
- layout/product isolation PASS
- clipping/overflow/font/internal metadata failures = 0
- required blank/answer-key/page-order rules PASS

10:
- partial/synthetic E2E only, or PDF path PASS but production source path not yet verified

0:
- no active E2E path or current E2E FAIL

### G5 REGRESSION_RELEASE_READY — 20
20:
- current subject/product canary PASS
- relevant fault injections blocked
- static/manifest/checksum validation PASS
- no unresolved S1 regression affecting release

10:
- canary exists but one relevant regression/fault class remains pending

0:
- no canary or current regression/CI FAIL affecting the product

## 4. PRIORITIZATION
At every scheduled run:
1. recompute all seven active subject/product readiness scores
2. identify the minimum score
3. work on the smallest number of blockers that can increase that score by at least 10 points
4. rerun the same canary/E2E
5. persist evidence in RUN_LOG and ERROR_DATABASE when meaningful
6. continue to next-lowest score if time remains

Do not spend a run polishing a combination already >=90 while any active combination is <80, unless the >=90 path contains a shared blocker that directly raises the lower combination.

## 5. QUALITY FLOOR
80% readiness is a minimum release-preparation threshold, not permission to lower quality.

Even if numerical readiness >=80:
- unresolved wrong-answer risk
- out-of-scope evidence
- answer-key mismatch
- duplicate leakage
- obvious-key bias
- FINAL difficulty-profile failure
- PDF corruption
are HARD FAIL and keep release blocked.

## 6. REPORT FORMAT
Every meaningful run reports:
- KOR_N
- SOC_N
- HIS_N
- SCI_REDOX_N
- ARC_N_PRODUCT_READINESS = minimum above
- KOR_FINAL
- SOC_FINAL
- SCI_REDOX_FINAL
- ARC_FINAL_PRODUCT_READINESS = minimum above
- lowest blocker
- score delta this run
- evidence used

END ARC PRODUCT READINESS GATE V1.0
