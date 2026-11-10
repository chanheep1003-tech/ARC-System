#!/usr/bin/env python3
"""Fixed KOR ARC_N canary with 10 MCQ items and complete PDF page order."""
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
pdf_gate = load_module("arc_pdf_preflight", ROOT / "tooling/pdf_qc/pdf_preflight.py")
typesetter_gateway = load_module("arc_typesetter_gateway", ROOT / "tooling/typeset/typesetter_gateway.py")
canary_fonts = load_module("arc_canary_fonts", ROOT / "tooling/canary/canary_fonts.py")


def make_qa_evidence(answers: dict[int, int], subject: str = "KOR") -> dict[str, Any]:
    item_gates = {name: "PASS" for name in content_gate.ITEM_GATES}
    items = []
    for number, answer in answers.items():
        option_judgments = []
        for option in range(1, 6):
            option_judgments.append({
                "option_id": str(option),
                "verdict": "TRUE" if option == answer else "FALSE",
                "claim_key": f"q{number}_claim_{option}",
                "axis": "reading_evidence",
                "evidence_refs": [f"FIXTURE:Q{number}:O{option}"],
                "competitiveness": "CORRECT" if option == answer else ("STRONG" if option in {(answer % 5) + 1, ((answer + 1) % 5) + 1} else "MEDIUM"),
            })
        second_best = next(str(option) for option in range(1, 6) if option != answer)
        items.append({
            "item_id": f"{subject}-CANARY-{number:03d}",
            "stem_polarity": "POSITIVE", # synthetic canary choices use one TRUE answer
            "target_difficulty": "D3",
            "pass_a": {"answer": str(answer), "answer_evidence": [f"FIXTURE:Q{number}"]},
            "pass_b": {
                "answer": str(answer), "blind": True,
                "excluded_inputs": ["ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY"],
                "confidence": "HIGH", "answer_evidence": [f"FIXTURE:Q{number}"],
                "scope_trace": {"status": "IN_SCOPE", "source_refs": [f"SYNTHETIC:{subject}"]},
                "option_judgments": option_judgments, "second_best_option": second_best,
                "second_best_risk": "MEDIUM", "reasoning_steps": 1, "evidence_count": 1,
                "immediate_elimination_count": 2, "transfer_required": False, "actual_difficulty": "D3",
            },
            "gates": item_gates,
        })
    return {
        "schema_version": "ARC-QA-EVIDENCE-V1.0", "subject": subject, "item_count": len(items),
        "item_format": "MCQ5", "uses_source_text": False, "items": items,
        "set_gates": {name: "PASS" for name in content_gate.SET_GATES}, "content_lock": True,
    }


def parse_questions(manuscript: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"^##\s+QUESTION\s+(\d+)\s*$", manuscript, re.M | re.I))
    questions = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(manuscript)
        questions.append((int(match.group(1)), manuscript[match.end():end].strip()))
    return questions


def typeset_n(manuscript: str, answers: dict[int, int], output: Path, profile: dict[str, Any], subject: str = "KOR") -> dict[str, Any]:
    if profile.get("columns") != 2 or not profile.get("cover_verso_blank") or not profile.get("answer_separator_blank"):
        raise ValueError("ARC_N product profile isolation failed")
    questions = parse_questions(manuscript)
    if len(questions) != 10:
        raise ValueError(f"expected 10 questions, found {len(questions)}")
    doc = fitz.open()
    cover = doc.new_page(width=A4_W, height=A4_H)
    canary_fonts.embed(cover)
    cover.draw_rect(fitz.Rect(50, 72, A4_W - 50, A4_H - 72), color=(0.08, 0.16, 0.30), width=1.2)
    cover.insert_text((72, 150), "ARC N", fontsize=28, fontname=canary_fonts.BOLD_NAME, color=(0.08, 0.16, 0.30))
    cover.insert_text((72, 194), f"{subject} CANARY / 10 ITEMS", fontsize=16, fontname=canary_fonts.BOLD_NAME)
    cover.insert_text((72, 760), "Synthetic pipeline fixture - not a study release", fontsize=9.9, fontname=canary_fonts.REGULAR_NAME)
    doc.new_page(width=A4_W, height=A4_H)

    for page_index in range(2):
        page = doc.new_page(width=A4_W, height=A4_H)
        canary_fonts.embed(page)
        page.insert_text((44, 36), f"ARC N / {subject} CANARY", fontsize=9.5, fontname=canary_fonts.REGULAR_NAME)
        page.draw_line((44, 48), (A4_W - 44, 48), color=(0.45, 0.55, 0.68), width=0.8)
        for local_index, (number, text) in enumerate(questions[page_index * 5:(page_index + 1) * 5]):
            column = local_index % 2
            row = local_index // 2
            x0 = 44 + column * 258
            y0 = 68 + row * 226
            width = 236
            page.insert_text((x0, y0), f"QUESTION {number}", fontsize=11.2, fontname=canary_fonts.BOLD_NAME, color=(0.08, 0.16, 0.30))
            display_text = re.sub(r"[ \t]+(?=[1-5]\))", "\n", text)
            remaining = page.insert_textbox(fitz.Rect(x0, y0 + 18, x0 + width, y0 + 198), display_text, fontsize=9.4, fontname=canary_fonts.REGULAR_NAME, lineheight=1.28)
            if remaining < 0:
                raise RuntimeError(f"question {number} overflow: {remaining}")
        page.insert_text((A4_W - 68, 812), str(page.number + 1), fontsize=9.5, fontname=canary_fonts.REGULAR_NAME)

    doc.new_page(width=A4_W, height=A4_H)
    key = doc.new_page(width=A4_W, height=A4_H)
    canary_fonts.embed(key)
    key.insert_text((58, 72), "ANSWER KEY", fontsize=20, fontname=canary_fonts.BOLD_NAME, color=(0.08, 0.16, 0.30))
    key.draw_line((58, 86), (A4_W - 58, 86), color=(0.45, 0.55, 0.68), width=0.8)
    for index, (number, answer) in enumerate(sorted(answers.items())):
        x = 80 if index < 5 else 310
        y = 135 + (index % 5) * 54
        key.insert_text((x, y), f"{number}. {answer}", fontsize=12, fontname=canary_fonts.REGULAR_NAME)
    key.insert_text((A4_W - 68, 812), str(key.number + 1), fontsize=9.5, fontname=canary_fonts.REGULAR_NAME)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output, garbage=4, deflate=True)
    doc.close()
    with fitz.open(output) as saved:
        canary_fonts.assert_embedded_fonts(saved)
    return {"status": "PASS", "page_count": 6, "question_count": len(questions), "answer_count": len(answers)}


def run(fixture_path: Path, output_dir: Path) -> dict[str, Any]:
    fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    bundle = fixture["content_bundle"]
    subject = str(bundle["subject"]).upper()
    answers = {int(k): int(v) for k, v in bundle["answer_key"].items()}
    manifest_path = ROOT / "SYSTEM_MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    qa_payload = make_qa_evidence(answers, subject)
    qa_payload["student_manuscript_sha256"] = serializer.sha256_text(str(bundle["student_manuscript"]).strip() + "\n")
    qa_result = content_gate.analyze(qa_payload)
    qa_path = output_dir / bundle["qa_evidence_filename"]
    qa_path.write_text(yaml.safe_dump(qa_payload, allow_unicode=True, sort_keys=False), encoding="utf-8")

    filename, handoff_text = serializer.serialize_bundle(bundle, manifest)
    handoff_path = output_dir / filename
    handoff_path.write_text(handoff_text, encoding="utf-8")
    handoff_result = handoff_gate.analyze(handoff_path, manifest_path)
    render_plan = typesetter_gateway.resolve_job(handoff_path, manifest_path, renderer="reportlab", archived_replay=True)

    manuscript = handoff_gate.section(handoff_text, "STUDENT MANUSCRIPT").strip()
    pdf_path = output_dir / f"{subject}_N_CANARY_V1.pdf"
    typeset_result = typeset_n(manuscript, answers, pdf_path, render_plan["profile"], subject)
    pdf_result = pdf_gate.analyze_pdf(pdf_path, "ARC_N", render_dir=output_dir / "render", dpi=144, expected_item_count=10)

    fault_results = []
    for fault_id, mutation in (
        ("ANSWER_KEY_MISSING", lambda data: data.pop("answer_key")),
        ("ANSWER_COUNT_SHORT", lambda data: data["answer_key"].pop(10)),
        ("STALE_PDF_MASTER", lambda data: data.update({"pdf_master": "ARC_PDF_LAYOUT_MASTER_V2.1"})),
        ("LAYOUT_DIRECTIVE", lambda data: data.update({"student_manuscript": data["student_manuscript"] + "\n\nUse body 8.8pt and two-column."})),
    ):
        changed = yaml.safe_load(yaml.safe_dump(bundle))
        try:
            mutation(changed)
            serializer.serialize_bundle(changed, manifest)
        except (serializer.SerializationError, KeyError) as exc:
            fault_results.append({"id": fault_id, "status": "BLOCKED", "message": str(exc)})
        else:
            fault_results.append({"id": fault_id, "status": "MISSED"})

    failures = []
    for name, status in (("CONTENT_QA", qa_result["status"]), ("HANDOFF", handoff_result["status"]), ("TYPESET", typeset_result["status"]), ("PDF_QC", pdf_result["status"])):
        if status != "PASS": failures.append(name)
    if any(item["status"] != "BLOCKED" for item in fault_results): failures.append("FAULT_INJECTION")
    return {
        "fixture_id": fixture["fixture_id"], "source_mode": fixture["source_mode"],
        "status": "CANARY_FAIL" if failures else "CANARY_PASS", "failures": failures,
        "stages": {"content_qa": qa_result["status"], "serializer": "PASS", "handoff_preflight": handoff_result["status"], "typesetter": typeset_result["status"], "pdf_preflight": pdf_result["status"]},
        "typeset": typeset_result, "pdf_qc": {"status": pdf_result["status"], "page_count": pdf_result["page_count"], "fail_count": pdf_result["fail_count"], "warn_count": pdf_result["warn_count"]},
        "render_plan": render_plan,
        "governance": {"FINAL_USER_APPROVAL": "NOT_APPLICABLE_CANARY", "DRIVE_SAVE": "BLOCKED"},
        "fault_injection": fault_results,
        "artifacts": {"qa_evidence": str(qa_path), "handoff": str(handoff_path), "pdf": str(pdf_path), "render_dir": str(output_dir / "render")},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=ROOT / "quality/canary/KOR_N_CANARY_V1.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = run(args.fixture, args.output_dir)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    report = args.report or args.output_dir / "canary-report.json"
    report.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "CANARY_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
