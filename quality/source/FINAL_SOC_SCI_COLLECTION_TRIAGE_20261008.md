# ARC 2026-2 FINAL — SOC/SCI candidate triage, 2026-10-08

Status: `PROVISIONAL_REMAINDER / NO_DIRECT_USE_APPROVAL`  
Scope: user's temporary lock = semester content minus actual midterm content. This is a candidate filter, not final school announcement.  
Product difficulty: ARC FINAL structural mean `3.00–3.50` (planning center `3.25`), 5-level D1–D5; item-level D12/D3/D45 shares and time load must additionally pass subject-specific verification. This does **not** apply to ARC N°.

## Canonical working data
- Prior curated data: `ARC_SOC_CURATED_20261004.jsonl`, `ARC_SCI_CURATED_20261004.jsonl` (Google Drive per-subject collection folders).
- Prior review: `ARC_자료검토결과_20261004.md` (Google Drive).
- New filterable, 617-row triage workbook: [ARC_FINAL_SOC_SCI_TRIAGE_20261008.xlsx](https://docs.google.com/spreadsheets/d/1sz4p311J07S1dq3eNnaOqPEggWdILdun/edit) (Drive > N제 시스템).
- Original source PDFs remain in their current folders. No move, duplicate-content approval, deletion, or source rewrite was performed.

## Global gates
- All 617 entries have `independent_solution_check=NOT_PERFORMED`.
- All are `eligible_for_current_exam=false`. Source+answer linkage **does not** mean verified item quality.
- Preserve source provenance. Do not treat official examples or commercial publisher items as actual past examinations for the 70%-past-exam generation policy.
- For high-school year 2/3 material, reject prerequisites beyond current 2022 revised grade-1 Integrated Science 2 / Integrated Society 2 unless independently confirmed in school source.
- No copying prior exam passages/options. Reconstruct question forms using in-scope evidence.

## Count reconciliation (617)
| Classification | SOC | SCI | Combined |
| --- | ---: | ---: | ---: |
| All records | 420 | 197 | 617 |
| Provisional final remainder | 247 | 121 | 368 |
| Recorded midterm overlap | 113 | 65 | 178 |
| Boundary / scope review | 52 | 7 | 59 |
| Mixed subject-1 hold | 8 | 4 | 12 |
| In remainder: source+official key linked, independent QA pending | 220 | 81 | 301 |
| In remainder: evidence repair needed | 21 | 30 | 51 |
| In remainder: advanced prerequisites hold | 6 | 10 | 16 |
| Previously tagged high-priority remainder | 241 | 111 | 352 |

The 301 are **QA queue**, not approved questions. Reconcile formulas: 301+51+16=368. Independent-solve PASS = 0, final direct-use approved = 0.

## SOC — conceptual triage
- Candidate-rich residual areas: rational-choice/economic actors (59 concept tag references), spatial/social inequality (42), international peace efforts (38), trade/sustainability (35), finance (29), energy/sustainable development (29), market capitalism (19), Korean peninsula/world peace (10).
- Weakest gap: future society/individual life (1 candidate reference).
- Boundary: human rights, justice classifications, liberal/communitarian positions; avoid silently returning midterm A/B/C scope.
- Previously collected Gaya 2024 final social actual items 14,15,17,19–22,24,25 provide provisional inequality structures; answer-key visual matches need independent solution.
- Dongbuk 2025-2 actual final original `1jNfzCL_FGP9nFdqmQOntzYs9MxfvUGt4` is tracked in FINAL collection candidates **separately** from curated 420; first-pass source mapping from readable item stems:
  - Q3–5: international society / peninsula history and conflicts — remainder reference.
  - Q6–7: peace thinker comparative application — remainder reference.
  - Q8–14: energy sources / international agreements / data-map analysis — remainder reference.
  - Q15–17: minority/juvenile labor rights — midterm overlap/boundary hold.
  - Q18–22: capitalism, economics, rational choice — remainder reference, high priority for direct Dongbuk task-family extraction.
  - Q1–2 and essays: require source layout/index validation before classification.
- Concept / item-tag links are provisional; not a release-grade scope or answer check.

## SCI — conceptual triage
- Candidate-rich residual areas: acid-base/neutralization (40 concept-tag refs), ecosystem equilibrium (24), efficiency/energy (35), energy absorption/release (9), solar energy (6), big data (7), technology advancement limits (4), infection diagnostic (3), ethics/SSI (1).
- Gap: **actual school** technology-development/limits questions scarcely represented; original 10/04 inventory noted no school past-exam representation for this concept. Collect new school sources and do not mislabel generic official examples.
- Midterm-excluded: geology/evolution/biodiversity, oxidation-reduction, recorded climate/environment change, induction/generation. Cross-unit and ecosystem-vs-biodiversity boundary candidates require original source check.
- Gaya 2024 SCI final exam Q1–3 energy, Q6–10 neutralization, Q11–15 ecosystem, essay 2 neutralization: useful structure references, not yet independent-solved.
- Dongbuk 2025-2 actual final original `1_N_CxoACXQl6NIbNBWYv_93TqawqLbBU` is tracked in FINAL collection candidates **separately** from curated 197; first-pass source mapping from readable item stems:
  - Q3–6: science technology/question formulation — provisional future-science.
  - Q7–12: acid-base and neutralization experiments, solution mixture quantities — remainder, high-priority school form.
  - Q13: biodiversity/conservation — recorded midterm overlap, temporary hold.
  - Q14–17: ecosystem interaction, food chain, energy flow/populations — remainder; cross-check biodiversity distinction.
  - Q18: infectious disease diagnostics — remainder.
  - Q19–21: solar energy processes/transformation — remainder.
  - Q22–24: technology/SSI/research ethics — remainder.
  - Q1–2 and essays: require source layout/index validation before classification.
- Visualization fidelity of numerical graphs/diagrams remains unverified in this review. Do not claim QA PASS.

## Recommended next QA queue
1. SCI: Dongbuk 2025 final Q7–12 and Gaya 2024 Q6–10; compare neutralization experimental variables / quantitative inference. Check all diagrams and keys independently.
2. SOC: Dongbuk 2025 final Q18–22 plus existing economic/finance school-exam gaps; select higher discriminating question forms rather than forced verbosity.
3. SCI: ecosystem Q14–17, solar Q19–21, infection/SSI Q18/Q22–24; fill gaps with new verified source.
4. SOC: data/map energy / international peace Q3–14; verify school-specific terminology and remove overlaps.
5. Independently solve 301 keyed shortlist rows, validate diagrams/source scope before moving any row to `eligible_for_current_exam=true`.

No generator/type-setting engine structure was modified. Any ARC FINAL release still requires verified subject-specific anchor, provenance, item QA, PDF E2E, and user approval.
