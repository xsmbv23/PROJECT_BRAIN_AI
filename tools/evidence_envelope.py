"""Canonical compact evidence envelope for forensic gate-local receipts."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_envelope(*, action_id: str, cycle_id: str, receipts: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "action_id": action_id,
        "cycle_id": cycle_id,
        "receipt_count": len(receipts),
        "receipts": receipts,
        "canonical_identity": "DENY_UNPROVEN",
        "payload_policy": "NO_DOWNLOAD_NO_PARSE_NO_SOURCE_HASH",
    }
    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return {
        "envelope_version": "1",
        "action_id": action_id,
        "cycle_id": cycle_id,
        "evidence_hash": digest,
        "payload": payload,
    }
