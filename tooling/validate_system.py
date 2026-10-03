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
        "exam_context_registry", "exam_context_policy", "collection_registry",
    ):
        value = runtime.get(key)
        if isinstance(value, str):
            active_paths.add(value)

    for rel in sorted(active_paths):
        if not (ROOT / rel).is_file():
            errors.append(f"manifest target missing: {rel}")

    for key in ("exam_scope_gate", "exam_scope_smoke_test", "source_collection_gate", "source_collection_smoke_test"):
        rel = tooling.get(key)
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"exam/collection tooling target missing: {key}={rel!r}")
    if runtime.get("exam_scope_gate") != "required" or runtime.get("midterm_scope_reuse") != "explicit_archived_replay_only":
        errors.append("exam scope admission must be required and midterm reuse must be replay-only")
    registry_rel = runtime.get("exam_context_registry")
    if registry_rel and (ROOT / registry_rel).is_file():
        registry = yaml.safe_load((ROOT / registry_rel).read_text(encoding="utf-8"))
        exams = registry.get("exams", {}) if isinstance(registry, dict) else {}
        exam = exams.get(runtime.get("active_exam_id")) if isinstance(exams, dict) else None
        if not isinstance(exam, dict) or exam.get("status") not in {"PREPARING", "ACTIVE"} or exam.get("inherit_midterm_scope") is not False:
            errors.append("active exam must exist, be preparing/active, and forbid inherited midterm scope")
        elif not isinstance(exam.get("subjects"), dict) or set(exam["subjects"]) != {"KOR", "SOC", "SCI", "HIS", "AI"}:
            errors.append("active exam must explicitly register all five subject configurations")
        elif any(isinstance(entry, dict) and entry.get("scope_status") == "PROVISIONAL_REMAINDER"
                 for entry in exam["subjects"].values()):
            policy = exam.get("provisional_scope_policy", {})
            if not isinstance(policy, dict) or policy.get("mode") != "CURRENT_SEMESTER_COURSE_MINUS_ACTUAL_MIDTERM":
                errors.append("provisional remainder needs an explicit course-minus-actual-midterm policy")
            else:
                basis = exams.get(policy.get("basis_exam_id"), {})
                if not isinstance(basis, dict) or basis.get("status") != "ARCHIVED":
                    errors.append("provisional remainder must identify its archived midterm basis")
                if (policy.get("school_confirmed") is not False or
                    policy.get("production_priority_is_scope_evidence") is not False or
                    policy.get("collection_enabled") is not True or
                    policy.get("on_school_scope_announcement") != "REPLACE_WITH_CONFIRMED_SCOPE"):
                    errors.append("provisional collection scope must remain distinct from school confirmation and production priorities")
                if set(policy.get("applies_to_subjects", [])) != set(exam["subjects"]):
                    errors.append("provisional remainder policy must cover all registered subjects")
                if not policy.get("authorized_by") or not policy.get("scope_expression"):
                    errors.append("provisional remainder needs the user instruction and range expression")
                for rel in policy.get("midterm_baseline_refs", []):
                    if not isinstance(rel, str) or not (ROOT / rel).is_file():
                        errors.append(f"midterm baseline reference missing: {rel!r}")
    ledger_rel = runtime.get("collection_registry")
    if ledger_rel and (ROOT / ledger_rel).is_file():
        import importlib.util
        spec = importlib.util.spec_from_file_location("arc_system_collection", ROOT / "tooling/sources/source_collection_gate.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ledger = yaml.safe_load((ROOT / ledger_rel).read_text(encoding="utf-8"))
        result = module.analyze(ledger)
        if result["status"] != "PASS":
            errors.extend("collection gate: " + f["code"] for f in result["findings"])

    required_runtime = {
        "exam_scope_gate": "required",
        "midterm_scope_reuse": "explicit_archived_replay_only",
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
        "handoff_serializer_gate": "required",
        "nightly_canary_gate": "required",
        "handoff_layout_directives": "forbidden",
        "universal_independent_solve_gate": "required",
        "blind_pass_b_context_gate": "required",
        "all_option_judgment_gate": "required",
        "option_semantic_duplication_gate": "required",
        "answer_evidence_trace_gate": "required",
        "scope_evidence_trace_gate": "required",
        "actual_difficulty_reclassification_gate": "required",
        "qa_evidence_schema_gate": "required",
        "qa_evidence_manuscript_binding": "required",
        "content_qa_runner_gate": "required_when_executable",
        "pdf_autofix_gate": "required",
        "pdf_autofix_max_attempts": 2,
        "pdf_autofix_content_mutation": "forbidden",
        "typesetter_single_authority": "required",
        "typesetter_manifest_resolution": "required",
        "typesetter_product_isolation": "required",
        "typesetter_renderer_route_consistency": "required",
        "korean_original_source_lock": "required_when_source_text_used",
        "korean_source_text_fidelity": "EXACT_ONLY",
        "korean_source_text_checksum": "required",
        "korean_generated_output_as_source": "forbidden",
        "social_school_source_integrity_gate": "required",
        "core_social_x_mark_mode": "BLOCKING_SCOPE_EXCLUSION",
        "prior_approved_item_history_required": True,
        "problem_generation_exclusion_registry_required": True,
        "problem_semantic_duplicate_gate": "required",
        "problem_exact_duplicate_target": 0,
        "problem_semantic_duplicate_target": 0,
        "problem_final_user_approval_before_drive_save": "required",
        "problem_drive_save_before_user_approval": "forbidden",
        "universal_distractor_competitiveness_gate": "required",
        "universal_answer_length_bias_gate": "required",
        "arc_n_dongbook_difficulty_floor": "reference_only_not_release_gate",
        "arc_n_school_difficulty_match": "not_required",
        "arc_n_balance_gate": "required",
        "arc_n_core_exam_point_target": "70-80%",
        "arc_n_advanced_discrimination_target": "20-30%",
        "arc_final_quality_gate": "required",
        "arc_final_difficulty_mode": "SCHOOL_MULTI_EXAM_ANCHOR",
        "arc_final_multi_exam_anchor_required": True,
        "arc_final_actual_exam_corpus_required": True,
        "arc_final_difficulty_profile": "required",
        "arc_final_item_quality_profile": "required",
        "arc_final_release_gate": "required",
        "korean_exam_realism_gate": "required",
        "korean_ai_style_leak_gate": "required",
        "korean_school_task_family_gate": "required",
    }
    for key, expected in required_runtime.items():
        if runtime.get(key) != expected:
            errors.append(f"runtime.{key} must equal {expected!r}")

    social_source_path = active["quality"].get("social_a_school_source_lock")
    if not social_source_path or not (ROOT / social_source_path).is_file():
        errors.append("active Social A school source lock is missing")
    else:
        social_sources = yaml.safe_load((ROOT / social_source_path).read_text(encoding="utf-8"))
        sources = social_sources.get("sources", [])
        if len(sources) != 2:
            errors.append("Social A school source lock must contain exactly two canonical worksheets")
        for source in sources:
            if not re.fullmatch(r"[0-9a-f]{64}", str(source.get("sha256", ""))):
                errors.append(f"invalid Social A source SHA-256: {source.get('source_id')}")
            if not source.get("drive_id") or int(source.get("page_count", 0)) < 1:
                errors.append(f"incomplete Social A source identity: {source.get('source_id')}")
            if source.get("visual_review") != "PASS":
                errors.append(f"Social A source lacks visual review PASS: {source.get('source_id')}")

    korean_inventory_path = active["quality"].get("korean_school_source_inventory")
    if not korean_inventory_path or not (ROOT / korean_inventory_path).is_file():
        errors.append("KOR school source inventory is missing")
    else:
        inventory = yaml.safe_load((ROOT / korean_inventory_path).read_text(encoding="utf-8"))
        supplement = inventory.get("supplement", {})
        textbook = inventory.get("textbook", {})
        for label, entry in (("supplement", supplement), ("textbook", textbook)):
            if not entry.get("drive_id") or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", ""))):
                errors.append(f"KOR {label} Drive identity/hash missing")
        if supplement.get("text_layer") != "absent" or supplement.get("exact_transcription_status") != "HOLD_VISUAL_CROSSCHECK_REQUIRED":
            errors.append("KOR supplement cannot be promoted to EXACT without visual crosscheck")
        if textbook.get("allowed_scope") != "UNIT_1_ONLY":
            errors.append("KOR textbook scope must remain UNIT_1_ONLY")

    korean_map_path = active["quality"].get("korean_supplement_page_map")
    if not korean_map_path or not (ROOT / korean_map_path).is_file():
        errors.append("KOR supplement visual page map is missing")
    else:
        page_map = yaml.safe_load((ROOT / korean_map_path).read_text(encoding="utf-8"))
        if page_map.get("review", {}).get("heading_and_boundary_status") != "VERIFIED_VISUAL":
            errors.append("KOR supplement headings and boundaries must be visually verified")
        if page_map.get("review", {}).get("exact_body_transcription_status") != "HOLD_VISUAL_LINE_BY_LINE_TRANSCRIPTION":
            errors.append("KOR page map must not claim exact body transcription")
        if len(page_map.get("pages", [])) != 3:
            errors.append("KOR supplement page map must cover exactly three source pages")

    social_x_path = active["quality"].get("social_c_xmark_exclusion_index")
    if not social_x_path or not (ROOT / social_x_path).is_file():
        errors.append("Social C X-mark exclusion index is missing")
    else:
        x_index = yaml.safe_load((ROOT / social_x_path).read_text(encoding="utf-8"))
        exclusions = x_index.get("exclusions", [])
        if len(exclusions) != 3 or any(x.get("status") != "EXCLUDE" for x in exclusions):
            errors.append("Social C X-mark index must contain the three visually confirmed exclusions")
        gate = x_index.get("gate", {})
        for key in ("excluded_as_answer_basis", "excluded_as_required_distractor_knowledge", "excluded_as_visual_source", "excluded_as_core_required_content"):
            if gate.get(key) is not True:
                errors.append(f"Social C X-mark gate must enforce {key}")
        if gate.get("ambiguous_marks_default") != "HOLD":
            errors.append("ambiguous Social C marks must default to HOLD")

        for fixture_key in ("soc_core_canary_fixture", "soc_n_canary_fixture"):
            fixture_path = tooling.get(fixture_key)
            if not fixture_path or not (ROOT / fixture_path).is_file():
                errors.append(f"Social fixture missing for X-mark isolation: {fixture_key}")
                continue
            fixture = yaml.safe_load((ROOT / fixture_path).read_text(encoding="utf-8"))
            fixture_text = yaml.safe_dump(fixture, allow_unicode=True)
            if social_x_path not in fixture_text or "PASS_SYNTHETIC_EXCLUDED_REGIONS_NOT_USED" not in fixture_text:
                errors.append(f"{fixture_key} must bind the Social C exclusion index and attest excluded regions are unused")

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
        [
            "SCOPE_LOCK", "UNIQUE_ANSWER", "PASS A", "PASS B", "ANSWER_KEY_COMPLETE",
            "OPTION_SEMANTIC_DUPLICATION_REVIEW", "ANSWER_EVIDENCE_TRACE",
            "SCOPE_EVIDENCE_TRACE", "ACTUAL_DIFFICULTY", "PASSAGE_TRUNCATION",
        ],
    )
    require_markers(
        errors,
        active["quality"]["universal_independent_solve"],
        [
            "PASS B BLIND INDEPENDENT SOLVE",
            "ALL-OPTION VERDICT AUDIT",
            "OPTION SEMANTIC DUPLICATION REVIEW",
            "ACTUAL DIFFICULTY RECLASSIFICATION",
            "KOREAN EXACT SOURCE LOCK",
        ],
    )
    require_markers(
        errors,
        active["subjects"]["korean"]["path"],
        [
            "KOR EXACT SOURCE-BOUND ORIGINAL TEXT MODE",
            "TEXT_FIDELITY = EXACT",
            "WHITESPACE_NORMALIZED는 학생용 원문에 사용 금지",
            "SOURCE_TEXT_SHA256",
        ],
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
        ["ARC PDF PREFLIGHT V1.2", "CORE_TWO_COLUMN_FLOW", "vertical interval union", "BOUNDED AUTO-FIX CONNECTION"],
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
        "pdf_autofix_controller",
        "pdf_autofix_smoke_test",
        "typesetter_gateway",
        "typesetter_gateway_smoke_test",
        "handoff_preflight",
        "handoff_preflight_smoke_test",
        "content_qa_gate",
        "content_qa_gate_smoke_test",
        "korean_exam_realism_gate_exec",
        "korean_exam_realism_gate_smoke_test",
        "final_quality_gate_exec",
        "final_quality_gate_smoke_test",
        "handoff_serializer",
        "handoff_serializer_smoke_test",
        "nightly_canary",
        "nightly_canary_smoke_test",
        "kor_core_canary_fixture",
        "kor_n_canary",
        "kor_n_canary_smoke_test",
        "kor_n_canary_fixture",
        "kor_final_canary",
        "kor_final_canary_smoke_test",
        "kor_final_canary_fixture",
        "soc_core_canary_fixture",
        "soc_n_canary_fixture",
        "xmark_detector",
        "xmark_detector_smoke_test",
    ):
        rel = tooling.get(key)
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"tooling.{key} target missing: {rel!r}")

    require_markers(
        errors,
        tooling["content_qa_gate"],
        [
            "ANSWER_AB_MISMATCH",
            "OPTION_SEMANTIC_DUPLICATION",
            "SCOPE_TRACE_INVALID",
            "D4_SHORT",
            "KOR_SOURCE_ORIGIN_FORBIDDEN",
            "KOR_SOURCE_NOT_EXACT",
        ],
    )
    require_markers(
        errors,
        tooling["pdf_autofix_controller"],
        ["AUTO_FIX_NO_PROGRESS", "LOCKED_CONTENT_OR_COUNT_DEFECT", "PRODUCT_RULE_LEAK", "RESTORE_CORE_BODY_9_9PT"],
    )
    require_markers(
        errors,
        tooling["typesetter_gateway"],
        [
            "TYPESETTER_GATEWAY",
            "typesetter_single_authority",
            "typesetter_product_isolation",
            "QA_MANUSCRIPT_BINDING_MISMATCH",
            "route_invariants",
        ],
    )
    require_markers(
        errors,
        tooling["handoff_serializer"],
        ["layout-blind", "STUDENT_MANUSCRIPT_SHA256", "internal metadata ID"],
    )
    require_markers(
        errors,
        tooling["nightly_canary"],
        ["bundle -> handoff -> PDF -> preflight", "CANARY_PASS", "fault_injection"],
    )
    require_markers(
        errors,
        tooling["kor_n_canary"],
        ["10 MCQ items", "expected_item_count=10", "ANSWER_KEY_MISSING", "ANSWER_COUNT_SHORT"],
    )
    require_markers(
        errors,
        active["quality"]["problem_prompt_dedup_policy"],
        ["DUP_HISTORY_ACCESS=UNAVAILABLE", "FINAL_USER_APPROVAL=PENDING", "DRIVE_SAVE=BLOCKED"],
    )

    require_markers(
        errors,
        tooling["final_quality_gate_exec"],
        [
            "WEAK_DISTRACTOR_HARD_FAIL",
            "CORRECT_OPTION_LENGTH_BIAS",
            "FINAL_SCHOOL_ANCHOR_MISSING",
            "FINAL_ANCHOR_PROVENANCE_INVALID",
            "SCHOOL_MULTI_EXAM_ANCHOR",
            "FINAL_RELEASE",
        ],
    )

    require_markers(
        errors,
        active["quality"]["final_quality_gate"],
        [
            "DIFFICULTY_PROFILE",
            "ITEM_QUALITY_PROFILE",
            "SCHOOL_MULTI_EXAM_ANCHOR",
            "FINAL_SCHOOL_ANCHOR_MISSING",
            "KOR TARGET",
            "SOC TARGET",
            "SCI-REDOX TARGET",
            "FINAL_RELEASE=BLOCKED",
        ],
    )
    require_markers(
        errors,
        active["quality"]["item_quality"],
        [
            "EFFECTIVE FIVE-CHOICE RULE",
            "CORRECT OPTION LENGTH BIAS",
            "WEAK_DISTRACTOR_HARD_FAIL",
            "OBVIOUS_KEY_HARD_FAIL",
        ],
    )
    require_markers(
        errors,
        active["quality"]["difficulty_engine"],
        [
            "N° / FINAL DIFFICULTY DECOUPLING",
            "ARC_N은 동북고 실제 시험의 난도 분포와 일치할 의무가 없다.",
            "DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0.yaml",
            "DIRECT-SCOPE PRIORITY",
            "NO TEACHER-STYLE PREDICTION",
        ],
    )
    # Subject-specific FINAL anchors must be multi-exam, normalized, and evidence-linked.
    anchor_keys = (
        "final_difficulty_anchor_kor",
        "final_difficulty_anchor_soc",
        "final_difficulty_anchor_sci_redox",
    )
    for key in anchor_keys:
        rel = active["quality"].get(key)
        if not rel or not (ROOT / rel).is_file():
            errors.append(f"active FINAL anchor missing: {key}={rel!r}")
            continue
        anchor = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
        if str(anchor.get("mode", "")).upper() not in {"MULTI_EXAM_ENSEMBLE", "DIRECT_SCOPE_PLUS_MULTI_EXAM"}:
            errors.append(f"{key} must use a multi-exam anchor mode")
        if int(anchor.get("source_exam_count", 0) or 0) < 2:
            errors.append(f"{key} must reference at least two actual exams")
        if not anchor.get("corpus"):
            errors.append(f"{key} must reference the actual-exam corpus")
        profile = anchor.get("profile", {})
        shares = profile.get("shares", {})
        try:
            share_sum = float(shares["D12"]) + float(shares["D3"]) + float(shares["D45"])
        except Exception:
            errors.append(f"{key} has invalid difficulty shares")
        else:
            if abs(share_sum - 1.0) > 0.01:
                errors.append(f"{key} difficulty shares must sum to 1.0, got {share_sum:.3f}")

    corpus_rel = active["quality"].get("dongbuk_actual_exam_difficulty_corpus")
    if not corpus_rel or not (ROOT / corpus_rel).is_file():
        errors.append("Dongbuk actual-exam difficulty corpus is missing")
    else:
        corpus = yaml.safe_load((ROOT / corpus_rel).read_text(encoding="utf-8"))
        exams = corpus.get("exams", [])
        if len(exams) < 16:
            errors.append(f"Dongbuk difficulty corpus must retain at least 16 actual exams, got {len(exams)}")
        ids = {str(row.get("exam_id")) for row in exams if isinstance(row, dict)}
        required_ids = {
            "KOR_2025_2_MID", "KOR_2025_2_FINAL", "KOR_2026_1_MID", "KOR_2026_1_FINAL",
            "SOC_2025_2_MID", "SOC_2025_2_FINAL", "SOC_2026_1_MID", "SOC_2026_1_FINAL",
            "SCI_2025_2_MID", "SCI_2025_2_FINAL", "SCI_2026_1_MID", "SCI_2026_1_FINAL",
            "HIS_2025_2_MID", "HIS_2025_2_FINAL", "HIS_2026_1_MID", "HIS_2026_1_FINAL",
        }
        missing_exam_ids = sorted(required_ids - ids)
        if missing_exam_ids:
            errors.append(f"Dongbuk difficulty corpus missing exams: {', '.join(missing_exam_ids)}")

    require_markers(
        errors,
        active["quality"]["n_balance_gate"],
        [
            "CORE_EXAM_POINT = 70~80%",
            "ADVANCED_DISCRIMINATION = 20~30%",
            "ARC_N_BALANCE_GATE=PASS",
            "ARC_FINAL에는 본 게이트의 70/30 비율을 강제하지 않는다.",
        ],
    )

    require_markers(
        errors,
        active["quality"]["korean_exam_realism_gate"],
        [
            "KOR_EXAM_REALISM_GATE=PASS",
            "KOR_AI_STYLE_LEAK_GATE=PASS",
            "KOR_SCHOOL_TASK_FAMILY_GATE=PASS",
            "UNANCHORED META LANGUAGE",
            "WRAPPER WITHOUT FUNCTION",
        ],
    )
    require_markers(
        errors,
        active["quality"]["korean_item_qa"],
        [
            "EXAM REALISM / AI-STYLE LEAK GATE",
            "KOR_EXAM_REALISM_GATE=PASS",
            "KOR_AI_STYLE_LEAK_GATE=PASS",
            "KOR_SCHOOL_TASK_FAMILY_GATE=PASS",
        ],
    )
    require_markers(
        errors,
        active["korean_item_engine"]["path"],
        [
            "SCHOOL-REALISM BLUEPRINT",
            "AI-like generation 방지",
            "KOR_EXAM_REALISM_GATE=PASS",
        ],
    )
    require_markers(
        errors,
        tooling["korean_exam_realism_gate_exec"],
        [
            "SCHOOL_TASK_FAMILY_RATE_LOW",
            "AI_CHOICE_PATTERN",
            "CORRECT_LENGTH_CUE",
            "KOR_AI_STYLE_LEAK_GATE",
        ],
    )

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
        ephemeral = {"CHECKSUMS.sha256", "ops/RUN_LOG.csv", "ops/RUN_LOG.jsonl"}
        expected_files = [p for p in tracked_files() if p not in ephemeral]
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
