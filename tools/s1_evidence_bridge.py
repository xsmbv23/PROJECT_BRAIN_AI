"""S1 canonical evidence -> durable forensic receipt bridge.

This bridge persists only evidence that has already passed the independent
S1 verifier. It never promotes S1 and never discovers a "latest" artifact.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.action_receipt_store import issue_action_receipt
from tools.durable_postgres import EvidenceReceipt, record_envelope, verify_receipt


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def admit_s1_evidence(*, cycle_id: str, action_id: str, commit_sha: str, deployment_id: str,
                      canonical_path: str | Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if not all((cycle_id, action_id, commit_sha, deployment_id)):
        raise ValueError("S1_IDENTITY_INCOMPLETE")

    canonical = Path(canonical_path).resolve()
    if not canonical.is_file():
        raise ValueError("S1_CANONICAL_ARTIFACT_MISSING")

    declared_sha = str(manifest.get("frozen_canonical_sha256", "")).lower()
    computed_sha = _sha256_file(canonical)
    if not declared_sha or declared_sha != computed_sha:
        raise ValueError("S1_CANONICAL_HASH_MISMATCH")
    if manifest.get("canonical_artifact_path") and Path(str(manifest["canonical_artifact_path"])).name != canonical.name:
        raise ValueError("S1_CANONICAL_PATH_MISMATCH")
    if manifest.get("cycle_id") != cycle_id:
        raise ValueError("S1_CYCLE_MISMATCH")
    if manifest.get("synthetic_data") is not False:
        raise ValueError("S1_SYNTHETIC_DATA_FORBIDDEN")
    if manifest.get("source_provenance") != "REAL_AND_TRACEABLE":
        raise ValueError("S1_PROVENANCE_INVALID")
    if int(manifest.get("unresolved_conflicts", -1)) != 0:
        raise ValueError("S1_UNRESOLVED_CONFLICTS")

    envelope = {
        "schema": "s1-evidence-envelope/v1",
        "cycle_id": cycle_id,
        "action_id": action_id,
        "commit_sha": commit_sha,
        "deployment_id": deployment_id,
        "canonical_sha256": computed_sha,
        "canonical_size_bytes": canonical.stat().st_size,
        "manifest": manifest,
    }
    evidence_receipt: EvidenceReceipt = record_envelope(envelope)
    if not verify_receipt(evidence_receipt):
        raise RuntimeError("S1_DURABLE_ROUND_TRIP_FAILED")

    action_receipt = issue_action_receipt(
        action_id=action_id,
        commit_sha=commit_sha,
        deployment_id=deployment_id,
        evidence_sha=evidence_receipt.envelope_sha,
    )
    return {
        "status": "EVIDENCE_PERSISTED",
        "s1_admission": "DENY_UNTIL_INDEPENDENT_VERIFIER_PASS",
        "cycle_id": cycle_id,
        "action_id": action_id,
        "canonical_sha256": computed_sha,
        "evidence_sha": evidence_receipt.envelope_sha,
        "receipt_sha256": action_receipt["receipt_sha256"],
    }
