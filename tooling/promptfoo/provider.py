import json
import os
import shlex
import subprocess
from pathlib import Path

def _run(kind, prompt, context):
    vars_ = context.get("vars", {})
    fixture_id = str(vars_.get("fixture_id", ""))
    prefix = kind.upper()

    result_dir = os.environ.get(f"ARC_{prefix}_RESULTS_DIR")
    if result_dir:
        p = Path(result_dir) / f"{fixture_id}.json"
        if p.exists():
            return {"output": p.read_text(encoding="utf-8")}

    cmd = os.environ.get(f"ARC_{prefix}_CMD")
    if not cmd:
        return {
            "error": (
                f"Set ARC_{prefix}_CMD or ARC_{prefix}_RESULTS_DIR "
                f"for the {kind} regression provider."
            )
        }

    payload = {
        "provider_kind": kind,
        "prompt": prompt,
        "fixture_id": fixture_id,
        "vars": vars_,
    }
    proc = subprocess.run(
        shlex.split(cmd),
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        timeout=int(os.environ.get("ARC_REGRESSION_TIMEOUT_SEC", "180")),
    )
    if proc.returncode != 0:
        return {"error": f"{kind} command failed: {proc.stderr[-2000:]}"}

    out = proc.stdout.strip()
    if not out:
        return {"error": f"{kind} command returned empty stdout"}

    try:
        parsed = json.loads(out)
    except json.JSONDecodeError:
        return {"error": f"{kind} command must return JSON on stdout"}

    return {"output": json.dumps(parsed, ensure_ascii=False)}

def baseline_api(prompt, options, context):
    return _run("baseline", prompt, context)

def candidate_api(prompt, options, context):
    return _run("candidate", prompt, context)

def call_api(prompt, options, context):
    return candidate_api(prompt, options, context)
