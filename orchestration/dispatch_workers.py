#!/usr/bin/env python3
"""Deterministic worker dispatcher for Project_Brain_AI.

This process does not perform forensic promotion and does not run LLM reasoning.
It converts the canonical next_action + department allocation policy into
append-only worker task envelopes. A real background worker can consume these
envelopes without a ChatGPT browser session.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "current_state.json"
NEXT = ROOT / "state" / "next_action.json"
MATRIX = ROOT / "coordination" / "next_action_matrix_v1.json"
OUTBOX = ROOT / "coordination" / "worker_outbox"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stable_id(*parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def main() -> int:
    state = read_json(STATE)
    nxt = read_json(NEXT)
    matrix = read_json(MATRIX)

    cycle_id = matrix["cycle_id"]
    phase = matrix["phase"]
    now = datetime.now(timezone.utc).isoformat()

    # Only department scopes declared by BOT1 may be dispatched.
    departments = matrix["departments"]
    for worker_id, allocation in departments.items():
        action = allocation["next_action"]
        task_id = f"TASK-{cycle_id}-{worker_id}-{stable_id(cycle_id, worker_id, action)}"
        task_dir = OUTBOX / cycle_id
        task_dir.mkdir(parents=True, exist_ok=True)
        task_path = task_dir / f"{worker_id}.json"

        if task_path.exists():
            continue

        envelope = {
            "schema": "forensic-worker-task/v1",
            "created_at": now,
            "cycle_id": cycle_id,
            "task_id": task_id,
            "worker_id": worker_id,
            "role": worker_id,
            "phase": phase,
            "canonical_state": state["state"],
            "canonical_next_action": nxt["action_id"],
            "task": action,
            "lease": {
                "lease_id": f"LEASE-{stable_id(task_id, now)}",
                "state": "PENDING",
                "attempt": 1,
                "exclusive_write_scope": [f"coordination/inbox/{worker_id}.jsonl"]
            },
            "authority": {
                "forensic_gate": "NONE",
                "promotion": "DENY",
                "state_mutation": "BRANCH_LOCAL"
            },
            "input_refs": [
                "state/current_state.json",
                "state/next_action.json",
                "coordination/next_action_matrix_v1.json"
            ],
            "completion": {
                "result": "UNKNOWN",
                "evidence_refs": [],
                "next_action": "Return a persistent result before any new allocation."
            }
        }
        task_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        print(f"created {task_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
