#!/usr/bin/env python3
"""Draft preview: run every content gate and typeset a REVIEW draft while exam scope is pending.

The normal production run stops at EXAM_SCOPE before rendering when the exam range is not
confirmed. Teachers still need to read a draft. This tool:

- runs the exam scope gate and reports its real result (never overridden),
- runs the same measurement, QA-evidence and content gates as production_pipeline.run,
- renders the same PDF layout, stamped DRAFT_PREVIEW in the file name,
- writes a teacher-only explanation file (정답·선지별 근거) from the bundle's judgments.

Its status is always DRAFT_PREVIEW_NOT_RELEASABLE. It skips handoff/typesetter admission
and never writes to Drive. A missing blind review is reported as pending, not passed.

    python tooling/production/draft_preview.py <bundle_dir> --output-dir <out>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_production_pipeline", ROOT / "tooling/production/production_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pipeline)

_spec = importlib.util.spec_from_file_location("arc_archetype_gate", ROOT / "tooling/korean/archetype_gate.py")
archetype_gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(archetype_gate)

CIRC = "①②③④⑤"


def explanations(bundle: dict, labels: dict[str, str]) -> str:
    lines = [f"# {bundle['set_label']} {bundle['course']} — 정답과 선지별 근거 (교사용)", "",
             f"범위: {bundle['scope']}", ""]
    for it in bundle["items"]:
        if it.get("format") == "CR":
            lines += [f"## {labels[it['item_id']]}  ({it.get('points', '')}점)", it["stem"],
                      f"- 모범 답안: {it['model_answer']}"] + [f"- 채점 기준: {r}" for r in it.get("rubric", [])] + [""]
            continue
        a = int(it["answer"])
        lines.append(f"## {labels[it['item_id']]}번  정답 {CIRC[a - 1]}  ({it['difficulty']}, {it['family']})")
        lines.append(it["stem"])
        for i, (opt, j) in enumerate(zip(it.get("options", []), it.get("judgments", [])), 1):
            mark = "정답" if i == a else ("2순위" if i == int(it["second_best"]) else "")
            shown = "" if opt == CIRC[i - 1] else f" {opt}"
            lines.append(f"- {CIRC[i - 1]}{shown} — {j['why']}" + (f" **[{mark}]**" if mark else ""))
        lines.append("")
    return "\n".join(lines)


def run(bundle_dir: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = yaml.safe_load((bundle_dir / "items.yaml").read_text(encoding="utf-8"))
    exam = pipeline.exam_gate.check_bundle(raw, ROOT / "SYSTEM_MANIFEST.yaml")
    bundle = pipeline.normalize(raw)
    blind_path = bundle_dir / "blind_review.yaml"
    blind = yaml.safe_load(blind_path.read_text(encoding="utf-8")) if blind_path.is_file() else {"items": []}
    for it in bundle["items"]:
        pipeline.resolve_figure(it, bundle_dir, f"item {it['item_id']}")
    for st in bundle["sets"]:
        for w in st["works"]:
            pipeline.resolve_figure(w, bundle_dir, f"set {st['id']}")
    sources = pipeline.load_sources(bundle["sets"], bundle["subject"])
    text = pipeline.manuscript(bundle, sources)
    (out_dir / "student_manuscript.md").write_text(text, encoding="utf-8")
    metrics = pipeline.measure(bundle, sources, blind, text)
    findings = metrics["findings"]
    qa = pipeline.qa_evidence(bundle, sources, blind, text, findings)
    qa_result = pipeline.content_gate.analyze(qa)
    labels = pipeline.numbering(bundle)
    pdf = out_dir / f"{bundle['batch_id']}_DRAFT_PREVIEW.pdf"
    key = out_dir / f"{bundle['batch_id']}_ANSWER_KEY_DRAFT_PREVIEW.pdf" if bundle["product_mode"] == "ARC_FINAL" else None
    render = pipeline.renderer.render(bundle, sources, labels, pipeline.set_header, pdf, key_pdf=key)
    pdf_qc = pipeline.pdf_gate.analyze_pdf(pdf, bundle["product_mode"],
                                           expected_item_count=len(pipeline.mcq_items(bundle)) if bundle["product_mode"] == "ARC_N" else None)
    (out_dir / f"{bundle['batch_id']}_EXPLANATIONS.md").write_text(explanations(bundle, labels), encoding="utf-8")

    # Author self-check: the key stands in for the blind solver, so only author-side defects remain.
    # This is NOT an independent review; blind-only codes are dropped from it.
    selfblind = {"reviewer": "AUTHOR_SELF_CHECK", "excluded_inputs": [], "items": [
        {"item_id": i["item_id"], "answer": i["answer"], "second_best": i["second_best"], "difficulty": i["difficulty"],
         "first_pass_top3": [i["answer"], i["second_best"]] + [k for k in range(1, 6) if k not in (i["answer"], i["second_best"])][:1],
         "flags": []} for i in pipeline.mcq_items(bundle)]}
    self_m = pipeline.measure(bundle, sources, selfblind, text)
    self_qa = pipeline.content_gate.analyze(pipeline.qa_evidence(bundle, sources, selfblind, text, self_m["findings"]))
    blind_only = {"BLIND_INPUT_LEAK", "BLIND_REVIEWER_MISSING"}
    selfcheck = sorted({(f["code"], f.get("item_id")) for f in self_m["findings"] + self_qa.get("findings", [])
                        if f.get("severity") == "FAIL" and f["code"] not in blind_only}, key=str)

    blind_missing = sum(1 for f in findings if f["code"] == "BLIND_REVIEW_MISSING")
    other_fail = [f for f in findings if f["severity"] == "FAIL" and f["code"] != "BLIND_REVIEW_MISSING"]
    qa_other = [f for f in qa_result.get("findings", []) if f.get("severity") == "FAIL"
                and "BLIND" not in f.get("code", "") and "PASS_B" not in f.get("code", "")]
    report = {
        "tool": "ARC_DRAFT_PREVIEW_V1.0", "batch_id": bundle["batch_id"], "status": "DRAFT_PREVIEW_NOT_RELEASABLE",
        "exam_scope": {"status": exam["status"], "codes": [f["code"] for f in exam["findings"]]},
        "blind_review": "PENDING" if blind_missing else "PRESENT",
        "author_selfcheck_failures": [{"code": c, "item_id": i} for c, i in selfcheck],
        "blind_missing_items": blind_missing,
        "author_side_failures": other_fail,
        "archetype_gate": archetype_gate.analyze(raw),
        "content_qa_status": qa_result["status"],
        "content_qa_non_blind_failures": qa_other,
        "metrics": {k: v for k, v in metrics.items() if k not in {"findings", "realism", "length_rows"}},
        "realism": metrics["realism"]["status"],
        "typeset": render["status"], "pages": render["pages"], "pdf_qc": pdf_qc["status"],
        "pdf": str(pdf), "answer_key_pdf": str(key) if key else None,
        "governance": {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED", "RELEASE": "BLOCKED"},
    }
    (out_dir / "draft_preview_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle_dir", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    report = run(args.bundle_dir, args.output_dir)
    print(json.dumps({k: report[k] for k in ("batch_id", "status", "exam_scope", "blind_review", "author_selfcheck_failures",
                                               "content_qa_status", "realism", "typeset", "pages", "pdf_qc")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
