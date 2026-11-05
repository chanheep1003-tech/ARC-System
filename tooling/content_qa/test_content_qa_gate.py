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

    print("ARC CONTENT QA GATE SMOKE: PASS")


if __name__ == "__main__":
    run()
