#!/usr/bin/env python3
"""Manifest-owned Typesetter admission and render-plan gateway.

All executable renderers must obtain their product profile and active assets
from this module.  The handoff may carry locked content, but it may not select
templates, columns, typography, page geometry, preflight, or auto-fix policy.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
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
        "metadata_strip_difficulty": "NONE",
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
        # User decisions 2026-11-08 (ops/ARC_DECISIONS_20261108.md)
        "slots_per_page": 4,
        "slot_layout": "TWO_PER_COLUMN_FIXED",
        "passage_set_slot_release": True,
        "metadata_strip_difficulty": "D1_D5",
        "cover_logo_variant": "BW_REGISTERED_ASSET",
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
        "metadata_strip_difficulty": "NONE",
    },
}


BW_LOGO = "ARC_N_LOCKUP_MASTER_BW.png"


def brand_release_blockers(root: Path, manifest: dict[str, Any], product: str) -> list[str]:
    """The ARC_N cover needs the registered B/W logo (exact registry row + byte-identical repo copy)."""
    if product != "ARC_N" or manifest.get("runtime", {}).get("arc_n_cover_logo_variant") != "BW_REGISTERED_ASSET_REQUIRED":
        return []
    registry = root / "templates/brand/ARC_BRAND_ASSET_REGISTRY_V1.0.md"
    row = next((line for line in registry.read_text(encoding="utf-8").splitlines() if BW_LOGO in line), "") if registry.is_file() else ""
    match = re.search(r"\b([0-9a-f]{64})\b", row)
    if not match:
        return ["BRAND_ASSET_MISSING:" + BW_LOGO + " (no registered SHA-256 in the brand asset registry)"]
    asset = root / "templates/brand/assets" / BW_LOGO
    if not asset.is_file():
        return ["BRAND_ASSET_MISSING:" + BW_LOGO + " (registered, but the repository copy is absent)"]
    if hashlib.sha256(asset.read_bytes()).hexdigest() != match.group(1):
        return ["BRAND_HASH_MISMATCH:" + BW_LOGO]
    return []


def preflight_args(profile: dict[str, Any]) -> list[str]:
    """Extra pdf_preflight flags implied by a product profile (the caller must pass them)."""
    args: list[str] = []
    if profile.get("slots_per_page"):
        args += ["--max-questions-per-page", str(profile["slots_per_page"])]
    if profile.get("metadata_strip_difficulty") == "D1_D5":
        args.append("--require-difficulty-strip")
    return args


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
content_gate = load_module(
    "arc_typesetter_content_qa",
    ROOT / "tooling/content_qa/content_qa_gate.py",
)
exam_gate = load_module("arc_typesetter_exam_scope", ROOT / "tooling/exams/exam_scope_gate.py")


class TypesetterAdmissionError(RuntimeError):
    """A job may not enter a renderer."""


def verify_qa_evidence(handoff_path: Path, metadata: dict[str, Any], text: str) -> dict[str, Any]:
    """Check the referenced QA proof rather than trusting self-declared PASS fields."""
    filename = str(metadata.get("QA_EVIDENCE_FILENAME", ""))
    if not filename or Path(filename).name != filename or filename in {".", ".."}:
        raise TypesetterAdmissionError("QA_EVIDENCE_FILENAME must be a local basename")
    qa_path = handoff_path.parent / filename
    if not qa_path.is_file() or qa_path.is_symlink():
        raise TypesetterAdmissionError("QA_EVIDENCE_MISSING: " + filename)
    try:
        proof = yaml.safe_load(qa_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise TypesetterAdmissionError("QA_EVIDENCE_UNREADABLE: " + filename) from exc
    if not isinstance(proof, dict):
        raise TypesetterAdmissionError("QA_EVIDENCE_INVALID: expected mapping")
    qa_result = content_gate.analyze(proof)
    if qa_result["status"] != "PASS":
        codes = sorted({finding["code"] for finding in qa_result["findings"]})
        raise TypesetterAdmissionError("QA_EVIDENCE_FAILED: " + ", ".join(codes))
    if str(proof.get("subject", "")).upper() != str(metadata.get("SUBJECT", "")).upper():
        raise TypesetterAdmissionError("QA_SUBJECT_MISMATCH")
    try:
        expected_count = int(metadata["ITEM_COUNT"])
    except (TypeError, ValueError, KeyError) as exc:
        raise TypesetterAdmissionError("QA_ITEM_COUNT_INVALID") from exc
    if proof.get("item_count") != expected_count:
        raise TypesetterAdmissionError("QA_ITEM_COUNT_MISMATCH")
    locked_digest = str(metadata.get("STUDENT_MANUSCRIPT_SHA256", ""))
    proof_digest = str(proof.get("student_manuscript_sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", proof_digest):
        raise TypesetterAdmissionError("QA_MANUSCRIPT_BINDING_MISSING")
    if proof_digest != locked_digest:
        raise TypesetterAdmissionError("QA_MANUSCRIPT_BINDING_MISMATCH")
    manuscript = handoff_gate.section(text, "STUDENT MANUSCRIPT").strip() + "\n"
    if hashlib.sha256(manuscript.encode("utf-8")).hexdigest() != proof_digest:
        raise TypesetterAdmissionError("QA_MANUSCRIPT_CONTENT_MISMATCH")
    answer_text = handoff_gate.section(text, "ANSWER KEY")
    try:
        answer_key = yaml.safe_load(answer_text)
    except yaml.YAMLError as exc:
        raise TypesetterAdmissionError("QA_ANSWER_KEY_UNREADABLE") from exc
    if not isinstance(answer_key, dict) or len(answer_key) != expected_count:
        raise TypesetterAdmissionError("QA_ANSWER_COUNT_MISMATCH")
    for index, item in enumerate(proof["items"], start=1):
        try:
            evidence_answer = str(item["pass_a"]["answer"])
        except (KeyError, TypeError) as exc:
            raise TypesetterAdmissionError(f"QA_ANSWER_PROOF_INVALID at question {index}") from exc
        try:
            locked_answer = str(answer_key[index])
        except KeyError as exc:
            raise TypesetterAdmissionError("QA_ANSWER_NUMBER_MISSING") from exc
        if evidence_answer != locked_answer:
            raise TypesetterAdmissionError(f"QA_ANSWER_MISMATCH at question {index}")
    return {"status": "PASS", "filename": filename, "item_count": expected_count, "student_manuscript_sha256": proof_digest}


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
        "qa_evidence_manuscript_binding": "required",
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
    *, archived_replay: bool = False,
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

    metadata, text = handoff_gate.parse_handoff(handoff_path)
    product = str(metadata.get("PRODUCT_MODE", "")).upper()
    if product not in PRODUCTS:
        raise TypesetterAdmissionError(f"unsupported product: {product or '<missing>'}")
    active_products = {str(value).upper() for value in manifest.get("runtime", {}).get("active_products", [])}
    if product not in active_products:
        raise TypesetterAdmissionError(f"product is not active: {product}")
    qa_proof = verify_qa_evidence(handoff_path, metadata, text) if product in {"ARC_N", "ARC_FINAL"} else None
    exam_proof = None
    if manifest.get("runtime", {}).get("exam_scope_gate") == "required":
        admission_bundle = {"exam_context": metadata.get("EXAM_CONTEXT"),
                            "subject": metadata.get("SUBJECT"), "product_mode": product}
        if qa_proof and not archived_replay:
            raw_qa = yaml.safe_load((handoff_path.parent / qa_proof["filename"]).read_text(encoding="utf-8"))
            if raw_qa.get("exam_context") != metadata.get("EXAM_CONTEXT"):
                raise TypesetterAdmissionError("QA_EXAM_CONTEXT_BINDING_MISMATCH")
            locks = raw_qa.get("source_text_locks", [])
            if locks:
                admission_bundle["passages"] = [{"source_text_id": lock.get("source_text_id")} for lock in locks]
        exam_proof = exam_gate.check_bundle(admission_bundle, manifest_path, archived_replay=archived_replay)
        if exam_proof["status"] == "FAIL":
            codes = sorted({row["code"] for row in exam_proof["findings"]})
            raise TypesetterAdmissionError("EXAM_SCOPE_FAILED: " + ", ".join(codes))

    layout = manifest.get("active", {}).get("layout", {})
    tooling = manifest.get("tooling", {})
    pdf_master = manifest_path.parent / str(layout.get("pdf_master", ""))
    html_master = manifest_path.parent / str(layout.get(HTML_MASTER_KEYS[product], ""))
    preflight_tool = manifest_path.parent / str(tooling.get("pdf_preflight", ""))
    autofix_tool = manifest_path.parent / str(tooling.get("pdf_autofix_controller", ""))

    root = manifest_path.parent
    blockers = brand_release_blockers(root, manifest, product)
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
        "qa_evidence": qa_proof,
        "exam_scope": exam_proof,
        "release_blockers": blockers,
        "release_eligible": bool(exam_proof and exam_proof.get("release_allowed")) and not blockers,
        "profile": dict(PRODUCT_PROFILES[product]),
        "preflight_args": preflight_args(PRODUCT_PROFILES[product]),
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
    parser.add_argument("--archived-replay", action="store_true", help="Test-only admission; not release eligible")
    parser.add_argument("--renderer", choices=sorted(RENDERERS), default="reportlab")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = resolve_job(args.handoff, args.manifest, args.renderer, archived_replay=args.archived_replay)
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
