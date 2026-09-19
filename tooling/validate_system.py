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


def require_markers(errors: list[str], rel: str, markers: list[str]) -> None:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"required file missing: {rel}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"required policy marker missing in {rel}: {marker}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-checksums", action="store_true", help="legacy alias; structural validation already skips full-tree checksum audit")
    parser.add_argument("--strict-checksums", action="store_true", help="also audit the legacy full-tree CHECKSUMS.sha256 registry")
    args = parser.parse_args()
    errors: list[str] = []

    manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
    if not re.fullmatch(r"1\.8(?:\.\d+)?-dev", str(manifest["system"]["version"])):
        errors.append("system.version must be on the 1.8 dev line")

    active = manifest.get("active", {})
    runtime = manifest.get("runtime", {})
    tooling = manifest.get("tooling", {})
    active_paths = set(walk_paths(active))

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
        "core_layout_mode": "ONE_COLUMN",
        "core_two_column_flow": "forbidden",
        "core_semantic_pagination_gate": "required",
        "core_major_boundary_page_break": "required",
        "core_major_boundary_blank_page": "forbidden",
        "core_major_boundary_sparse_exception": "registered_only",
        "core_heading_hierarchy_gate": "required",
        "core_html_overflow_gate": "required_when_source_available",
        "typeset_qa_skill_required": True,
        "stale_handoff_gate": "required",
        "handoff_layout_directives": "forbidden",
    }
    for key, expected in required_runtime.items():
        if runtime.get(key) != expected:
            errors.append(f"runtime.{key} must equal {expected!r}")

    common_path = active["common_generation_engine"]["path"]
    pdf_master = active["layout"]["pdf_master"]
    core_patch = active["layout"]["core_patch"]
    core_html_master = active["layout"]["core_html_master"]
    pdf_preflight_policy = active["quality"]["pdf_preflight"]
    pipeline_contract = runtime["pipeline_integrity_contract"]
    typesetter_contract = runtime["typesetter_contract"]

    require_markers(
        errors,
        common_path,
        ["SCOPE_LOCK", "UNIQUE_ANSWER", "PASS A", "PASS B", "ANSWER_KEY_COMPLETE"],
    )
    require_markers(
        errors,
        pdf_master,
        [
            "ARC CORE PRODUCT ISOLATION — HARD LOCK",
            "CORE_TWO_COLUMN_FLOW",
            "SEMANTIC PAGINATION — ARC_CORE REQUIRED",
            "MAJOR BOUNDARY PAGE START — HARD LOCK",
            "TYPOGRAPHY TOKENS — ARC_CORE DEFAULT",
            "LAST_PROBLEM_PAGE + 2 = ANSWER_KEY_START",
        ],
    )
    require_markers(
        errors,
        core_patch,
        [
            "PRODUCT ISOLATION — HARD LOCK",
            "INFORMATION HIERARCHY — FOUR LEVELS",
            "CORE_TWO_COLUMN_FLOW = 0",
            "CORE_REGISTERED_BOUNDARY_REMAINDER",
            "fixed-height page + overflow:hidden",
        ],
    )
    require_markers(
        errors,
        core_html_master,
        [
            'data-product="arc-core"',
            'column-count:1!important',
            '"Pretendard"',
            'ARC_CORE_SOURCE_PREFLIGHT',
            'data-boundary="major-topic"',
            'overflow:visible',
        ],
    )
    core_html_text = (ROOT / core_html_master).read_text(encoding="utf-8")
    if '.page{width:210mm;height:297mm;position:relative;page-break-after:always;overflow:hidden' in core_html_text:
        errors.append("active CORE HTML master must not hide page overflow")

    require_markers(
        errors,
        pdf_preflight_policy,
        ["ARC PDF PREFLIGHT V1.2", "CORE_TWO_COLUMN_FLOW", "vertical interval union"],
    )
    require_markers(
        errors,
        typesetter_contract,
        ["arc-typeset-qa", "ONE_COLUMN", "scrollHeight/clientHeight", "STALE_HANDOFF_GATE"],
    )
    require_markers(
        errors,
        pipeline_contract,
        ["SCHOOL_SOURCE_PRIORITY", "VISUAL_AUTHENTICITY", "ANSWER_INTEGRITY"],
    )

    # Typesetting skill must be registered and present.
    registry_path = active["skills"]["registry"]
    registry = yaml.safe_load((ROOT / registry_path).read_text(encoding="utf-8"))
    typeset_skill = registry.get("skills", {}).get("arc-typeset-qa")
    if not typeset_skill:
        errors.append("arc-typeset-qa must be registered")
    else:
        skill_path = typeset_skill.get("path")
        if typeset_skill.get("phase") != "typesetting":
            errors.append("arc-typeset-qa phase must be typesetting")
        if not skill_path or not (ROOT / skill_path).is_file():
            errors.append("arc-typeset-qa path is missing")
        else:
            require_markers(errors, skill_path, ["Product isolation", "Semantic pagination", "Render review", "Major boundary hard rule"])

    # Executable preflight and smoke-test targets must exist.
    for key in (
        "pdf_preflight",
        "pdf_preflight_smoke_test",
        "handoff_preflight",
        "handoff_preflight_smoke_test",
    ):
        rel = tooling.get(key)
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"tooling.{key} target missing: {rel!r}")

    science = (ROOT / "subjects/SCIENCE_MASTER_V4.0.md").read_text(encoding="utf-8")
    if "ARC_N 학생 PDF에는 넣지 않는다" in science:
        errors.append("Science MASTER still forbids the mandatory ARC_N answer section")

    # Active CORE layout must not reintroduce legacy fixed-card requirements.
    layout_text = (ROOT / pdf_master).read_text(encoding="utf-8")
    forbidden_layout = ["각 개념마다:\n- CONCEPT_ID", "- MUST 누락 여부"]
    for marker in forbidden_layout:
        if marker in layout_text:
            errors.append(f"legacy CORE card requirement remains in active PDF master: {marker}")

    fixtures = yaml.safe_load((ROOT / "quality/regression/REGRESSION_FIXTURES_V1.0.yaml").read_text(encoding="utf-8"))
    cases = [case for pack in fixtures["packs"].values() for case in pack["cases"]]
    if fixtures.get("frozen") is not True or fixtures.get("fixture_count") != 30 or len(cases) != 30:
        errors.append("frozen regression fixture invariant must remain exactly 30 cases")
    ids = [case["fixture_id"] for case in cases]
    if len(set(ids)) != len(ids):
        errors.append("duplicate regression fixture_id")

    if args.strict_checksums and not args.skip_checksums:
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

    print(
        f"ARC SYSTEM VALIDATION: PASS "
        f"({len(active_paths)} active paths, 30 fixtures, PDF={pdf_master}, CORE={core_patch}, strict_checksums={args.strict_checksums})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
