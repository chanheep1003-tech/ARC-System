# ARC handoff preflight

Run before Typesetter acceptance:

```bash
python tooling/handoff/handoff_preflight.py ARC_HANDOFF_CORE_SOC_<BATCH>_READY.md
```

The gate rejects stale rulesets, handoff-local layout commands, CORE two-column
directives, PDF-master/font/CSS/PageTemplate pins, student-facing internal IDs,
and A/B/C part headings that are not level-1 major boundaries.

Exit code `1` means the handoff must return to Generator. The tool does not
rewrite locked student content.
