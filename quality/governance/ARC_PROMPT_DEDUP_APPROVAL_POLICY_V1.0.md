# ARC PROMPT DEDUP + USER APPROVAL POLICY V1.0
DATE: 2026-09-22
STATUS: ACTIVE-DEV
ROLE: universal governance for every ARC problem-generation prompt authored for the user

## 0. PURPOSE
Every future prompt that asks any model to generate ARC questions/problems must prevent duplication with previously approved ARC outputs and must not persist a new final problem set to Google Drive until the user explicitly approves the completed result.

This policy governs prompt authoring as well as downstream generation workflow.

## 1. SCOPE
Apply whenever the user asks to:
- write a prompt for problem/question generation
- generate an ARC N°/FINAL/problem set through a prompt
- revise an existing generation prompt
- create a reusable generator instruction for any subject

This policy is independent of subject and product.

## 2. PRE-GENERATION HISTORY LOAD — REQUIRED
Before a new generation prompt permits question creation, it must require a HISTORY LOAD stage.

Authoritative history sources, in order:
1. previously USER-APPROVED final problem sets in Google Drive
2. ARC verified item bank / approved output index
3. registered similarity/fingerprint ledger when available
4. prior approved artifacts supplied directly by the user

The prompt must instruct the generator to build an EXCLUSION REGISTRY from prior approved items before writing new items.

If the runtime cannot access the required prior-history source, it must not pretend to have performed the dedup check. It must mark:
DUP_HISTORY_ACCESS=UNAVAILABLE
and request/import the previous approved set or registry before claiming DUPLICATE_GATE=PASS.

## 3. WHAT COUNTS AS A DUPLICATE
Exact wording duplication is only the easiest case.

Treat an item as duplicate or materially redundant when one or more of the following substantially matches a prior approved item:
- same stem/question intent
- same source segment + same judgment target
- same comparison axis + same conclusion
- same answer-bearing evidence + same reasoning path
- same data/visual structure + same inference task
- same correct-answer logic with only superficial number/name/order changes
- same distractor architecture with only cosmetic rewriting
- paraphrase that preserves essentially the same solve path

A shared passage, poem, historical event, concept, experiment, graph domain, or curriculum point is NOT automatically a duplicate if the new item tests a genuinely different reasoning axis.

## 4. DUPLICATION GATE — REQUIRED BEFORE FINAL OUTPUT
Every problem-generation prompt must require:
1. compare every newly generated item against the EXCLUSION REGISTRY
2. run exact/near-text similarity when tooling exists
3. run semantic duplication review regardless of tooling
4. replace or redesign any duplicate/redundant item
5. rerun the check after replacement

Required status fields:
DUP_HISTORY_ACCESS
DUPLICATE_GATE
EXACT_DUPLICATE_COUNT
SEMANTIC_DUPLICATE_COUNT
REPLACED_ITEM_IDS[]
PRIOR_SET_REFERENCES[]

Final candidate set requires:
DUPLICATE_GATE=PASS
EXACT_DUPLICATE_COUNT=0
SEMANTIC_DUPLICATE_COUNT=0

## 5. PROMPT AUTHORING RULE
When ChatGPT writes a problem-generation prompt for the user, the prompt itself must include:
- prior approved set loading
- exclusion registry construction
- duplication definitions
- post-generation dedup audit
- replacement/recheck loop
- final user approval gate
- post-approval Google Drive save
- history/index update after save

Do not rely on the model remembering previous questions implicitly.

## 6. USER FINAL APPROVAL GATE — ABSOLUTE
After the candidate problem set and its QA are complete:
1. present the completed candidate to the user
2. clearly state that it is READY_FOR_USER_APPROVAL
3. wait for explicit user approval

Examples of sufficient approval:
- "확인"
- "좋아 저장해"
- "최종본으로 저장"
- other unambiguous approval of that exact result

Do NOT upload/save the final problem set to Google Drive before explicit approval.

Status before approval:
FINAL_USER_APPROVAL=PENDING
DRIVE_SAVE=BLOCKED

After explicit approval:
FINAL_USER_APPROVAL=PASS
DRIVE_SAVE=ALLOWED

A general instruction to run automatically is not a substitute for approval of a specific final problem set.

## 7. POST-APPROVAL DRIVE SAVE
After approval:
- save the exact approved final artifact to the canonical Google Drive location
- never silently change content between approval and save
- preserve version/BATCH_ID
- save or update the dedup history metadata/index
- record enough fingerprints/metadata so future prompts can exclude this set

At minimum record:
BATCH_ID
SUBJECT
PRODUCT
SCOPE
APPROVED_AT
DRIVE_FILE_ID or canonical file reference
ITEM_IDS[]
ITEM_COUNT
source/passage identifiers where permitted
reasoning-axis / concept tags
similarity fingerprints when executable tooling exists

## 8. FUTURE PROMPT BEHAVIOR
Every later problem-generation prompt must treat all previously user-approved and Drive-saved final sets as an exclusion corpus.

The goal is not merely "do not copy wording".
The goal is:
NEW SET = no exact duplicates + no materially redundant solve paths.

## 9. STORAGE FAILURE
If the final result is approved but Drive write is unavailable:
- do not claim it was saved
- preserve the approved artifact unchanged
- report DRIVE_SAVE=HOLD
- retry only when an authorized Drive write path is available

## 10. CONFLICT PRIORITY
For problem-generation artifacts, this policy overrides any zero-touch rule that would otherwise auto-save a generated final artifact without the user's approval.

Generation, QA, handoff, typesetting, and draft rendering may continue automatically.
Persistent Google Drive save of the final problem set must wait for user approval.

END ARC PROMPT DEDUP + USER APPROVAL POLICY V1.0
