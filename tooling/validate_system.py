#!/usr/bin/env python3
"""Static ARC manifest, policy, checksum, and anti-regression validator."""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def walk_paths(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "path" and isinstance(value, str):
                yield value
            else:
                yield from walk_paths(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_paths(value)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [p.strip().replace("\\", "/") for p in result.stdout.splitlines() if p.strip()]


def parse_checksums() -> dict[str, str]:
    rows = {}
    checksum_file = ROOT / "CHECKSUMS.sha256"
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, path = line.split(maxsplit=1)
        rows[path.strip().replace("\\", "/")] = digest
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-checksums", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
    if not re.fullmatch(r"1\.8(?:\.\d+)?-dev", str(manifest["system"]["version"])):
        errors.append("system.version must be on the 1.8 dev line")

    active_paths = set(walk_paths(manifest.get("active", {})))
    runtime = manifest.get("runtime", {})
    for key in (
        "automation_runtime", "production_orchestrator", "publisher_contract",
        "storage_targets", "drive_write_adapter", "runtime_priority_policy",
        "post_exam_calibration", "claude_handoff", "multi_model_governance",
        "generator_contract", "content_bundle_contract", "typesetter_contract",
        "pipeline_integrity_contract",
    ):
        value = runtime.get(key)
        if isinstance(value, str):
            active_paths.add(value)

    for rel in sorted(active_paths):
        if not (ROOT / rel).is_file():
            errors.append(f"manifest target missing: {rel}")

    required_runtime = {
        "arc_n_cover_verso_blank": "required",
        "arc_n_problem_answer_separator_blank": "required",
        "arc_n_answer_key_completeness_gate": "required",
        "arc_brand_asset_hash_gate": "required",
        "core_student_metadata_exposure": "forbidden",
    }
    for key, expected in required_runtime.items():
        if runtime.get(key) != expected:
            errors.append(f"runtime.{key} must equal {expected!r}")

    must_contain = {
        "engine/common/COMMON_GENERATION_ENGINE_V4.4_ARC.md": [
            "SCOPE_LOCK", "UNIQUE_ANSWER", "PASS A", "PASS B", "ANSWER_KEY_COMPLETE"
        ],
        "templates/ARC_PDF_LAYOUT_MASTER_V2.2.md": [
            "COVER → BLANK_COVER_VERSO → PROBLEM_PAGES → BLANK_BEFORE_ANSWER → ANSWER_KEY",
            "BRAND_HASH_MATCH",
        ],
        "templates/core/ARC_TEMPLATE_SYSTEM_v0.6_CORE_PATCH.md": [
            "RETIRED FROM v0.3", "고정된 9블록", "학생용 내부 metadata 노출"
        ],
        "ops/ARC_PIPELINE_INTEGRITY_CONTRACT_V1.0.md": [
            "SCHOOL_SOURCE_PRIORITY", "VISUAL_AUTHENTICITY", "ANSWER_INTEGRITY"
        ],
    }
    for rel, needles in must_contain.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"required policy marker missing in {rel}: {needle}")

    science = (ROOT / "subjects/SCIENCE_MASTER_V4.0.md").read_text(encoding="utf-8")
    if "ARC_N 학생 PDF에는 넣지 않는다" in science:
        errors.append("Science MASTER still forbids the mandatory ARC_N answer section")

    layout = (ROOT / "templates/ARC_PDF_LAYOUT_MASTER_V2.2.md").read_text(encoding="utf-8")
    forbidden_layout = ["각 개념마다:\n- CONCEPT_ID", "- MUST 누락 여부"]
    for marker in forbidden_layout:
        if marker in layout:
            errors.append(f"legacy CORE card requirement remains in active PDF master: {marker}")

    fixtures = yaml.safe_load((ROOT / "quality/regression/REGRESSION_FIXTURES_V1.0.yaml").read_text(encoding="utf-8"))
    cases = [case for pack in fixtures["packs"].values() for case in pack["cases"]]
    if fixtures.get("frozen") is not True or fixtures.get("fixture_count") != 30 or len(cases) != 30:
        errors.append("frozen regression fixture invariant must remain exactly 30 cases")
    ids = [case["fixture_id"] for case in cases]
    if len(set(ids)) != len(ids):
        errors.append("duplicate regression fixture_id")

    if not args.skip_checksums:
        checksums = parse_checksums()
        expected_files = [p for p in tracked_files() if p != "CHECKSUMS.sha256"]
        missing = sorted(set(expected_files) - set(checksums))
        extra = sorted(set(checksums) - set(expected_files))
        if missing:
            errors.append(f"checksum entries missing: {', '.join(missing[:10])}")
        if extra:
            errors.append(f"checksum entries not tracked: {', '.join(extra[:10])}")
        for rel in expected_files:
            if rel in checksums and sha256(ROOT / rel) != checksums[rel]:
                errors.append(f"checksum mismatch: {rel}")

    if errors:
        print("ARC SYSTEM VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ARC SYSTEM VALIDATION: PASS ({len(active_paths)} active paths, 30 fixtures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
