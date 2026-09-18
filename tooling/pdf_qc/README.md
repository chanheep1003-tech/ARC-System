# ARC PDF / X-mark QC

## PDF preflight

```bash
python tooling/pdf_qc/pdf_preflight.py output.pdf \
  --report tooling/results/preflight.json \
  --render-dir tooling/results/rendered
```

PyMuPDF performs coordinate-level screening. If `pdftoppm` is installed, it is preferred for raster verification; otherwise PyMuPDF renders pages.

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
