#!/usr/bin/env python3
"""Executable ARC CORE canary: bundle -> handoff -> PDF -> preflight.

The fixture is synthetic and validates pipeline behavior, not Korean source
fidelity or model-authored content quality.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import fitz
import yaml


ROOT = Path(__file__).resolve().parents[2]
A4_W = 595.276
A4_H = 841.890


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


serializer = load_module("arc_handoff_serializer", ROOT / "tooling/handoff/handoff_serializer.py")
handoff_gate = load_module("arc_handoff_preflight", ROOT / "tooling/handoff/handoff_preflight.py")
pdf_gate = load_module("arc_pdf_preflight", ROOT / "tooling/pdf_qc/pdf_preflight.py")
autofix = load_module("arc_pdf_autofix", ROOT / "tooling/pdf_qc/autofix_controller.py")
typesetter_gateway = load_module("arc_typesetter_gateway", ROOT / "tooling/typeset/typesetter_gateway.py")
canary_fonts = load_module("arc_canary_fonts", ROOT / "tooling/canary/canary_fonts.py")


def parse_sections(manuscript: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^#(?!#)\s+(.+?)\s*$", manuscript, re.M))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(manuscript)
        sections.append((match.group(1).strip(), manuscript[match.end() : end].strip()))
    if not sections:
        raise ValueError("canary manuscript needs level-1 major boundaries")
    return sections


def dense_body(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return "\n\n".join([normalized] * 3)


def typeset_core(manuscript: str, output: Path, profile: dict[str, Any] | None = None, subject: str = "KOR") -> dict[str, Any]:
    profile = profile or {}
    body_size = float(profile.get("body_size", 9.9))
    sections = parse_sections(manuscript)
    doc = fitz.open()
    cover = doc.new_page(width=A4_W, height=A4_H)
    canary_fonts.embed(cover)
    cover.insert_text((64, 76), "ARC SYSTEM  ·  DONGBUK HIGH SCHOOL", fontsize=10, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))
    cover.draw_line((64, 86), (A4_W - 64, 86), color=(0.0, 0.0, 0.0), width=1.0)
    cover.draw_rect(fitz.Rect(64, 112, 164, 136), color=(0.0, 0.0, 0.0), width=0.9)
    cover.insert_text((78, 128), "ARC CORE", fontsize=9.4, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))
    cover.insert_text((64, 186), "ARC CORE", fontsize=28, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))
    cover.insert_text((64, 226), f"{subject} CANARY", fontsize=18, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))
    cover.insert_text((64, 258), "Pure B&W Open Editorial Pipeline Validation", fontsize=11, fontname=canary_fonts.REGULAR_NAME, color=(0.35, 0.35, 0.35))
    cover.draw_line((64, 282), (A4_W - 64, 282), color=(0.0, 0.0, 0.0), width=0.9)
    cover.insert_text((64, 768), "Synthetic content fixture - not a study release", fontsize=9.9, fontname=canary_fonts.REGULAR_NAME, color=(0.25, 0.25, 0.25))

    for page_number, (title, body) in enumerate(sections, start=2):
        page = doc.new_page(width=A4_W, height=A4_H)
        canary_fonts.embed(page)
        page.insert_text((52, 38), f"ARC CORE  ·  {subject} CANARY", fontsize=9.0, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))
        page.draw_line((52, 46), (A4_W - 52, 46), color=(0.0, 0.0, 0.0), width=0.65)
        heading_remaining = page.insert_textbox(
            fitz.Rect(52, 68, A4_W - 52, 118),
            title,
            fontsize=16.5,
            fontname=canary_fonts.BOLD_NAME,
            lineheight=1.18,
            color=(0.0, 0.0, 0.0),
        )
        if heading_remaining < 0:
            raise RuntimeError(f"heading overflow on {title}: {heading_remaining}")
        page.draw_line((52, 118), (A4_W - 52, 118), color=(0.0, 0.0, 0.0), width=1.4)
        remaining = page.insert_textbox(
            fitz.Rect(52, 134, A4_W - 52, 768),
            dense_body(body),
            fontsize=body_size,
            fontname=canary_fonts.REGULAR_NAME,
            lineheight=1.62,
            color=(0.10, 0.10, 0.10),
            align=fitz.TEXT_ALIGN_LEFT,
        )
        if remaining < 0:
            raise RuntimeError(f"typeset overflow on {title}: {remaining}")
        page.draw_line((52, A4_H - 42), (A4_W - 52, A4_H - 42), color=(0.75, 0.75, 0.75), width=0.4)
        page.insert_text((A4_W - 68, A4_H - 28), f"{page_number:02d}", fontsize=9.0, fontname=canary_fonts.BOLD_NAME, color=(0.0, 0.0, 0.0))

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output, garbage=4, deflate=True)
    doc.close()
    with fitz.open(output) as saved:
        canary_fonts.assert_embedded_fonts(saved)
    return {"status": "PASS", "page_count": 1 + len(sections), "major_boundaries": [s[0] for s in sections]}


def run_faults(fixture: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, str]]:
    results = []
    for fault in fixture.get("fault_injection", []):
        payload = copy.deepcopy(fixture["content_bundle"])
        field = fault["field"]
        if field == "student_manuscript_suffix":
            payload["student_manuscript"] += str(fault["value"])
        else:
            payload[field] = fault["value"]
        try:
            serializer.serialize_bundle(payload, manifest)
        except serializer.SerializationError as exc:
            results.append({"id": fault["id"], "status": "BLOCKED", "message": str(exc)})
        else:
            results.append({"id": fault["id"], "status": "MISSED", "message": "serializer accepted fault"})
    return results


def run(fixture_path: Path, output_dir: Path) -> dict[str, Any]:
    fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    subject = str(fixture["content_bundle"]["subject"]).upper()
    manifest_path = ROOT / "SYSTEM_MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    filename, handoff_text = serializer.serialize_bundle(fixture["content_bundle"], manifest)
    handoff_path = output_dir / filename
    handoff_path.write_text(handoff_text, encoding="utf-8")
    handoff_result = handoff_gate.analyze(handoff_path, manifest_path)
    render_plan = typesetter_gateway.resolve_job(handoff_path, manifest_path, renderer="reportlab", archived_replay=True)

    manuscript = handoff_gate.section(handoff_text, "STUDENT MANUSCRIPT").strip()
    pdf_path = output_dir / f"{subject}_CORE_CANARY_V1.pdf"
    injected_path = output_dir / "_fault_small_font.pdf"
    injected_profile = dict(render_plan["profile"])
    injected_profile["body_size"] = 8.5
    typeset_core(manuscript, injected_path, injected_profile, subject)
    injected_result = pdf_gate.analyze_pdf(injected_path, "ARC_CORE")
    autofix_plan = autofix.build_plan(injected_result, "ARC_CORE")
    fixed_profile = autofix.apply_profile_fixes(injected_profile, autofix_plan)
    typeset_result = typeset_core(manuscript, pdf_path, fixed_profile, subject)
    render_dir = output_dir / "render"
    pdf_result = pdf_gate.analyze_pdf(pdf_path, "ARC_CORE", render_dir=render_dir, dpi=144)
    fault_results = run_faults(fixture, manifest)

    pdf_text = "\n".join(page.get_text("text") for page in fitz.open(pdf_path))
    forbidden_text = [token for token in ("CONTENT_LOCK", "BATCH_ID", "[ARC-") if token in pdf_text]
    missed_faults = [item["id"] for item in fault_results if item["status"] != "BLOCKED"]
    failures = []
    if handoff_result["status"] != "PASS":
        failures.append("HANDOFF_PREFLIGHT")
    if pdf_result["status"] != "PASS":
        failures.append("PDF_PREFLIGHT")
    if typeset_result["page_count"] not in {4, 5, 6}:
        failures.append("CORE_PAGE_RANGE")
    if forbidden_text:
        failures.append("STUDENT_METADATA_LEAK")
    if missed_faults:
        failures.append("FAULT_INJECTION")
    if injected_result["status"] != "FAIL" or autofix_plan["decision"] != "AUTO_FIX" or fixed_profile.get("body_size") != 9.9:
        failures.append("AUTO_FIX_EXERCISE")

    return {
        "fixture_id": fixture["fixture_id"],
        "source_mode": fixture["source_mode"],
        "status": "CANARY_FAIL" if failures else "CANARY_PASS",
        "failures": failures,
        "stages": {
            "serializer": "PASS",
            "handoff_preflight": handoff_result["status"],
            "typesetter": typeset_result["status"],
            "pdf_preflight": pdf_result["status"],
        },
        "artifacts": {"handoff": str(handoff_path), "pdf": str(pdf_path), "render_dir": str(render_dir)},
        "typeset": typeset_result,
        "render_plan": render_plan,
        "pdf_qc": {"page_count": pdf_result["page_count"], "fail_count": pdf_result["fail_count"], "warn_count": pdf_result["warn_count"], "pages": pdf_result["pages"]},
        "fault_injection": fault_results,
        "auto_fix": {"initial_status": injected_result["status"], "plan": autofix_plan, "fixed_profile": fixed_profile, "retest_status": pdf_result["status"]},
        "forbidden_pdf_text": forbidden_text,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=ROOT / "quality/canary/KOR_CORE_CANARY_V1.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = run(args.fixture, args.output_dir)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    report = args.report or (args.output_dir / "canary-report.json")
    report.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "CANARY_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
