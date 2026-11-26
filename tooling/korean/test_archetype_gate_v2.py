#!/usr/bin/env python3
"""V2 orthography archetype gate regression.

A synthetic 10-item block that follows quality/korean/ARC_KOR_ORTHO_ITEM_RULES_V2.0.md passes;
each injected fault (fake difficulty, spacing flood, missing fields, broken passage set, ...) fails
with its own code. Item texts are placeholders: this checks the contract, not content quality.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_archetype_gate", ROOT / "tooling/korean/archetype_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
LIB = "quality/korean/ARC_KOR_ORTHO_ARCHETYPES_V2.0.yaml"
TRAPS = ["T2_EXCEPTION_CONDITION", "T5_RULE_JURISDICTION", "T9_SUBCLAUSE_SWAP", "T8_PREANALYSIS_ERROR"]
OPTIONS = [f"선지 {n}의 예와 판단, 근거 조항을 함께 적은 문장" for n in range(1, 6)]
MARKED_VIEW = ["<학생이 쓴 글> ㉠ … ㉡ … ㉢ … ㉣ … ㉤ … ㉥ … ㉦ …", "선생님: 틀린 곳은 [A]란다."]


def item(n: int, arch: str, topic: str, difficulty: str, units: int, rules: list[str], levers: list[str], **extra) -> dict:
    answer = (n % 5) + 1
    judgments = []
    for k in range(1, 6):
        j = {"axis": "orthography", "c": "CORRECT" if k == answer else "STRONG", "claim": f"c{n}_{k}",
             "ev": ["VIEW", f"OPTION{k}"], "v": k == answer, "why": "근거"}
        if k != answer:
            j["trap"] = TRAPS[k % len(TRAPS)]
        judgments.append(j)
    base = {"item_id": f"V2T-{n:02d}", "archetype": arch, "topic": topic, "rules": rules,
            "judgment_units": units, "levers": levers, "stem": "<보기>를 바탕으로 탐구한 내용으로 적절하지 않은 것은?",
            "view": ["<보기> 규정 원문과 새 예문"], "options": OPTIONS, "answer": answer, "difficulty": difficulty,
            "judgments": judgments}
    base.update(extra)
    return base


def sample() -> dict:
    items = [
        item(1, "K1_RULE_APPLY", "SOUND", "D3", 5, ["제11항", "제11항 [붙임 1]"], ["SUBCLAUSE"]),
        item(2, "K11_FORM_CHOICE_SET", "DISTINCT", "D3", 5, ["제57항"], ["UNITS"]),
        item(3, "K3_CLASSIFY_TABLE", "SAISIOT", "D4", 15, ["제30항 1", "제30항 2"], ["UNITS", "SECOND_AXIS"]),
        item(4, "K4_PASSAGE_SET", "FORM", "D4", 8, ["제1항", "제19항"], ["PASSAGE_CONDITION"], set_id="P1"),
        item(5, "K4_PASSAGE_SET", "SPACING", "D4", 8, ["제41항", "제42항"], ["PASSAGE_CONDITION"], set_id="P1"),
        item(6, "K6_TEXT_MARKED_SPOTS", "SPACING", "D4", 7 + 1, ["제42항", "제43항"], ["UNITS", "RULES"], view=MARKED_VIEW),
        item(7, "K2_SUBCLAUSE_MATCH", "FORM", "D5", 12, ["제19항", "제19항 [붙임]", "제25항"], ["SUBCLAUSE", "PREANALYSIS"]),
        item(8, "K5_STATEMENT_AUDIT", "ABBREV", "D5", 12, ["제35항 [붙임 2]", "제39항", "제40항"], ["RULES", "CLAIM_WITH_REASON"]),
        item(9, "K7_MINIMAL_PAIR_WHY", "SAISIOT", "D4", 10, ["제30항", "제27항"], ["PREANALYSIS"]),
        item(10, "K8_SAME_FORM_TWO_FUNCTIONS", "SPACING", "D3", 8, ["제41항", "제42항"], ["CLAIM_WITH_REASON"]),
    ]
    return {"archetype_library": LIB, "balance_profile": "KOR_N_ORTHO_SCHOOL", "unit_size": 10,
            "user_override": "전 문항 객관식", "items": items}


def codes(report: dict) -> set[str]:
    return {f["code"] for f in report["findings"] if f["severity"] == "FAIL"}


def main() -> int:
    good = gate.analyze(sample())
    assert good["status"] == "PASS", good["findings"]
    assert good["tool"] == "ARC_KOR_ARCHETYPE_GATE_V1.1"

    def variant(mutate) -> set[str]:
        bundle = copy.deepcopy(sample())
        mutate(bundle)
        return codes(gate.analyze(bundle))

    def item_at(b: dict, n: int) -> dict:
        return b["items"][n - 1]

    assert "FAKE_DIFFICULTY_UNITS" in variant(lambda b: item_at(b, 9).update(judgment_units=5))
    assert "FAKE_DIFFICULTY_RULES" in variant(lambda b: item_at(b, 9).update(rules=["제30항"]))
    assert "FAKE_DIFFICULTY_LEVERS" in variant(lambda b: item_at(b, 7).update(levers=["SUBCLAUSE"]))
    assert "ARCHETYPE_DIFFICULTY_OUT_OF_RANGE" in variant(lambda b: item_at(b, 2).update(difficulty="D5", judgment_units=12, rules=["제57항", "제51항"], levers=["UNITS", "RULES"]))
    assert "ORTHO_FIELD_MISSING" in variant(lambda b: item_at(b, 1).pop("topic"))
    assert "TOPIC_UNKNOWN" in variant(lambda b: item_at(b, 1).update(topic="PRONUNCIATION"))
    assert "LEVER_UNKNOWN" in variant(lambda b: item_at(b, 1).update(levers=["HARDER"]))
    assert "PASSAGE_SET_INCOMPLETE" in variant(lambda b: item_at(b, 5).update(set_id="P2"))
    assert "MARKED_SPOT_COUNT" in variant(lambda b: item_at(b, 6).update(view=["<학생이 쓴 글> ㉠ … ㉡ … ㉢ …"]))
    assert "TOPIC_SHARE_OUT_OF_RANGE" in variant(lambda b: [it.update(topic="SPACING") for it in b["items"][:6]])
    assert "TOPIC_DIVERSITY_LOW" in variant(lambda b: [it.update(topic="FORM") for it in b["items"][:8]])
    assert "TEXTBOOK_EXAMPLE_FLOOD" in variant(lambda b: [it.update(textbook_example_reuse=True) for it in b["items"][:4]])
    assert "LEXICON_ONLY_TRAP" in variant(lambda b: item_at(b, 2).update(needs_lexicon=True))
    long_view = ["가" * 500]
    assert "LONG_VIEW_SHARE_HIGH" in variant(lambda b: [it.update(view=long_view) for it in b["items"][:2]])
    assert "LONG_VIEW_SHARE_HIGH" not in variant(lambda b: item_at(b, 1).update(view=long_view))
    assert "LEXICON_ONLY_TRAP" not in variant(lambda b: item_at(b, 2).update(needs_lexicon=True, lexicon_in_view=True))
    # Full 50-item bundles must cover all six topics.
    def fifty(b: dict) -> None:
        b["items"] = [dict(copy.deepcopy(it), item_id=f"V2T-{k}-{it['item_id']}", set_id=f"{it.get('set_id', '')}{k}")
                      for k in range(5) for it in b["items"]]
        b["unit_size"] = 10
    assert "TOPIC_COVERAGE_MISSING" not in variant(fifty)

    def fifty_without_distinct(b: dict) -> None:
        fifty(b)
        for it in b["items"]:
            if it["topic"] == "DISTINCT":
                it["topic"] = "FORM"
    assert "TOPIC_COVERAGE_MISSING" in variant(fifty_without_distinct)
    # Without the objective-only override the missing constructed items only warn.
    report = gate.analyze({**sample(), "user_override": None})
    assert report["status"] == "PASS" and "CONSTRUCTED_BELOW_RECOMMENDED" in {f["code"] for f in report["findings"]}
    print("archetype gate V2 regression PASS (block ok, 16 faults blocked, constructed warning only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
