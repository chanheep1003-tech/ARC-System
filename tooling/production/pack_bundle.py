#!/usr/bin/env python3
"""Dense packing for two-column problem pages: reorder a bundle's MCQs so every column is filled to the bottom.

The renderer places blocks sequentially (a block that does not fit moves to the next column). This tool measures every
question block with the real renderer, searches for the MCQ order that needs the fewest columns, keeps the answer-position
and stem-skeleton rules (no 3 equal keys / endings in a row), renumbers item ids to the new order and moves the blind-review
file along by content fingerprint. Constructed-response items stay at the end.

    python tooling/production/pack_bundle.py pack  <bundle_dir>
    python tooling/production/pack_bundle.py stamp <bundle_dir>   # add content fingerprints to blind_review.yaml entries
"""
from __future__ import annotations

import importlib.util
import random
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _renderer():
    spec = importlib.util.spec_from_file_location("arc_kor_renderer", ROOT / "tooling/typeset/kor_renderer.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fingerprint(it: dict) -> str:
    stem = re.sub(r"^\[[^\]]*\] ", "", it["stem"])
    return stem + "#" + "|".join(it.get("view", [])) + "#" + "|".join(sorted(it.get("options", [])))


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _dump(path: Path, data) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")


def stamp(bundle_dir: Path) -> int:
    bundle = _load(bundle_dir / "items.yaml")
    fps = {it["item_id"]: fingerprint(it) for it in bundle["items"]}
    bf = _load(bundle_dir / "blind_review.yaml")
    n = 0
    for b in bf["items"]:
        if "fp" not in b and b["item_id"] in fps:
            b["fp"] = fps[b["item_id"]]
            n += 1
    _dump(bundle_dir / "blind_review.yaml", bf)
    return n


GAP = 16.0


def simulate(heights: list[float], cap: float) -> tuple[int, float]:
    """heights are block heights without their trailing gap; blocks in one column are separated by GAP."""
    cols, y = 1, 0.0
    for h in heights:
        need = h if y == 0 else y + GAP + h
        if need > cap + 1e-9:
            cols += 1
            y = h
        else:
            y = need
    return cols, cap - y


def _ok_sequence(answers: list[int], ends: list[str]) -> bool:
    for i in range(2, len(answers)):
        if answers[i] == answers[i - 1] == answers[i - 2] or ends[i] == ends[i - 1] == ends[i - 2]:
            return False
    return True


def pack(bundle_dir: Path, trials: int = 20000, seed: int = 20261119) -> dict:
    bundle_dir = Path(bundle_dir)
    bundle = _load(bundle_dir / "items.yaml")
    items = bundle["items"]
    mcq = [it for it in items if it.get("options")]
    crs = [it for it in items if not it.get("options")]
    R = _renderer()
    R._ACTIVE_SUBJECT = (bundle.get("subject") or "").upper() or None
    R._FONTS = None
    cfg = bundle.get("layout") or {}
    if cfg.get("body_pt"):  # measure with the same body size / line height the renderer will use
        R.SIZE = float(cfg["body_pt"])
        R.LH = R.SIZE * float(cfg.get("line_height_ratio", 1.62))
    lay = R.Layout()
    cap = (R.A4_H - R.MB) - R.MT
    bm = [R.question_block(lay, it, "1", bundle["product_mode"], True) for it in mcq]
    bc = [R.question_block(lay, it, "서술형 1", bundle["product_mode"], True) for it in crs]
    gap = bm[0].gap if bm else 0
    hm = [b.h - b.gap for b in bm]  # effective height: the gap after a column's last block does not count, so add it back per join
    hc = [b.h - b.gap for b in bc]
    if max(hm + hc) > cap:
        raise SystemExit(f"block taller than column: {max(hm + hc):.1f} > {cap:.1f}")
    ans = [int(it["answer"]) for it in mcq]
    ends = [re.sub(r"\s", "", it["stem"])[-8:] for it in mcq]
    before_cols, _ = simulate(hm + hc, cap)
    rng = random.Random(seed)
    n = len(mcq)

    def load(items_: list[int]) -> float:
        return sum(hm[i] for i in items_) + GAP * (len(items_) - 1) if items_ else 0.0

    def anneal(K: int, iters: int) -> list[list[int]] | None:
        order = sorted(range(n), key=lambda i: -hm[i])
        bins: list[list[int]] = [[] for _ in range(K)]
        for i in order:  # greedy start: emptiest bin first
            min(bins, key=lambda b: load(b)).append(i)
        loads = [load(b) for b in bins]
        over = lambda x: max(0.0, x - cap) ** 2
        cost = sum(over(x) for x in loads)
        T = cap * 0.05
        for step in range(iters):
            if cost <= 1e-9:
                return bins
            T = max(0.4, T * 0.99996)
            i_b = rng.randrange(K)
            if not bins[i_b]:
                continue
            i = rng.choice(bins[i_b])
            j_b = rng.randrange(K)
            if j_b == i_b:
                continue
            if bins[j_b] and rng.random() < 0.5:  # swap
                j = rng.choice(bins[j_b])
                nb_i = [x for x in bins[i_b] if x != i] + [j]
                nb_j = [x for x in bins[j_b] if x != j] + [i]
            else:  # move
                j = None
                nb_i = [x for x in bins[i_b] if x != i]
                nb_j = bins[j_b] + [i]
            ni, nj = load(nb_i), load(nb_j)
            delta = over(ni) + over(nj) - over(loads[i_b]) - over(loads[j_b])
            if delta <= 0 or rng.random() < pow(2.718281828, -delta / (T * T)):
                bins[i_b], bins[j_b] = nb_i, nb_j
                loads[i_b], loads[j_b] = ni, nj
                cost += delta
        return bins if cost <= 1e-9 else None

    import math
    lower = max(1, math.ceil((sum(hm) + GAP * n) / (cap + GAP)))

    def total_cols(bins_: list[list[int]]) -> int:
        ordered = sorted(bins_, key=load, reverse=True)
        return simulate([hm[i] for b in ordered for i in b] + hc, cap)[0]

    # 1) noisy best-fit-decreasing restarts (fast, strong on mixed sizes)
    cands: list[list[list[int]]] = []
    best_key = None
    for _ in range(trials):
        noise = [h * (1 + 0.15 * rng.random()) for h in hm]
        order = sorted(range(n), key=lambda i: -noise[i])
        bins_: list[list] = []
        for i in order:
            pick, left = None, None
            for k, (rem, _lst) in enumerate(bins_):
                if hm[i] + GAP <= rem + 1e-9 and (left is None or rem - hm[i] - GAP < left):
                    pick, left = k, rem - hm[i] - GAP
            if pick is None:
                bins_.append([cap - hm[i], [i]])
            else:
                bins_[pick][0] -= hm[i] + GAP
                bins_[pick][1].append(i)
        plain = [list(b[1]) for b in bins_]
        key = (total_cols(plain), len(plain))
        if best_key is None or key < best_key:
            best_key, cands = key, [plain]
    # 2) annealing for one bin fewer than the best restart found
    k_try = best_key[1] - 1
    while k_try >= lower:
        got = None
        for _try in range(8):
            got = anneal(k_try, 120000)
            if got:
                break
        if not got:
            break
        plain = [b for b in got if b]
        key = (total_cols(plain), len(plain))
        if key < best_key:
            best_key, cands = key, [plain]
        k_try -= 1
    best_bins = sorted(cands[0], key=load, reverse=True)  # emptiest bin last, next to the written-answer items
    target = simulate([hm[i] for b in best_bins for i in b] + hc, cap)[0]
    chosen = None
    for _ in range(40000):
        bins = [list(b) for b in best_bins]
        for b in bins:
            rng.shuffle(b)
        head, tail = bins[:-1], bins[-1:]
        rng.shuffle(head)
        seq = [i for b in head + tail for i in b]
        if simulate([hm[i] for i in seq] + hc, cap)[0] > target:
            continue
        if _ok_sequence([ans[i] for i in seq], [ends[i] for i in seq]):
            chosen = seq
            break
    if chosen is None:
        raise SystemExit("no ordering satisfied the answer/stem-run rules")
    new_mcq = [mcq[i] for i in chosen]
    final = new_mcq + crs
    stamped = {it["item_id"]: fingerprint(it) for it in items}
    bf = _load(bundle_dir / "blind_review.yaml") if (bundle_dir / "blind_review.yaml").is_file() else {"items": []}
    for b in bf["items"]:
        if "fp" not in b and b["item_id"] in stamped:
            b["fp"] = stamped[b["item_id"]]
    new_fp_id = {}
    for k, it in enumerate(final, 1):
        old = it["item_id"]
        new = re.sub(r"\d+$", "", old) + f"{k:03d}"
        for j in it.get("judgments", []):
            j["claim"] = j["claim"].replace(old, new)
        it["item_id"] = new
        new_fp_id[fingerprint(it)] = new
    bundle["items"] = final
    bundle.setdefault("layout", {})["dense"] = True
    _dump(bundle_dir / "items.yaml", bundle)
    kept, dropped = [], 0
    for b in bf["items"]:
        new = new_fp_id.get(b.get("fp"))
        if new:
            b["item_id"] = new
            kept.append(b)
        else:
            dropped += 1
    bf["items"] = sorted(kept, key=lambda b: b["item_id"])
    _dump(bundle_dir / "blind_review.yaml", bf)
    after_cols, _ = simulate([hm[i] for i in chosen] + hc, cap)
    return {"columns_before": before_cols, "columns_after": after_cols, "pages_before": (before_cols + 1) // 2,
            "pages_after": (after_cols + 1) // 2, "blind_kept": len(kept), "blind_dropped": dropped,
            "mcq_columns": len(best_bins), "mcq_lower_bound": lower}


if __name__ == "__main__":
    mode, target = sys.argv[1], Path(sys.argv[2])
    print(stamp(target) if mode == "stamp" else pack(target))
