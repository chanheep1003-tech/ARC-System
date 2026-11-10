#!/usr/bin/env python3
import argparse
import json
import os
import uuid
from pathlib import Path

import yaml
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
AXES = ("full", "stem", "distractor")

def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def text_for(item, axis):
    stem = str(item.get("stem", "")).strip()
    choices = item.get("choices", []) or []
    distractor = "\n".join(str(x) for x in choices)
    full = str(item.get("full_text") or (stem + "\n" + distractor)).strip()
    return {"full": full, "stem": stem, "distractor": distractor}[axis]

def meta(item):
    keys = [
        "item_id", "concept_id", "question_form", "reasoning_form",
        "condition_pattern", "answer_path", "visual_template", "product", "subject"
    ]
    return {k: item.get(k) for k in keys}

def collection(axis):
    return f"arc_similarity_{axis}"

def ensure_collection(client, name, size):
    names = {c.name for c in client.get_collections().collections}
    if name not in names:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

def point_id(item_id, axis):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"arc:{axis}:{item_id}"))

def structural_matches(a, b):
    fields = ["concept_id", "question_form", "reasoning_form", "condition_pattern", "answer_path", "visual_template"]
    matched = [f for f in fields if a.get(f) and b.get(f) and a.get(f) == b.get(f)]
    return matched

def thresholds(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data

def risk_from(scores, structural_count, cfg):
    if cfg.get("status") != "CALIBRATED":
        return "UNCALIBRATED"
    t = cfg["thresholds"]
    full = scores.get("full", -1)
    stem = scores.get("stem", -1)
    dist = scores.get("distractor", -1)
    if full >= t["full_critical"] or (full >= t["full_high"] and structural_count >= 4):
        return "CRITICAL"
    if full >= t["full_high"] or stem >= t["stem_high"] or dist >= t["distractor_high"] or structural_count >= 4:
        return "HIGH"
    if structural_count >= 2:
        return "MEDIUM"
    return "LOW"

def cmd_index(args):
    model = SentenceTransformer(args.model)
    client = QdrantClient(path=args.db)
    items = list(load_jsonl(args.input))
    for axis in AXES:
        texts = [text_for(x, axis) for x in items]
        vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        ensure_collection(client, collection(axis), vectors.shape[1])
        points = []
        for item, vector in zip(items, vectors):
            item_id = str(item["item_id"])
            payload = meta(item)
            payload["axis"] = axis
            payload["text"] = text_for(item, axis)
            points.append(PointStruct(id=point_id(item_id, axis), vector=vector.tolist(), payload=payload))
        client.upsert(collection_name=collection(axis), points=points)
    print(json.dumps({"indexed": len(items), "model": args.model, "db": args.db}, ensure_ascii=False))

def query_axis(client, model, item, axis, top_k):
    vec = model.encode([text_for(item, axis)], normalize_embeddings=True, show_progress_bar=False)[0]
    resp = client.query_points(
        collection_name=collection(axis),
        query=vec.tolist(),
        limit=top_k,
        with_payload=True,
    )
    return [{"score": float(p.score), "payload": p.payload} for p in resp.points]

def cmd_query(args):
    model = SentenceTransformer(args.model)
    client = QdrantClient(path=args.db)
    cfg = thresholds(args.thresholds)
    items = list(load_jsonl(args.input))
    for item in items:
        axis_hits = {axis: query_axis(client, model, item, axis, args.top_k) for axis in AXES}
        candidate_ids = set()
        for hits in axis_hits.values():
            candidate_ids.update(h["payload"].get("item_id") for h in hits if h["payload"].get("item_id"))

        combined = []
        for cid in candidate_ids:
            scores = {}
            payload = None
            for axis, hits in axis_hits.items():
                hit = next((h for h in hits if h["payload"].get("item_id") == cid), None)
                scores[axis] = hit["score"] if hit else -1.0
                payload = payload or (hit["payload"] if hit else None)
            matched = structural_matches(meta(item), payload or {})
            combined.append({
                "nearest_item_id": cid,
                "scores": scores,
                "structural_matches": matched,
                "structural_match_count": len(matched),
                "risk": risk_from(scores, len(matched), cfg),
            })
        combined.sort(key=lambda x: max(x["scores"].values()), reverse=True)
        print(json.dumps({
            "item_id": item.get("item_id"),
            "threshold_status": cfg.get("status"),
            "model": args.model,
            "matches": combined[:args.top_k],
        }, ensure_ascii=False))

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("index")
    pi.add_argument("--input", required=True, help="BANK items JSONL")
    pi.add_argument("--db", default="tooling/.cache/qdrant")
    pi.add_argument("--model", default=os.getenv("ARC_EMBEDDING_MODEL", DEFAULT_MODEL))
    pi.set_defaults(func=cmd_index)

    pq = sub.add_parser("query")
    pq.add_argument("--input", required=True, help="new items JSONL")
    pq.add_argument("--db", default="tooling/.cache/qdrant")
    pq.add_argument("--model", default=os.getenv("ARC_EMBEDDING_MODEL", DEFAULT_MODEL))
    pq.add_argument("--thresholds", default="quality/similarity/SIMILARITY_THRESHOLDS_V1.0.yaml")
    pq.add_argument("--top-k", type=int, default=5)
    pq.set_defaults(func=cmd_query)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
