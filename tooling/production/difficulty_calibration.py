#!/usr/bin/env python3
"""AI 풀이자 난이도 눈금 보정 (D-23).

풀이 평가 원고 끝에 기준 문항(ANCHOR-<id>)을 붙여 같은 풀이자가 풀게 하고, 출판사 난이도 라벨과 풀이자 평가의 차이로
눈금(관대/엄격)을 잰다. 기준 문항이 부족하면 보정값을 적용하지 않고 UNCALIBRATED 로 표시한다.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "quality/anchors/CALIBRATION_ANCHOR_REGISTRY_V1.0.yaml"
LEVEL = {"D1": 1.0, "D2": 2.0, "D3": 3.0, "D4": 4.0, "D5": 5.0}
MIN_ANCHORS = 4
TOLERANCE = 0.5


def load_registry(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or REGISTRY).read_text(encoding="utf-8"))


def anchor_reference(anchor: dict[str, Any], reg: dict[str, Any]) -> float | None:
    return reg["label_to_level"].get(anchor.get("label"))


def calibrate(blind_items: list[dict[str, Any]], reg: dict[str, Any] | None = None) -> dict[str, Any]:
    reg = reg or load_registry()
    by_id = {a["id"]: a for a in reg["anchors"]}
    rows = []
    for it in blind_items:
        iid = str(it.get("item_id", ""))
        if not iid.startswith("ANCHOR-"):
            continue
        aid = iid[len("ANCHOR-"):]
        anchor = by_id.get(aid)
        if anchor is None or it.get("difficulty") not in LEVEL:
            continue
        ref = anchor_reference(anchor, reg)
        if ref is None:
            continue
        rows.append({"anchor": aid, "label": anchor["label"], "reference": ref, "solver": it["difficulty"],
                     "diff": round(ref - LEVEL[it["difficulty"]], 2)})
    n = len(rows)
    refs = [r["reference"] for r in rows]
    report: dict[str, Any] = {"tool": "ARC_DIFFICULTY_CALIBRATION_V1.0", "anchors": rows, "anchor_count": n}
    if n < MIN_ANCHORS or not refs or min(refs) > 2.5 or max(refs) < 3.5:
        report.update(status="INSUFFICIENT_ANCHORS", offset=0.0, applied=False,
                      message=f"기준 문항 {n}개(최소 {MIN_ANCHORS}개, 낮은 라벨과 높은 라벨 모두 필요). 눈금 보정을 적용하지 않는다.")
        return report
    offset = round(sum(r["diff"] for r in rows) / n, 2)
    if offset > TOLERANCE:
        status, msg = "SOLVER_LENIENT", f"풀이자가 출판사 라벨보다 평균 {offset} 단계 낮게 평가한다. 풀이 결과에 보정값을 더해 해석한다."
    elif offset < -TOLERANCE:
        status, msg = "SOLVER_HARSH", f"풀이자가 출판사 라벨보다 평균 {-offset} 단계 높게 평가한다."
    else:
        status, msg = "CALIBRATED", "풀이자 눈금이 출판사 라벨과 ±0.5 단계 안에서 일치한다."
    report.update(status=status, offset=offset, applied=True, message=msg)
    return report


def adjusted_level(solver: str, report: dict[str, Any]) -> float:
    lv = LEVEL[solver]
    if not report.get("applied"):
        return lv
    return max(2.0, min(4.0, lv + report["offset"]))


def calibrated_distribution(blind_items: list[dict[str, Any]], report: dict[str, Any]) -> dict[str, Any]:
    items = [it for it in blind_items if not str(it.get("item_id", "")).startswith("ANCHOR-") and it.get("difficulty") in LEVEL]
    n = len(items)
    if not n:
        return {"basis": "NONE", "shares": None}
    raw = {"D2": 0, "D3": 0, "D45": 0}
    adj = {"D2": 0, "D3": 0, "D45": 0}

    def bucket(x: float) -> str:
        return "D2" if x < 2.5 else ("D3" if x < 3.5 else "D45")
    for it in items:
        raw[bucket(LEVEL[it["difficulty"]])] += 1
        adj[bucket(adjusted_level(it["difficulty"], report))] += 1
    return {"basis": "CALIBRATED" if report.get("applied") else "UNCALIBRATED_RAW_SOLVER",
            "raw": {k: round(v / n, 3) for k, v in raw.items()},
            "adjusted": {k: round(v / n, 3) for k, v in adj.items()}, "n": n}


def structure_solver_mismatch(structure_rows: list[dict[str, Any]], blind_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """구조 밴드와 풀이자 평가가 한 단계 이상 어긋난 문항을 모은다(사람이 확인할 대상)."""
    blind = {b["item_id"]: b["difficulty"] for b in blind_items if b.get("difficulty") in LEVEL}
    out = []
    for r in structure_rows:
        s = blind.get(r["item_id"])
        if s and abs(LEVEL[s] - LEVEL[r["band"]]) >= 1.0:
            out.append({"item_id": r["item_id"], "structure_band": r["band"], "solver": s, "label": r.get("label")})
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: difficulty_calibration.py <blind_output.yaml>", file=sys.stderr)
        return 2
    blind = yaml.safe_load(Path(argv[1]).read_text(encoding="utf-8"))["items"]
    report = calibrate(blind)
    report["distribution"] = calibrated_distribution(blind, report)
    print(yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=200))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
