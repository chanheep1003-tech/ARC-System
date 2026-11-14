#!/usr/bin/env python3
"""ARC examiner-lens gate: school exam-sheet conventions + teacher receipts.

Spec: quality/ARC_EXAMINER_LENS_V1.1.md (V1.0 bundles are still checked by the V1.0 rules)
- Always: NON_SCHOOL_MARKUP, META_LANGUAGE_LEAK, LONGEST_ANSWER_CUE, ANSWER_POSITION_SKEW.
- When the bundle declares `examiner_lens: V1.0`: blueprint, teaching_anchor,
  distinct distractor_misconceptions per wrong option, appeal_check.
- V1.1 adds the discrimination lens: transfer_level per item, novel_material for
  INFER/EXTEND, and a RECALL / transfer mix per product.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import yaml

# Spacing mask glued to the previous syllable: 년[만]에, 할[뿐]. Pronunciation like '꽃이'를 [꼬치]로 is preceded by a space and allowed;
# [A]~[C] section marks are Latin and allowed.
BRACKET_MARK = re.compile(r"(?<=[가-힣])\[[가-힣]{1,4}\]")
META_TERMS = ("판단축", "근거 범위", "정답 후보", "추론 단계", "second-best", "distractor", "true kernel", "독해 전략")
ERROR, WARN = "ERROR", "WARN"
LENS_VERSIONS = {"V1.0", "V1.1"}
TRANSFER_LEVELS = ("RECALL", "APPLY", "INFER", "EXTEND")
NOVEL_KINDS = {"NEW_EXAMPLE", "NEW_PASSAGE", "NEW_DATA", "NEW_CLAUSE", "NEW_CASE"}
# product -> (max RECALL share, min INFER+EXTEND share); checked on sets with >= MIX_MIN_ITEMS MCQs
TRANSFER_MIX = {"ARC_N": (0.30, 0.30), "ARC_FINAL": (0.25, 0.35)}
MIX_MIN_ITEMS = 8


def _items(bundle: dict) -> list[dict]:
    return bundle.get("items", []) if isinstance(bundle, dict) else list(bundle or [])


def _mcq(item: dict) -> bool:
    opts = item.get("options")
    return isinstance(opts, list) and len(opts) >= 4 and isinstance(item.get("answer"), int)


def _text(item: dict, include_view: bool = True) -> str:
    parts = [str(item.get("stem", ""))] + ([str(item.get("view", "") or "")] if include_view else [])
    parts += [str(o) for o in item.get("options") or []]
    return "\n".join(parts)


def analyze(bundle: dict) -> dict:
    items = _items(bundle)
    version = str(bundle.get("examiner_lens", "")) if isinstance(bundle, dict) else ""
    lens = version in LENS_VERSIONS
    v11 = version == "V1.1"
    levels: list[str] = []
    findings: list[dict] = []

    def add(code: str, level: str, item_id: str | None, detail: str) -> None:
        findings.append({"code": code, "level": level, "item_id": item_id, "detail": detail})

    mcq = [it for it in items if _mcq(it)]
    longest_hits = 0
    for it in items:
        iid = it.get("item_id")
        text = _text(it)
        # Archetype library exception: A3 may mark target forms with [ ] inside <보기 2>.
        a3 = str(it.get("archetype", "")).startswith("A3")
        marks = sorted(set(BRACKET_MARK.findall(_text(it, include_view=not a3))))
        if marks:
            add("NON_SCHOOL_MARKUP", ERROR, iid, f"대괄호 표시 {', '.join(marks)} → 밑줄/㉠ 표기로")
        leaked = [t for t in META_TERMS if t in text]
        if leaked:
            add("META_LANGUAGE_LEAK", ERROR, iid, f"학생용 문장에 제작 용어: {', '.join(leaked)}")
        if _mcq(it):
            lens_ = [len(str(o)) for o in it["options"]]
            ans = it["answer"] - 1
            if 0 <= ans < len(lens_) and lens_[ans] == max(lens_) and lens_.count(max(lens_)) == 1:
                longest_hits += 1
        if lens:
            if not it.get("blueprint"):
                add("MISSING_BLUEPRINT", ERROR, iid, "출제 계획표 칸(blueprint)이 없다")
            if not str(it.get("teaching_anchor", "")).strip():
                add("NOT_TAUGHT", ERROR, iid, "수업 근거(teaching_anchor)가 없다")
            if not it.get("appeal_check"):
                add("MISSING_APPEAL_CHECK", ERROR, iid, "이의 제기 검토(appeal_check)가 없다")
            if _mcq(it):
                dm = {int(k): str(v).strip() for k, v in (it.get("distractor_misconceptions") or {}).items()}
                wrong = [i for i in range(1, len(it["options"]) + 1) if i != it["answer"]]
                missing = [i for i in wrong if not dm.get(i)]
                if missing:
                    add("MISSING_MISCONCEPTION", ERROR, iid, f"오개념이 비어 있는 오답 선지: {missing}")
                vals = [dm[i] for i in wrong if dm.get(i)]
                dupes = [v for v, c in collections.Counter(vals).items() if c > 1]
                if dupes:
                    add("CLONE_DISTRACTORS", ERROR, iid, f"같은 오개념을 반복하는 오답: {dupes}")
        if v11:
            level = str(it.get("transfer_level", "")).upper()
            if level not in TRANSFER_LEVELS:
                add("MISSING_TRANSFER_LEVEL", ERROR, iid, f"transfer_level은 {'/'.join(TRANSFER_LEVELS)} 중 하나")
                continue
            if _mcq(it):
                levels.append(level)
            nm = it.get("novel_material") or {}
            if level in ("INFER", "EXTEND"):
                if str(nm.get("kind", "")).upper() not in NOVEL_KINDS or not str(nm.get("source", "")).strip():
                    add("NOVEL_MATERIAL_MISSING", ERROR, iid, f"{level} 문항은 novel_material(kind·source)이 필요하다")
                if level == "EXTEND" and str(nm.get("kind", "")).upper() not in {"NEW_CLAUSE", "NEW_DATA", "NEW_CASE"}:
                    add("EXTEND_WITHOUT_NEW_CONDITION", ERROR, iid, "EXTEND는 새 조항·조건(NEW_CLAUSE/NEW_DATA/NEW_CASE)을 <보기>로 준다")

    n = len(mcq)
    if n >= 10 and longest_hits / n > 0.4:
        add("LONGEST_ANSWER_CUE", WARN, None, f"정답이 가장 긴 선지인 문항 {longest_hits}/{n}")
    if n >= 20:
        k = max(len(it["options"]) for it in mcq)
        pos = collections.Counter(it["answer"] for it in mcq)
        shares = {p: round(pos.get(p, 0) / n, 2) for p in range(1, k + 1)}
        if min(shares.values()) < 0.6 / k or max(shares.values()) > 1.5 / k:
            add("ANSWER_POSITION_SKEW", WARN, None, f"정답 번호 비율 {shares}")

    product = str(bundle.get("product_mode", "ARC_N")) if isinstance(bundle, dict) else "ARC_N"
    if v11 and len(levels) >= MIX_MIN_ITEMS and product in TRANSFER_MIX:
        max_recall, min_transfer = TRANSFER_MIX[product]
        recall = levels.count("RECALL") / len(levels)
        transfer = (levels.count("INFER") + levels.count("EXTEND")) / len(levels)
        mix = {lv: levels.count(lv) for lv in TRANSFER_LEVELS}
        if recall > max_recall:
            add("RECALL_OVERUSE", ERROR, None, f"{product} RECALL {recall:.0%} > {max_recall:.0%} {mix}")
        if transfer < min_transfer:
            add("TRANSFER_SHORT", ERROR, None, f"{product} INFER+EXTEND {transfer:.0%} < {min_transfer:.0%} {mix}")

    errors = [f for f in findings if f["level"] == ERROR]
    status = "FAIL" if errors else ("WARN" if findings else "PASS")
    return {"tool": "ARC_EXAMINER_LENS_GATE_V1.1", "lens_declared": version or None, "items": len(items),
            "mcq": n, "status": status, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items", type=Path)
    args = ap.parse_args()
    report = analyze(yaml.safe_load(args.items.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
