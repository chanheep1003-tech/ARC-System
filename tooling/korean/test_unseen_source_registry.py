#!/usr/bin/env python3
"""Korean-only just-in-time unseen source and real exam inventory regression.

A config test does not prove live retrieval was performed for an actual item.
"""
from __future__ import annotations
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def read_yaml(path: str) -> dict:
    obj = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(obj, dict), path
    return obj

def test_dynamic_source_policy() -> None:
    runtime = read_yaml("SYSTEM_MANIFEST.yaml")["runtime"]
    policy_path = "quality/korean/ARC_KOR_DYNAMIC_SOURCE_SELECTION_V1.0.yaml"
    assert runtime["korean_dynamic_source_selection_policy"] == policy_path
    assert runtime["korean_unseen_sources_selected_per_item"] == "required"
    assert runtime["korean_fixed_candidate_pool"] == "forbidden"
    assert runtime["korean_learning_level_policy"] == "quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md"
    assert "learning_level_policy" not in runtime
    assert "korean_unseen_source_registry" not in runtime
    assert all(not k.startswith("learning_level_v") for k in runtime)
    for key in ("korean_unseen_source_necessity_gate",
                "korean_lyrics_full_text_copyright_gate",
                "korean_medieval_edition_and_period_gate"):
        assert runtime[key] == "required", key

    config = read_yaml(policy_path)
    assert config["subject"] == "KOR" and config["scope_only"] is True
    assert config["selection_mode"] == "PER_ITEM_JUST_IN_TIME_SEARCH"
    assert config["fixed_candidate_pool"] is False
    assert config["reuse_from_preselected_title_list"] is False
    assert len(config["steps"]) >= 6
    for genre in ("literature", "nonfiction", "medieval_grammar", "modern_orthography"):
        assert config["genres"][genre]["required"], genre
    rights = config["rights"]
    assert rights["store_full_copyrighted_lyrics_in_repo"] is False
    assert rights["print_copyrighted_excerpt_without_review"] is False
    essential = {"item_id", "search_queries", "search_timestamp", "considered_sources",
                 "selected_source_url", "exact_edition_and_span", "rights_decision",
                 "why_this_passage", "why_unseen_passage_needed", "five_option_truth_receipt"}
    assert essential <= set(config["receipt_required"])
    assert config["on_failure"] == "REVIEW_PENDING"

    previous = read_yaml("quality/korean/ARC_KOR_UNSEEN_CANDIDATES_V1.0.yaml")
    assert previous["fixed_candidate_pool"] is False
    assert previous["candidates"] == []
    assert previous["superseded_by"] == policy_path

    older = (ROOT / "quality/ARC_V1_V5_LEARNING_LADDER_V1.0.md").read_text(encoding="utf-8")
    assert "DEPRECATED AS UNIVERSAL" in older
    policy = (ROOT / runtime["korean_learning_level_policy"]).read_text(encoding="utf-8")
    assert "KOR ONLY" in policy
    assert all(x in policy for x in ("문학", "비문학", "문법", "V6"))
    assert runtime["korean_learning_level_v5"] == "ARC_FINAL_DONGBUK_SIMULATION"
    assert runtime["korean_learning_level_v6"] == "ARC_N_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY"
    v6 = (ROOT / runtime["korean_v6_specialist_policy"]).read_text(encoding="utf-8")
    assert "KOR ONLY" in v6 and "ARC N°" in v6 and "V5 ARC FINAL" in v6
    assert all(x in v6 for x in ("산 넘어 산", "너머", "제15항", "독립풀이", "100문항"))
    for v6_gate in ("korean_v6_no_fixed_lexeme_bank", "korean_v6_lexical_pos_and_clause_evidence", "korean_v6_blind_solution_before_answer"):
        assert runtime[v6_gate] == "required", v6_gate
    assert "learning_level_v6" not in runtime and "korean_learning_level_v6" in runtime


def test_grade1_exam_inventory() -> None:
    runtime = read_yaml("SYSTEM_MANIFEST.yaml")["runtime"]
    inventory = read_yaml(runtime["korean_grade1_exam_inventory"])
    assert inventory["subject"] == "KOR" and inventory["grade"] == 1
    originals = inventory["known_originals"]
    assert len(originals) == 3
    known = {(x["year"], x["semester"], x["exam"]): x for x in originals}
    assert set(known) == {(2025, 2, "final"), (2026, 1, "midterm"), (2026, 2, "midterm")}
    assert all(x["status"] == "VERIFIED" for x in originals)
    new = known[(2026, 1, "midterm")]
    assert new["file_id"] == "1Sh7VxadM72s6QUH0e0E55oVdjBpYmDzn"
    assert new["questions"] == {"mcq": 20, "constructed": 4}
    assert new["source_zip_id"] == "1-rwkpvattljgrr5caM-iRc_EAN-Q3T0K"

    session = inventory["newly_indexed_session"]
    assert (session["year"], session["semester"], session["exam"]) == (2026, 1, "midterm")
    assert session["source_zip_kept_in_inbox"] is True
    files = session["original_papers"]
    assert len(files) == 7
    assert len({x["subject"] for x in files}) == 7
    assert new["file_id"] in {x["file_id"] for x in files}

    common = read_yaml(inventory["cross_subject_exam_index"])
    assert common["exam_id"] == "DONGBUK_G1_2026_S1_MID"
    assert common["zip_preserved_in_original_inbox"] is True
    assert len(common["subjects"]) == 7
    assert len({x["file_id"] for x in common["subjects"]}) == 7
    assert {x["file_id"] for x in files} == {x["file_id"] for x in common["subjects"]}
    assert all(len(x["sha256_uploaded_pdf"]) == 64 for x in common["subjects"])
    assert all(len(x["sha256_original_zip_member"]) == 64 for x in common["subjects"])
    assert {x["subject"] for x in common["subjects"]} == {"KOR", "ENG", "MATH", "INFO", "SCI", "SOC", "HIST"}
    kor = next(x for x in common["subjects"] if x["subject"] == "KOR")
    assert kor["sha256_uploaded_pdf"] == (
        "f40409ba3d141a1fdb2a977feb2ce43347ccddc3c8bdbe405a209ca084e75fd8"
    )
    assert kor["sha256_original_zip_member"] == (
        "934faece3bba5ae2f117db8b7b99c7390a25f1114455bde590f33c856623f094"
    )

    excluded = inventory["user_confirmed_not_available"]
    assert {(x["year"], x["semester"], x["exam"]) for x in excluded} == {
        (2025, 1, "midterm"), (2025, 1, "final")}
    remaining = inventory["missing_search_targets"]
    assert {(x["year"], x["semester"], x["exam"]) for x in remaining} == {
        (2025, 2, "midterm"), (2026, 1, "final")}
    assert all(x["status"] == "NOT_FOUND_IN_CURRENT_SEARCH" for x in remaining)
    assert inventory["future"][0]["status"] == "NOT_YET_HELD_AS_OF_2026_11_06"

def main() -> None:
    test_dynamic_source_policy()
    test_grade1_exam_inventory()
    print("PASS: KOR V1-V6 incl V6 specialist + per-item sources + 3 verified papers + 7-subject archive")

if __name__ == "__main__":
    main()
