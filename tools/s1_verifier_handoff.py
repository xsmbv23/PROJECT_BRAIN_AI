"""Independent S1 verifier -> durable evidence handoff.

The handoff accepts only the structured Result produced by core.s1_admission.
A caller cannot manufacture an admission-critical PASS by passing a bare string.
This module never promotes canonical state.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from core.s1_admission import CONTRACT_ID, Result
from tools.s1_evidence_bridge import admit_s1_evidence


def verify_and_persist_s1(*, verifier_result: Result, cycle_id: str, action_id: str,
                          commit_sha: str, deployment_id: str,
                          canonical_path: str | Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(verifier_result, Result):
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_RESULT_TYPE_INVALID"}
    if verifier_result.status != "PASS":
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_NOT_PASS"}
    if verifier_result.contract_id != CONTRACT_ID:
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_CONTRACT_INVALID"}
    if verifier_result.errors:
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_ERRORS_PRESENT"}
    required_verified = {"raw_artifact_sha256", "raw_byte_sha256", "frozen_canonical_sha256"}
    if not required_verified.issubset(set(verifier_result.verified)):
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_PROOF_INCOMPLETE"}

    return admit_s1_evidence(
        cycle_id=cycle_id,
        action_id=action_id,
        commit_sha=commit_sha,
        deployment_id=deployment_id,
        canonical_path=canonical_path,
        manifest=manifest,
    )
