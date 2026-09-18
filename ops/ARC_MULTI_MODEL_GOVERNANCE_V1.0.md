# ARC MULTI-MODEL GOVERNANCE V1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

## 0. ROLES

ARC uses multiple independent generators but one system maintainer.

GENERATOR_GPT
- generate ARC items/sets
- run the active ARC QA required for its batch
- create visuals/PDFs when requested
- save new artifacts to Drive
- GitHub is READ-ONLY during production

GENERATOR_CLAUDE
- same production authority as GENERATOR_GPT
- generate independent ARC items/sets
- run the active ARC QA required for its batch
- create visuals/PDFs when requested
- save new artifacts to Drive
- GitHub is READ-ONLY during production

SYSTEM_MAINTAINER
- owner: ChatGPT interactive maintenance session
- exclusive authority for ARC engine/rules/code/template/manifest updates
- reviews GPT/Claude production results
- diagnoses recurring defects
- modifies GitHub dev
- performs regression/consistency checks available in the current host
- promotes stable changes according to release policy

The user remains the final acceptance authority for released study products.

## 1. SINGLE-WRITER RULE

Only SYSTEM_MAINTAINER may modify:
- SYSTEM_MANIFEST.yaml
- engine/**
- subjects/**
- quality/**
- templates/**
- tooling/**
- skills/**
- mcp/**
- ops/** except generator-produced runtime logs

Generators must never patch the rules that govern their own batch.

This prevents GPT and Claude from racing to rewrite ARC policy.

## 2. SHARED SOURCE OF TRUTH

All generators read the same canonical sources:
- GitHub latest approved dev rules
- Google Drive current textbooks/worksheets/school materials
- Google Drive verified banks and production history

No GPT-specific MASTER.
No Claude-specific MASTER.
No duplicated rule tree.

## 3. APPEND-ONLY PRODUCTION

Generator production is append-only.

Never overwrite an existing batch, QA report, PDF, or BANK artifact.
Every batch uses a unique BATCH_ID.

Required:
GENERATOR=GPT | CLAUDE
BATCH_ID
SUBJECT
SCOPE
CREATED_AT
SOURCE_SET
ITEM_COUNT
QA_STATUS
PDF_STATUS
ARC_RULESET_VERSION

Recommended IDs:
ARC-GPT-YYYYMMDD-SUBJECT-NN
ARC-CLAUDE-YYYYMMDD-SUBJECT-NN

## 4. COLLISION AVOIDANCE

Before generation:
1. inspect fresh batch metadata for the requested subject/scope
2. reserve a unique BATCH_ID
3. if the user explicitly wants an alternate independent set, generation is allowed even when the same scope already has another generator's batch
4. otherwise avoid materially equivalent duplicate work

A batch never replaces another generator's batch.

## 5. PRODUCT OWNERSHIP

A single batch has exactly one primary generator.
Do not mix authorship inside one batch unless explicitly requested.

Default:
- GPT batch stays GPT-authored
- Claude batch stays Claude-authored
- universal cross-model rewriting/regrading is disabled

Selective independent review is allowed for high-risk items only.

## 6. SYSTEM FEEDBACK CHANNEL

Generators may detect system defects but may not fix GitHub directly.

They record:
SYSTEM_FEEDBACK
- BATCH_ID
- GENERATOR
- DEFECT_CLASS = ITEM_LEVEL | SET_LEVEL | SOURCE | VISUAL | PDF_LAYOUT | SYSTEM_RULE
- OBSERVED_BEHAVIOR
- REPRODUCTION_EVIDENCE
- PROPOSED_DIRECTION
- SEVERITY = LOW | MEDIUM | HIGH | BLOCKER

SYSTEM_MAINTAINER decides whether the observation warrants a rule/code/template change.

## 7. CHANGE CONTROL

System changes follow:
production evidence
→ maintainer diagnosis
→ dev patch
→ regression/consistency check
→ next production observation
→ main promotion only when stable

Generators always reload latest manifest before a new production session.

If rules change while a batch is in progress:
- finish the current batch using its recorded ARC_RULESET_VERSION
- do not silently switch rules mid-batch
- new batches use the newer ruleset

## 8. DRIVE WRITE POLICY

Generators:
- create new artifacts only
- do not rename/move/delete another generator's artifacts unless the user explicitly requests maintenance
- do not overwrite BANK/history
- use subject production folders or durable staging according to the active Drive adapter
- preserve BATCH_ID in filenames/metadata

Maintainer:
- may organize staged artifacts
- may archive superseded drafts
- may reconcile folder placement
- may update system indices

## 9. BANK POLICY

Generator output is never automatically equivalent to canonical release.

States:
DRAFT
QA_COMPLETE
BANK_CANDIDATE
HUMAN_REVIEW
FINAL_RELEASED

GPT and Claude may produce BANK_CANDIDATE.
Promotion/release follows active BANK/HUMAN_REVIEW rules.

## 10. PDF POLICY

GPT and Claude may both typeset ARC products.
Generator PDFs default to DRAFT_REVIEW.
They may not edit the PDF master or brand specification during production.

Recurring layout defects are sent through SYSTEM_FEEDBACK for maintainer correction.

## 11. CONFLICT RESOLUTION

Priority when instructions conflict:
1. explicit current user instruction
2. SYSTEM_MANIFEST
3. active subject MASTER / scope exclusions
4. active common generation and QA policies
5. generator handoff/runtime instructions
6. generator preference

A generator must stop or flag rather than invent a new rule.

## 12. RESPONSIBILITY SUMMARY

GPT + Claude:
PRODUCE

ChatGPT system maintainer:
OBSERVE → DIAGNOSE → OPTIMIZE → MODIFY CODE/RULES → VALIDATE

User:
DECIDE WHAT TO PRODUCE + ACCEPT FINAL STUDY PRODUCTS

END ARC MULTI-MODEL GOVERNANCE V1.0
