#!/usr/bin/env python3
"""Manifest-owned Typesetter admission and render-plan gateway.

All executable renderers must obtain their product profile and active assets
from this module.  The handoff may carry locked content, but it may not select
templates, columns, typography, page geometry, preflight, or auto-fix policy.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
PRODUCTS = {"ARC_CORE", "ARC_N", "ARC_FINAL"}
RENDERERS = {"html", "reportlab"}
HTML_MASTER_KEYS = {
    "ARC_CORE": "core_html_master",
    "ARC_N": "arc_n_html_master",
    "ARC_FINAL": "arc_final_html_master",
}
PRODUCT_PROFILES: dict[str, dict[str, Any]] = {
    "ARC_CORE": {
        "layout_mode": "ONE_COLUMN",
        "columns": 1,
        "body_size": 9.9,
        "body_weight": 400,
        "major_boundary_page_break": True,
        "cover_verso_blank": False,
        "answer_separator_blank": False,
        "answer_key_mode": "NONE",
    },
    "ARC_N": {
        "layout_mode": "COLUMN_ONLY",
        "columns": 2,
        "body_size_floor": 9.0,
        "body_weight": 400,
        "major_boundary_page_break": False,
        "cover_verso_blank": True,
        "answer_separator_blank": True,
        "answer_key_mode": "INLINE_FINAL_COMPACT",
    },
    "ARC_FINAL": {
        "layout_mode": "PRODUCT_MASTER",
        "columns": None,
        "body_size_floor": 9.0,
        "body_weight": 400,
        "major_boundary_page_break": False,
        "cover_verso_blank": False,
        "answer_separator_blank": False,
        "answer_key_mode": "SEPARATE_ARTIFACT_ONLY",
    },
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


handoff_gate = load_module(
    "arc_typesetter_handoff_preflight",
    ROOT / "tooling/handoff/handoff_preflight.py",
)


class TypesetterAdmissionError(RuntimeError):
    """A job may not enter a renderer."""


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise TypesetterAdmissionError("SYSTEM_MANIFEST must be a mapping")
    return manifest


def require_manifest_path(root: Path, rel: str, label: str) -> str:
    candidate = (root / rel).resolve()
    root_resolved = root.resolve()
    if root_resolved not in candidate.parents:
        raise TypesetterAdmissionError(f"{label} escapes repository root: {rel}")
    if not candidate.is_file():
        raise TypesetterAdmissionError(f"active {label} is missing: {rel}")
    return candidate.relative_to(root_resolved).as_posix()


def _required_runtime(manifest: dict[str, Any]) -> None:
    runtime = manifest.get("runtime", {})
    expected = {
        "typesetter_single_authority": "required",
        "typesetter_manifest_resolution": "required",
        "typesetter_product_isolation": "required",
        "typesetter_renderer_route_consistency": "required",
        "pdf_autofix_gate": "required",
        "pdf_autofix_content_mutation": "forbidden",
    }
    mismatches = [
        f"runtime.{key}={runtime.get(key)!r}, expected {value!r}"
        for key, value in expected.items()
        if runtime.get(key) != value
    ]
    if mismatches:
        raise TypesetterAdmissionError("inactive Typesetter authority gates: " + "; ".join(mismatches))


def resolve_job(
    handoff_path: Path,
    manifest_path: Path | None = None,
    renderer: str = "reportlab",
) -> dict[str, Any]:
    """Admit a locked handoff and return the sole authoritative render plan."""
    manifest_path = manifest_path or (ROOT / "SYSTEM_MANIFEST.yaml")
    manifest = load_manifest(manifest_path)
    _required_runtime(manifest)

    renderer = renderer.lower()
    if renderer not in RENDERERS:
        raise TypesetterAdmissionError(f"unsupported renderer: {renderer}")

    preflight = handoff_gate.analyze(handoff_path, manifest_path)
    if preflight["fail_count"]:
        codes = sorted({item["code"] for item in preflight["findings"] if item["severity"] == "FAIL"})
        raise TypesetterAdmissionError("handoff preflight failed: " + ", ".join(codes))

    metadata, _text = handoff_gate.parse_handoff(handoff_path)
    product = str(metadata.get("PRODUCT_MODE", "")).upper()
    if product not in PRODUCTS:
        raise TypesetterAdmissionError(f"unsupported product: {product or '<missing>'}")
    active_products = {str(value).upper() for value in manifest.get("runtime", {}).get("active_products", [])}
    if product not in active_products:
        raise TypesetterAdmissionError(f"product is not active: {product}")

    layout = manifest.get("active", {}).get("layout", {})
    tooling = manifest.get("tooling", {})
    pdf_master = manifest_path.parent / str(layout.get("pdf_master", ""))
    html_master = manifest_path.parent / str(layout.get(HTML_MASTER_KEYS[product], ""))
    preflight_tool = manifest_path.parent / str(tooling.get("pdf_preflight", ""))
    autofix_tool = manifest_path.parent / str(tooling.get("pdf_autofix_controller", ""))

    root = manifest_path.parent
    plan = {
        "status": "ADMITTED",
        "authority": "TYPESETTER_GATEWAY",
        "ruleset_version": str(manifest["system"]["version"]),
        "batch_id": str(metadata.get("BATCH_ID", "")),
        "product": product,
        "subject": str(metadata.get("SUBJECT", "")).upper(),
        "renderer": renderer,
        "pdf_master": require_manifest_path(root, str(pdf_master.relative_to(root)), "PDF master"),
        "html_master": require_manifest_path(root, str(html_master.relative_to(root)), f"{product} HTML master"),
        "renderer_source": (
            require_manifest_path(root, str(html_master.relative_to(root)), f"{product} HTML master")
            if renderer == "html"
            else require_manifest_path(root, str(pdf_master.relative_to(root)), "PDF master")
        ),
        "pdf_preflight": require_manifest_path(root, str(preflight_tool.relative_to(root)), "PDF preflight"),
        "pdf_autofix": require_manifest_path(root, str(autofix_tool.relative_to(root)), "PDF auto-fix controller"),
        "max_autofix_attempts": int(manifest["runtime"]["pdf_autofix_max_attempts"]),
        "locked_content_mutation": False,
        "profile": dict(PRODUCT_PROFILES[product]),
        "handoff_preflight": {
            "status": preflight["status"],
            "warning_codes": sorted(
                {item["code"] for item in preflight["findings"] if item["severity"] == "WARN"}
            ),
        },
    }
    return plan


def route_invariants(plan: dict[str, Any]) -> dict[str, Any]:
    """Values that must not differ between HTML and ReportLab routes."""
    return {
        key: plan[key]
        for key in (
            "ruleset_version", "batch_id", "product", "subject", "pdf_master",
            "pdf_preflight", "pdf_autofix", "max_autofix_attempts",
            "locked_content_mutation", "profile",
        )
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--manifest", type=Path, default=ROOT / "SYSTEM_MANIFEST.yaml")
    parser.add_argument("--renderer", choices=sorted(RENDERERS), default="reportlab")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = resolve_job(args.handoff, args.manifest, args.renderer)
    except TypesetterAdmissionError as exc:
        result = {"status": "RETURN_CONTENT", "error": str(exc)}
        code = 1
    else:
        code = 0
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
