#!/usr/bin/env python3
"""Run the GitHub Actions smoke workflow steps locally.

Reads .github/workflows/arc-tooling-smoke.yml and executes every `run:` step
in order, so the local result matches CI. Dependency-install steps
(pip / apt-get) are skipped; install them once with:

    python -m pip install -r tooling/requirements-smoke.txt

Usage:
    python tooling/run_ci_local.py            # run all steps, summary at end
    python tooling/run_ci_local.py --fail-fast
    python tooling/run_ci_local.py --only checksum   # substring match on step name
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "arc-tooling-smoke.yml"
SKIP_MARKERS = ("pip install", "apt-get")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fail-fast", action="store_true")
    ap.add_argument("--only", default=None, help="run only steps whose name contains this text")
    ap.add_argument("--tail", type=int, default=15, help="lines of output shown for a failing step")
    args = ap.parse_args()

    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    results: list[tuple[str, str, float]] = []
    for job_name, job in workflow["jobs"].items():
        for step in job.get("steps", []):
            script = step.get("run")
            if not script:
                continue
            name = step.get("name", script.splitlines()[0][:60])
            if args.only and args.only.lower() not in name.lower():
                continue
            if any(marker in script for marker in SKIP_MARKERS):
                results.append((name, "SKIP", 0.0))
                continue
            started = time.time()
            # CI uses `python`; make sure the same interpreter runs here.
            proc = subprocess.run(
                ["bash", "-eo", "pipefail", "-c", script],
                cwd=ROOT,
                capture_output=True,
                text=True,
                env={**__import__("os").environ, "PYTHONWARNINGS": "ignore"},
            )
            elapsed = time.time() - started
            status = "PASS" if proc.returncode == 0 else "FAIL"
            results.append((name, status, elapsed))
            print(f"[{status}] {name} ({elapsed:.1f}s)", flush=True)
            if status == "FAIL":
                output = (proc.stdout + proc.stderr).strip().splitlines()
                for line in output[-args.tail:]:
                    print("    " + line)
                if args.fail_fast:
                    return 1

    failed = [r for r in results if r[1] == "FAIL"]
    passed = [r for r in results if r[1] == "PASS"]
    skipped = [r for r in results if r[1] == "SKIP"]
    print(f"\nARC LOCAL CI: {len(passed)} pass / {len(failed)} fail / {len(skipped)} skipped")
    for name, _, _ in failed:
        print("  FAIL:", name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
