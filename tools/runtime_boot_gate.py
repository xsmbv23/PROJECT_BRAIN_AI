"""Run lightweight foundation verifiers before Brain serves traffic.

Boot/liveness and forensic admission are deliberately different gates.
External source probes, durable receipt writes, and prior-receipt database reads
are explicit admission actions, never hidden boot dependencies. This keeps
remote-site latency and database availability outside the Brain boot critical
path while preserving DEFAULT_DENY for admission.
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
COMMANDS = (("state_consistency", "tools/check_state_consistency.py"), ("state_drift", "tools/state_drift_detector.py"), ("action_receipt", "tools/verify_action_receipt_runtime.py"), ("foundation", "tools/verify_foundation.py"), ("access_path", "tools/verify_access_path.py"), ("database_admission_contract", "tools/verify_database_binding_contract.py"), ("admission_fsm", "tools/verify_admission_fsm.py"), ("deterministic_replay", "tools/replay_verifier.py"), ("gate_invariant", "tools/verify_gate_invariant.py"))


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
    admission_denials: list[str] = []

    for name, relpath in COMMANDS:
        if name == "action_receipt" and env.get("FORENSIC_PRIOR_RECEIPT_VERIFY") != "1":
            results.append({"name": name, "exit_code": 0, "evidence": {"status": "DISABLED_BOOT_PATH", "reason": "PRIOR_RECEIPT_DB_READ_IS_EXPLICIT_ADMISSION_ACTION"}})
            continue
        proc = subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        result = {"name": name, "exit_code": proc.returncode, "stdout_tail": proc.stdout[-4000:], "stderr_tail": proc.stderr[-2000:]}
        results.append(result)
        if proc.returncode != 0 and name == "action_receipt":
            admission_denials.append("ACTION_RECEIPT")
            result["gate_role"] = "ADMISSION_DENY_ONLY"
            continue
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
    if env.get("FORENSIC_SOURCE_PROBES") == "1":
        origin = _run_json_tool(env, "tools/origin_metadata_probe.py", 24, "DENY_ORIGIN_METADATA")
        canonical = _run_json_tool(env, "tools/canonical_identity_probe.py", 24, "DENY_CANONICAL_IDENTITY")
        independence = _run_json_tool(env, "tools/source_independence_probe.py", 24, "DENY_INDEPENDENCE")
    else:
        origin = {"status": "DISABLED_BOOT_PATH"}
        canonical = {"status": "DISABLED_BOOT_PATH"}
        independence = {"status": "DISABLED_BOOT_PATH"}

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
    reconciliation = evaluate_admission(runtime_commit=os.environ.get("RENDER_GIT_COMMIT"), deployment_id=os.environ.get("RENDER_DEPLOY_ID") or os.environ.get("RENDER_INSTANCE_ID"), quant_projection=None)
    results.append({"name": "state_reconciliation_admission", "exit_code": 0, "evidence": reconciliation})

    receipt_issue = {"status": "DEFERRED", "reason": "DURABLE_RECEIPT_ISSUANCE_IS_EXPLICIT_ADMISSION_ACTION;NOT_BOOT_DEPENDENCY", "action_id": "N173_FRESH-PROBE-RECEIPT-AND-S1-BRIDGE", "promotes": False}
    results.append({"name": "action_receipt_issuer", "exit_code": 0, "evidence": receipt_issue, "gate_role": "POST_BOUNDARY_DEFERRED_ISSUER"})

    admission_status = "DENY" if admission_denials else "PASS"
    print(json.dumps({
        "runtime_boot_gate": "PASS",
        "admission_gate": admission_status,
        "admission_denials": admission_denials,
        "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "memory_guard_bytes": MEMORY_GUARD_BYTES,
        "origin_metadata": origin,
        "canonical_identity": canonical,
        "source_independence": independence,
        "database_admission_chain": admission_summary(str(binding["status"]), str(network.get("status", "DISABLED")), round_trip_proven=False),
        "n104c1_transport": n104c1,
        "state_reconciliation_admission": reconciliation,
        "room01_runtime": room01,
        "action_receipt_issuer": receipt_issue,
        "external_event_path": "ISOLATED; NO_SELF_MANUFACTURED_EVENT",
        "foundation_path": "ADVANCE_ALLOWED; EXTERNAL_STATE_UNCHANGED",
        "source_probe_policy": "DISABLED_ON_BOOT; EXPLICIT_N173_EXECUTION_ONLY",
        "prior_receipt_policy": "DISABLED_ON_BOOT; EXPLICIT_N173_EXECUTION_ONLY",
        "durable_receipt_policy": "DEFERRED_OFF_BOOT; EXPLICIT_N173_EXECUTION_ONLY",
        "room_02": "LOCKED",
        "staircase": "LOCKED",
        "elapsed_seconds": round(time.time() - started, 4),
        "results": results,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
