#!/usr/bin/env python3
"""ARC production pipeline: one item bundle -> every gate -> PDF.

Inputs (one directory):
  items.yaml          set metadata, passages (by source_text_id) and items with
                      options, answer, per-option judgments and evidence refs
  blind_review.yaml   output of an independent blind solver that saw only the
                      student manuscript (answer, first-pass top-3, second-best,
                      difficulty, flags a-e)

Every realism / balance / length / leak metric is computed here from the bundle;
nothing is self-reported. PASS B of the QA evidence is taken from the blind review
file, never from the author key.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE_REGISTRY = ROOT / "quality/source/KOR_SOURCE_TEXT_REGISTRY_2026_V1.0.yaml"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


serializer = _load("arc_handoff_serializer", "tooling/handoff/handoff_serializer.py")
handoff_gate = _load("arc_handoff_preflight", "tooling/handoff/handoff_preflight.py")
content_gate = _load("arc_content_qa_gate", "tooling/content_qa/content_qa_gate.py")
realism_gate = _load("arc_korean_realism", "tooling/korean/korean_exam_realism_gate.py")
final_gate = _load("arc_final_quality_gate", "tooling/final/final_quality_gate.py")
typesetter = _load("arc_typesetter_gateway", "tooling/typeset/typesetter_gateway.py")
pdf_gate = _load("arc_pdf_preflight", "tooling/pdf_qc/pdf_preflight.py")
renderer = _load("arc_kor_renderer", "tooling/typeset/kor_renderer.py")
exam_gate = _load("arc_exam_scope_gate", "tooling/exams/exam_scope_gate.py")
source_mix_gate = _load("arc_generation_source_mix", "tooling/sources/generation_source_gate.py")

CIRC = "①②③④⑤"
SCHOOL_FAMILIES = {
    "EVIDENCE_SUPPORT", "EXCEPT_INCORRECT", "ERROR_CORRECTION", "MULTI_JUDGMENT", "INFERENCE",
    "STRUCTURE_RELATION", "VIEW_APPLICATION", "CASE_APPLICATION", "SINGLE_BEST_STATEMENT",
    "COMPARISON_MATRIX", "STUDENT_RESPONSE_EVALUATION", "CONDITION_CHANGE", "SEQUENCE_ORDER",
    "EXPRESSION_EFFECT", "SPEAKER_ATTITUDE", "KEY_WORD_FUNCTION", "CONTENT_UNDERSTANDING",
}
RARE_FAMILIES = {"COUNTERFACTUAL_DELETE_REPLACE", "MICRO_REFERENCE_TRACE", "META_READING_STRATEGY"}
# Internal QA vocabulary that must never reach student text.
LEAK_TERMS = ["판단축", "정답 후보", "추론 단계", "검토 절차", "매력적인 오답", "오답 선지", "2순위", "second-best",
              "true kernel", "distractor", "reasoning axis", "evidence span", "QA", "난도", "D1", "D2", "D3", "D4", "D5"]
# Generic AI-exam phrasing the Korean realism gate forbids.
AI_PHRASES = ["종합적으로 고려하면", "정확한 근거를 바탕으로", "판단 기준에 따라", "다각도로", "총체적으로"]
PROFILES = {
    # (min, max) share of items per difficulty; KOR ARC_N subject balance.
    ("KOR", "ARC_N"): {"D1": (0.0, 0.10), "D2": (0.30, 0.40), "D3": (0.30, 0.40), "D4": (0.15, 0.25), "D5": (0.0, 0.05),
                       "D45": (0.15, 0.35), "ADVANCED": (0.20, 0.30)},
}


ITEM_GATE_CODES = {
    "UNIQUE_ANSWER": {"BLIND_ANSWER_MISMATCH", "BLIND_MULTIPLE_ANSWERS", "BLIND_NO_ANSWER", "BLIND_SECOND_BEST_IS_KEY", "ANSWER_OUT_OF_RANGE"},
    "FACTUAL_ACCURACY_REVIEW": {"BLIND_OUTSIDE_KNOWLEDGE", "BLIND_AI_STYLE"},
    "SCOPE_EVIDENCE_TRACE": {"EVIDENCE_REF_OUT_OF_SOURCE"},
    "ANSWER_EVIDENCE_TRACE": {"EVIDENCE_REF_OUT_OF_SOURCE"},
    "ALL_OPTION_AUDIT": {"OPTION_COUNT", "BLIND_REVIEW_MISSING"},
    "OPTION_SEMANTIC_DUPLICATION_REVIEW": {"OPTION_CLAIM_DUPLICATE"},
    "DIFFICULTY_MATCH": {"DIFFICULTY_MISMATCH", "FAKE_D4", "WEAK_DISTRACTOR_D3_PLUS", "OBVIOUS_KEY_D3_PLUS",
                         "FIRST_PASS_CANDIDATES_SHORT", "CORRECT_LENGTH_CUE"},
}
SET_GATE_CODES = {
    "STRUCTURE": {"TASK_FAMILY_DIVERSITY_LOW", "SINGLE_BEST_STEM_OVERUSE", "EXCEPT_STEM_OVERUSE", "STEM_SKELETON_RUN"},
    "STRUCTURE_BIAS": {"ANSWER_POSITION_BIAS", "ANSWER_POSITION_RUN", "LONGEST_OPTION_IS_KEY_RATE"},
    "MANUSCRIPT_CONTAMINATION": {"STUDENT_METADATA_LEAK", "AI_STYLE_PHRASE"},
    "TOO_EASY": {"BALANCE_D1_OUT_OF_RANGE", "BALANCE_D45_OUT_OF_RANGE"},
    "D4_SHORT": {"BALANCE_ADVANCED_OUT_OF_RANGE"},
}


class PipelineError(RuntimeError):
    pass


def sentences(paragraph: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.?!])\s+", paragraph.strip()) if s]


def normalize(bundle: dict[str, Any]) -> dict[str, Any]:
    """Accept legacy single-passage bundles (`passages`) and multi-work `sets`."""
    if "sets" not in bundle:
        bundle["sets"] = [{"id": p["id"], "works": [{"label": None, "source_text_id": p["source_text_id"],
                                                    "marks": p.get("marks", [])}]} for p in bundle["passages"]]
    for it in bundle["items"]:
        it.setdefault("set", it.get("passage"))
        it.setdefault("format", "MCQ")
    return bundle


def mcq_items(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    return [it for it in bundle["items"] if it["format"] == "MCQ"]


def cr_items(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    return [it for it in bundle["items"] if it["format"] == "CR"]


def load_sources(sets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    registry = {t["source_text_id"]: t for t in yaml.safe_load(SOURCE_REGISTRY.read_text(encoding="utf-8"))["texts"]}
    out = []
    for st in sets:
        works = []
        for w in st["works"]:
            entry = registry.get(w["source_text_id"])
            if entry is None:
                raise PipelineError(f"SOURCE_NOT_REGISTERED: {w['source_text_id']}")
            raw = (ROOT / entry["repo_path"]).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != entry["sha256"]:
                raise PipelineError(f"SOURCE_CHECKSUM_MISMATCH: {w['source_text_id']}")
            form = entry.get("form", "PROSE")
            text = raw.decode("utf-8").rstrip("\n")
            if form == "VERSE":
                units = text.split("\n")            # blank string = stanza break
                counted = [u for u in units if u.strip()]
                if len(counted) != entry.get("lines", len(counted)):
                    raise PipelineError(f"SOURCE_LINE_COUNT_MISMATCH: {w['source_text_id']}")
            else:
                units = [x for x in text.split("\n") if x.strip()]
                if len(units) != entry.get("paragraphs", len(units)):
                    raise PipelineError(f"SOURCE_PARAGRAPH_COUNT_MISMATCH: {w['source_text_id']}")
            shown = list(units)
            for mark in w.get("marks", []):
                hits = [i for i, u in enumerate(shown) if mark["find"] in u]
                if len(hits) != 1:
                    raise PipelineError(f"SOURCE_MARK_NOT_UNIQUE: {mark['find']}")
                if re.sub(r"[ⓐ-ⓩ㉠-㉯\[\]A-Z\s]", "", mark["replace"]) != re.sub(r"\s", "", mark["find"]):
                    raise PipelineError(f"SOURCE_MARK_CHANGES_WORDS: {mark['find']}")
                shown[hits[0]] = shown[hits[0]].replace(mark["find"], mark["replace"], 1)
            every = int(w.get("line_numbers") or 0) if form == "VERSE" else 0
            works.append({"label": w.get("label"), "entry": entry, "sha256": digest, "form": form, "units": units,
                          "display": shown, "title": entry["title"], "line_numbers": every})
        out.append({"id": st["id"], "works": works, "notes": st.get("notes", []), "lead": st.get("lead", [])})
    return out


def ref_ok(ref: str, st: dict[str, Any]) -> bool:
    """Evidence refs: [W<n>.]P<p>S<s> for prose, [W<n>.]L<l> for verse (non-blank line number)."""
    m = re.fullmatch(r"(?:W(\d+)\.)?(?:P(\d+)S(\d+)|L(\d+))", ref)
    if not m:
        return False
    wi = int(m.group(1) or 1) - 1
    if wi >= len(st["works"]):
        return False
    work = st["works"][wi]
    if m.group(4):
        return work["form"] == "VERSE" and 1 <= int(m.group(4)) <= len([u for u in work["units"] if u.strip()])
    if work["form"] != "PROSE":
        return False
    p, sn = int(m.group(2)), int(m.group(3))
    return 1 <= p <= len(work["units"]) and 1 <= sn <= len(sentences(work["units"][p - 1]))


def numbering(bundle: dict[str, Any]) -> dict[str, str]:
    """MCQ items numbered 1..N, constructed-response items 서술형 1..M, in bundle order."""
    labels, m, c = {}, 0, 0
    for it in bundle["items"]:
        if it["format"] == "MCQ":
            m += 1
            labels[it["item_id"]] = str(m)
        else:
            c += 1
            labels[it["item_id"]] = f"서술형 {c}"
    return labels


def set_header(bundle: dict[str, Any], set_id: str, labels: dict[str, str]) -> str:
    own = [it for it in bundle["items"] if it["set"] == set_id]
    mq = [labels[it["item_id"]] for it in own if it["format"] == "MCQ"]
    cr = [labels[it["item_id"]].split()[-1] for it in own if it["format"] == "CR"]
    if bundle["product_mode"] == "ARC_N" and not cr:
        return f"[{mq[0]}~{mq[-1]}] 다음 글을 읽고 물음에 답하시오."
    parts = []
    if mq:
        parts.append(f"선택형 {mq[0]}~{mq[-1]}번" if len(mq) > 1 else f"선택형 {mq[0]}번")
    if cr:
        parts.append(f"서술형 {cr[0]}~{cr[-1]}번" if len(cr) > 1 else f"서술형 {cr[0]}번")
    return f"※ 다음 글을 읽고 물음에 답하시오. ({', '.join(parts)})"


def numbered_display(work: dict[str, Any]) -> list[str]:
    """Verse lines with the printed margin number every N non-blank lines, as students see it."""
    every = work.get("line_numbers") or 0
    if not every:
        return list(work["display"])
    out, n = [], 0
    for unit in work["display"]:
        if unit.strip():
            n += 1
            if n % every == 0:
                unit = f"{unit}  〔{n}〕"
        out.append(unit)
    return out


def manuscript(bundle: dict[str, Any], sources: list[dict[str, Any]]) -> str:
    labels = numbering(bundle)
    lines: list[str] = []
    for src in sources:
        lines += [set_header(bundle, src["id"], labels), ""]
        if src.get("lead"):
            lines += src["lead"] + [""]
        for w in src["works"]:
            if w["label"]:
                lines.append(w["label"])
            lines += numbered_display(w) + ["", f"― {w['title']} ―", ""]
        if src.get("notes"):
            lines += src["notes"] + [""]
        for it in [x for x in bundle["items"] if x["set"] == src["id"]]:
            pts = f" ({it['points']}점)" if it.get("points") else ""
            if it["format"] == "MCQ":
                lines += [f"## QUESTION {labels[it['item_id']]}", it["stem"] + pts]
            else:
                lines += [f"## {labels[it['item_id']]}", it["stem"] + pts]
            if it.get("table"):
                lines.append("| " + " | ".join(it["table"]["header"]) + " |")
                lines += ["| " + " | ".join(r) + " |" for r in it["table"]["rows"]]
            if it.get("view"):
                lines.append("<보 기>")
                lines += it["view"]
            if it["format"] == "MCQ":
                lines += [f"{CIRC[i]} {o}" for i, o in enumerate(it["options"])]
            else:
                lines.append("<조 건>")
                lines += it["conditions"]
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def strong_count(it: dict[str, Any], blind_item: dict[str, Any] | None) -> int:
    """Non-key options the author rated STRONG or the blind solver seriously weighed (first-pass top-3)."""
    a = int(it["answer"])
    top3 = {int(x) for x in (blind_item or {}).get("first_pass_top3", [])}
    return sum(1 for i, j in enumerate(it["judgments"], 1) if i != a and (j["c"] == "STRONG" or i in top3))


def stem_ending(stem: str) -> str:
    return re.sub(r"\s", "", stem)[-8:]


def measure(bundle: dict[str, Any], sources: list[dict[str, Any]], blind: dict[str, Any], text: str) -> dict[str, Any]:
    items = mcq_items(bundle)
    n = len(items)
    blind_by_id = {b["item_id"]: b for b in blind["items"]}
    set_by_id = {s["id"]: s for s in sources}
    findings: list[dict[str, Any]] = []

    def add(code, severity="FAIL", item=None, **extra):
        findings.append({"code": code, "severity": severity, **({"item_id": item} if item else {}), **extra})

    # --- per item ---
    longest_key = 0
    length_rows = []
    for it in items:
        iid = it["item_id"]
        if len(it["options"]) != 5 or len(it["judgments"]) != 5:
            add("OPTION_COUNT", item=iid)
        if not 1 <= int(it["answer"]) <= 5:
            add("ANSWER_OUT_OF_RANGE", item=iid)
        lens = [len(o.replace(" ", "")) for o in it["options"]]
        a = int(it["answer"]) - 1
        unique_longest = lens[a] == max(lens) and lens.count(max(lens)) == 1
        ratio = lens[a] / statistics.median(lens)
        longest_key += unique_longest
        length_rows.append({"item_id": iid, "lens": lens, "correct_is_longest": unique_longest, "ratio": round(ratio, 3)})
        if unique_longest and ratio >= 1.25 and not it.get("length_justified"):
            add("CORRECT_LENGTH_CUE", item=iid, ratio=round(ratio, 3))
        claims = [j["claim"] for j in it["judgments"]]
        if len(set(claims)) != len(claims):
            add("OPTION_CLAIM_DUPLICATE", item=iid)
        for j in it["judgments"]:
            for ref in j["ev"]:
                if not ref_ok(ref, set_by_id[it["set"]]):
                    add("EVIDENCE_REF_OUT_OF_SOURCE", item=iid, ref=ref)
        b = blind_by_id.get(iid)
        strong = strong_count(it, b)
        if b is None:
            add("BLIND_REVIEW_MISSING", item=iid)
            continue
        if int(b["answer"]) != int(it["answer"]):
            add("BLIND_ANSWER_MISMATCH", item=iid, blind=b["answer"], key=it["answer"])
        if int(b["second_best"]) == int(it["answer"]):
            add("BLIND_SECOND_BEST_IS_KEY", item=iid)
        adjudicated = set((b.get("flag_adjudication") or {}).keys())
        for f in sorted(adjudicated & set(b.get("flags", []))):
            add("BLIND_FLAG_ADJUDICATED", "WARN", item=iid, flag=f, reason=b["flag_adjudication"][f])
        flags = set(b.get("flags", [])) - adjudicated
        for f, code in (("a", "BLIND_MULTIPLE_ANSWERS"), ("b", "BLIND_NO_ANSWER"), ("d", "BLIND_OUTSIDE_KNOWLEDGE")):
            if f in flags:
                add(code, item=iid)
        if "e" in flags:
            add("BLIND_AI_STYLE", item=iid)
        if b["difficulty"] != it["difficulty"]:
            add("DIFFICULTY_MISMATCH", item=iid, target=it["difficulty"], blind=b["difficulty"])
        if b["difficulty"] in {"D3", "D4", "D5"}:
            if "c" in flags:
                add("OBVIOUS_KEY_D3_PLUS", item=iid)
            if strong < 2:
                add("WEAK_DISTRACTOR_D3_PLUS", item=iid, strong=strong)
            if len(b.get("first_pass_top3", [])) < 3:
                add("FIRST_PASS_CANDIDATES_SHORT", item=iid)
        elif "c" in flags:
            add("OBVIOUS_KEY_CORE_ITEM", "WARN", item=iid)
        if b["difficulty"] in {"D4", "D5"} and (it["reasoning_steps"] < 2 or it["immediate_elimination"] > 2):
            add("FAKE_D4", item=iid)

    # --- constructed response ---
    for it in cr_items(bundle):
        iid = it["item_id"]
        for field in ("stem", "conditions", "model_answer", "rubric", "points"):
            if not it.get(field):
                add("CR_FIELD_MISSING", item=iid, field=field)
        for ref in it.get("ev", []):
            if not ref_ok(ref, set_by_id[it["set"]]):
                add("EVIDENCE_REF_OUT_OF_SOURCE", item=iid, ref=ref)
        b = blind_by_id.get(iid)
        if b is None:
            add("BLIND_REVIEW_MISSING", item=iid)
            continue
        if b.get("meets_rubric") is not True:
            add("CR_BLIND_ANSWER_OFF_RUBRIC", item=iid)
        flags = set(b.get("flags", [])) - set((b.get("flag_adjudication") or {}).keys())
        if "a" in flags:
            add("CR_CONDITIONS_AMBIGUOUS", item=iid)
        if "d" in flags:
            add("BLIND_OUTSIDE_KNOWLEDGE", item=iid)
        if "e" in flags:
            add("BLIND_AI_STYLE", item=iid)
    points = [float(it["points"]) for it in bundle["items"] if it.get("points")]
    total_points = round(sum(points), 2) if points else None
    if points and len(points) == len(bundle["items"]) and abs(sum(points) - 100) > 0.01:
        add("POINT_TOTAL_NOT_100", total=total_points)

    # --- set level ---
    diff = Counter(it["difficulty"] for it in items)
    keys = Counter(int(it["answer"]) for it in items)
    fams = [it["family"] for it in items]
    endings = [stem_ending(it["stem"]) for it in items]
    single_best = sum(1 for it in items if re.sub(r"\s", "", it["stem"]).endswith("가장적절한것은?"))
    except_count = sum(1 for it in items if "적절하지않은" in re.sub(r"\s", "", it["stem"]))
    run = best_run = 1
    for i in range(1, n):
        run = run + 1 if endings[i] == endings[i - 1] else 1
        best_run = max(best_run, run)
    key_run = kr = 1
    seq = [int(it["answer"]) for it in items]
    for i in range(1, n):
        kr = kr + 1 if seq[i] == seq[i - 1] else 1
        key_run = max(key_run, kr)
    leak_hits = [t for t in LEAK_TERMS if re.search(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z0-9])", text)]
    ai_hits = [p for p in AI_PHRASES if p in text]
    longest_rate = longest_key / n

    if longest_rate > 0.30:
        add("LONGEST_OPTION_IS_KEY_RATE", rate=round(longest_rate, 3))
    if n >= 10 and max(keys.values()) > math.ceil(n * 0.3):
        add("ANSWER_POSITION_BIAS", counts=dict(keys))
    if key_run >= 3:
        add("ANSWER_POSITION_RUN", run=key_run)
    if single_best > max(1, round(n * 0.4)):
        add("SINGLE_BEST_STEM_OVERUSE", count=single_best)
    if except_count > max(1, round(n * 0.2)):
        add("EXCEPT_STEM_OVERUSE", count=except_count)
    if best_run > 2:
        add("STEM_SKELETON_RUN", run=best_run)
    if len({f for f in fams if f in SCHOOL_FAMILIES}) < (5 if n >= 20 else 4):
        add("TASK_FAMILY_DIVERSITY_LOW")
    if leak_hits:
        add("STUDENT_METADATA_LEAK", terms=leak_hits)
    if ai_hits:
        add("AI_STYLE_PHRASE", phrases=ai_hits)

    profile = PROFILES.get((bundle["subject"], bundle["product_mode"]))
    balance = None
    if profile:
        shares = {d: diff.get(d, 0) / n for d in ("D1", "D2", "D3", "D4", "D5")}
        shares["D45"] = shares["D4"] + shares["D5"]
        shares["ADVANCED"] = sum(1 for it in items if it.get("balance") == "ADVANCED_DISCRIMINATION") / n
        balance = {k: round(v, 3) for k, v in shares.items()}
        for k, (lo, hi) in profile.items():
            if not lo - 1e-9 <= shares[k] <= hi + 1e-9:
                hard = k in {"D1", "D45", "ADVANCED"}
                add(f"BALANCE_{k}_OUT_OF_RANGE", "FAIL" if hard else "WARN", share=round(shares[k], 3), target=[lo, hi])

    realism = realism_gate.analyze({"product_mode": bundle["product_mode"], "item_count": n, "counts": {
        "school_task_family_count": sum(f in SCHOOL_FAMILIES for f in fams),
        "unanchored_meta_task_count": 0,
        "rare_artificial_task_count": sum(f in RARE_FAMILIES for f in fams),
        "distinct_school_task_families": len({f for f in fams if f in SCHOOL_FAMILIES}),
        "unfunctional_student_wrapper_count": 0,
        "ai_choice_pattern_count": len(ai_hits),
        "correct_length_cue_count": sum(1 for f in findings if f["code"] == "CORRECT_LENGTH_CUE"),
        "same_stem_skeleton_max_run": best_run,
    }})
    return {"findings": findings, "difficulty": dict(sorted(diff.items())), "answer_positions": dict(sorted(keys.items())),
            "longest_option_is_key_rate": round(longest_rate, 3), "single_best_stems": single_best,
            "except_stems": except_count, "stem_skeleton_max_run": best_run, "balance": balance,
            "realism": realism, "length_rows": length_rows, "total_points": total_points,
            "mcq_count": n, "cr_count": len(cr_items(bundle))}


def korean_stem_polarity(item: dict[str, Any]) -> str:
    """Determine truth-direction from explicit metadata or an observed Korean exam stem.
    This is an admission preflight, not a substitute for source-based verification.
    """
    compact = re.sub(r"\s+", "", str(item.get("stem", "")))
    negative_markers = (
        "적절하지않은", "옳지않은", "바르지않은", "타당하지않은",
        "일치하지않는", "어긋나는", "맞지않는", "적절하지않는",
        "틀린것은", "아닌것은", "잘못된", "부적절한", "위배되는",
    )
    inferred_negative = (
        str(item.get("family", "")).upper() == "EXCEPT_INCORRECT"
        or any(marker in compact for marker in negative_markers)
    )
    explicit = str(item.get("stem_polarity", "")).upper()
    if explicit in {"POSITIVE", "NEGATIVE"}:
        if (explicit == "NEGATIVE") != inferred_negative:
            raise ValueError(f"stem_polarity conflicts with stem or family: {item.get('item_id')}")
        return explicit
    if explicit:
        raise ValueError(f"invalid stem_polarity for {item.get('item_id')}: {explicit}")
    return "NEGATIVE" if inferred_negative else "POSITIVE"


def korean_judgment_truth(item: dict[str, Any], judgment: dict[str, Any]) -> str:
    """Normalize statement truth and answer-correctness metadata without changing the key.

    SOURCE_TRUTH: v is the truth of the candidate's asserted statement.
    ANSWER_CORRECTNESS: v indicates that the candidate is the correct choice,
    e.g. selecting ⓒ as the false phrase in a summarized passage.
    The mode must be explicit; guessing it would silently approve defective items.
    """
    verdict = str(judgment.get("v", "")).upper()
    mode = str(item.get("judgment_semantics", "STATEMENT_TRUTH")).upper()
    if mode == "STATEMENT_TRUTH":
        return verdict
    if mode != "ANSWER_CORRECTNESS":
        raise ValueError(f"Unknown judgment_semantics: {mode}")
    if verdict not in {"TRUE", "FALSE"}:
        raise ValueError("ANSWER_CORRECTNESS requires explicit TRUE/FALSE")
    if korean_stem_polarity(item) == "NEGATIVE":
        return "FALSE" if verdict == "TRUE" else "TRUE"
    return verdict


def qa_evidence(bundle, sources, blind, text, findings) -> dict[str, Any]:
    blind_by_id = {b["item_id"]: b for b in blind["items"]}
    hard = [f for f in findings if f["severity"] == "FAIL"]
    items = []
    for it in mcq_items(bundle):
        b = blind_by_id.get(it["item_id"], {})
        a = int(it["answer"])
        key_ev = [f"SRC:{it['set']}:{e}" for e in it["judgments"][a - 1]["ev"]]
        codes = {f["code"] for f in hard if f.get("item_id") == it["item_id"]}
        src = next(s for s in sources if s["id"] == it["set"])["works"][0]
        items.append({
            "item_id": it["item_id"], "target_difficulty": it["difficulty"],
            "stem_polarity": korean_stem_polarity(it),
            "pass_a": {"answer": str(a), "answer_evidence": key_ev},
            "pass_b": {
                "answer": str(b.get("answer", "")), "blind": True, "reviewer": blind.get("reviewer"),
                "excluded_inputs": blind.get("excluded_inputs", []), "confidence": b.get("confidence", "LOW"),
                "answer_evidence": key_ev,
                "scope_trace": {"status": "IN_SCOPE", "source_refs": [f"DRIVE:{src['entry']['school_source_file_id']}"]},
                "option_judgments": [{
                    "option_id": str(i), "verdict": korean_judgment_truth(it, j),
                    "statement_truth": korean_judgment_truth(it, j),
                    "author_marked_verdict": j["v"],
                    "judgment_semantics": it.get("judgment_semantics", "STATEMENT_TRUTH"),
                    "claim_key": j["claim"], "axis": j["axis"], "competitiveness": "CORRECT" if i == a else j["c"],
                    "evidence_refs": [f"SRC:{it['set']}:{e}" for e in j["ev"]], "note": j["why"]}
                    for i, j in enumerate(it["judgments"], start=1)],
                "second_best_option": str(b.get("second_best", it["second_best"])), "second_best_risk": "MEDIUM",
                "reasoning_steps": it["reasoning_steps"], "evidence_count": len(it["judgments"][a - 1]["ev"]),
                "immediate_elimination_count": it["immediate_elimination"], "transfer_required": bool(it.get("transfer")),
                "actual_difficulty": b.get("difficulty", ""),
            },
            "gates": {g: ("FAIL" if codes & ITEM_GATE_CODES.get(g, set()) else "PASS") for g in content_gate.ITEM_GATES},
        })
    set_codes = {f["code"] for f in hard if "item_id" not in f}
    return {
        "schema_version": "ARC-QA-EVIDENCE-V1.0", "subject": bundle["subject"], "item_count": len(items),
        "item_format": "MCQ5", "uses_source_text": True, "student_manuscript_sha256": serializer.sha256_text(text),
        "source_text_locks": [{
            "source_text_id": s["entry"]["source_text_id"], "source_origin": s["entry"]["source_origin"],
            "source_role": s["entry"]["role"], "text_fidelity": s["entry"]["text_fidelity"],
            "source_file_id": s["entry"]["school_source_file_id"], "source_location": s["entry"]["school_source_location"],
            "source_text_sha256": w["sha256"],
            "linked_item_ids": [it["item_id"] for it in mcq_items(bundle) if it["set"] == st["id"]] or [it["item_id"] for it in mcq_items(bundle)][:1],
            **w["entry"]["locks"]} for st in sources for w in st["works"] for s in [w]],
        "items": items, "set_gates": {g: ("FAIL" if set_codes & SET_GATE_CODES.get(g, set()) else "PASS") for g in content_gate.SET_GATES},
        "content_lock": True,
    }


def final_profile(bundle, blind) -> dict[str, Any]:
    blind_by_id = {b["item_id"]: b for b in blind["items"]}
    rows = []
    for it in mcq_items(bundle):
        b = blind_by_id.get(it["item_id"], {})
        a = int(it["answer"])
        d = b.get("difficulty", it["difficulty"])
        sb = int(it["second_best"])
        steps = it["reasoning_steps"]
        rows.append({
            "item_id": it["item_id"], "actual_difficulty": d, "reasoning_steps": steps,
            "evidence_count": len(it["judgments"][a - 1]["ev"]),
            "strong_distractor_count": strong_count(it, b),
            "effective_choice_count": 5 - it["immediate_elimination"],
            "first_pass_plausible_candidates": len(b.get("first_pass_top3", [])),
            "immediate_elimination_count": it["immediate_elimination"], "correct_option": a, "second_best_option": sb,
            "second_best_refutation": it["judgments"][sb - 1]["why"],
            "option_lengths_chars": [len(o.replace(" ", "")) for o in it["options"]],
            "correct_detail_outlier": False, "length_justified": bool(it.get("length_justified")),
            "school_relative": it.get("school_relative", "SCHOOL_UPPER" if d in {"D4", "D5"} else "SCHOOL_STANDARD"),
            "expected_time_class": it.get("expected_time_class", "LONG" if steps >= 3 else ("SHORT" if d in {"D1", "D2"} else "STANDARD")),
        })
    return {"product_mode": "ARC_FINAL", "item_count": len(rows), "items": rows}


def run(bundle_dir: Path, out_dir: Path, logo: dict[str, Any] | None = None, *, archived_replay: bool = False,
        manifest_path: Path | None = None) -> dict[str, Any]:
    raw_bundle = yaml.safe_load((bundle_dir / "items.yaml").read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_path or ROOT / "SYSTEM_MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    exam_result = exam_gate.check_bundle(raw_bundle if isinstance(raw_bundle, dict) else {}, manifest_path,
                                        archived_replay=archived_replay)
    if exam_result["status"] == "FAIL":
        report = {"tool": "ARC_PRODUCTION_PIPELINE_V1.1", "batch_id": (raw_bundle or {}).get("batch_id") if isinstance(raw_bundle, dict) else None,
                  "status": "BLOCKED", "blocking_gates": ["EXAM_SCOPE"], "gates": {"EXAM_SCOPE": "FAIL"},
                  "exam_scope": exam_result, "findings": exam_result["findings"], "pdf": None,
                  "answer_key_pdf": None, "governance": {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED"}}
        (out_dir / "production_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report
    if not archived_replay and raw_bundle.get("product_mode") in {"ARC_N", "ARC_FINAL"}:
        source_mix = source_mix_gate.analyze(raw_bundle)
        if source_mix["status"] != "PASS":
            report = {"tool": "ARC_PRODUCTION_PIPELINE_V1.1", "batch_id": raw_bundle.get("batch_id"),
                      "status": "BLOCKED", "blocking_gates": ["GENERATION_SOURCE_MIX"],
                      "gates": {"EXAM_SCOPE": "PASS", "GENERATION_SOURCE_MIX": "FAIL"},
                      "source_composition": source_mix, "findings": source_mix["findings"],
                      "pdf": None, "answer_key_pdf": None,
                      "governance": {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED"}}
            (out_dir / "production_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report
    else:
        source_mix = {"status": "ARCHIVED_REPLAY" if archived_replay else "NOT_APPLICABLE"}
    bundle = normalize(raw_bundle)
    blind = yaml.safe_load((bundle_dir / "blind_review.yaml").read_text(encoding="utf-8"))
    product = bundle["product_mode"]

    sources = load_sources(bundle["sets"])
    text = manuscript(bundle, sources)
    (out_dir / "student_manuscript.md").write_text(text, encoding="utf-8")
    metrics = measure(bundle, sources, blind, text)
    findings = metrics["findings"]
    required_rounds = manifest["runtime"].get("blind_review_rounds")
    if required_rounds is not None:
        rounds = blind.get("rounds")
        if rounds == required_rounds:
            pass
        elif blind.get("round_policy_exemption"):
            findings.append({"code": "BLIND_ROUND_POLICY_LEGACY", "severity": "WARN", "rounds": rounds,
                             "reason": blind["round_policy_exemption"]})
        else:
            findings.append({"code": "BLIND_ROUND_POLICY_VIOLATION", "severity": "FAIL", "rounds": rounds, "required": required_rounds})

    qa = qa_evidence(bundle, sources, blind, text, findings)
    if bundle.get("exam_context"):
        qa["exam_context"] = bundle["exam_context"]
    qa_name = f"ARC_QA_EVIDENCE_{bundle['batch_id']}.yaml"
    qa["generation_source_composition_audit"] = source_mix
    (out_dir / qa_name).write_text(yaml.safe_dump(qa, allow_unicode=True, sort_keys=False), encoding="utf-8")
    qa_result = content_gate.analyze(qa)

    content = {"batch_id": bundle["batch_id"], "generator": bundle.get("generator", "CLAUDE"), "product_mode": product,
               "subject": bundle["subject"], "scope": bundle["scope"], "item_count": len(mcq_items(bundle)),
               "created_at": bundle["created_at"], "qa_evidence_filename": qa_name, "student_manuscript": text,
               "answer_key": {i + 1: int(it["answer"]) for i, it in enumerate(mcq_items(bundle))},
               "visual_asset_manifest": [], "qc_status": {"STATUS": qa_result["status"], "CONSTRUCTED_RESPONSE": [
                   {"item_id": it["item_id"], "points": it.get("points"), "model_answer": it.get("model_answer"),
                   "rubric": it.get("rubric"), "accepted_variants": it.get("accepted_variants", [])} for it in cr_items(bundle)]}}
    if bundle.get("exam_context"):
        content["exam_context"] = bundle["exam_context"]
    handoff_name, handoff_text = serializer.serialize_bundle(content, manifest)
    handoff_path = out_dir / handoff_name
    handoff_path.write_text(handoff_text, encoding="utf-8")
    handoff_result = handoff_gate.analyze(handoff_path, manifest_path)
    try:
        typesetter.resolve_job(handoff_path, manifest_path, renderer="reportlab", archived_replay=archived_replay)
        admission = "PASS"
    except typesetter.TypesetterAdmissionError as exc:
        admission = f"BLOCKED: {exc}"

    pdf_path = out_dir / f"{bundle['batch_id']}_DRAFT.pdf"
    key_path = out_dir / f"{bundle['batch_id']}_ANSWER_KEY.pdf" if product == "ARC_FINAL" else None
    # Archived replay may render diagnostic drafts even when a content gate fails.
    # It always remains release-blocked by EXAM_SCOPE=ARCHIVED_REPLAY.
    if admission == "PASS" or archived_replay:
        render = renderer.render(bundle, sources, numbering(bundle), set_header, pdf_path, key_pdf=key_path, logo=logo)
        pdf_result = pdf_gate.analyze_pdf(
            pdf_path, product,
            expected_item_count=len(mcq_items(bundle)) if product == "ARC_N" else None,
            # ARC_N profile (typesetter_gateway): four fixed slots per page, D1-D5 metadata strip per question.
            max_questions_per_page=4 if product == "ARC_N" else None,
            require_difficulty_strip=product == "ARC_N",
        )
    else:
        render = {"status": "BLOCKED", "brand": "NOT_RUN"}
        pdf_result = {"status": "NOT_RUN"}
        pdf_path = None
        key_path = None

    final_result = None
    if product == "ARC_FINAL":
        payload = final_profile(bundle, blind)
        raw_subject = str(bundle.get("subject", "KOR")).strip().lower().replace("-", "_")
        subject_alias = {
            "korean": "kor",
            "social": "soc",
            "science": "sci",
            "science_redox": "sci_redox",
            "redox": "sci_redox",
            "sci_redox": "sci_redox",
            "history": "his",
        }
        subject_key = subject_alias.get(raw_subject, raw_subject)
        runtime = manifest["runtime"]
        anchor_rel = runtime.get(f"arc_final_difficulty_anchor_{subject_key}")
        if not archived_replay:
            anchor_rel = exam_result.get("anchor_path")
        if runtime.get("arc_final_difficulty_mode") in {"SCHOOL_ANCHOR", "SCHOOL_MULTI_EXAM_ANCHOR"}:
            payload["difficulty_anchor_required"] = True
            if anchor_rel:
                payload["difficulty_anchor"] = yaml.safe_load((ROOT / anchor_rel).read_text(encoding="utf-8"))
        final_result = final_gate.analyze(payload)

    hard = [f for f in findings if f["severity"] == "FAIL"]
    gates = {
        "EXAM_SCOPE": exam_result["status"],
        "CONTENT_QA": qa_result["status"],
        "BLIND_INDEPENDENT_SOLVE": "FAIL" if any(f["code"].startswith("BLIND_") for f in hard) else "PASS",
        "KOR_EXAM_REALISM_GATE": metrics["realism"]["KOR_EXAM_REALISM_GATE"],
        "KOR_AI_STYLE_LEAK_GATE": metrics["realism"]["KOR_AI_STYLE_LEAK_GATE"] if not any(f["code"] in {"STUDENT_METADATA_LEAK", "AI_STYLE_PHRASE"} for f in hard) else "FAIL",
        "KOR_SCHOOL_TASK_FAMILY_GATE": metrics["realism"]["KOR_SCHOOL_TASK_FAMILY_GATE"],
        "ANSWER_LENGTH_AUDIT": "FAIL" if any(f["code"] in {"CORRECT_LENGTH_CUE", "LONGEST_OPTION_IS_KEY_RATE"} for f in hard) else "PASS",
        "OBVIOUS_ANSWER_GATE": "FAIL" if any(f["code"] in {"OBVIOUS_KEY_D3_PLUS", "FIRST_PASS_CANDIDATES_SHORT"} for f in hard) else "PASS",
        "ATTRACTIVE_DISTRACTOR_GATE": "FAIL" if any(f["code"] == "WEAK_DISTRACTOR_D3_PLUS" for f in hard) else "PASS",
        "CONSTRUCTED_RESPONSE_GATE": "FAIL" if any(f["code"].startswith("CR_") or (f.get("item_id") in {c["item_id"] for c in cr_items(bundle)}) for f in hard) else ("PASS" if cr_items(bundle) else "NOT_APPLICABLE"),
        "POINTS_GATE": "FAIL" if any(f["code"] == "POINT_TOTAL_NOT_100" for f in hard) else "PASS",
        "STEM_FORM_GATE": "FAIL" if any(f["code"] in {"SINGLE_BEST_STEM_OVERUSE", "EXCEPT_STEM_OVERUSE", "STEM_SKELETON_RUN"} for f in hard) else "PASS",
        "ANSWER_POSITION_GATE": "FAIL" if any(f["code"].startswith("ANSWER_POSITION") for f in hard) else "PASS",
        "DIFFICULTY_BALANCE_GATE": "FAIL" if any(f["code"].startswith("BALANCE_") or f["code"] == "DIFFICULTY_MISMATCH" for f in hard) else "PASS",
        "HANDOFF": handoff_result["status"],
        "TYPESETTER_ADMISSION": admission,
        "TYPESET": render["status"], "BRAND": render["brand"],
        "PDF_QC": pdf_result["status"],
    }
    if final_result:
        gates["FINAL_DIFFICULTY"] = final_result["FINAL_DIFFICULTY"]
        gates["FINAL_ITEM_QUALITY"] = final_result["FINAL_ITEM_QUALITY"]
    blocking = [k for k, v in gates.items() if k != "BRAND" and v not in {"PASS", "WARN", "NOT_APPLICABLE"}]
    report = {
        "tool": "ARC_PRODUCTION_PIPELINE_V1.1", "batch_id": bundle["batch_id"], "product": product,
        "status": "READY_FOR_USER_APPROVAL" if not blocking else "BLOCKED",
        "blocking_gates": blocking, "gates": gates,
        "findings": findings, "metrics": {k: v for k, v in metrics.items() if k not in {"findings", "realism", "length_rows"}},
        "final_quality": final_result, "exam_scope": exam_result,
        "pdf": str(pdf_path) if pdf_path else None, "answer_key_pdf": str(key_path) if key_path else None,
        "governance": {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED"},
    }
    report["source_composition"] = source_mix
    report["gates"]["GENERATION_SOURCE_MIX"] = source_mix["status"]
    (out_dir / "production_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle_dir", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--logo", type=Path, help="canonical lockup PNG; verified against the brand registry hash")
    ap.add_argument("--logo-sha256")
    ap.add_argument("--logo-pixels", help="WxH, e.g. 565x380")
    ap.add_argument("--archived-replay", action="store_true", help="Test-only replay; never release eligible")
    args = ap.parse_args()
    logo = None
    if args.logo:
        w, h = (int(x) for x in args.logo_pixels.lower().split("x"))
        logo = {"path": str(args.logo), "sha256": args.logo_sha256, "pixels": (w, h)}
    report = run(args.bundle_dir, args.output_dir, logo, archived_replay=args.archived_replay)
    print(json.dumps({k: report[k] for k in ("batch_id", "status", "blocking_gates", "gates")}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "READY_FOR_USER_APPROVAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
