"""Run lightweight foundation verifiers before Brain serves traffic.

All checks are metadata-only and subprocess-isolated. Database admission is
classified without exposing credentials. Durable DB promotion remains a
separate explicit gate. Room 01 and N104C.1 runtime verification are opt-in
and one-shot. N101/N102/N103 observations are bounded and never treated as
downstream truth. State drift is a mandatory deny gate.
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
from tools.state_reconciliation_admission import evaluate_admission

ROOT = Path(__file__).resolve().parents[1]
MEMORY_GUARD_BYTES = 320 * 1024 * 1024
COMMANDS = (("state_consistency", "tools/check_state_consistency.py"), ("state_drift", "tools/state_drift_detector.py"), ("foundation", "tools/verify_foundation.py"), ("access_path", "tools/verify_access_path.py"), ("database_admission_contract", "tools/verify_database_binding_contract.py"), ("admission_fsm", "tools/verify_admission_fsm.py"), ("deterministic_replay", "tools/replay_verifier.py"), ("gate_invariant", "tools/verify_gate_invariant.py"))


def database_binding_evidence() -> dict[str, object]:
    from tools.binding_probe import classify_database_binding
    return classify_database_binding()


def _run_json_tool(env: dict[str, str], filename: str, timeout: int, deny_status: str) -> dict[str, object]:
    proc = subprocess.run([sys.executable, str(ROOT / filename)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout)
    raw = proc.stdout.strip().splitlines()
    if raw:
        try:
            evidence = json.loads(raw[-1])
            if isinstance(evidence, dict):
                evidence["exit_code"] = proc.returncode
                return evidence
        except (ValueError, json.JSONDecodeError):
            pass
    return {"status": deny_status, "exit_code": proc.returncode, "evidence_parse": "DENY", "stderr_class": "NON_SECRET_RUNTIME_DIAGNOSTIC", "stderr_tail": proc.stderr[-1200:]}


def network_admission_evidence(env: dict[str, str]) -> dict[str, object]:
    if env.get("FORENSIC_NETWORK_PROBE") != "1":
        return {"status": "DISABLED"}
    return _run_json_tool(env, "tools/network_admission_probe.py", 30, "DENY_NETWORK_ORIGIN")


def n104c1_transport_evidence(env: dict[str, str]) -> dict[str, object]:
    if env.get("FORENSIC_N104C1_PROBE") != "1":
        return {"status": "DISABLED"}
    return _run_json_tool(env, "tools/n104c1_transport_inspection.py", 45, "DENY_N104C1_TRANSPORT")


def room01_runtime_evidence(env: dict[str, str]) -> dict[str, object]:
    if env.get("FORENSIC_ROOM01_RUNTIME_VERIFY") != "1":
        return {"status": "DISABLED"}
    return _run_json_tool(env, "tools/runtime_room01_verify.py", 45, "DENY")


def admission_summary(binding_status: str, network_status: str, round_trip_proven: bool = False) -> dict[str, object]:
    network_pass = network_status == "PASS"
    state = AdmissionState(existence=False, binding=binding_status == "BOUND_TLS", tls=binding_status == "BOUND_TLS", round_trip=round_trip_proven)
    evaluated = evaluate(state)
    return {"db_existence": "PREREQUISITE_EXTERNAL_EVIDENCE", "db_binding": binding_status, "db_tls_admission": "PASS" if binding_status == "BOUND_TLS" else "DENY", "network_origin_proof": "PASS" if network_pass else "NOT_PROVEN", "db_round_trip": "PASS" if round_trip_proven else "NOT_PROVEN", "promotion": "ALLOW" if (network_pass and evaluated["promotion"]) else "DENY", "rule": "PASS_IS_LOCAL_TO_GATE;PASS_IS_PREREQUISITE_ONLY;NO_PASS_INHERITANCE"}


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
    origin = _run_json_tool(env, "tools/origin_metadata_probe.py", 24, "DENY_ORIGIN_METADATA")
    canonical = _run_json_tool(env, "tools/canonical_identity_probe.py", 24, "DENY_CANONICAL_IDENTITY")
    independence = _run_json_tool(env, "tools/source_independence_probe.py", 24, "DENY_INDEPENDENCE")
    results.extend([
        {"name": "database_binding_probe", "exit_code": 0, "evidence": binding},
        {"name": "origin_metadata_probe", "exit_code": int(origin.get("exit_code", 0)), "evidence": origin},
        {"name": "canonical_identity_probe", "exit_code": int(canonical.get("exit_code", 0)), "evidence": canonical},
        {"name": "source_independence_probe", "exit_code": int(independence.get("exit_code", 0)), "evidence": independence},
    ])
    network = network_admission_evidence(env)
    n104c1 = n104c1_transport_evidence(env)
    results.append({"name": "network_admission_probe", "exit_code": int(network.get("exit_code", 0)), "evidence": network})
    results.append({"name": "n104c1_transport_inspection", "exit_code": int(n104c1.get("exit_code", 0)), "evidence": n104c1})
    room01 = room01_runtime_evidence(env)
    results.append({"name": "room01_runtime_verify", "exit_code": int(room01.get("exit_code", 0)), "evidence": room01})
    reconciliation = evaluate_admission(runtime_commit=os.environ.get("RENDER_GIT_COMMIT"), deployment_id=os.environ.get("RENDER_DEPLOY_ID"), quant_projection=None)
    results.append({"name": "state_reconciliation_admission", "exit_code": 0, "evidence": reconciliation})

    print(json.dumps({"runtime_boot_gate": "PASS", "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"), "memory_guard_bytes": MEMORY_GUARD_BYTES, "origin_metadata": origin, "canonical_identity": canonical, "source_independence": independence, "database_admission_chain": admission_summary(str(binding["status"]), str(network.get("status", "DISABLED")), round_trip_proven=False), "n104c1_transport": n104c1, "state_reconciliation_admission": reconciliation, "room01_runtime": room01, "external_event_path": "ISOLATED; NO_SELF_MANUFACTURED_EVENT", "foundation_path": "ADVANCE_ALLOWED; EXTERNAL_STATE_UNCHANGED", "room_02": "LOCKED", "staircase": "LOCKED", "elapsed_seconds": round(time.time() - started, 4), "results": results}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
