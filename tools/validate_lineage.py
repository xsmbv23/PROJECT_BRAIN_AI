"""Validate prediction lineage without touching source truth.

This is intentionally tiny and deterministic. It validates the presence and
shape of an already-produced evidence envelope; it never invents hashes.
"""
from __future__ import annotations

import hashlib
from typing import Mapping

REQUIRED = ("prediction_id", "feature_snapshot_sha", "canonical_sha", "raw_receipt_sha")
SHA256_HEX_LEN = 64


def validate_lineage(record: Mapping[str, object]) -> dict[str, object]:
    missing = [key for key in REQUIRED if not record.get(key)]
    malformed = []
    for key in REQUIRED[1:]:
        value = record.get(key)
        if value is not None and (not isinstance(value, str) or len(value) != SHA256_HEX_LEN):
            malformed.append(key)

    if missing or malformed:
        return {
            "status": "NOT_PROVEN",
            "execution": "CANCEL",
            "missing": missing,
            "malformed": malformed,
        }

    return {
        "status": "PROVEN_LINEAGE",
        "execution": "ELIGIBLE_FOR_NEXT_GATE",
        "missing": [],
        "malformed": [],
    }


def sha256_bytes(payload: bytes) -> str:
    """Canonical helper: hashes bytes only; never normalizes or mutates payload."""
    return hashlib.sha256(payload).hexdigest()
