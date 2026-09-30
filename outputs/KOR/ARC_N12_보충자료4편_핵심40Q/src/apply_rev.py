# -*- coding: utf-8 -*-
"""V1.0 문항(Q)에 V1.1 개정(REV)을 덮어쓴다. 계보: parent=N12 V1.0 동일 번호 / change=OPTION_REBUILD·ASK_SHIFT."""
import revise_n12  # noqa: F401
from revise_n12 import REV

def apply(Q):
    keep_e = []
    for n, r in REV.items():
        q = Q[n - 1]
        q["choices"] = list(r["choices"]); q["c"] = r["c"]; q["pts"] = r["pts"]
        if r["stem"]: q["stem"] = r["stem"]
        if r["box"]: q["box"] = r["box"]
        if r["table"]: q["table"] = r["table"]
        if r["e"]: q["e"] = r["e"]
        else: keep_e.append(n)
        q["rev"] = "V1.1 OPTION_REBUILD"
    return keep_e
