import json

def _norm_decision(value):
    return str(value or "").strip().upper()

def get_assert(output, context):
    try:
        result = json.loads(output)
    except Exception as e:
        return {"pass": False, "score": 0, "reason": f"Invalid JSON output: {e}"}

    v = context["vars"]
    decision = _norm_decision(result.get("decision"))
    expected = _norm_decision(v.get("expected_decision"))
    forbidden = {_norm_decision(x) for x in v.get("forbidden_decisions", [])}
    hard_fail = bool(result.get("hard_fail", False))
    expected_hard = bool(v.get("expected_hard_fail", False))
    score = result.get("item_score")

    reasons = []
    fail = False
    warn = False

    if decision in forbidden:
        fail = True
        reasons.append(f"forbidden decision: {decision}")

    if expected == "BANK_A" and decision in {"REVISE", "DISCARD"}:
        fail = True
        reasons.append(f"GOOD fixture degraded to {decision}")

    if expected == "REVISE" and decision in {"BANK_A", "PREMIUM_BANK_A"}:
        fail = True
        reasons.append(f"BAD-REVISE fixture inflated to {decision}")

    if expected == "DISCARD" and decision in {"PASS", "BANK_A", "BANK_B", "PREMIUM_BANK_A"}:
        fail = True
        reasons.append(f"BAD-DISCARD fixture promoted to {decision}")

    if expected_hard and not hard_fail:
        if expected == "DISCARD" and decision == "REVISE":
            warn = True
            reasons.append("hard-fail semantics disappeared but decision still blocks BANK")
        else:
            fail = True
            reasons.append("expected hard_fail=true")

    if not expected_hard and hard_fail:
        fail = True
        reasons.append("unexpected hard_fail on non-hard-fail fixture")

    try:
        numeric_score = None if score is None else float(score)
    except Exception:
        numeric_score = None
        fail = True
        reasons.append("item_score is not numeric")

    lo = v.get("expected_item_min")
    hi = v.get("expected_item_max")
    ceiling = v.get("expected_max_item")

    if numeric_score is not None and lo is not None and hi is not None:
        lo, hi = float(lo), float(hi)
        if numeric_score < lo - 5 or numeric_score > hi + 5:
            fail = True
            reasons.append(f"score drift >5: {numeric_score} vs {lo}-{hi}")
        elif numeric_score < lo - 2 or numeric_score > hi + 2:
            warn = True
            reasons.append(f"score drift 3-5: {numeric_score} vs {lo}-{hi}")

    if numeric_score is not None and ceiling is not None:
        ceiling = float(ceiling)
        if numeric_score > ceiling + 3:
            fail = True
            reasons.append(f"score inflation: {numeric_score} > ceiling {ceiling}+3")

    if fail:
        return {"pass": False, "score": 0, "reason": "; ".join(reasons) or "regression fail"}
    if warn:
        return {"pass": True, "score": 0.5, "reason": "WARN: " + "; ".join(reasons)}
    return {"pass": True, "score": 1, "reason": "fixture matches frozen expectation"}
