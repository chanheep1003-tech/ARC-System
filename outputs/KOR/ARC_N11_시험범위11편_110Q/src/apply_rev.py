# -*- coding: utf-8 -*-
"""V1.0 문항(Q)에 V1.1 개정(REV)을 덮어쓴다. 계보: parent=N11 V1.0 동일 번호 / change=OPTION_REBUILD."""
import revise_a, revise_b, revise_c, revise_d, revise_e, revise_f, revise_g  # noqa: F401  (REV 채우기; e는 후속 보정, f는 V1.2 난도 상향)
from revise_a import REV

def apply(Q):
    keep_e = []
    for n, r in REV.items():
        q = Q[n - 1]
        if r.get("reset"):                      # V1.2: 발문 유형 자체를 바꾼 문항은 이전 <보기>·표·고정 여부를 비운다
            for k in ("box", "table", "boxpre", "boxleft"): q.pop(k, None)
            q["fixed"] = bool(r.get("fixed"))
        if r.get("boxleft"): q["boxleft"] = True
        q["choices"] = list(r["choices"]); q["c"] = r["c"]; q["pts"] = r["pts"]
        if r["stem"]: q["stem"] = r["stem"]
        if r["box"]: q["box"] = r["box"]
        if r["table"]: q["table"] = r["table"]
        if r["e"]: q["e"] = r["e"]
        else: keep_e.append(n)
        q["rev"] = "V1.1 OPTION_REBUILD"
    return keep_e
