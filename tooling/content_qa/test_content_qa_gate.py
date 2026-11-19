#!/usr/bin/env python3
"""Behavioral smoke tests for the ARC content QA gate."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "arc_content_qa_gate", ROOT / "tooling/content_qa/content_qa_gate.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def option(option_id: str, verdict: str, claim_key: str, competitiveness: str) -> dict:
    return {
        "option_id": option_id,
        "verdict": verdict,
        "claim_key": claim_key,
        "axis": "concept_application",
        "evidence_refs": [f"SRC:{option_id}"],
        "competitiveness": competitiveness,
    }


def base_payload(subject: str = "SOC") -> dict:
    gates = {
        "FACTUAL_ACCURACY_REVIEW": "PASS",
        "OPTION_SEMANTIC_DUPLICATION_REVIEW": "PASS",
        "ANSWER_EVIDENCE_TRACE": "PASS",
        "SCOPE_EVIDENCE_TRACE": "PASS",
        "ALL_OPTION_AUDIT": "PASS",
        "UNIQUE_ANSWER": "PASS",
        "DIFFICULTY_MATCH": "PASS",
    }
    return {
        "schema_version": "ARC-QA-EVIDENCE-V1.0",
        "subject": subject,
        "item_count": 1,
        "item_format": "MCQ5",
        "uses_source_text": False,
        "items": [{
            "item_id": f"{subject}-001",
            "target_difficulty": "D4",
            "pass_a": {"answer": "3", "answer_evidence": ["SRC:A"]},
            "pass_b": {
                "answer": "3",
                "blind": True,
                "excluded_inputs": ["ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY"],
                "confidence": "HIGH",
                "answer_evidence": ["SRC:A"],
                "scope_trace": {"status": "IN_SCOPE", "source_refs": ["SCOPE:1"]},
                "option_judgments": [
                    option("1", "FALSE", "claim_1", "STRONG"),
                    option("2", "HALF_TRUE", "claim_2", "STRONG"),
                    option("3", "TRUE", "claim_3", "CORRECT"),
                    option("4", "FALSE", "claim_4", "MEDIUM"),
                    option("5", "UNSUPPORTED", "claim_5", "WEAK"),
                ],
                "second_best_option": "2",
                "second_best_risk": "MEDIUM",
                "reasoning_steps": 2,
                "evidence_count": 2,
                "immediate_elimination_count": 2,
                "transfer_required": True,
                "actual_difficulty": "D4",
            },
            "gates": gates,
        }],
        "set_gates": {name: "PASS" for name in mod.SET_GATES},
        "content_lock": True,
    }


def codes(result: dict) -> set[str]:
    return {entry["code"] for entry in result["findings"]}


def run() -> None:
    good = base_payload()
    result = mod.analyze(good)
    assert result["status"] == "PASS", result
    assert result["content_lock_allowed"] is True

    mismatch = copy.deepcopy(good)
    mismatch["items"][0]["pass_b"]["answer"] = "4"
    result = mod.analyze(mismatch)
    assert "ANSWER_AB_MISMATCH" in codes(result)
    assert "UNIQUE_ANSWER_INVALID" in codes(result)

    duplicate = copy.deepcopy(good)
    duplicate["items"][0]["pass_b"]["option_judgments"][1]["claim_key"] = "claim_1"
    result = mod.analyze(duplicate)
    assert "OPTION_SEMANTIC_DUPLICATION" in codes(result)

    short = copy.deepcopy(good)
    short["items"][0]["pass_b"]["reasoning_steps"] = 1
    result = mod.analyze(short)
    assert "D4_SHORT" in codes(result)

    d3_weak = copy.deepcopy(good)
    d3_weak["items"][0]["target_difficulty"] = "D3"
    d3_weak["items"][0]["pass_b"]["actual_difficulty"] = "D3"
    d3_weak["items"][0]["pass_b"]["reasoning_steps"] = 1
    assert mod.analyze(d3_weak)["status"] == "PASS"
    d3_weak["items"][0]["pass_b"]["immediate_elimination_count"] = 3
    assert "D3_SHORT" in codes(mod.analyze(d3_weak))
    d3_weak["items"][0]["pass_b"]["immediate_elimination_count"] = 1
    d3_weak["items"][0]["pass_b"]["option_judgments"][0]["competitiveness"] = "MEDIUM"
    d3_weak["items"][0]["pass_b"]["option_judgments"][1]["competitiveness"] = "MEDIUM"
    assert "D3_SHORT" in codes(mod.analyze(d3_weak))

    korean = base_payload("KOR")
    korean["items"][0]["stem_polarity"] = "POSITIVE"
    korean["items"][0]["pass_b"]["option_judgments"][1]["verdict"] = "FALSE"
    korean["items"][0]["pass_b"]["option_judgments"][4]["verdict"] = "FALSE"
    korean["uses_source_text"] = True
    korean["source_text_locks"] = [{
        "source_text_id": "KOR-TEXT-01",
        "source_origin": "USER_PROVIDED_SCHOOL_SUPPLEMENT",
        "source_role": "RAW_SCHOOL_SOURCE",
        "text_fidelity": "EXACT",
        "source_file_id": "school-file-1",
        "source_location": "p.2",
        "source_text_sha256": "a" * 64,
        "linked_item_ids": ["KOR-001"],
        "wording_lock": True,
        "punctuation_lock": True,
        "line_break_lock": True,
        "boundary_lock": True,
    }]
    result = mod.analyze(korean)
    assert result["status"] == "PASS", result

    negative = copy.deepcopy(korean)
    item = negative["items"][0]
    item["stem_polarity"] = "NEGATIVE"
    for judgement in item["pass_b"]["option_judgments"]:
        judgement["verdict"] = "FALSE" if judgement["option_id"] == "3" else "TRUE"
    assert mod.analyze(negative)["status"] == "PASS"
    multi_false = copy.deepcopy(negative)
    multi_false["items"][0]["pass_b"]["option_judgments"][0]["verdict"] = "FALSE"
    assert "UNIQUE_ANSWER_INVALID" in codes(mod.analyze(multi_false))
    missing_polarity = copy.deepcopy(korean)
    del missing_polarity["items"][0]["stem_polarity"]
    assert "STEM_POLARITY_MISSING" in codes(mod.analyze(missing_polarity))
    unsupported = copy.deepcopy(korean)
    unsupported["items"][0]["pass_b"]["option_judgments"][0]["verdict"] = "UNSUPPORTED"
    assert "KOR_OPTION_UNSUPPORTED" in codes(mod.analyze(unsupported))

    korean_bad = copy.deepcopy(korean)
    korean_bad["source_text_locks"][0]["source_origin"] = "ARC_N_OUTPUT"
    korean_bad["source_text_locks"][0]["text_fidelity"] = "WHITESPACE_NORMALIZED"
    result = mod.analyze(korean_bad)
    assert {"KOR_SOURCE_ORIGIN_FORBIDDEN", "KOR_SOURCE_NOT_EXACT"} <= codes(result)

    incomplete = copy.deepcopy(good)
    incomplete["items"][0]["pass_b"]["confidence"] = ""
    incomplete["items"][0]["pass_b"]["transfer_required"] = "yes"
    result = mod.analyze(incomplete)
    assert {"CONFIDENCE_INVALID", "TRANSFER_FLAG_INVALID"} <= codes(result)


    # --- Print-exam integrity lint: regressions from the 2026-11 orthography set review ---
    def lint_codes(bundle):
        return {(f["code"], f["severity"]) for f in mod.lint_bundle_text(bundle)}

    def j(why):
        return {"axis": "orthography", "why": why}

    # B-1 no-hint view: a derived decision formula may not sit in <보기>.
    hinted = {"items": [{"item_id": "H1", "stem": "<보기>를 바탕으로 적절하지 않은 것은?",
                         "view": ["[해설 자료] '하' 앞 받침이 [ㄱ, ㄷ, ㅂ]이면 '하'가 통째로 탈락한다."],
                         "options": ["a", "b", "c", "d", "e"], "judgments": [j("")] * 5}]}
    assert ("VIEW_SOLUTION_LABEL", "FAIL") in lint_codes(hinted)
    unlabeled = copy.deepcopy(hinted)
    unlabeled["items"][0]["view"] = ["'하' 앞 받침이 ㄱ, ㄷ, ㅂ이면 '하'가 통째로 탈락한다."]
    assert ("VIEW_SOLUTION_FORMULA", "FAIL") in lint_codes(unlabeled)
    official = copy.deepcopy(hinted)
    official["items"][0]["view"] = ["제40항 [붙임 2] 어간의 끝음절 '하'가 아주 줄 적에는 준 대로 적는다.",
                                    "[발음 자료] 깨끗하지 않다[깨끄타지 안타]", "[사전 뜻풀이] 생각하건대: 생각하다의 활용형"]
    assert not lint_codes(official), lint_codes(official)

    # B-4 self-identical correction and unintended spacing outside the target.
    selfsame = copy.deepcopy(official)
    selfsame["items"][0]["options"][0] = "'똑똑하다'를 '똑똑하다'로 적지 않는 것은 어간이 바뀌기 때문이다."
    assert ("OPTION_SELF_IDENTICAL_CORRECTION", "FAIL") in lint_codes(selfsame)
    stray = copy.deepcopy(official)
    stray["items"][0]["options"][1] = "아직 할게 남아 있다는 뜻이다."
    assert ("UNINTENDED_SPACING_ERROR", "FAIL") in lint_codes(stray)
    declared = copy.deepcopy(stray)
    declared["items"][0]["judgments"][1] = j("'할 게'로 띄어 써야 하므로 틀린 표기이다.")
    assert ("UNINTENDED_SPACING_ERROR", "FAIL") not in lint_codes(declared)

    # Core-headword typo: plan says 곗날, the option printed 옛날.
    typo = copy.deepcopy(official)
    typo["items"][0]["headwords"] = ["곗날"]
    typo["items"][0]["options"][2] = "옛날은 사이시옷을 적는다."
    found = [f for f in mod.lint_bundle_text(typo) if f["code"] == "HEADWORD_MISSING"]
    assert found and "옛날" in found[0]["message"], found

    # B-3 cross-item leak: the constructed-response answer printed in an earlier MCQ.
    leak = {"v6": {"area": "A"}, "items": [
        {"item_id": "M1", "stem": "바른 표기는?", "options": ["깨끗이 닦았다.", "꼼꼼이 보았다.", "일일히 셌다.", "번번히 졌다.", "솔직이 말했다."],
         "judgments": [j("")] * 5},
        {"item_id": "C1", "format": "CR", "stem": "다음 문장의 밑줄 친 말을 바르게 고쳐 쓰시오. 방을 깨끗히 치웠다.",
         "answer_targets": ["깨끗이"], "model_answer": "'깨끗이'", "conditions": ["한 단어로 쓸 것."]},
    ]}
    found = {f["code"] for f in mod.lint_bundle_text(leak) if f["severity"] == "FAIL"}
    assert "CROSS_ITEM_ANSWER_LEAK" in found, found
    reuse = copy.deepcopy(leak)
    reuse["items"][1]["answer_targets"] = ["정갈히"]
    reuse["items"][1]["stem"] = "‘방을 깨끗이 닦았다.’를 활용하여 부사 파생 규정을 서술하시오."
    assert "CROSS_ITEM_EXAMPLE_REUSE" in {f["code"] for f in mod.lint_bundle_text(reuse)}

    print("ARC PRINT-EXAM INTEGRITY LINT: PASS")
    print("ARC CONTENT QA GATE SMOKE: PASS")


if __name__ == "__main__":
    run()
