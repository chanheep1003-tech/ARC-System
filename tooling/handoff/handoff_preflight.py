#!/usr/bin/env python3
"""Deterministic gate for ARC Markdown handoffs.

The handoff carries locked content, not layout authority. This gate prevents
stale generator-era layout instructions from overriding the active manifest.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
INTERNAL_ID_RE = re.compile(r"\[(?:ARC-[A-Z0-9]+-[A-Z0-9]+-\d+|CONCEPT_ID|SOURCE_ID)[^\]]*\]", re.I)
TWO_COLUMN_RE = re.compile(
    r"(?:\b2\s*단\s*(?:조판|형식|레이아웃|배치|본문)|two[- ]column|column-count\s*:\s*2)",
    re.I,
)
PDF_MASTER_RE = re.compile(r"ARC_PDF_LAYOUT_MASTER_V\d+(?:\.\d+)*", re.I)
LAYOUT_CODE_RE = re.compile(
    r"(?:grid-template-columns|column-count|@page|PageTemplate|\bFrame\s*\(|"
    r"margin\s*:|page-break-(?:before|after)|break-before\s*:)",
    re.I,
)
FONT_PIN_RE = re.compile(r"(?:본문|body|font(?:-size)?)\D{0,35}(\d+(?:\.\d+)?)\s*pt", re.I)
PART_RE = re.compile(r"(?:[ABC]\s*파트|파트\s*[ABC]|\bPART\s*[ABC]\b)", re.I)
H1_RE = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.M)

STANDARD_SECTION_HEADINGS = (
    "ANSWER KEY",
    "VISUAL / LAYOUT ASSET MANIFEST",
    "SOURCE TEXT BLOCKS",
    "QC STATUS",
)


def section(text: str, heading: str) -> str:
    start = re.search(rf"^#\s+{re.escape(heading)}\s*$", text, re.M | re.I)
    if not start:
        return ""
    tail = text[start.end() :]
    stops = []
    for name in STANDARD_SECTION_HEADINGS:
        found = re.search(rf"^#\s+{re.escape(name)}(?:\s+.*)?$", tail, re.M | re.I)
        if found:
            stops.append(found.start())
    return tail[: min(stops)] if stops else tail


def parse_handoff(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.search(text)
    if not match:
        return {}, text
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        metadata = {}
    return metadata, text


def finding(code: str, message: str, severity: str = "FAIL") -> dict:
    return {"severity": severity, "code": code, "message": message}


def analyze(path: Path, manifest_path: Path) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    active_version = str(manifest["system"]["version"])
    active_master = Path(manifest["active"]["layout"]["pdf_master"]).stem
    metadata, text = parse_handoff(path)
    findings: list[dict] = []

    if not metadata:
        findings.append(finding("FRONT_MATTER_MISSING", "YAML front matter is required."))

    product = str(metadata.get("PRODUCT_MODE", "")).upper()
    ruleset = str(metadata.get("ARC_RULESET_VERSION", ""))
    if ruleset != active_version:
        findings.append(
            finding(
                "STALE_RULESET",
                f"handoff ruleset {ruleset or '<missing>'} does not match active {active_version}",
            )
        )

    student_marker = re.search(r"^#\s+STUDENT MANUSCRIPT\s*$", text, re.M | re.I)
    instructions_region = text[: student_marker.start()] if student_marker else text
    student = section(text, "STUDENT MANUSCRIPT")
    if not student_marker or not student.strip():
        findings.append(finding("STUDENT_MANUSCRIPT_MISSING", "STUDENT MANUSCRIPT is required."))

    if product == "ARC_CORE":
        if TWO_COLUMN_RE.search(instructions_region):
            findings.append(finding("CORE_TWO_COLUMN_DIRECTIVE", "CORE handoff contains a two-column directive."))

        masters = sorted(set(PDF_MASTER_RE.findall(instructions_region)))
        if masters:
            findings.append(
                finding(
                    "PDF_MASTER_PIN_FORBIDDEN",
                    f"handoff pins {', '.join(masters)}; active master is {active_master} and must be resolved at runtime",
                )
            )

        if LAYOUT_CODE_RE.search(instructions_region):
            findings.append(finding("LAYOUT_CODE_FORBIDDEN", "handoff contains concrete CSS/ReportLab/page geometry."))

        pinned_sizes = [float(value) for value in FONT_PIN_RE.findall(instructions_region)]
        if pinned_sizes:
            findings.append(
                finding(
                    "FONT_SIZE_PIN_FORBIDDEN",
                    f"handoff pins body/font size(s): {pinned_sizes}; typography belongs to the active Typesetter",
                )
            )

        leaks = INTERNAL_ID_RE.findall(student)
        if leaks:
            findings.append(
                finding(
                    "STUDENT_INTERNAL_ID_LEAK",
                    f"student manuscript exposes internal IDs: {sorted(set(leaks))[:5]}",
                )
            )

        h1_titles = H1_RE.findall(student)
        part_lines = [line.strip() for line in student.splitlines() if PART_RE.search(line)]
        unmarked_parts = [line for line in part_lines if not re.match(r"^#(?!#)\s+", line)]
        if unmarked_parts:
            findings.append(
                finding(
                    "UNMARKED_MAJOR_BOUNDARY",
                    "A/B/C part heading must be a level-1 Markdown heading: " + "; ".join(unmarked_parts[:5]),
                )
            )
        if not h1_titles:
            findings.append(
                finding(
                    "MAJOR_BOUNDARY_UNDECLARED",
                    "No level-1 PART/MAJOR_TOPIC boundary is declared in the ARC_CORE manuscript.",
                    "WARN",
                )
            )
    else:
        h1_titles = []

    fail_count = sum(item["severity"] == "FAIL" for item in findings)
    warn_count = sum(item["severity"] == "WARN" for item in findings)
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    return {
        "tool": "ARC_HANDOFF_PREFLIGHT_V1.0",
        "handoff": str(path),
        "product": product or None,
        "active_ruleset": active_version,
        "status": status,
        "fail_count": fail_count,
        "warn_count": warn_count,
        "major_boundaries": h1_titles,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--manifest", type=Path, default=ROOT / "SYSTEM_MANIFEST.yaml")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.handoff, args.manifest)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
