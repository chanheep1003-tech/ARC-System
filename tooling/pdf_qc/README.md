# ARC PDF / X-mark QC

## PDF preflight

```bash
python tooling/pdf_qc/pdf_preflight.py output.pdf \
  --product ARC_CORE \
  --report tooling/results/preflight.json \
  --render-dir tooling/results/rendered
```

PyMuPDF performs coordinate-level screening plus product-aware checks. ARC CORE adds one-column flow detection, sparse-page/occupancy analysis, typography metrics, heading-orphan screening, raw-markup and production-metadata leak checks. If `pdftoppm` is installed, it is preferred for raster verification; otherwise PyMuPDF renders pages.

`autofix_controller.py` converts eligible preflight findings into a bounded,
allowlisted Typesetter-profile repair plan. It never mutates locked content and
returns content/count/source defects upstream. A repeated finding fingerprint
or more than two attempts becomes HOLD.

Behavioral smoke test:

```bash
python tooling/pdf_qc/test_preflight_smoke.py
```

## Social C-part X detection

```bash
python tooling/pdf_qc/xmark_detect.py c_worksheet.pdf \
  --report tooling/results/xmarks.json
```

Detection priority:

1. PDF annotation/ink objects
2. vector diagonal crossings from `get_drawings()`
3. OpenCV raster fallback

High-confidence annotation/vector marks become `AUTO_EXCLUDE`. Raster/ambiguous marks become `HUMAN_CHECK`; they must not be silently treated as in-scope.
