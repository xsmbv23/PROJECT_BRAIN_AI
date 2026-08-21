#!/usr/bin/env python3
"""Claim, execute and reconcile worker tasks without mutating canonical state."""
from __future__ import annotations

import hashlib
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path

from llm_provider import invoke

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "current_state.json"
NEXT = ROOT / "state" / "next_action.json"
OUTBOX = ROOT / "coordination" / "worker_outbox"
RESULTS = ROOT / "coordination" / "worker_results"
RECON = ROOT / "coordination" / "reconciliation"
WORKERS = tuple(x.strip() for x in os.environ.get("WORKERS", "BOT2_QUANT,BOT4_EXECUTION").split(",") if x.strip())


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def unwrap(value):
    if isinstance(value, dict) and isinstance(value.get("content"), str):
        try:
            return json.loads(value["content"])
        except json.JSONDecodeError:
            pass
    return value


def load(path: Path):
    return unwrap(json.loads(path.read_text(encoding="utf-8")))


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def latest_result(path: Path, task_id: str):
    if not path.exists():
        return None
    found = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("task_id") == task_id:
            found = record
    return found


def prompt_for(task: dict) -> str:
    return json.dumps({
        "worker_id": task.get("worker_id"),
        "role": task.get("role"),
        "objective": task.get("objective"),
        "constraints": task.get("constraints", []),
        "required_outputs": task.get("required_outputs", []),
        "authority": "execution-only; no canonical state mutation; no forensic promotion",
    }, sort_keys=True)


def execute(task: dict) -> dict:
    """Run the guarded provider adapter; never grant forensic authority."""
    result = invoke(prompt_for(task))
    if result.get("status") == "LLM_COMPLETED":
        result["reasoning_classification"] = "ADVISORY_ONLY"
        result["evidence_refs"] = []
        result["forensic_gate"] = "NONE"
        result["promotion"] = "DENY"
    return result


def process(task_path: Path, current_cycle: str) -> dict | None:
    task = json.loads(task_path.read_text(encoding="utf-8"))
    worker = task.get("worker_id")
    if worker not in WORKERS:
        return None
    cycle = task.get("cycle_id")
    task_id = task.get("task_id")
    result_path = RESULTS / str(cycle) / f"{worker}.jsonl"

    if cycle != current_cycle:
        return {"status": "STALE_REJECTED", "worker_id": worker, "cycle_id": cycle, "task_id": task_id, "reason": "task cycle differs from exact current canonical cycle", "canonical_mutation": "FORBIDDEN"}

    prior = latest_result(result_path, task_id)
    if prior is not None:
        return {"status": "DUPLICATE_IGNORED", "worker_id": worker, "cycle_id": cycle, "task_id": task_id, "lease_id": prior.get("lease_id"), "reason": "task already has an immutable result receipt"}

    lease = task.get("lease", {})
    lease_id = lease.get("lease_id") or f"LEASE-{digest(task)[:20]}"
    attempt = int(lease.get("attempt", 1))
    claim = {
        "schema": "forensic-worker-claim/v2",
        "recorded_at": now(),
        "worker_id": worker,
        "cycle_id": cycle,
        "task_id": task_id,
        "lease_id": lease_id,
        "attempt": attempt,
        "state": "CLAIMED",
        "runner": socket.gethostname(),
        "task_sha256": digest(task),
    }
    append_jsonl(RESULTS / str(cycle) / f"{worker}.claims.jsonl", claim)

    result = execute(task)
    record = {
        "schema": "forensic-worker-result/v4",
        "recorded_at": now(),
        "worker_id": worker,
        "cycle_id": cycle,
        "task_id": task_id,
        "task_sha256": digest(task),
        "lease_id": lease_id,
        "attempt": attempt,
        "result": result,
        "evidence_refs": result.get("evidence_refs", []),
        "canonical_mutation": "FORBIDDEN",
        "forensic_gate": "NONE",
        "promotion": "DENY",
    }
    append_jsonl(result_path, record)
    return record


def reconcile(cycle: str, results: list[dict]) -> dict:
    active = [r for r in results if r.get("status") not in {"STALE_REJECTED", "DUPLICATE_IGNORED"}]
    statuses = [r.get("result", {}).get("status") for r in active]
    if any(r.get("status") == "STALE_REJECTED" for r in results):
        decision, reason = "HOLD", "stale task/result detected; no stale evidence may influence current cycle"
    elif not active or any(s is None for s in statuses):
        decision, reason = "UNREACHED", "required worker result missing"
    elif any(s in {"FAIL", "CONFLICT"} for s in statuses):
        decision, reason = "HOLD", "blocking worker disagreement/failure preserved"
    elif any(s == "BLOCKED_PROVIDER_NOT_CONFIGURED" for s in statuses):
        decision, reason = "HOLD", "background reasoning provider unavailable"
    else:
        decision, reason = "REVIEW_REQUIRED", "results exist but BOT1 must perform forensic synthesis"
    return {"schema": "forensic-worker-reconciliation/v2", "recorded_at": now(), "cycle_id": cycle, "worker_results": results, "decision": decision, "reason": reason, "minority_preserved": True, "canonical_next_action_mutation": "FORBIDDEN", "promotion": "DENY"}


def main() -> int:
    current_state = load(STATE)
    current_next = load(NEXT)
    current_cycle = current_next.get("action_id", "UNKNOWN-CYCLE")
    matrix_path = ROOT / "coordination" / "next_action_matrix_v1.json"
    if matrix_path.exists():
        current_cycle = load(matrix_path).get("cycle_id", current_cycle)

    produced = []
    if OUTBOX.exists():
        for cycle_dir in sorted(OUTBOX.iterdir()):
            if not cycle_dir.is_dir():
                continue
            for worker in WORKERS:
                path = cycle_dir / f"{worker}.json"
                if path.exists():
                    result = process(path, current_cycle)
                    if result is not None:
                        produced.append(result)

    ledger = reconcile(current_cycle, produced)
    ledger["canonical_state_digest"] = digest(current_state)
    ledger["canonical_next_action_digest"] = digest(current_next)
    append_jsonl(RECON / f"{current_cycle}.jsonl", ledger)
    print(json.dumps({"event": "RECONCILIATION", **ledger}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
