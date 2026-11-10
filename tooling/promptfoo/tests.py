import re
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIXTURE_FILE = ROOT / "quality" / "regression" / "REGRESSION_FIXTURES_V1.0.yaml"

def _anchor_text(pack_path: Path, anchor_id: str) -> str:
    text = pack_path.read_text(encoding="utf-8")
    pat = rf"(?ms)^###\s+{re.escape(anchor_id)}\b.*?(?=^###\s+|^##\s+|\Z)"
    m = re.search(pat, text)
    if not m:
        raise ValueError(f"Anchor not found: {anchor_id} in {pack_path}")
    return m.group(0).strip()

def generate_tests(config=None):
    data = yaml.safe_load(FIXTURE_FILE.read_text(encoding="utf-8"))
    tests = []
    for subject, pack in data["packs"].items():
        pack_path = ROOT / pack["source"]
        for case in pack["cases"]:
            vars_ = {
                "fixture_id": case["fixture_id"],
                "subject": subject,
                "fixture_class": case["class"],
                "fixture_text": _anchor_text(pack_path, case["anchor_id"]),
                "expected_decision": case["expected_decision"],
                "expected_hard_fail": bool(case.get("expected_hard_fail", False)),
                "expected_item_min": case.get("expected_item_min"),
                "expected_item_max": case.get("expected_item_max"),
                "expected_max_item": case.get("expected_max_item"),
                "forbidden_decisions": case.get("forbidden_decisions", []),
            }
            tests.append({
                "description": case["fixture_id"],
                "vars": vars_,
                "metadata": {"anchor_id": case["anchor_id"], "subject": subject},
            })
    if len(tests) != int(data["fixture_count"]):
        raise ValueError(f"Fixture count mismatch: {len(tests)} != {data['fixture_count']}")
    return tests
