"""Strict research-admission gate layered above structural receipt validation.

A structurally valid claimant receipt is not independent evidence. This gate
requires a separately produced evidence-resolution result bound to the exact
date manifest before returning ADMITTED.
"""
from __future__ import annotations

import re
from datetime import datetime

from tools.research_dataset_admission_validator import validate_research_dataset_receipt

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _iso_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def admit_research_dataset_receipt(
    receipt: dict[str, object],
    evidence_resolution: dict[str, object] | None,
) -> dict[str, object]:
    """Return research eligibility only after independent evidence is bound.

    Structural receipt validation is local schema checking. Admission requires
    a separately traceable resolution artifact whose manifest hash exactly
    matches the claimant receipt. Missing or malformed resolution metadata is
    UNKNOWN, never PASS.
    """
    structural = validate_research_dataset_receipt(receipt)
    if structural.get("status") not in {"ADMITTED", "SCHEMA_VALID"}:
        return structural

    if not isinstance(evidence_resolution, dict):
        return {"status": "UNKNOWN", "reason": "INDEPENDENT_EVIDENCE_NOT_RESOLVED"}
    if evidence_resolution.get("status") != "VERIFIED":
        return {"status": "UNKNOWN", "reason": "INDEPENDENT_EVIDENCE_NOT_VERIFIED"}

    required_resolution_fields = (
        "verifier_reference",
        "resolved_manifest_reference",
        "resolved_manifest_sha256",
        "observed_at",
        "verification_method",
        "verifier_code_version",
    )
    for field in required_resolution_fields:
        if not _nonempty(evidence_resolution.get(field)):
            return {"status": "UNKNOWN", "reason": f"{field.upper()}_MISSING"}

    if not _iso_timestamp(evidence_resolution.get("observed_at")):
        return {"status": "UNKNOWN", "reason": "OBSERVED_AT_INVALID"}

    resolved_hash = evidence_resolution.get("resolved_manifest_sha256")
    receipt_hash = receipt.get("date_manifest_sha256")
    if not isinstance(resolved_hash, str) or not _SHA256.fullmatch(resolved_hash):
        return {"status": "UNKNOWN", "reason": "RESOLVED_MANIFEST_HASH_INVALID"}
    if not isinstance(receipt_hash, str) or not _SHA256.fullmatch(receipt_hash):
        return {"status": "UNKNOWN", "reason": "RECEIPT_MANIFEST_HASH_INVALID"}
    if resolved_hash != receipt_hash:
        return {"status": "UNKNOWN", "reason": "RESOLVED_MANIFEST_HASH_MISMATCH"}

    return {
        "status": "ADMITTED",
        "reason": "RESEARCH_ELIGIBILITY_ONLY",
        "canonical_promotion": "NOT_PROVEN",
        "edge": "NOT_PROVEN",
        "ev_pnl": "NOT_PROVEN",
        "action": "NOT_AUTHORIZED",
    }
