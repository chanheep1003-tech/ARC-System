#!/usr/bin/env python3
"""KOR-only external-source provenance and rights policy regression."""
from __future__ import annotations
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def read_yaml(rel: str) -> dict:
    path = ROOT / rel
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict), rel
    return doc

def main() -> None:
    manifest = read_yaml("SYSTEM_MANIFEST.yaml")
    rt = manifest["runtime"]
    reg_path = rt["korean_unseen_source_registry"]
    pol_path = rt["korean_learning_level_policy"]
    assert pol_path == "quality/korean/ARC_KOR_V1_V5_LEVEL_POLICY_V1.1.md"
    assert reg_path == "quality/korean/ARC_KOR_UNSEEN_CANDIDATES_V1.0.yaml"
    assert "learning_level_policy" not in rt, "V1-V5 must not be globally routed"
    assert not any(
        key.startswith("learning_level_v") for key in rt
    ), "Korean levels leaked into global manifest"
    for key in ("korean_unseen_source_necessity_gate", "korean_lyrics_full_text_copyright_gate", "korean_medieval_edition_and_period_gate"):
        assert rt[key] == "required", key

    registry = read_yaml(reg_path)
    assert registry["subject"] == "KOR" and registry["not_global_for_other_subjects"] is True
    assert registry["copyright_protocol"]["repository_stores_original_lyrics_full_text"] is False
    records = registry["candidates"]
    assert len(records) >= 12, len(records)
    assert len({r["id"] for r in records}) == len(records), "duplicate candidate ID"
    tags = {record["genre"] for record in records}
    assert {"popular-song-lyrics", "modern-poem", "modern-fiction", "arc-original-fiction"} <= tags, tags
    assert any(record["genre"].startswith("medieval-language") for record in records)
    for candidate in records:
        assert candidate["target_skills"] and candidate["selection"] and candidate["copyright_status"], candidate["id"]
        assert "excerpt_text" not in candidate and "raw_lyrics" not in candidate, candidate["id"]
        if candidate["genre"] == "popular-song-lyrics":
            assert candidate["copyright_status"].startswith("PERMISSION_OR_")
            assert candidate["authority_url"].startswith("https://")
        if candidate["genre"].startswith("medieval-language"):
            assert candidate["era"] in {"15C", "16C"}, candidate["id"]
            assert candidate["excerpt_status"] == "UNSELECTED", candidate["id"]
        if candidate["genre"] != "arc-original-fiction":
            assert candidate["authority_url"] and candidate["authority_url"].startswith("https://"), candidate["id"]
    legacy = (ROOT / "quality/ARC_V1_V5_LEARNING_LADDER_V1.0.md").read_text(encoding="utf-8")
    assert "DEPRECATED AS UNIVERSAL" in legacy
    policy = (ROOT / pol_path).read_text(encoding="utf-8")
    assert "KOR ONLY" in policy
    assert "문학" in policy and "비문학" in policy and "문법" in policy
    print(f"PASS KOR-only registry, {len(records)} candidates and explicit rights/status gates")

if __name__ == "__main__":
    main()
