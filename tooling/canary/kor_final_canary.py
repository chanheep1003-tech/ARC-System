#!/usr/bin/env python3
"""Fixed KOR ARC_FINAL canary: QA -> FINAL quality gate -> handoff -> typeset -> PDF preflight."""
from __future__ import annotations

import argparse
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
content_gate = load_module("arc_content_qa_gate", ROOT / "tooling/content_qa/content_qa_gate.py")
final_gate = load_module("arc_final_quality_gate", ROOT / "tooling/final/final_quality_gate.py")
pdf_gate = load_module("arc_pdf_preflight", ROOT / "tooling/pdf_qc/pdf_preflight.py")
typesetter_gateway = load_module("arc_typesetter_gateway", ROOT / "tooling/typeset/typesetter_gateway.py")
canary_fonts = load_module("arc_canary_fonts", ROOT / "tooling/canary/canary_fonts.py")

def make_qa_evidence(profile: dict[str, Any], answers: dict[int, int], subject: str) -> dict[str, Any]:
    item_gates = {name: "PASS" for name in content_gate.ITEM_GATES}
    items = []
    for idx, meta in enumerate(profile["items"], start=1):
        answer = answers[idx]
        strong_options = []
        for option in range(1, 6):
            if option != answer and len(strong_options) < 2:
                strong_options.append(option)
        judgments = []
        for option in range(1, 6):
            judgments.append({
                "option_id": str(option),
                "verdict": "TRUE" if option == answer else "FALSE",
                "claim_key": f"q{idx}_claim_{option}",
                "axis": f"q{idx}_axis_{option}",
                "evidence_refs": [f"FINAL_FIXTURE:Q{idx}:O{option}"],
                "competitiveness": "CORRECT" if option == answer else ("STRONG" if option in strong_options else "MEDIUM"),
            })
        items.append({
            "item_id": meta["item_id"],
            "stem_polarity": "POSITIVE", # synthetic final fixture has exactly one TRUE
            "target_difficulty": meta["actual_difficulty"],
            "pass_a": {"answer": str(answer), "answer_evidence": [f"FINAL_FIXTURE:Q{idx}"]},
            "pass_b": {
                "answer": str(answer),
                "blind": True,
                "excluded_inputs": ["ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY"],
                "confidence": "HIGH",
                "answer_evidence": [f"FINAL_FIXTURE:Q{idx}"],
                "scope_trace": {"status": "IN_SCOPE", "source_refs": ["SYNTHETIC:KOR_FINAL"]},
                "option_judgments": judgments,
                "second_best_option": str(meta["second_best_option"]),
                "second_best_risk": "MEDIUM",
                "reasoning_steps": meta["reasoning_steps"],
                "evidence_count": meta["evidence_count"],
                "immediate_elimination_count": meta["immediate_elimination_count"],
                "transfer_required": meta["actual_difficulty"] in {"D4", "D5"},
                "actual_difficulty": meta["actual_difficulty"],
            },
            "gates": item_gates,
        })
    return {
        "schema_version": "ARC-QA-EVIDENCE-V1.0",
        "subject": subject,
        "item_count": len(items),
        "item_format": "MCQ5",
        "uses_source_text": False,
        "items": items,
        "set_gates": {name: "PASS" for name in content_gate.SET_GATES},
        "content_lock": True,
    }

def parse_questions(manuscript: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"^##\s+QUESTION\s+(\d+)\s*$", manuscript, re.M | re.I))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(manuscript)
        out.append((int(m.group(1)), manuscript[m.end():end].strip()))
    return out

def typeset_final(manuscript: str, answers: dict[int, int], output: Path, answer_output: Path, profile: dict[str, Any], subject: str) -> dict[str, Any]:
    if profile.get("answer_key_mode") != "SEPARATE_ARTIFACT_ONLY":
        raise ValueError("ARC_FINAL answer-key isolation failed")
    questions = parse_questions(manuscript)
    if len(questions) != 10:
        raise ValueError(f"expected 10 questions, found {len(questions)}")
    doc = fitz.open()
    cover = doc.new_page(width=A4_W, height=A4_H)
    canary_fonts.embed(cover)
    cover.draw_rect(fitz.Rect(50, 72, A4_W - 50, A4_H - 72), color=(0.48, 0.18, 0.21), width=1.2)
    cover.insert_text((72, 150), "ARC FINAL", fontsize=27, fontname=canary_fonts.BOLD_NAME, color=(0.48, 0.18, 0.21))
    cover.insert_text((72, 194), f"{subject} CANARY / 10 ITEMS", fontsize=16, fontname=canary_fonts.BOLD_NAME)
    cover.insert_text((72, 760), "Synthetic pipeline fixture - not a study release", fontsize=9.9, fontname=canary_fonts.REGULAR_NAME)

    groups = [questions[:4], questions[4:7], questions[7:]]
    for page_no, group in enumerate(groups, start=1):
        page = doc.new_page(width=A4_W, height=A4_H)
        canary_fonts.embed(page)
        page.insert_text((44, 36), f"ARC FINAL / {subject} CANARY", fontsize=9.5, fontname=canary_fonts.BOLD_NAME, color=(0.48, 0.18, 0.21))
        page.draw_line((44, 48), (A4_W - 44, 48), color=(0.55, 0.35, 0.38), width=0.8)
        for local, (number, text) in enumerate(group):
            col = local % 2
            row = local // 2
            x0 = 44 + col * 258
            y0 = 72 + row * 330
            width = 236
            page.insert_text((x0, y0), f"QUESTION {number}", fontsize=10.8, fontname=canary_fonts.BOLD_NAME)
            display = re.sub(r"[ \t]+(?=[1-5]\))", "\n", text)
            remaining = page.insert_textbox(fitz.Rect(x0, y0 + 18, x0 + width, y0 + 292), display, fontsize=9.3, fontname=canary_fonts.REGULAR_NAME, lineheight=1.30)
            if remaining < 0:
                raise RuntimeError(f"question {number} overflow: {remaining}")
        page.insert_text((A4_W - 68, 812), str(page_no), fontsize=9.5, fontname=canary_fonts.REGULAR_NAME)

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output, garbage=4, deflate=True)
    doc.close()
    with fitz.open(output) as saved:
        canary_fonts.assert_embedded_fonts(saved)
    answer_output.write_text("\n".join(f"{n}. {a}" for n, a in sorted(answers.items())) + "\n", encoding="utf-8")
    return {"status": "PASS", "page_count": 4, "question_count": len(questions), "answer_count": len(answers), "answer_artifact": str(answer_output)}

def run(fixture_path: Path, output_dir: Path) -> dict[str, Any]:
    fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    bundle = fixture["content_bundle"]
    profile = fixture["final_quality_profile"]
    subject = str(bundle["subject"]).upper()
    answers = {int(k): int(v) for k, v in bundle["answer_key"].items()}
    manifest_path = ROOT / "SYSTEM_MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    qa_payload = make_qa_evidence(profile, answers, subject)
    qa_payload["student_manuscript_sha256"] = serializer.sha256_text(str(bundle["student_manuscript"]).strip() + "\n")
    qa_result = content_gate.analyze(qa_payload)
    qa_path = output_dir / bundle["qa_evidence_filename"]
    qa_path.write_text(yaml.safe_dump(qa_payload, allow_unicode=True, sort_keys=False), encoding="utf-8")

    final_quality_result = final_gate.analyze(profile)
    quality_path = output_dir / "ARC_FINAL_QUALITY_PROFILE_KOR_CANARY_001.yaml"
    quality_path.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8")

    filename, handoff_text = serializer.serialize_bundle(bundle, manifest)
    handoff_path = output_dir / filename
    handoff_path.write_text(handoff_text, encoding="utf-8")
    handoff_result = handoff_gate.analyze(handoff_path, manifest_path)
    render_plan = typesetter_gateway.resolve_job(handoff_path, manifest_path, renderer="reportlab", archived_replay=True)

    manuscript = handoff_gate.section(handoff_text, "STUDENT MANUSCRIPT").strip()
    pdf_path = output_dir / f"{subject}_FINAL_CANARY_V1.pdf"
    answer_path = output_dir / f"{subject}_FINAL_CANARY_V1_ANSWER.txt"
    typeset_result = typeset_final(manuscript, answers, pdf_path, answer_path, render_plan["profile"], subject)
    pdf_result = pdf_gate.analyze_pdf(pdf_path, "ARC_FINAL", render_dir=output_dir / "render", dpi=144, expected_item_count=10)

    fault_results = []
    mutations = [
        ("WEAK_DISTRACTOR", lambda p: p["items"][2].update({"strong_distractor_count": 0})),
        ("LONGEST_CORRECT", lambda p: p["items"][1].update({"correct_option": 5, "option_lengths_chars": [20, 21, 19, 22, 40]})),
        ("FAKE_D4", lambda p: p["items"][7].update({"reasoning_steps": 1})),
        ("TOO_EASY_SET", lambda p: [x.update({"actual_difficulty": "D2", "reasoning_steps": 1}) for x in p["items"]]),
    ]
    for fault_id, mut in mutations:
        changed = yaml.safe_load(yaml.safe_dump(profile))
        mut(changed)
        result = final_gate.analyze(changed)
        fault_results.append({"id": fault_id, "status": "BLOCKED" if result["status"] == "FAIL" else "MISSED", "codes": [x["code"] for x in result["findings"]]})

    failures = []
    for name, status in (
        ("CONTENT_QA", qa_result["status"]),
        ("FINAL_QUALITY", final_quality_result["status"]),
        ("HANDOFF", handoff_result["status"]),
        ("TYPESET", typeset_result["status"]),
        ("PDF_QC", pdf_result["status"]),
    ):
        if status != "PASS":
            failures.append(name)
    if any(x["status"] != "BLOCKED" for x in fault_results):
        failures.append("FINAL_FAULT_INJECTION")

    return {
        "fixture_id": fixture["fixture_id"],
        "source_mode": fixture["source_mode"],
        "status": "CANARY_FAIL" if failures else "CANARY_PASS",
        "failures": failures,
        "stages": {
            "content_qa": qa_result["status"],
            "final_quality_gate": final_quality_result["status"],
            "serializer": "PASS",
            "handoff_preflight": handoff_result["status"],
            "typesetter": typeset_result["status"],
            "pdf_preflight": pdf_result["status"],
        },
        "final_quality": final_quality_result,
        "typeset": typeset_result,
        "pdf_qc": {"status": pdf_result["status"], "page_count": pdf_result["page_count"], "fail_count": pdf_result["fail_count"], "warn_count": pdf_result["warn_count"]},
        "render_plan": render_plan,
        "governance": {"FINAL_USER_APPROVAL": "NOT_APPLICABLE_CANARY", "DRIVE_SAVE": "BLOCKED"},
        "fault_injection": fault_results,
        "artifacts": {"qa_evidence": str(qa_path), "quality_profile": str(quality_path), "handoff": str(handoff_path), "pdf": str(pdf_path), "answer": str(answer_path), "render_dir": str(output_dir / "render")},
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", type=Path, default=ROOT / "quality/canary/KOR_FINAL_CANARY_V1.yaml")
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    result = run(args.fixture, args.output_dir)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    report = args.report or args.output_dir / "canary-report.json"
    report.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "CANARY_PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
