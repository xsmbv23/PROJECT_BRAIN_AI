"""S1 evidence -> durable receipt bridge.

This is the only bridge allowed to turn an already-built S1 canonical artifact
into durable forensic evidence and an action receipt. It never promotes S1.
Every identity is explicit; there is no "latest evidence" fallback.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.action_receipt_store import issue_action_receipt
from tools.durable_postgres import EvidenceReceipt, record_envelope, verify_receipt


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def admit_s1_evidence(*, cycle_id: str, action_id: str, commit_sha: str, deployment_id: str,
                      canonical_path: str | Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if not all((cycle_id, action_id, commit_sha, deployment_id)):
        raise ValueError("S1_IDENTITY_INCOMPLETE")
    canonical = Path(canonical_path).read_bytes()
    canonical_sha = _sha256(canonical)
    declared_sha = manifest.get("canonical_sha256")
    if declared_sha != canonical_sha:
        raise ValueError("S1_CANONICAL_HASH_MISMATCH")
    if manifest.get("cycle_id") != cycle_id:
        raise ValueError("S1_CYCLE_MISMATCH")

    envelope = {
        "schema": "s1-evidence-envelope/v1",
        "cycle_id": cycle_id,
        "action_id": action_id,
        "commit_sha": commit_sha,
        "deployment_id": deployment_id,
        "canonical_sha256": canonical_sha,
        "canonical_size_bytes": len(canonical),
        "manifest": manifest,
    }
    receipt: EvidenceReceipt = record_envelope(envelope)
    if not verify_receipt(receipt):
        raise RuntimeError("S1_DURABLE_ROUND_TRIP_FAILED")

    action_receipt = issue_action_receipt(
        action_id=action_id,
        commit_sha=commit_sha,
        deployment_id=deployment_id,
        evidence_sha=receipt.envelope_sha,
    )
    return {
        "status": "EVIDENCE_PERSISTED",
        "s1_admission": "DENY_UNTIL_INDEPENDENT_VERIFIER_PASS",
        "cycle_id": cycle_id,
        "action_id": action_id,
        "canonical_sha256": canonical_sha,
        "evidence_sha": receipt.envelope_sha,
        "receipt_sha256": action_receipt["receipt_sha256"],
    }
