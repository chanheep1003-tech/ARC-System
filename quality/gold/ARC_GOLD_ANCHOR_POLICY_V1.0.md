# ARC GOLD ANCHOR POLICY V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: concrete good/bad item anchors for generation and QA calibration

## 1. PURPOSE
Rules alone are insufficient for stable item quality. Every subject uses a fixed comparison pack containing:
- GOOD 3 items: target-quality examples
- BAD 3 items: rejection/revision examples
- expected score range
- expected decision
- explicit reasons

The anchors calibrate generation and QA. They are not scope authorities and never expand the user's current scope.

## 2. LOAD CONTRACT
Before subject item generation or subject item QA:
1. read subject MASTER
2. read the matching GOLD_ANCHOR_PACK
3. compare the draft item to the nearest GOOD and BAD anchors by structure, reasoning load, distractor realism, and evidence use
4. record internal ANCHOR_MATCH metadata

Required metadata:
- GOLD_PACK_VERSION
- NEAREST_GOOD_ANCHOR
- NEAREST_BAD_ANCHOR
- ANCHOR_MATCH_NOTE

## 3. COPYRIGHT / SOURCE RULE
Anchors must be ARC-original items.
Textbook, worksheet, commercial workbook, and past-exam materials may supply:
- layout grammar
- reasoning structure
- distractor strength
- information density
- difficulty mechanism
but their item wording, long passages, tables, or artwork must not be copied.

## 4. SCORE CALIBRATION
GOOD anchors define the observable features expected for BANK_A/PREMIUM candidates.
BAD anchors define ceilings or rejection reasons.

A draft may not receive a score above its nearest GOOD anchor merely because it is cleanly written.
A draft similar to a BAD anchor inherits the relevant score ceiling until the defect is removed.

## 5. GOOD REQUIREMENTS
A GOOD anchor should normally contain at least one:
- functional material/data
- condition combination
- concept transfer
- source/passsage analysis
- multi-step reasoning
and at least two plausible distractors tied to real misconceptions/condition errors.

## 6. BAD CATEGORIES
BAD anchors should cover at least:
- DIRECT_RECALL / trivial recognition
- WEAK_DISTRACTOR / effective 2–3 choice item
- FAKE_DIFFICULTY / unsupported or generic difficulty
Additional subject-specific bad types are allowed.

## 7. CHANGE CONTROL
Anchor packs live on dev.
Changing an existing anchor ID requires:
- reason
- old/new expected decision comparison
- regression note
Do not silently replace anchors to make a new engine look better.

## 8. ACTIVE PACKS
- quality/gold/KOR_GOLD_ANCHORS_V1.0.md
- quality/gold/SCI_GOLD_ANCHORS_V1.0.md
- quality/gold/SOC_GOLD_ANCHORS_V1.0.md
- quality/gold/HIS_GOLD_ANCHORS_V1.0.md
- quality/gold/AI_GOLD_ANCHORS_V1.0.md
