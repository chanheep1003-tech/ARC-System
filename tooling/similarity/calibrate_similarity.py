#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import yaml
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def load_pairs(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out

def axis_text(item, axis):
    stem = str(item.get("stem", ""))
    choices = "\n".join(str(x) for x in item.get("choices", []) or [])
    full = str(item.get("full_text") or (stem + "\n" + choices))
    return {"full": full, "stem": stem, "distractor": choices}[axis]

def cos(a, b):
    return float(np.dot(a, b))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True, help="JSONL with a,b,label")
    ap.add_argument("--out", default="quality/similarity/SIMILARITY_THRESHOLDS_V1.0.yaml")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    pairs = load_pairs(args.pairs)
    high = [p for p in pairs if p["label"] in {"HIGH", "DUPLICATE"}]
    dup = [p for p in pairs if p["label"] == "DUPLICATE"]
    if len(high) < 10 or len(dup) < 5:
        raise SystemExit("Need at least 10 HIGH/DUPLICATE pairs and 5 DUPLICATE pairs.")

    model = SentenceTransformer(args.model)
    scores = []
    for p in pairs:
        rec = {"label": p["label"]}
        for axis in ("full", "stem", "distractor"):
            v = model.encode(
                [axis_text(p["a"], axis), axis_text(p["b"], axis)],
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            rec[axis] = cos(v[0], v[1])
        scores.append(rec)

    high_scores = [x for x in scores if x["label"] in {"HIGH", "DUPLICATE"}]
    dup_scores = [x for x in scores if x["label"] == "DUPLICATE"]

    # Conservative lower-bound thresholds from observed positive examples.
    cfg = {
        "version": "ARC-SIM-THRESHOLDS-V1.0",
        "status": "CALIBRATED",
        "embedding_model": args.model,
        "sample_counts": {"all": len(scores), "high_or_duplicate": len(high_scores), "duplicate": len(dup_scores)},
        "thresholds": {
            "full_high": float(np.quantile([x["full"] for x in high_scores], 0.10)),
            "full_critical": float(np.quantile([x["full"] for x in dup_scores], 0.10)),
            "stem_high": float(np.quantile([x["stem"] for x in high_scores], 0.10)),
            "distractor_high": float(np.quantile([x["distractor"] for x in high_scores], 0.10)),
        },
        "notes": [
            "Generated from labeled ARC BANK pairs.",
            "Recalibrate after embedding-model or BANK-distribution changes.",
        ],
    }
    Path(args.out).write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(json.dumps(cfg, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
