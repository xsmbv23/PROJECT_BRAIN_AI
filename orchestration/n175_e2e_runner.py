#!/usr/bin/env python3
"""Direct E2E execution verifier for N175.

Runs the three canonical worker programs in parallel on an independent execution
plane. This is a runtime test, not a promotion mechanism. A worker must emit a
fresh structured receipt bound to the current N175 allocation/cycle.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone

WORKERS = {
    "BOT2_QUANT": "orchestration/bot2_worker_v2.py",
    "BOT3_REALITY": "orchestration/bot3_worker.py",
    "BOT4_EXECUTION": "orchestration/bot4_worker_v2.py",
}
PORTS = {"BOT2_QUANT": "18002", "BOT3_REALITY": "18003", "BOT4_EXECUTION": "18004"}
EXPECTED_ALLOCATION = "ALLOC-N175-TRIPLE-WORKER-REACTIVATION-001"
EXPECTED_CYCLE = "BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER"


def run_worker(worker: str, script: str, out: dict) -> None:
    env = os.environ.copy()
    env.update({
        "COORDINATION_REPO": "xsmbv23/Project_Brain_AI",
        "COORDINATION_BRANCH": "main",
        "POLL_SECONDS": "1",
        "PORT": PORTS[worker],
    })
    started = datetime.now(timezone.utc).isoformat()
    proc = subprocess.Popen(
        [sys.executable, script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    receipt = None
    lines = []
    deadline = time.monotonic() + 30
    try:
        while time.monotonic() < deadline:
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                time.sleep(0.05)
                continue
            line = line.strip()
            if line:
                lines.append(line)
                try:
                    candidate = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(candidate, dict) and candidate.get("schema", "").startswith("headless-worker-result/"):
                    receipt = candidate
                    break
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)

    out[worker] = {
        "started_at": started,
        "script": script,
        "receipt": receipt,
        "stdout_tail": lines[-5:],
    }


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    results: dict = {}
    threads = [threading.Thread(target=run_worker, args=(w, s, results), daemon=True) for w, s in WORKERS.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=40)

    checks = {}
    for worker in WORKERS:
        r = results.get(worker, {})
        receipt = r.get("receipt") or {}
        checks[worker] = {
            "process_executed": bool(r.get("started_at")),
            "receipt_observed": bool(receipt),
            "allocation_bound": receipt.get("allocation_id") == EXPECTED_ALLOCATION,
            "cycle_bound": receipt.get("cycle_id") == EXPECTED_CYCLE,
            "worker_identity": receipt.get("worker") == worker,
            "local_result_pass": receipt.get("result") == "PASS",
            "promotion_denied": receipt.get("promotion") == "DENY",
        }

    all_execution_checks = all(all(v.values()) for v in checks.values())
    final = {
        "schema": "n175-e2e-execution-verification/v1",
        "result_type": "E2E_EXECUTION_VERIFICATION",
        "allocation_id": EXPECTED_ALLOCATION,
        "cycle_id": EXPECTED_CYCLE,
        "started_at": started,
        "workers": results,
        "checks": checks,
        "result": "PASS" if all_execution_checks else "HOLD",
        "promotion": "DENY",
        "note": "PASS proves direct execution of the canonical worker programs on the fallback execution plane; it does not promote S1 data admission.",
    }
    print(json.dumps(final, indent=2, sort_keys=True))
    return 0 if all_execution_checks else 2


if __name__ == "__main__":
    raise SystemExit(main())
