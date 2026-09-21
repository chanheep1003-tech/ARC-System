#!/usr/bin/env python3
"""Behavioral smoke for manifest-owned Typesetter routing."""
from __future__ import annotations

import copy
import importlib.util
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


gateway = load_module("arc_typesetter_gateway", ROOT / "tooling/typeset/typesetter_gateway.py")
serializer = load_module("arc_gateway_serializer", ROOT / "tooling/handoff/handoff_serializer.py")


def make_handoff(product: str, destination: Path) -> Path:
    fixture = yaml.safe_load((ROOT / "quality/canary/KOR_N_CANARY_V1.yaml").read_text(encoding="utf-8"))
    bundle = copy.deepcopy(fixture["content_bundle"])
    bundle["product_mode"] = product
    bundle["batch_id"] = f"ARC-KOR-{product.replace('ARC_', '')}-GATEWAY"
    if product == "ARC_CORE":
        bundle.pop("answer_key", None)
        bundle.pop("qa_evidence_filename", None)
        bundle["item_count"] = 0
        bundle["student_manuscript"] = "# A 파트\n\n게이트웨이 검증 본문."
        bundle["core_architecture_summary"] = {"major_boundaries": ["A 파트"]}
    manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
    filename, text = serializer.serialize_bundle(bundle, manifest)
    path = destination / filename
    path.write_text(text, encoding="utf-8")
    return path


def run() -> None:
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        plans = {}
        for product in sorted(gateway.PRODUCTS):
            handoff = make_handoff(product, temp)
            html = gateway.resolve_job(handoff, renderer="html")
            reportlab = gateway.resolve_job(handoff, renderer="reportlab")
            assert gateway.route_invariants(html) == gateway.route_invariants(reportlab)
            assert html["html_master"] != reportlab["renderer_source"]
            assert html["product"] == product and reportlab["product"] == product
            plans[product] = reportlab

        assert plans["ARC_CORE"]["profile"]["columns"] == 1
        assert plans["ARC_CORE"]["profile"]["answer_key_mode"] == "NONE"
        assert plans["ARC_N"]["profile"]["columns"] == 2
        assert plans["ARC_N"]["profile"]["cover_verso_blank"] is True
        assert plans["ARC_N"]["profile"]["answer_separator_blank"] is True
        assert plans["ARC_FINAL"]["profile"]["answer_key_mode"] == "SEPARATE_ARTIFACT_ONLY"
        assert plans["ARC_FINAL"]["profile"]["cover_verso_blank"] is False

        bad_manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
        bad_manifest["runtime"]["typesetter_single_authority"] = "disabled"
        bad_path = temp / "bad-manifest.yaml"
        bad_path.write_text(yaml.safe_dump(bad_manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")
        handoff = make_handoff("ARC_CORE", temp)
        try:
            gateway.resolve_job(handoff, manifest_path=bad_path)
        except gateway.TypesetterAdmissionError as exc:
            assert "authority gates" in str(exc)
        else:
            raise AssertionError("disabled single authority gate was accepted")

    print("ARC TYPESETTER GATEWAY SMOKE: PASS")


if __name__ == "__main__":
    run()
