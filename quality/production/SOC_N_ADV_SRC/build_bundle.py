"""Compact SOC ARC_N manuscript (src.yaml) -> production bundle items.yaml.

usage: python build_bundle.py <src.yaml> <bundle_dir>
"""
import sys
from pathlib import Path

import yaml

COMBO5 = ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"]
COMBO_MIX = ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ", "ㄴ, ㄷ, ㄹ"]
COMBO3 = ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]


def main(src: str, out: str) -> None:
    s = yaml.safe_load(Path(src).read_text(encoding="utf-8"))
    meta = s["meta"]
    items = []
    keys = []
    for raw in s["items"]:
        opts = raw["options"]
        if opts == "COMBO5":
            opts = COMBO5
        elif opts == "COMBO_MIX":
            opts = COMBO_MIX
        elif opts == "COMBO3":
            opts = COMBO3
        assert len(opts) == 5, raw["id"]
        key = raw["key"]
        sb = raw["sb"]
        why = raw["why"]
        assert len(why) == 5, raw["id"]
        assert key != sb, raw["id"]
        d = raw["d"]
        scope = f"SCOPE:{raw['scope']}"
        ev_base = [scope]
        if raw.get("passage"):
            ev_base.append("PASSAGE")
        if raw.get("view"):
            ev_base.append("VIEW")
        if raw.get("table"):
            ev_base.append("TABLE")
        judg = []
        for i in range(5):
            n = i + 1
            if n == key:
                c = "CORRECT"
            elif n == sb:
                c = "STRONG"
            elif n in raw.get("medium", []):
                c = "STRONG" if d in ("D4", "D5") else "MEDIUM"
            else:
                c = "WEAK"
            judg.append({
                "v": n == key if not raw.get("negative") else n != key,
                "c": c,
                "axis": raw.get("axis", "content"),
                "claim": f"{raw['id']}-opt{n}",
                "ev": ev_base + [f"OPTION{n}"],
                "why": why[i],
            })
        it = {
            "item_id": raw["id"],
            "stem": raw["stem"],
            "set": None,
        }
        for k in ("passage", "table", "view", "view_label"):
            if raw.get(k):
                it[k] = raw[k]
        it.update({
            "options": opts,
            "answer": key,
            "second_best": sb,
            "difficulty": d,
            "family": raw["fam"],
            "balance": "ADVANCED_DISCRIMINATION" if d in ("D4", "D5") else "CORE_EXAM_POINT",
            "reasoning_steps": {"D2": 1, "D3": 2, "D4": 3, "D5": 4}[d],
            "immediate_elimination": raw.get("elim", 0 if d == "D5" else 1),
            "evidence_count": raw.get("evidence", 2),
            "transfer": bool(raw.get("transfer", False)),
            "scope_refs": [raw["scope"]],
            "judgments": judg,
        })
        items.append(it)
        keys.append(key)
    # local self-checks
    from collections import Counter
    cnt = Counter(keys)
    for i in range(len(keys) - 2):
        assert not (keys[i] == keys[i + 1] == keys[i + 2]), f"3 in a row at {i+1}"
    assert max(cnt.values()) <= 0.3 * len(keys), cnt
    bundle = dict(meta)
    bundle["items"] = items
    outp = Path(out)
    outp.mkdir(parents=True, exist_ok=True)
    (outp / "items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print("ok", len(items), dict(sorted(cnt.items())), Counter(i["difficulty"] for i in items))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
