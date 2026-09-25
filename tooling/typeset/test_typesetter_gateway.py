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
kor_n_canary = load_module("arc_gateway_kor_n_canary", ROOT / "tooling/canary/kor_n_canary.py")


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
    if product in {"ARC_N", "ARC_FINAL"}:
        proof = kor_n_canary.make_qa_evidence({int(k): int(v) for k, v in bundle["answer_key"].items()})
        proof["student_manuscript_sha256"] = serializer.sha256_text(str(bundle["student_manuscript"]).strip() + "\n")
        (destination / bundle["qa_evidence_filename"]).write_text(
            yaml.safe_dump(proof, allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
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

        n_handoff = make_handoff("ARC_N", temp)
        n_metadata, _ = gateway.handoff_gate.parse_handoff(n_handoff)
        qa_path = temp / n_metadata["QA_EVIDENCE_FILENAME"]
        qa_proof = yaml.safe_load(qa_path.read_text(encoding="utf-8"))
        qa_proof["items"][0]["pass_a"]["answer"] = "5"
        qa_proof["items"][0]["pass_b"]["answer"] = "5"
        qa_path.write_text(yaml.safe_dump(qa_proof, allow_unicode=True), encoding="utf-8")
        try:
            gateway.resolve_job(n_handoff)
        except gateway.TypesetterAdmissionError as exc:
            assert "QA_EVIDENCE_FAILED" in str(exc) or "QA_ANSWER_MISMATCH" in str(exc)
        else:
            raise AssertionError("QA proof with mutated answer was accepted")
        qa_path.unlink()
        try:
            gateway.resolve_job(n_handoff)
        except gateway.TypesetterAdmissionError as exc:
            assert "QA_EVIDENCE_MISSING" in str(exc)
        else:
            raise AssertionError("missing QA proof was accepted")

        n_handoff = make_handoff("ARC_N", temp)
        original = n_handoff.read_text(encoding="utf-8")
        assert "\n1: 3\n" in original
        n_handoff.write_text(original.replace("\n1: 3\n", "\n1: 2\n", 1), encoding="utf-8")
        preflight_result = gateway.handoff_gate.analyze(n_handoff, ROOT / "SYSTEM_MANIFEST.yaml")
        assert preflight_result["status"] == "PASS", preflight_result
        try:
            gateway.resolve_job(n_handoff)
        except gateway.TypesetterAdmissionError as exc:
            assert "QA_ANSWER_MISMATCH at question 1" in str(exc)
        else:
            raise AssertionError("locked answer key diverged from QA proof but was accepted")

        # A structurally valid, reserialized manuscript cannot borrow another
        # batch's QA evidence just because the ten answers are identical.
        n_handoff = make_handoff("ARC_N", temp)
        proof_path = temp / gateway.handoff_gate.parse_handoff(n_handoff)[0]["QA_EVIDENCE_FILENAME"]
        original_bundle = yaml.safe_load((ROOT / "quality/canary/KOR_N_CANARY_V1.yaml").read_text(encoding="utf-8"))["content_bundle"]
        changed_bundle = copy.deepcopy(original_bundle)
        changed_bundle["batch_id"] = "ARC-KOR-N-GATEWAY"
        changed_bundle["student_manuscript"] += "\n\nSecond manuscript with the same answer sequence."
        manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
        _, swapped_handoff = serializer.serialize_bundle(changed_bundle, manifest)
        n_handoff.write_text(swapped_handoff, encoding="utf-8")
        preflight_result = gateway.handoff_gate.analyze(n_handoff, ROOT / "SYSTEM_MANIFEST.yaml")
        assert preflight_result["status"] == "PASS", preflight_result
        try:
            gateway.resolve_job(n_handoff)
        except gateway.TypesetterAdmissionError as exc:
            assert "QA_MANUSCRIPT_BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("QA proof from another manuscript was accepted")
        n_handoff = make_handoff("ARC_N", temp)
        proof = yaml.safe_load(proof_path.read_text(encoding="utf-8"))
        proof.pop("student_manuscript_sha256")
        proof_path.write_text(yaml.safe_dump(proof, allow_unicode=True), encoding="utf-8")
        try:
            gateway.resolve_job(n_handoff)
        except gateway.TypesetterAdmissionError as exc:
            assert "QA_MANUSCRIPT_BINDING_MISSING" in str(exc)
        else:
            raise AssertionError("unbound QA proof was accepted")

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
