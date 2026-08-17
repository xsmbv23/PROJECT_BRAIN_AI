"""Run the lightweight foundation verifiers before Brain serves traffic.

This is deliberately metadata-only and subprocess-isolated. A failing or
unobservable verifier prevents the Brain HTTP process from becoming live.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = (
    ("state_consistency", "tools/check_state_consistency.py"),
    ("foundation", "tools/verify_foundation.py"),
    ("access_path", "tools/verify_access_path.py"),
)


def main() -> int:
    started = time.time()
    results = []
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    for name, relpath in COMMANDS:
        cmd = [sys.executable, str(ROOT / relpath)]
        proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        results.append({
            "name": name,
            "exit_code": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-2000:],
        })
        if proc.returncode != 0:
            print(json.dumps({"runtime_boot_gate": "DENY", "failed": name, "results": results}, ensure_ascii=False), flush=True)
            return 1

    print(json.dumps({
        "runtime_boot_gate": "PASS",
        "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "elapsed_seconds": round(time.time() - started, 4),
        "results": results,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
