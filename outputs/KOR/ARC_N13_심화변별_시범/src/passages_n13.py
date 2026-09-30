# -*- coding: utf-8 -*-
"""N°13 심화 변별: N°11의 시험 범위 지문 11편을 그대로 사용(외부 지문 추가 없음). 문항이 쓰지 않는 ㉠~㉤ 표기는 모두 제거하고
지문당 2문항(시범)의 범위(rng)로 다시 매긴다."""
import re, copy
from passages_n11 import SETS as _S

def _strip(x):
    if isinstance(x, str): return re.sub(r"\{(.)\|([^}]*)\}", r"\2", x)
    if isinstance(x, list): return [_strip(i) for i in x]
    if isinstance(x, tuple): return tuple(_strip(i) for i in x)
    if isinstance(x, dict): return {k: (v if k == "rng" else _strip(v)) for k, v in x.items()}
    return x

SETS = []
for k, st in enumerate(_S):
    d = _strip(copy.deepcopy(st)); d["rng"] = (2 * k + 1, 2 * k + 2); SETS.append(d)
