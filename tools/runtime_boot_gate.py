"""Run lightweight foundation verifiers before Brain serves traffic.

All checks are metadata-only and subprocess-isolated. Database admission is
classified without exposing credentials. Durable DB promotion remains a
separate explicit gate. The external-event path is never manufactured here.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY_GUARD_BYTES = 320 * 1024 * 1024
COMMANDS = (
    ("state_consistency", "tools/check_state_consistency.py"),
    ("foundation", "tools/verify_foundation.py"),
    ("access_path", "tools/verify_access_path.py"),
    ("database_admission_contract", "tools/verify_database_binding_contract.py"),
    ("admission_fsm", "tools/verify_admission_fsm.py"),
    ("deterministic_replay", "tools/replay_verifier.py"),
)


def database_binding_evidence() -> dict[str, object]:
    from tools.binding_probe import classify_database_binding
    return classify_database_binding()


def main() -> int:
    started = time.time()
    results = []
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    for name, relpath in COMMANDS:
        cmd = [sys.executable, str(ROOT / relpath)]
        proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        result = {
            "name": name,
            "exit_code": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-2000:],
        }
        results.append(result)
        if proc.returncode != 0:
            print(json.dumps({"runtime_boot_gate": "DENY", "failed": name, "results": results}, ensure_ascii=False), flush=True)
            return 1

        if name == "foundation":
            try:
                report = ast.literal_eval(proc.stdout.strip().splitlines()[-1])
                peak = int(report["tracemalloc_peak_bytes"])
            except (ValueError, SyntaxError, KeyError, IndexError, TypeError):
                print(json.dumps({"runtime_boot_gate": "DENY", "failed": "foundation_memory_evidence_missing", "results": results}, ensure_ascii=False), flush=True)
                return 1
            result["tracemalloc_peak_bytes"] = peak
            result["memory_guard_bytes"] = MEMORY_GUARD_BYTES
            if peak >= MEMORY_GUARD_BYTES:
                print(json.dumps({"runtime_boot_gate": "DENY", "failed": "FOUNDATION_MEMORY_GUARD", "results": results}, ensure_ascii=False), flush=True)
                return 1

    binding = database_binding_evidence()
    results.append({"name": "database_binding_probe", "exit_code": 0, "evidence": binding})
    promotion = "ALLOW" if binding["status"] == "BOUND_TLS" else "DENY"
    print(json.dumps({
        "runtime_boot_gate": "PASS",
        "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "memory_guard_bytes": MEMORY_GUARD_BYTES,
        "database_admission_chain": {
            "db_existence": "PREREQUISITE_EXTERNAL_EVIDENCE",
            "db_binding": binding["status"],
            "db_tls_admission": "PASS" if binding["status"] == "BOUND_TLS" else "DENY",
            "db_round_trip": "NOT_PROVEN",
            "promotion": promotion if binding["status"] == "BOUND_TLS" else "DENY",
            "rule": "PASS_AT_GATE_IS_PREREQUISITE_ONLY; NEVER_INFER_DEEPER_PASS",
        },
        "external_event_path": "ISOLATED; NO_SELF_MANUFACTURED_EVENT",
        "foundation_path": "ADVANCE_ALLOWED; EXTERNAL_STATE_UNCHANGED",
        "room_02": "LOCKED",
        "staircase": "LOCKED",
        "elapsed_seconds": round(time.time() - started, 4),
        "results": results,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
