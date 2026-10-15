#!/usr/bin/env python3
"""ARC CORE BOOK builder (profile core_profile=BOOK, all subjects).

parts/*.html (sorted) + ARC_CORE_BOOK_style_v0.4.css -> A4 PDF.
Gates run here: gray-only color source check, rasterized grayscale check,
two-pass TOC page numbers ({{PG:KEY}}), and PDF preflight with --core-profile BOOK.
This tool contains no subject content; content lives in the handoff/parts only.

usage:
  python tooling/core_book/build_book.py --parts DIR --out OUT.pdf \
      --running-left "공통국어2 · 중세 국어" --running-right "동북고 1학년 2학기 기말" \
      [--vars vars.json] [--toc-markers markers.json] [--title TITLE] [--workdir DIR]
vars.json:        {"PLACEHOLDER": "<html or text>"}   replaces {{PLACEHOLDER}}
toc-markers.json: {"KEY": "unique text printed on the first page of that unit", ...}
                  {{PG:KEY}} is replaced by the first page (>= toc_after_page) that contains it.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "templates/core/book/ARC_CORE_BOOK_style_v0.4.css"
RENDER_JS = Path(__file__).with_name("render_pdf.js")
PREFLIGHT = ROOT / "tooling/pdf_qc/pdf_preflight.py"
HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def non_gray_colors(text: str) -> list[str]:
    bad = []
    for c in HEX_RE.findall(text):
        c = c.lower()
        gray = (len(c) == 3 and c[0] == c[1] == c[2]) or (len(c) == 6 and c[0:2] == c[2:4] == c[4:6])
        if not gray:
            bad.append("#" + c)
    return sorted(set(bad))


def assemble(parts: list[Path], css: str, variables: dict[str, str], pages: dict[str, int] | None, title: str) -> str:
    body = "\n".join(p.read_text(encoding="utf-8") for p in parts)
    for key, value in variables.items():
        body = body.replace("{{" + key + "}}", value)
    body = re.sub(r"\{\{PG:([A-Za-z0-9_-]+)\}\}", lambda m: str((pages or {}).get(m.group(1), "00")), body)
    left = re.findall(r"\{\{([^}]+)\}\}", body)
    if left:
        raise SystemExit(f"unresolved placeholders: {sorted(set(left))}")
    return (
        f'<!doctype html><html lang="ko" data-product="arc-core" data-core-profile="BOOK"><head><meta charset="utf-8">'
        f"<title>{title}</title><style>{css}\ntd.ctr,th.ctr{{text-align:center}}</style></head><body class='core-flow'>{body}</body></html>"
    )


def render(html: str, workdir: Path, out: Path) -> None:
    doc = workdir / "doc.html"
    doc.write_text(html, encoding="utf-8")
    proc = subprocess.run(["node", str(RENDER_JS), str(doc), str(out)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"render failed ({proc.returncode}): {proc.stderr[-600:]}")


def page_texts(pdf: Path) -> list[str]:
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.check_output(["pdfinfo", str(pdf)], text=True)).group(1))
    return [subprocess.check_output(["pdftotext", "-f", str(i), "-l", str(i), "-layout", str(pdf), "-"], text=True) for i in range(1, n + 1)]


def page_map(pdf: Path, markers: dict[str, str], toc_after: int) -> tuple[int, dict[str, int]]:
    texts = page_texts(pdf)
    result: dict[str, int] = {}
    for key, marker in markers.items():
        for i, text in enumerate(texts, 1):
            if i > toc_after and marker in text:
                result[key] = i
                break
    return len(texts), result


def grayscale_check(pdf: Path, workdir: Path, tolerance: int = 8) -> dict:
    from PIL import Image, ImageChops  # local import: only needed for this gate

    shutil.rmtree(workdir / "gray", ignore_errors=True)
    (workdir / "gray").mkdir(parents=True)
    subprocess.run(["pdftoppm", "-r", "40", "-png", str(pdf), str(workdir / "gray/p")], check=True)
    worst = 0
    for img in sorted((workdir / "gray").glob("p-*.png")):
        r, g, b = Image.open(img).convert("RGB").split()
        for x, y in ((r, g), (g, b)):
            worst = max(worst, ImageChops.difference(x, y).getextrema()[1])
    return {"status": "PASS" if worst <= tolerance else "FAIL", "max_channel_diff": worst}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--running-left", default="")
    ap.add_argument("--running-right", default="")
    ap.add_argument("--title", default="ARC CORE")
    ap.add_argument("--vars", type=Path)
    ap.add_argument("--toc-markers", type=Path)
    ap.add_argument("--toc-after-page", type=int, default=5)
    ap.add_argument("--workdir", type=Path, default=Path("book_build"))
    ap.add_argument("--no-preflight", action="store_true")
    args = ap.parse_args()

    args.workdir.mkdir(parents=True, exist_ok=True)
    parts = sorted(args.parts.glob("*.html"))
    if not parts:
        raise SystemExit("no parts/*.html found")
    css = CSS.read_text(encoding="utf-8").replace("{{RUNNING_LEFT}}", args.running_left).replace("{{RUNNING_RIGHT}}", args.running_right)
    variables = json.loads(args.vars.read_text(encoding="utf-8")) if args.vars else {}
    markers = json.loads(args.toc_markers.read_text(encoding="utf-8")) if args.toc_markers else {}

    html0 = assemble(parts, css, variables, None, args.title)
    bad = non_gray_colors(html0)
    report: dict = {"non_gray_source_colors": bad}
    if bad:
        print("FAIL non-gray colors in source:", bad)
        return 1

    render(html0, args.workdir, args.out)
    pages = None
    if markers:
        n, pm = page_map(args.out, markers, args.toc_after_page)
        for _ in range(3):
            render(assemble(parts, css, variables, pm, args.title), args.workdir, args.out)
            n, pm2 = page_map(args.out, markers, args.toc_after_page)
            if pm2 == pm:
                break
            pm = pm2
        pages = pm
        missing = sorted(set(markers) - set(pm))
        report["toc_pages"] = pm
        report["toc_missing"] = missing
        if missing:
            print("FAIL toc markers not found:", missing)
            return 1
    report["gray"] = grayscale_check(args.out, args.workdir)
    if not args.no_preflight:
        pf = subprocess.run(
            [sys.executable, str(PREFLIGHT), str(args.out), "--product", "ARC_CORE", "--core-profile", "BOOK",
             "--report", str(args.workdir / "preflight.json")],
            capture_output=True, text=True,
        )
        data = json.loads((args.workdir / "preflight.json").read_text(encoding="utf-8"))
        report["preflight"] = {"status": data["status"], "fail": data["fail_count"], "warn": data["warn_count"], "pages": data["page_count"]}
    (args.workdir / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    ok = report["gray"]["status"] == "PASS" and report.get("preflight", {}).get("fail", 0) == 0
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
