import json
import os
import shlex
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

def call_api(prompt, options, context):
    vars_ = context.get("vars", {})
    fixture_id = str(vars_.get("fixture_id", ""))

    result_dir = os.environ.get("ARC_CANDIDATE_RESULTS_DIR")
    if result_dir:
        p = Path(result_dir) / f"{fixture_id}.json"
        if p.exists():
            return {"output": p.read_text(encoding="utf-8")}

    cmd = os.environ.get("ARC_CANDIDATE_CMD")
    if not cmd:
        return {
            "error": (
                "Set ARC_CANDIDATE_CMD to an executable that reads JSON from stdin "
                "and returns candidate QA JSON, or set ARC_CANDIDATE_RESULTS_DIR."
            )
        }

    payload = {
        "prompt": prompt,
        "fixture_id": fixture_id,
        "vars": vars_,
    }
    proc = subprocess.run(
        shlex.split(cmd),
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        timeout=int(os.environ.get("ARC_CANDIDATE_TIMEOUT_SEC", "180")),
    )
    if proc.returncode != 0:
        return {"error": f"candidate command failed: {proc.stderr[-2000:]}"}

    out = proc.stdout.strip()
    if not out:
        return {"error": "candidate command returned empty stdout"}

    try:
        parsed = json.loads(out)
    except json.JSONDecodeError:
        return {"error": "candidate command must return JSON on stdout"}

    return {"output": json.dumps(parsed, ensure_ascii=False)}
