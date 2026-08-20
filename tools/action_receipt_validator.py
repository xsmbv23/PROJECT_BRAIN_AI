"""Validate that durable action receipts actually support repository state.

This module is intentionally non-authoritative: it NEVER advances the FSM,
rewrites state, creates a receipt, or treats chat intent as evidence.
It only validates evidence already emitted by runtime/processes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _canonical(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def expected_receipt_sha(receipt: dict[str, Any]) -> str:
    body = dict(receipt)
    body.pop("receipt_sha256", None)
    return hashlib.sha256(_canonical(body)).hexdigest()


def _expected_execution_nonce(receipt: dict[str, Any]) -> str | None:
    action_id = receipt.get("action_id")
    commit_sha = receipt.get("commit_sha")
    deployment_id = receipt.get("deployment_id")
    issued_at = receipt.get("issued_at")
    if not all((action_id, commit_sha, deployment_id, issued_at)):
        return None
    seed = f"{action_id}|{commit_sha}|{deployment_id}|{issued_at}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def validate_action_receipt(receipt: dict[str, Any], state: dict[str, Any], runtime: dict[str, Any]) -> dict[str, Any]:
    # Canonical state schema uses *_id. Legacy aliases are deliberately rejected
    # here so a stale schema cannot silently satisfy a production evidence gate.
    action_id = state.get("last_action_id")
    next_action = state.get("next_action_id")
    if not action_id or not next_action:
        return {"status": "DENY", "reason": "STATE_POINTER_MISSING"}

    if receipt.get("action_id") != action_id:
        return {"status": "DENY", "reason": "RECEIPT_ACTION_MISMATCH"}

    supplied_sha = receipt.get("receipt_sha256")
    if not supplied_sha or supplied_sha != expected_receipt_sha(receipt):
        return {"status": "DENY", "reason": "RECEIPT_SHA_MISMATCH"}

    runtime_commit = runtime.get("commit_sha")
    receipt_commit = receipt.get("commit_sha")
    if not runtime_commit or not receipt_commit or runtime_commit != receipt_commit:
        return {"status": "DENY", "reason": "RUNTIME_COMMIT_MISMATCH"}

    issued_at = receipt.get("issued_at")
    if not issued_at:
        return {"status": "DENY", "reason": "RECEIPT_ISSUED_AT_MISSING"}
    try:
        datetime.fromisoformat(str(issued_at).replace("Z", "+00:00"))
    except ValueError:
        return {"status": "DENY", "reason": "RECEIPT_ISSUED_AT_INVALID"}

    execution_nonce = receipt.get("execution_nonce")
    expected_nonce = _expected_execution_nonce(receipt)
    if not execution_nonce or not expected_nonce or execution_nonce != expected_nonce:
        return {"status": "DENY", "reason": "RECEIPT_NONCE_MISMATCH"}

    if receipt.get("status") not in {"PASS", "DENY", "HOLD"}:
        return {"status": "DENY", "reason": "RECEIPT_STATUS_INVALID"}

    return {
        "status": "PASS",
        "reason": "ACTION_RECEIPT_SUPPORTS_STATE",
        "action_id": action_id,
        "next_action": next_action,
        "commit_sha": runtime_commit,
    }


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
