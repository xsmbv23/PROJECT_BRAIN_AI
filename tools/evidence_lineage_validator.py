"""Validate evidence lineage against EVIDENCE_LINEAGE_ADMISSION_V1.

Non-authoritative by design: this validator never creates evidence, advances
state, promotes data, or treats chat assertions as evidence. It only evaluates
an already-emitted evidence object for provenance completeness and forbidden
masquerading shortcuts.
"""
from __future__ import annotations

from typing import Any


REQUIRED_PROVENANCE = {"source_identity", "observation_timestamp", "observation_origin"}
FOR_DERIVED = {"upstream_evidence_ids", "derivation_contract"}
FOR_RUNTIME = {"runtime_identity", "gate_evidence_id"}
FOR_CANONICAL = {"canonical_payload_sha256"}


def _canonical_or_legacy(evidence: dict[str, Any], canonical: str, legacy: str) -> tuple[str | None, bool, bool]:
    """Return value, whether a legacy alias is present, and whether it is fixture-authorized."""
    if evidence.get(canonical):
        return evidence[canonical], False, False
    if evidence.get(legacy):
        return evidence[legacy], True, evidence.get("legacy_fixture") is True
    return None, False, False


def validate_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(k for k in REQUIRED_PROVENANCE if not evidence.get(k))
    if missing:
        return {"status": "DENY", "reason": "REQUIRED_PROVENANCE_MISSING", "missing": missing}

    if evidence.get("authority") == "source_truth" and evidence.get("derived", False):
        return {"status": "DENY", "reason": "DERIVED_CANNOT_BE_SOURCE_TRUTH"}

    if evidence.get("observation_origin") == "local_receipt" and evidence.get("independent_external", False):
        return {"status": "DENY", "reason": "LOCAL_RECEIPT_CANNOT_BE_INDEPENDENT_EXTERNAL_OBSERVATION"}

    raw_sha, raw_legacy, raw_legacy_authorized = _canonical_or_legacy(evidence, "raw_artifact_sha256", "raw_sha256")
    semantic_fp, semantic_legacy, semantic_legacy_authorized = _canonical_or_legacy(evidence, "semantic_fingerprint", "semantic_sha256")

    # Legacy aliases are an explicit migration boundary. Detect a legacy alias
    # misuse before canonical-field completeness checks so the forensic failure
    # identifies the actual forbidden shortcut.
    if raw_legacy and not raw_legacy_authorized:
        return {"status": "DENY", "reason": "LEGACY_ALIAS_REQUIRES_EXPLICIT_FIXTURE", "field": "raw_sha256"}
    if semantic_legacy and not semantic_legacy_authorized:
        return {"status": "DENY", "reason": "LEGACY_ALIAS_REQUIRES_EXPLICIT_FIXTURE", "field": "semantic_sha256"}

    if evidence.get("raw_artifact_exists", False) and not raw_sha:
        return {"status": "DENY", "reason": "RAW_ARTIFACT_SHA256_MISSING"}

    if evidence.get("semantic_quorum", False) and not semantic_fp:
        return {"status": "DENY", "reason": "SEMANTIC_FINGERPRINT_MISSING"}

    if raw_sha and semantic_fp and raw_sha == semantic_fp and evidence.get("hashes_explicitly_distinct") is not True:
        return {"status": "DENY", "reason": "RAW_AND_SEMANTIC_HASH_CONFLATED"}

    if semantic_fp and evidence.get("semantic_truth_asserted", False) and not evidence.get("validated_canonical_domain", False):
        return {"status": "DENY", "reason": "SEMANTIC_HASH_REQUIRES_VALIDATED_DOMAIN"}

    if evidence.get("derived", False):
        missing_derived = sorted(k for k in FOR_DERIVED if not evidence.get(k))
        if missing_derived:
            return {"status": "DENY", "reason": "DERIVED_PROVENANCE_MISSING", "missing": missing_derived}

    if evidence.get("runtime_admission", False):
        missing_runtime = sorted(k for k in FOR_RUNTIME if not evidence.get(k))
        if missing_runtime:
            return {"status": "DENY", "reason": "RUNTIME_ADMISSION_PROVENANCE_MISSING", "missing": missing_runtime}

    if evidence.get("promoted_canonical", False):
        missing_canonical = sorted(k for k in FOR_CANONICAL if not evidence.get(k))
        if missing_canonical:
            return {"status": "DENY", "reason": "CANONICAL_PROVENANCE_MISSING", "missing": missing_canonical}

    return {"status": "PASS", "reason": "EVIDENCE_LINEAGE_COMPLETE_FOR_DECLARED_SCOPE"}
