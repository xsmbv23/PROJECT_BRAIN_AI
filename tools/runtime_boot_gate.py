"""Run lightweight foundation verifiers before Brain serves traffic.

All checks are metadata-only and subprocess-isolated. Database admission is
classified without exposing credentials. Durable DB promotion remains a
separate explicit gate. Room 01 runtime verification is opt-in and one-shot.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from tools.database_admission import AdmissionState, evaluate

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


def network_admission_evidence(env: dict[str, str]) -> dict[str, object]:
    if env.get("FORENSIC_NETWORK_PROBE") != "1":
        return {"status": "DISABLED"}
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/network_admission_probe.py")],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=30,
    )
    try:
        evidence = ast.literal_eval(proc.stdout.strip().splitlines()[-1])
        if not isinstance(evidence, dict):
            raise ValueError("non-dict")
    except (ValueError, SyntaxError, IndexError):
        evidence = {"status": "DENY_NETWORK_ORIGIN", "evidence_parse": "DENY"}
    evidence["exit_code"] = proc.returncode
    return evidence


def room01_runtime_evidence(env: dict[str, str]) -> dict[str, object]:
    if env.get("FORENSIC_ROOM01_RUNTIME_VERIFY") != "1":
        return {"status": "DISABLED"}
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/runtime_room01_verify.py")],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=45,
    )
    if proc.returncode != 0:
        return {"status": "DENY", "exit_code": proc.returncode, "output": proc.stdout[-2000:]}
    try:
        evidence = json.loads(proc.stdout.strip().splitlines()[-1])
        if not isinstance(evidence, dict):
            raise ValueError("non-dict")
    except (ValueError, json.JSONDecodeError, IndexError):
        return {"status": "DENY", "exit_code": proc.returncode, "evidence_parse": "DENY"}
    evidence["status"] = "PASS"
    evidence["exit_code"] = proc.returncode
    return evidence


def admission_summary(binding_status: str, network_status: str, round_trip_proven: bool = False) -> dict[str, object]:
    network_pass = network_status == "PASS"
    state = AdmissionState(existence=False, binding=binding_status == "BOUND_TLS", tls=binding_status == "BOUND_TLS", round_trip=round_trip_proven)
    evaluated = evaluate(state)
    return {
        "db_existence": "PREREQUISITE_EXTERNAL_EVIDENCE",
        "db_binding": binding_status,
        "db_tls_admission": "PASS" if binding_status == "BOUND_TLS" else "DENY",
        "network_origin_proof": "PASS" if network_pass else "NOT_PROVEN",
        "db_round_trip": "PASS" if round_trip_proven else "NOT_PROVEN",
        "promotion": "ALLOW" if (network_pass and evaluated["promotion"]) else "DENY",
        "rule": "PASS_AT_GATE_IS_PREREQUISITE_ONLY; NEVER_INFER_DEEPER_PASS",
    }


def main() -> int:
    started = time.time()
    results = []
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    for name, relpath in COMMANDS:
        proc = subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        result = {"name": name, "exit_code": proc.returncode, "stdout_tail": proc.stdout[-4000:], "stderr_tail": proc.stderr[-2000:]}
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
    network = network_admission_evidence(env)
    results.append({"name": "network_admission_probe", "exit_code": int(network.get("exit_code", 0)), "evidence": network})
    room01 = room01_runtime_evidence(env)
    results.append({"name": "room01_runtime_verify", "exit_code": int(room01.get("exit_code", 0)), "evidence": room01})

    print(json.dumps({
        "runtime_boot_gate": "PASS",
        "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "memory_guard_bytes": MEMORY_GUARD_BYTES,
        "database_admission_chain": admission_summary(str(binding["status"]), str(network.get("status", "DISABLED")), round_trip_proven=False),
        "room01_runtime": room01,
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
