# ARC CORE EDITORIAL ARCHITECTURE V2.0
VERSION: 2.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC CORE macro-structure, information hierarchy, anti-listing architecture

## 0. PURPOSE
ARC CORE must read like a coherent school reference book, not a sequence of accurate but disconnected note blocks.
The unit of organization is not the isolated concept card. The primary unit is the chapter/cluster with one dominant question, one explanatory backbone, and a controlled set of supporting details.

CORE quality is therefore judged at two levels:
1. MICRO: each fact/concept is accurate and useful.
2. MACRO: the reader can see why the facts belong together and what structure should be remembered.

A manuscript that is factually strong but reads as repeated lists, tables, warnings, and summaries is EDITORIAL_REVISE.

## 1. CHAPTER BACKBONE — REQUIRED
Before student-facing prose is written, create internal chapter architecture:

CENTRAL_QUESTION
CHAPTER_THESIS
DOMINANT_ORGANIZATION
BACKBONE_NODES[]
ESSENTIAL_RELATIONS[]
SUPPORTING_DETAILS[]
END_SYNTHESIS_MODE

These are internal metadata and must not appear as system labels in the student PDF.

CENTRAL_QUESTION:
- one question the chapter answers
- should organize multiple concepts, not merely restate a heading

CHAPTER_THESIS:
- 1–3 sentences answering the central question
- gives the reader a mental model before detail

DOMINANT_ORGANIZATION — choose one primary mode:
- CHRONOLOGICAL
- CAUSAL
- COMPARATIVE
- PROBLEM_SOLUTION
- SYSTEM_STRUCTURE
- TEXT_FLOW
- MECHANISM_CONDITION

A chapter may use secondary modes, but one mode must dominate so the chapter does not become a mixed list.

BACKBONE_NODES:
- usually 3–6 major moves
- each node is a meaningful stage/idea, not every named concept

## 2. INFORMATION HIERARCHY
Classify student-facing content internally:

TIER_1_BACKBONE
- necessary to understand the chapter as a whole
- receives full prose and visual priority

TIER_2_ESSENTIAL_DETAIL
- dates, terms, actors, conditions, evidence needed to apply Tier 1
- embedded near the relevant backbone node

TIER_3_SUPPORTING_EVIDENCE
- examples, quotations, statistics, secondary illustrations
- included only when they clarify or substantiate
- not allowed to interrupt the backbone repeatedly

Do not present Tier 1, 2, and 3 with equal visual weight.

## 3. NARRATIVE FIRST
Default student-facing sequence:

ORIENTATION
→ EXPLANATORY FLOW
→ SELECTIVE COMPARISON / EVIDENCE
→ SYNTHESIS

ORIENTATION:
- 3–6 sentences
- states what problem/question the chapter is about
- may identify the main dividing line or causal relationship
- must not sound like a teacher-prediction script

EXPLANATORY FLOW:
- continuous prose is the default
- details are introduced where they become meaningful
- facts should answer why, how, when, under what condition, or how they connect

SELECTIVE COMPARISON / EVIDENCE:
- only when comparison/evidence performs real cognitive work

SYNTHESIS:
- compresses the chapter into one memorable model
- must transform, not merely repeat, the preceding lists

## 4. ANTI-LISTING RULE
The following pattern is prohibited as the dominant chapter structure:

concept
→ 핵심 정리
→ 주의할 점
→ comparison table
→ time axis
→ problem application
→ diagram
→ same facts repeated again

A chapter may use some of these elements, but not as a routine checklist.

Hard editorial triggers:
- three or more consecutive sections dominated by bullet lists with little connective prose
- the same fact appears in prose + table + summary + diagram without a new function
- chapter ending is mainly a second inventory of names/dates already listed
- every subtopic ends with the same labeled block
- a reader can remove paragraph prose and lose little because the document is mostly cards

If triggered:
ARCHITECTURE_REVISE_REQUIRED=true

## 5. REDUNDANCY BUDGET
A fact may normally appear:
- once in explanatory prose
- once more in a transformed synthesis/comparison if that second appearance changes its function

Third repetition requires explicit pedagogical justification.

Allowed transformation examples:
- prose explanation → timeline that reveals sequence
- prose explanation → comparison table that reveals contrasting criteria
- several details → causal diagram that reveals one mechanism

Not allowed:
- prose → identical bullet recap → identical card → identical end summary

## 6. BLOCK BUDGET
Auxiliary blocks are scarce editorial tools.

Per chapter, use only what is useful:
- comparison table
- warning/confusion note
- process diagram
- timeline
- source/evidence box
- end synthesis

Do not force all of them.

Soft target for ordinary CORE pages:
- continuous prose should visually dominate
- roughly 65–75% explanatory text
- roughly 15–20% functional table/diagram
- roughly 5–15% warning/summary/support blocks

These are diagnostics, not fixed quotas. Content need overrides percentages.

## 7. CHAPTER ENDING
Choose ONE main synthesis mode by default:

A. INTEGRATED_PARAGRAPH
5–8 lines connecting the chapter's main relations.

B. SINGLE_MODEL
one timeline, causal chain, comparison matrix, or structure diagram.

C. DECISION_FRAME
a short set of criteria the student can use to distinguish similar cases.

Do not automatically combine timeline + summary bullets + exam types + diagram at every chapter ending.

## 8. LANGUAGE / VOICE
Use reference-book prose, not tutoring chatter.

Avoid repeated meta-address:
- 외워 두세요
- 반드시 기억하세요
- 시험에 나옵니다
- 이 부분이 핵심입니다
- 여기서 함정은
- 문제에서 자주

Such phrases may appear selectively when supported, but must not organize the book.

Prefer:
- direct explanation
- causal linkage
- contrastive sentences
- evidence-led transitions
- concise synthesis

Avoid inflated certainty about school exam frequency unless current school evidence supports it.

## 9. HISTORY PROFILE
Default architecture is cluster-first, not event-card-first.

Typical CENTRAL_QUESTION examples:
- 왜 일제의 통치 방식은 세 차례 달라졌는가?
- 3·1 운동 이후 민족 운동은 왜 여러 노선으로 갈라졌고 다시 통합을 시도했는가?
- 광복 직전 여러 독립운동 세력은 어떤 방식으로 통합을 모색했는가?

Preferred backbone:
context/trigger
→ structural change
→ actors/policies
→ consequence
→ link to next phase

Dates and organizations should be embedded into this flow.

Use tables for genuine cross-confusion:
- similar organizations
- overlapping periods
- location/person/organization mapping
- policy comparison

Do not turn every event into a separate mini-card.

## 10. SOCIAL PROFILE
Prefer conceptual problem architecture.

Typical CENTRAL_QUESTION examples:
- 인권은 어떤 과정을 거쳐 자유권에서 사회권·연대권으로 확장되었는가?
- 기본권은 왜 보장되면서도 제한될 수 있는가?
- 칸트와 베카리아는 왜 같은 형벌 문제를 전혀 다른 근거로 판단하는가?
- 세계화는 왜 통합과 격차를 동시에 만든는가?

Structure concepts around the question, then place definitions, cases, institutions, and comparison points inside that structure.

Avoid glossary-like accumulation of:
definition → feature table → example list → trap table.

## 11. SCIENCE PROFILE
Prefer mechanism-condition architecture.

Start from:
- what changes
- what causes the change
- what conditions alter the result
- what evidence/graph/experiment shows it

Use formulas or tables only when they reveal a relation.
Do not split one mechanism into many isolated definition boxes.

## 12. KOREAN PROFILE
Prefer work/text-flow architecture.

work as whole
→ important movement/scene/voice
→ textual evidence
→ interpretive relation
→ comparison where useful

Do not fragment a work into repeated theme/emotion/device cards.

## 13. AI PROFILE
Prefer system/process architecture.

input/state
→ rule/process
→ output
→ condition/exception
→ comparison

Avoid definition inventories when sequence or dependency is the real concept.

## 14. INTERNAL EDITORIAL PASS
Before CONTENT_LOCK, perform a macro pass independent from fact QA.

Required:
CHAPTER_BACKBONE_PRESENT = PASS
DOMINANT_ORGANIZATION_CLEAR = PASS
INFORMATION_HIERARCHY = PASS
ANTI_LISTING = PASS
REDUNDANCY_BUDGET = PASS
SYNTHESIS_TRANSFORMS = PASS
PROSE_DOMINANCE = PASS
CHAPTER_TRANSITIONS = PASS

If two or more fail:
CORE_EDITORIAL_ARCHITECTURE = REVISE

If ANTI_LISTING or CHAPTER_BACKBONE_PRESENT fails:
CORE_EDITORIAL_ARCHITECTURE = FAIL

## 15. REPAIR ORDER
When a manuscript feels cluttered or AI-like, do not first rewrite sentence style.

Repair in this order:
1. identify the chapter question
2. merge concepts into 3–6 backbone nodes
3. remove repeated recaps
4. choose one dominant synthesis
5. demote supporting evidence
6. reduce auxiliary boxes/tables
7. then smooth sentence rhythm

Macro repair precedes micro wording repair.

END ARC CORE EDITORIAL ARCHITECTURE V2.0
