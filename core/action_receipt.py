"""Forensic ACTION_RECEIPT admission.

A receipt proves only that one exact runtime action occurred. It does not prove
source truth, canonical quorum, Edge, EV/P&L, or global promotion.

The issuer is deliberately separate from the verifier. The verifier never
manufactures a receipt. Replay is rejected by requiring an exact execution
nonce supplied by the execution boundary and an exact commit/deployment/action
identity.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Mapping

REQUIRED_FIELDS = (
    "receipt_version",
    "action_id",
    "commit_sha",
    "deployment_id",
    "execution_nonce",
    "issued_at",
    "evidence_sha",
)


def canonical_receipt_payload(receipt: Mapping[str, object]) -> bytes:
    import json
    payload = {key: receipt[key] for key in REQUIRED_FIELDS}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def receipt_sha(receipt: Mapping[str, object]) -> str:
    return sha256(canonical_receipt_payload(receipt)).hexdigest()


def verify_action_receipt(
    receipt: Mapping[str, object] | None,
    *,
    action_id: str,
    commit_sha: str,
    deployment_id: str,
    evidence_sha: str,
    execution_nonce: str,
    now: datetime | None = None,
    max_age_seconds: int = 900,
) -> dict[str, object]:
    if not receipt:
        return {"status": "DENY", "reason": "ACTION_RECEIPT_MISSING", "pass_is_local": True, "promotes": False}

    missing = [key for key in REQUIRED_FIELDS if key not in receipt]
    if missing:
        return {"status": "DENY", "reason": "ACTION_RECEIPT_MALFORMED", "missing": missing, "pass_is_local": True, "promotes": False}

    expected = {
        "action_id": action_id,
        "commit_sha": commit_sha,
        "deployment_id": deployment_id,
        "evidence_sha": evidence_sha,
        "execution_nonce": execution_nonce,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            return {"status": "DENY", "reason": f"ACTION_RECEIPT_{key.upper()}_MISMATCH", "pass_is_local": True, "promotes": False}

    try:
        issued = datetime.fromisoformat(str(receipt["issued_at"]).replace("Z", "+00:00"))
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return {"status": "DENY", "reason": "ACTION_RECEIPT_BAD_TIMESTAMP", "pass_is_local": True, "promotes": False}

    current = now or datetime.now(timezone.utc)
    age = (current - issued).total_seconds()
    if age < 0 or age > max_age_seconds:
        return {"status": "DENY", "reason": "ACTION_RECEIPT_STALE_OR_FUTURE", "age_seconds": age, "pass_is_local": True, "promotes": False}

    return {
        "status": "PASS_LOCAL",
        "reason": "EXACT_CURRENT_ACTION_RECEIPT",
        "receipt_sha": receipt_sha(receipt),
        "pass_is_local": True,
        "promotes": False,
    }
