#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import cv2
import fitz
import numpy as np

def segment_angle(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    a = math.degrees(math.atan2(dy, dx)) % 180
    return a

def diagonal(a):
    return 25 <= a <= 65 or 115 <= a <= 155

def opposite_diag(a, b):
    return (25 <= a <= 65 and 115 <= b <= 155) or (25 <= b <= 65 and 115 <= a <= 155)

def bbox_points(points, pad=3):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return [min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad]

def line_intersection(a1, a2, b1, b2):
    x1,y1,x2,y2 = *a1,*a2
    x3,y3,x4,y4 = *b1,*b2
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < 1e-9:
        return None
    px = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / den
    py = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / den
    return (px, py)

def in_segment_box(p, a, b, slack=5):
    return min(a[0], b[0])-slack <= p[0] <= max(a[0], b[0])+slack and min(a[1], b[1])-slack <= p[1] <= max(a[1], b[1])+slack

def annotation_candidates(page):
    out = []
    annots = page.annots()
    if not annots:
        return out
    for a in annots:
        name = a.type[1] if a.type else "Unknown"
        conf = 0.95 if name in {"Ink", "Line", "PolyLine"} else 0.65
        out.append({
            "page": page.number + 1,
            "source": "annotation",
            "annotation_type": name,
            "bbox": list(a.rect),
            "confidence": conf,
            "action": "AUTO_EXCLUDE" if conf >= 0.9 else "HUMAN_CHECK",
        })
    return out

def vector_candidates(page):
    lines = []
    for d in page.get_drawings():
        for item in d.get("items", []):
            if item and item[0] == "l":
                p1, p2 = item[1], item[2]
                length = math.hypot(p2.x-p1.x, p2.y-p1.y)
                angle = segment_angle(p1, p2)
                if length >= 12 and diagonal(angle):
                    lines.append(((p1.x,p1.y),(p2.x,p2.y),angle))
    out = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            a1,a2,aa = lines[i]
            b1,b2,ba = lines[j]
            if not opposite_diag(aa, ba):
                continue
            p = line_intersection(a1,a2,b1,b2)
            if p and in_segment_box(p,a1,a2) and in_segment_box(p,b1,b2):
                out.append({
                    "page": page.number + 1,
                    "source": "vector",
                    "bbox": bbox_points([a1,a2,b1,b2], 2),
                    "confidence": 0.90,
                    "action": "AUTO_EXCLUDE",
                })
    return out

def raster_candidates(page, dpi=150):
    scale = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    else:
        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(arr, cv2.COLOR_BGR2HSV)
    sat_mask = cv2.inRange(hsv, np.array([0, 60, 20]), np.array([179, 255, 255]))
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    # Prefer colored marks when present, but retain edges for black pen scans.
    mask = cv2.bitwise_or(edges, sat_mask)

    lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold=45, minLineLength=35, maxLineGap=10)
    if lines is None:
        return []

    segs = []
    for l in lines[:,0,:]:
        x1,y1,x2,y2 = map(float, l)
        angle = math.degrees(math.atan2(y2-y1, x2-x1)) % 180
        if diagonal(angle):
            segs.append(((x1,y1),(x2,y2),angle))

    out = []
    for i in range(len(segs)):
        for j in range(i+1, len(segs)):
            a1,a2,aa = segs[i]
            b1,b2,ba = segs[j]
            if not opposite_diag(aa,ba):
                continue
            p = line_intersection(a1,a2,b1,b2)
            if p and in_segment_box(p,a1,a2,10) and in_segment_box(p,b1,b2,10):
                bb = bbox_points([a1,a2,b1,b2], 5)
                bb_pt = [v/scale for v in bb]
                out.append({
                    "page": page.number + 1,
                    "source": "raster",
                    "bbox": bb_pt,
                    "confidence": 0.72,
                    "action": "HUMAN_CHECK",
                })
    return out[:50]

def dedupe(cands):
    seen = []
    out = []
    for c in sorted(cands, key=lambda x: x["confidence"], reverse=True):
        r = fitz.Rect(c["bbox"])
        duplicate = False
        for e in seen:
            inter = r & e
            if not inter.is_empty:
                denom = max(1.0, min(r.width*r.height, e.width*e.height))
                if inter.width*inter.height / denom > 0.5:
                    duplicate = True
                    break
        if not duplicate:
            out.append(c)
            seen.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--report", default=None)
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    all_candidates = []
    for page in doc:
        c = annotation_candidates(page)
        c += vector_candidates(page)
        # Raster fallback only when annotation/vector did not produce a high-confidence mark.
        if not any(x["confidence"] >= 0.9 for x in c):
            c += raster_candidates(page, args.dpi)
        all_candidates.extend(c)

    all_candidates = dedupe(all_candidates)
    auto = [c for c in all_candidates if c["action"] == "AUTO_EXCLUDE"]
    human = [c for c in all_candidates if c["action"] == "HUMAN_CHECK"]
    result = {
        "tool": "ARC_XMARK_DETECT_V1.0",
        "pdf": args.pdf,
        "auto_exclude_count": len(auto),
        "human_check_count": len(human),
        "candidates": all_candidates,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
