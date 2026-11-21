#!/usr/bin/env python3
"""KOR orthography set typesetting regression (gold exemplar KOR_ORTHO_PILOT_20261121).

Covers what the renderer needed for the user-approved orthography format
(quality/korean/ARC_KOR_SCHOOL_HYBRID_FORMAT_V1.1.md):
- a writer-authored explanation passage shared by two items (bundle set, material kind GRAMMAR_EXPLANATION)
- KOR material without that kind stays forbidden (school raw text must come from the registry)
- '<보기 1>' / '<보기 2>' lines print as two labelled boxes
- <u>…</u> underlines, '∘' bullets (font alias), no literal tags on the page"""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[2]
PILOT = ROOT / "quality/production/KOR_ORTHO_PILOT_20261121"


def load_module(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    preview = load_module("arc_draft_preview", "tooling/production/draft_preview.py")
    pipeline = load_module("arc_production_pipeline_t", "tooling/production/production_pipeline.py")
    renderer = load_module("arc_kor_renderer_t", "tooling/typeset/kor_renderer.py")

    # split_views: school-style numbered views become separate boxes
    groups = renderer.split_views(["<보기 1> 조건", "Ⓐ 하나", "<보기 2> ㉠ 냇가"], "<보 기>")
    assert [g[0] for g in groups] == ["<보기 1>", "<보기 2>"] and groups[0][1] == ["조건", "Ⓐ 하나"]
    assert renderer.split_views(["민지: 안녕"], "<보 기>") == [("<보 기>", ["민지: 안녕"])]

    # KOR material: allowed only for the authored explanation kind
    raw = yaml.safe_load((PILOT / "items.yaml").read_text(encoding="utf-8"))
    work = copy.deepcopy(raw["sets"][0]["works"][0])
    assert pipeline.material_work(work, "KOR", "t")["kind"] == "GRAMMAR_EXPLANATION"
    work["material"].pop("kind")
    try:
        pipeline.material_work(work, "KOR", "t")
        raise AssertionError("KOR material without GRAMMAR_EXPLANATION must be refused")
    except pipeline.PipelineError as exc:
        assert "MATERIAL_FORBIDDEN_FOR_SUBJECT" in str(exc)

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out"
        report = preview.run(PILOT, out)
        assert report["typeset"] == "PASS" and report["pdf_qc"] == "PASS", json.dumps(report, ensure_ascii=False)[:400]
        pdf = next(out.glob("*_DRAFT_PREVIEW.pdf"))
        text = "".join(page.get_text() for page in fitz.open(pdf)).replace("\xa0", " ")
        assert text.count("맞춤법 제1항은") == 1, "shared passage must print once"
        assert "[1~2]" in text
        assert "<보기 1>" in text and "<보기 2>" in text
        assert "<u>" not in text and "</u>" not in text
        assert "◦" in text or "∘" in text
    print("KOR grammar set typesetting regression PASS (shared explanation set, split views, underline, bullet alias)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
