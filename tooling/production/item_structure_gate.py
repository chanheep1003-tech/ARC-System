#!/usr/bin/env python3
"""ARC N 문항 구조 게이트 (D-22/D-23).

AI 풀이자의 체감 난이도와 별개로, 문항 구조에서 결정적으로 확인할 수 있는 것을 검사한다.
  1. 출제 구조 라이브러리: 문항마다 template 코드가 있어야 하고, 난이도 라벨이 템플릿의 허용 범위 안이어야 한다.
  2. 구조 점수: 풀이 단계, 자료 가공, 판단 진술 수, 비교 대상 수, 계산 여부를 세어 구조 밴드(D2/D3/D4)를 계산한다.
  3. 범위 대비 난이도 가능성(feasibility): 소단원 수에 비해 D4+ 비중이 과하면 생성 전에 사용자에게 묻도록 막는다.
  4. 자동 검사: 정답 선지 길이 단서, 절대 표현 단서, 정답 번호 분포, 교과서 문장 복제.
이 모듈은 파일을 쓰지 않는다. check_bundle()은 dict를 반환한다.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "quality/exam_style/EXAM_STRUCTURE_LIBRARY_V1.0.yaml"
RANK = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}
ABSOLUTE_WORDS = ["언제나", "어떤 경우에도", "반드시", "오직", "전혀", "절대", "모든 경우", "얼마든지", "무조건", "항상", "순전히"]
STATEMENT_RE = re.compile(r"^\s*(?:[ㄱ-ㅎ]\.|학생\s*[A-Z]\s*:|\([가-라]\)|[㉠-㉤]|[갑-병]\s*(?:\(.*?\))?\s*:)")
CIRC = "①②③④⑤"
SHINGLE = 14


def load_library(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or LIBRARY).read_text(encoding="utf-8"))


def _text_of(item: dict[str, Any]) -> str:
    parts = [str(item.get("stem", ""))] + [str(x) for x in item.get("view", [])] + [str(o) for o in item.get("options", [])]
    table = item.get("table")
    if isinstance(table, dict):
        parts += [str(c) for c in table.get("header", [])]
        for row in table.get("rows", []):
            parts += [str(c) for c in row]
    return "\n".join(parts)


def statement_count(item: dict[str, Any]) -> int:
    lines = [str(x) for x in item.get("view", [])]
    n = sum(1 for ln in lines if STATEMENT_RE.match(ln))
    if n == 0 and lines:  # 한 단락에 ①~⑤ 밑줄 진술이 들어간 원전형
        n = max(sum(joined.count(c) for c in CIRC) for joined in ["".join(lines)])
        n = n if n >= 3 else 0
    return n


def entity_count(item: dict[str, Any], subject: str, lib: dict[str, Any]) -> int:
    terms = lib.get("structure_score", {}).get("entity_terms", {}).get(subject, [])
    text = _text_of(item)
    return sum(1 for t in terms if t in text)


def structure_features(item: dict[str, Any], subject: str, lib: dict[str, Any]) -> dict[str, Any]:
    w = lib["structure_score"]["weights"]
    tpl = lib.get("templates", {}).get(item.get("template"), {})
    view = [str(x) for x in item.get("view", [])]
    steps = item.get("reasoning_steps")
    steps = min(int(steps), 5) if isinstance(steps, (int, float)) and not isinstance(steps, bool) else 1
    stmts = statement_count(item)
    ents = entity_count(item, subject, lib)
    feats = {
        "reasoning_steps": steps * w["reasoning_steps"],
        "table_or_diagram": w["table_or_diagram"] if (item.get("table") or any("[그림]" in ln for ln in view)) else 0.0,
        "long_material": w["long_material"] if len(view) >= 4 else 0.0,
        "statements_3": w["statements_3"] if stmts >= 3 else 0.0,
        "statements_4": w["statements_4"] if stmts >= 4 else 0.0,
        "entity_extra": w["entity_extra"] * (2 if ents >= 3 else 1 if ents >= 2 else 0),
        "computation": w["computation"] if tpl.get("computation") else 0.0,
        "low_elimination": w["low_elimination"] if (isinstance(item.get("immediate_elimination"), int) and item["immediate_elimination"] <= 1) else 0.0,
        "supplied_concept": w.get("supplied_concept", 0.0) if (item.get("supplied_concepts") and len(view) >= 1) else 0.0,
    }
    score = round(sum(feats.values()), 2)
    return {"features": feats, "score": score}


def band_of(score: float, lib: dict[str, Any]) -> str:
    bands = lib["structure_score"]["bands"]
    if score <= bands["D2"][1]:
        return "D2"
    if score <= bands["D3"][1]:
        return "D3"
    return "D4"


def _mcq(raw: dict[str, Any]) -> list[dict[str, Any]]:
    return [it for it in raw.get("items", []) if isinstance(it, dict) and it.get("format", "MCQ") == "MCQ"]


def _f(code: str, severity: str, message: str, **extra: Any) -> dict[str, Any]:
    return {"code": code, "severity": severity, "message": message, **extra}


def _symbolic(options: list[str]) -> bool:
    """ㄱ, ㄴ 조합·㉠~㉤·(가)(나) 처럼 길이가 의미 없는 선지."""
    return max((len(o) for o in options), default=0) <= 12


def outside_concept_findings(item: dict[str, Any], subject: str, lib: dict[str, Any]) -> list[dict[str, Any]]:
    """D-24: 교과서 밖 용어는 view 에서 정의를 줄 때만 쓸 수 있다(item.supplied_concepts 에 기록)."""
    rule = lib.get("supplied_concept_rule") or {}
    terms = rule.get("outside_terms", {}).get(subject, [])
    markers = rule.get("definitional_markers", [])
    supplied = [str(x) for x in item.get("supplied_concepts", []) or []]
    view = [str(x) for x in item.get("view", [])]
    out = []
    for term in terms:
        in_text = _text_of(item)
        if term not in in_text:
            continue
        defined = any(term in ln and any(m in ln for m in markers) for ln in view)
        if term in supplied and defined:
            continue
        out.append(_f("OUTSIDE_CONCEPT_NOT_SUPPLIED", "FAIL",
                      f"{item.get('item_id')}: 교과서 밖 개념 '{term}' 을(를) 학생이 안다고 가정했다. view 에서 정의를 주고 supplied_concepts 에 기록해야 한다(D-24)", item_id=item.get("item_id")))
    return out


def length_cue(item: dict[str, Any]) -> dict[str, Any] | None:
    opts = [str(o) for o in item.get("options", [])]
    if len(opts) != 5 or _symbolic(opts) or not isinstance(item.get("answer"), int):
        return None
    a = item["answer"] - 1
    others = [len(o) for i, o in enumerate(opts) if i != a]
    ratio = len(opts[a]) / (sum(others) / len(others))
    longest = len(opts[a]) == max(len(o) for o in opts) and len(opts[a]) > max(others)
    if longest and ratio > 1.25:
        return _f("LENGTH_CUE_ANSWER_LONGEST", "FAIL", f"{item.get('item_id')}: 정답 선지가 가장 길고 평균 오답의 {ratio:.2f}배", item_id=item.get("item_id"))
    if longest and ratio > 1.15:
        return _f("LENGTH_CUE_ANSWER_LONGEST_MILD", "WARN", f"{item.get('item_id')}: 정답 선지가 가장 길다({ratio:.2f}배)", item_id=item.get("item_id"))
    return None


def absolute_word_cue(item: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    opts = [str(o) for o in item.get("options", [])]
    if len(opts) == 5 and isinstance(item.get("answer"), int) and not _symbolic(opts):
        a = item["answer"] - 1
        has = [any(w in o for w in ABSOLUTE_WORDS) for o in opts]
        wrong = sum(h for i, h in enumerate(has) if i != a)
        if not has[a] and wrong >= 3:
            out.append(_f("ABSOLUTE_WORD_CUE", "FAIL", f"{item.get('item_id')}: 오답 {wrong}개에만 절대 표현이 있어 정답이 드러난다", item_id=item.get("item_id")))
        elif not has[a] and wrong == 2:
            out.append(_f("ABSOLUTE_WORD_CUE_MILD", "WARN", f"{item.get('item_id')}: 오답 2개에만 절대 표현이 있다", item_id=item.get("item_id")))
    for ln in item.get("view", []):
        if STATEMENT_RE.match(str(ln)) and any(w in str(ln) for w in ABSOLUTE_WORDS):
            out.append(_f("ABSOLUTE_WORD_IN_STATEMENT", "WARN", f"{item.get('item_id')}: 진술에 절대 표현이 있다(거짓 진술 단서 가능): {str(ln)[:30]}", item_id=item.get("item_id")))
    return out


def position_balance(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    answers = [it.get("answer") for it in items if isinstance(it.get("answer"), int)]
    out: list[dict[str, Any]] = []
    if len(answers) < 5:
        return out
    limit = math.ceil(len(answers) / 5) + 1
    for pos in range(1, 6):
        c = answers.count(pos)
        if c > limit:
            out.append(_f("ANSWER_POSITION_BIAS", "FAIL", f"정답 번호 {pos}이(가) {c}개로 한도 {limit}개를 넘는다"))
    run = 1
    for i in range(1, len(answers)):
        run = run + 1 if answers[i] == answers[i - 1] else 1
        if run >= 3:
            out.append(_f("ANSWER_POSITION_RUN", "FAIL", f"문항 {i - 1}~{i + 1}번이 같은 정답 번호가 연속된다"))
            break
    return out


def _shingles(text: str) -> set[str]:
    t = re.sub(r"\s+", "", text)
    return {t[i:i + SHINGLE] for i in range(max(0, len(t) - SHINGLE + 1))}


def textbook_copy(items: list[dict[str, Any]], source_texts: list[str] | None) -> list[dict[str, Any]]:
    if not source_texts:
        return [_f("TEXTBOOK_COPY_UNCHECKED", "WARN", "교과서 원문이 제공되지 않아 교과서 문장 복제를 확인하지 못했다(D-21). source_texts 를 넘겨야 한다.")]
    book: set[str] = set()
    for s in source_texts:
        book |= _shingles(s)
    out = []
    for it in items:
        pieces = [str(o) for o in it.get("options", [])] + [str(x) for x in it.get("view", [])]
        for p in pieces:
            sh = _shingles(p)
            if len(sh) < 4:
                continue
            ratio = len(sh & book) / len(sh)
            if ratio >= 0.6:
                out.append(_f("TEXTBOOK_COPY", "FAIL", f"{it.get('item_id')}: 선지/보기 문장이 교과서와 {ratio:.0%} 겹친다: {p[:30]}", item_id=it.get("item_id")))
                break
    return out


def feasibility(raw: dict[str, Any], lib: dict[str, Any]) -> list[dict[str, Any]]:
    """범위(소단원 수)에 비해 D4+ 목표가 과한지 요청 단계에서 확인한다. FAIL이면 사용자에게 묻는다."""
    spec = raw.get("request_spec")
    if raw.get("product_mode") != "ARC_N" or not isinstance(spec, dict):
        return []
    targets = spec.get("difficulty_targets")
    if not isinstance(targets, dict) or "D45" not in targets:
        return []
    scope = raw.get("scope_profile")
    if not isinstance(scope, dict) or type(scope.get("subunit_count")) is not int or scope["subunit_count"] < 1:
        return [_f("REQUEST_SCOPE_PROFILE_MISSING", "WARN", "scope_profile.subunit_count 가 없어 범위 대비 난이도 가능성을 확인하지 못했다. 범위의 소단원 수를 기록해야 한다.")]
    fz = lib["feasibility"]
    cap = min(fz["max_cap"], fz["base_cap"] + fz["per_extra_subunit"] * (scope["subunit_count"] - 1))
    tol = float(spec.get("tolerance", 0.12))
    if targets["D45"] > cap + tol and spec.get("feasibility_acknowledged_by") != "USER":
        return [_f("REQUEST_DIFFICULTY_INFEASIBLE_FOR_SCOPE", "FAIL",
                   f"ASK THE USER: 소단원 {scope['subunit_count']}개 범위에서 D4+ {targets['D45']:.0%} 는 가능성 기준({cap:.0%}+허용 {tol:.0%}) 을 넘는다. "
                   "(1) 범위를 넓힌다 (2) D4+ 목표를 낮춘다 (3) 그대로 진행한다를 물어보고, 그대로 진행하면 request_spec.feasibility_acknowledged_by: USER 를 기록한다.",
                   cap=cap, subunit_count=scope["subunit_count"])]
    return []


def check_bundle(raw: dict[str, Any], *, source_texts: list[str] | None = None, lib: dict[str, Any] | None = None,
                 enforce_templates: bool = True) -> dict[str, Any]:
    lib = lib or load_library()
    subject = str(raw.get("subject", "")).upper()
    items = _mcq(raw)
    findings: list[dict[str, Any]] = []
    struct_rows = []
    for it in items:
        iid = it.get("item_id")
        label = it.get("difficulty")
        tpl_code = it.get("template")
        tpl = lib["templates"].get(tpl_code) if tpl_code else None
        if enforce_templates:
            if not tpl_code:
                findings.append(_f("TEMPLATE_MISSING", "FAIL", f"{iid}: template 코드가 없다(출제 구조 라이브러리 D-22)", item_id=iid))
            elif tpl is None:
                findings.append(_f("TEMPLATE_UNKNOWN", "FAIL", f"{iid}: 라이브러리에 없는 template {tpl_code}", item_id=iid))
            elif tpl["subject"] != subject:
                findings.append(_f("TEMPLATE_SUBJECT_MISMATCH", "FAIL", f"{iid}: template {tpl_code} 는 {tpl['subject']} 용이다", item_id=iid))
            elif label in RANK:
                lo, hi = (RANK[x] for x in tpl["difficulty"])
                if not lo <= RANK[label] <= hi:
                    findings.append(_f("TEMPLATE_DIFFICULTY_OUT_OF_RANGE", "FAIL",
                                       f"{iid}: 라벨 {label} 은 template {tpl_code} 의 허용 범위 {tpl['difficulty']} 밖", item_id=iid))
        sf = structure_features(it, subject, lib)
        band = band_of(sf["score"], lib)
        struct_rows.append({"item_id": iid, "label": label, "template": tpl_code, "score": sf["score"], "band": band})
        if label in RANK and RANK[label] > RANK[band]:
            sev = "FAIL" if label == "D4" else "WARN"
            findings.append(_f("STRUCTURE_BAND_BELOW_LABEL", sev,
                               f"{iid}: 라벨 {label} 인데 구조 점수 {sf['score']} 는 {band} 밴드다(판단 횟수·자료 가공이 부족하다)", item_id=iid, score=sf["score"], band=band))
        findings += outside_concept_findings(it, subject, lib)
        lc = length_cue(it)
        if lc:
            findings.append(lc)
        findings += absolute_word_cue(it)
    findings += position_balance(items)
    findings += textbook_copy(items, source_texts)
    # 구조 밴드 분포 vs 사용자 목표
    spec = raw.get("request_spec") if isinstance(raw.get("request_spec"), dict) else None
    distribution = None
    if items:
        n = len(items)
        d = {k: sum(1 for r in struct_rows if r["band"] == k) / n for k in ("D2", "D3", "D4")}
        distribution = {"D2": round(d["D2"], 3), "D3": round(d["D3"], 3), "D45": round(d["D4"], 3)}
        if spec and isinstance(spec.get("difficulty_targets"), dict):
            t = spec["difficulty_targets"]
            tol = float(spec.get("tolerance", 0.12))
            for key, got in distribution.items():
                if key in t and abs(got - t[key]) > tol:
                    findings.append(_f("STRUCTURE_DISTRIBUTION_OFF_TARGET", "WARN",
                                       f"구조 점수 기준 {key} 비율 {got:.0%} 가 목표 {t[key]:.0%} ±{tol:.0%} 밖이다(풀이 평가 전 사전 점검)"))
    findings = feasibility(raw, lib) + findings
    status = "FAIL" if any(f["severity"] == "FAIL" for f in findings) else ("WARN" if findings else "PASS")
    return {"tool": "ARC_ITEM_STRUCTURE_GATE_V1.0", "status": status, "structure_distribution": distribution,
            "items": struct_rows, "findings": findings}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: item_structure_gate.py <items.yaml> [textbook_text_file ...]", file=sys.stderr)
        return 2
    raw = yaml.safe_load(Path(argv[1]).read_text(encoding="utf-8"))
    texts = [Path(p).read_text(encoding="utf-8") for p in argv[2:]] or None
    res = check_bundle(raw, source_texts=texts)
    print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False, width=200))
    return 1 if res["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
