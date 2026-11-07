# ARC external tools

Read `ops/ARC_EXTERNAL_TOOLS_V1.0.md` for setup, task routing, exact installation limits and the eight upstream sources. `tools.lock.json` pins upstream revisions; `node/` pins the CLI dependency graph. Runtime packages, native links, settings and private data stay under ignored `.arc-tools/`.

```bash
python tooling/external/arc_external.py install all
python tooling/external/arc_external.py doctor
python tooling/external/arc_external.py route source
python -m unittest discover -s tooling/external -p 'test_*.py' -v
```

No install status grants content approval. Native hooks, live model calls, automatic capture, GPU model modification and production activation are not implied by package installation.
