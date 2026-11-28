#!/usr/bin/env python3
"""Merge the two blind-review halves into ../blind_review.yaml and diff them against the key."""
import sys
from collections import Counter
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
BLIND = Path("/tmp/claude-0/-home-user-ARC-System/41c489c2-864e-5a02-81e4-8531b09e112d/scratchpad/blind")

items = {it["item_id"]: it for it in yaml.safe_load((BUNDLE / "items.yaml").read_text())["items"]}
merged = []
for f in ("blind_review_01_40.yaml", "blind_review_41_80.yaml"):
    merged += yaml.safe_load((BLIND / f).read_text())["items"]
by = {b["item_id"]: b for b in merged}
assert set(by) == set(items), set(items) ^ set(by)

mism, diffd, flagged = [], [], []
for iid, it in items.items():
    b = by[iid]
    if int(b["answer"]) != int(it["answer"]):
        mism.append((iid, it["answer"], b["answer"], b.get("confidence")))
    if b["difficulty"] != it["difficulty"]:
        diffd.append((iid, it["difficulty"], b["difficulty"]))
    if b.get("flags"):
        flagged.append((iid, b["flags"], b.get("flag_reasons")))
print("answer mismatches:", len(mism))
for m in mism: print("  ", m)
print("difficulty differences:", len(diffd), Counter((a, c) for _, a, c in diffd))
for d in diffd: print("  ", d)
print("flagged:", len(flagged))
for f in flagged: print("  ", f)
print("blind difficulty:", Counter(b["difficulty"] for b in merged))

if "--write" in sys.argv:
    out = {"review_id": "KOR-N-FINAL-LIT4-BLIND-R1",
           "reviewer": "independent blind reviewer agents (2, fresh context), student_manuscript.md only — same model family as the author, not a different provider",
           "rounds": 1, "manuscript_sha256": sys.argv[sys.argv.index("--write") + 1],
           "excluded_inputs": ["ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY", "items.yaml", "authoring/*"],
           "difficulty_rule": "item difficulty = blind rating (single round)",
           "items": [{k: b[k] for k in ("item_id", "answer", "first_pass_top3", "second_best", "difficulty", "confidence", "flags")}
                     | ({"flag_reasons": b["flag_reasons"]} if b.get("flag_reasons") else {}) for b in merged]}
    (BUNDLE / "blind_review.yaml").write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=1000))
    print("wrote blind_review.yaml")
