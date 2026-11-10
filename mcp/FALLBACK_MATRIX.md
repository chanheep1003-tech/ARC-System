# ARC MCP FALLBACK MATRIX

| Primary tool | Primary use | Fallback | Release rule |
|---|---|---|---|
| GitHub official MCP | repo context / engine lookup | native GitHub connector | no generation block if repo rules remain accessible |
| draw.io MCP | editable diagrams | `arc-visual-drawio-base` + SVG | visual QA required |
| ChemCP | molecule/structure rendering | `arc-visual-chem` deterministic fallback | omit asset rather than invent structure if accuracy is uncertain |
| Timeline MCP | timelines | `arc-visual-timeline` SVG fallback | dates/order must be independently checked |
| Google Drive connector | source materials | no third-party Drive MCP | ask for/upload material only if connector is unavailable and source is essential |

## Hard rules
- Fallback must not weaken Scope Lock.
- Fallback must not invent unavailable source content.
- Tool failure must not be hidden; record in RUN_LOG when it affects output.
- If a specialized chemistry or historical visual cannot be verified, prefer no asset over a plausible-looking wrong asset.
