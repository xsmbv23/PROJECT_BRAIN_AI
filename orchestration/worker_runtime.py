#!/usr/bin/env python3
"""Browser-independent worker runtime for Project Brain.

V1 claims deterministic task envelopes and executes only explicitly allocated
work. LLM reasoning is provider-neutral and fail-closed until configured.
Results are append-only JSONL records in the worker's local durable sink;
persistent GitHub reconciliation is performed by the orchestration workflow.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTBOX = ROOT / "coordination" / "worker_outbox"
RESULTS = ROOT / "coordination" / "worker_results"
WORKER_ID = os.environ.get("WORKER_ID", "BOT2_QUANT")
POLL_SECONDS = int(os.environ.get("POLL_SECONDS", "60"))
RUN_ONCE = os.environ.get("RUN_ONCE", "0") == "1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def execute(task: dict) -> dict:
    # V1 deliberately proves claim/lease/result plumbing without pretending
    # that an LLM provider exists in the background runtime yet.
    return {
        "status": "BLOCKED_PROVIDER_NOT_CONFIGURED",
        "reason": "LLM reasoning provider is not configured in Worker Runtime V1",
        "proposed_next_action": "Provision an approved provider/runtime budget before autonomous reasoning",
        "forensic_gate": "NONE",
        "promotion": "DENY",
    }


def process_task(path: Path) -> None:
    task = json.loads(path.read_text(encoding="utf-8"))
    if task.get("worker_id") != WORKER_ID:
        return
    task_id = task["task_id"]
    result_path = RESULTS / task["cycle_id"] / f"{WORKER_ID}.jsonl"
    existing = result_path.read_text(encoding="utf-8") if result_path.exists() else ""
    if task_id in existing:
        return
    result = execute(task)
    record = {
        "schema": "forensic-worker-result/v1",
        "recorded_at": now(),
        "worker_id": WORKER_ID,
        "cycle_id": task["cycle_id"],
        "task_id": task_id,
        "task_sha256": digest(json.dumps(task, sort_keys=True)),
        "lease_id": task.get("lease", {}).get("lease_id"),
        "attempt": task.get("lease", {}).get("attempt", 1),
        "result": result,
        "evidence_refs": [],
    }
    append_jsonl(result_path, record)
    print(json.dumps({"event": "TASK_RESULT", **record}, sort_keys=True), flush=True)


def main() -> int:
    print(json.dumps({"event": "START", "worker_id": WORKER_ID, "run_once": RUN_ONCE}, sort_keys=True), flush=True)
    while True:
        if OUTBOX.exists():
            for path in sorted(OUTBOX.glob("*/*.json")):
                process_task(path)
        if RUN_ONCE:
            break
        time.sleep(POLL_SECONDS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
