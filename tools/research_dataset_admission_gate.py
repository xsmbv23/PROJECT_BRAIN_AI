"""Strict research-admission gate layered above structural receipt validation.

A structurally valid claimant receipt is not independent evidence. This gate
requires a separately produced evidence-resolution result bound to the date
manifest hash before returning ADMITTED.
"""
from __future__ import annotations

from tools.research_dataset_admission_validator import validate_research_dataset_receipt


def admit_research_dataset_receipt(
    receipt: dict[str, object],
    evidence_resolution: dict[str, object] | None,
) -> dict[str, object]:
    structural = validate_research_dataset_receipt(receipt)
    if structural.get("status") != "ADMITTED":
        # The existing validator performs structural/internal checks. Even when
        # it reports ADMITTED, this function treats that as schema validation
        # only and still requires independent evidence resolution.
        if structural.get("status") not in {"ADMITTED", "SCHEMA_VALID"}:
            return structural

    if not isinstance(evidence_resolution, dict):
        return {"status": "UNKNOWN", "reason": "INDEPENDENT_EVIDENCE_NOT_RESOLVED"}
    if evidence_resolution.get("status") != "VERIFIED":
        return {"status": "UNKNOWN", "reason": "INDEPENDENT_EVIDENCE_NOT_VERIFIED"}

    verifier_reference = evidence_resolution.get("verifier_reference")
    resolved_hash = evidence_resolution.get("resolved_manifest_sha256")
    receipt_hash = receipt.get("date_manifest_sha256")

    if not isinstance(verifier_reference, str) or not verifier_reference.strip():
        return {"status": "UNKNOWN", "reason": "VERIFIER_REFERENCE_MISSING"}
    if not isinstance(receipt_hash, str) or resolved_hash != receipt_hash:
        return {"status": "UNKNOWN", "reason": "RESOLVED_MANIFEST_HASH_MISMATCH"}

    return {
        "status": "ADMITTED",
        "reason": "RESEARCH_ELIGIBILITY_ONLY",
        "canonical_promotion": "NOT_PROVEN",
        "edge": "NOT_PROVEN",
        "ev_pnl": "NOT_PROVEN",
        "action": "NOT_AUTHORIZED",
    }
