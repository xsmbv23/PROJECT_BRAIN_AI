#!/usr/bin/env python3
"""Claim/lease/reconcile worker tasks in a single GitHub Actions transaction.

This is deliberately provider-neutral. It proves background task lifecycle and
keeps canonical state writes under BOT1 governance. Workers may only emit
results; promotion and canonical next_action remain outside this module.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTBOX = ROOT / "coordination" / "worker_outbox"
RESULTS = ROOT / "coordination" / "worker_results"
WORKERS = tuple(os.environ.get("WORKERS", "BOT2_QUANT,BOT4_EXECUTION").split(","))
MAX_ATTEMPTS = int(os.environ.get("MAX_ATTEMPTS", "3"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def existing_task(path: Path) -> bool:
    if not path.exists():
        return False
    return any(line.strip() for line in path.read_text(encoding="utf-8").splitlines())


def execute(task: dict) -> dict:
    # Until an approved provider is configured, execution is intentionally
    # fail-closed. This result proves the orchestration path without inventing
    # an LLM conclusion.
    return {
        "status": "BLOCKED_PROVIDER_NOT_CONFIGURED",
        "reason": "LLM provider is not configured for background autonomous reasoning",
        "proposed_next_action": "Configure approved provider adapter and budget policy",
        "forensic_gate": "NONE",
        "promotion": "DENY",
    }


def process(path: Path) -> None:
    task = json.loads(path.read_text(encoding="utf-8"))
    worker = task.get("worker_id")
    if worker not in WORKERS:
        return
    cycle = task["cycle_id"]
    task_id = task["task_id"]
    result_path = RESULTS / cycle / f"{worker}.jsonl"
    if result_path.exists() and task_id in result_path.read_text(encoding="utf-8"):
        return

    # Lease is branch-local and immutable once claimed. A new attempt gets a
    # new lease id; it never rewrites an earlier result.
    lease = task.get("lease", {})
    attempt = int(lease.get("attempt", 1))
    lease_id = lease.get("lease_id") or f"LEASE-{sha(task)[:20]}"
    claim = {
        "schema": "forensic-worker-claim/v1",
        "recorded_at": now(),
        "worker_id": worker,
        "cycle_id": cycle,
        "task_id": task_id,
        "lease_id": lease_id,
        "attempt": attempt,
        "state": "CLAIMED",
        "runner": socket.gethostname(),
    }
    claim_path = RESULTS / cycle / f"{worker}.claims.jsonl"
    append_jsonl(claim_path, claim)

    result = execute(task)
    record = {
        "schema": "forensic-worker-result/v2",
        "recorded_at": now(),
        "worker_id": worker,
        "cycle_id": cycle,
        "task_id": task_id,
        "task_sha256": sha(task),
        "lease_id": lease_id,
        "attempt": attempt,
        "result": result,
        "evidence_refs": [],
        "canonical_mutation": "FORBIDDEN",
    }
    append_jsonl(result_path, record)
    print(json.dumps({"event": "TASK_RECONCILED", **record}, sort_keys=True))


def main() -> int:
    if not OUTBOX.exists():
        print("No worker outbox; nothing to process.")
        return 0
    for cycle_dir in sorted(OUTBOX.iterdir()):
        if not cycle_dir.is_dir():
            continue
        for worker in WORKERS:
            path = cycle_dir / f"{worker}.json"
            if path.exists():
                process(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
