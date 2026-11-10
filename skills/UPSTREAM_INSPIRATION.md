# Upstream inspiration and adaptation notes

ARC skills are original project-specific adaptations. External projects were used as design references; their text/code is not vendored here.

- GitHub `awesome-copilot`: Agent Skills structure, `eval-driven-dev`, `agent-skill-stack`, document-to-markdown workflow.
- NousResearch `hermes-agent`: source ledger / grounded-citation concepts.
- jwynia `agent-skills`: generation and fact-check separation.
- GarethManning `education-agent-skills`: criterion-referenced rubric and calibration-note concepts.
- mcroitor `agent-skills-library`: quiz/exam coverage and bank workflow concepts.
- memtomem `agent-skills-public`: HWP/HWPX and structure-preserving document parsing concepts.
- OpenDataLab `MinerU-Ecosystem`: multi-format structured extraction concepts.
- K-Dense-AI `scientific-agent-skills`: truthful scientific visualization principles.
- Liuxiangjian-ai `cet-skill`: plausible distractor construction and best-answer discrimination ideas.
- blader `humanizer` and related humanize-writing skills: named-pattern editorial audit concepts, adapted only to exam-item naturalness.
- Firecrawl `web-agent` deep-research: multi-angle search and source triangulation concepts.

- `jelaludo/claude-skill-typography`: typography-token, weight/line-height/spacing audit concepts for print/readability QA. REFERENCE_ONLY; no upstream code/text copied; license not established during intake.
- `thedanielmay/visual-review-skill`: render-first visual QA, fixed-height overflow detection, clipping/density review concepts. REFERENCE_ONLY; no upstream code/text copied; license not established during intake.

Before vendoring any upstream script or code in the future, verify the upstream license and record the exact version/commit separately.
