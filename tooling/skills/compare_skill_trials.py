#!/usr/bin/env python3
"""Compare paired ARC skill trial records; never infer accuracy from a model claim."""
import argparse
import json
import sys


def index(records):
    if not isinstance(records, list):
        raise ValueError("results must be an array")
    result = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each result must be an object")
        item_id = record.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("each result needs a non-empty id")
        if item_id in result:
            raise ValueError(f"duplicate id: {item_id}")
        if record.get("status") not in ("PASS", "FAIL", "NOT_RUN"):
            raise ValueError(f"invalid status: {item_id}")
        result[item_id] = record
    return result


def compare(baseline, candidate):
    left, right = index(baseline), index(candidate)
    shared = sorted(left.keys() & right.keys())
    evaluated = [i for i in shared if left[i]["status"] != "NOT_RUN"
                 and right[i]["status"] != "NOT_RUN"]
    return {
        "baseline_only": sorted(left.keys() - right.keys()),
        "candidate_only": sorted(right.keys() - left.keys()),
        "unevaluated": [i for i in shared if i not in evaluated],
        "paired_evaluated_count": len(evaluated),
        "changes": [
            {"id": i, "baseline": left[i]["status"], "candidate": right[i]["status"]}
            for i in evaluated if left[i]["status"] != right[i]["status"]
        ],
        "interpretation": "Reported statuses only; provenance, matched conditions and evaluator independence must be checked separately.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", help="JSON array of id and status")
    parser.add_argument("candidate", help="JSON array of id and status")
    args = parser.parse_args()
    try:
        with open(args.baseline, encoding="utf-8") as f:
            baseline = json.load(f)
        with open(args.candidate, encoding="utf-8") as f:
            candidate = json.load(f)
        print(json.dumps(compare(baseline, candidate), ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
