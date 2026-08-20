"""Validate Quant Engine repository-workflow receipts without granting runtime truth."""
from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = (
    "evidence_kind",
    "repository_execution",
    "external_runtime_truth",
    "independent_external_observation",
    "commit_sha",
    "workflow_run_id",
    "workflow_run_attempt",
    "receipt_generated_at",
)


def validate_quant_workflow_receipt(receipt: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in receipt:
            errors.append(f"MISSING:{field}")

    if errors:
        return False, errors

    if receipt["evidence_kind"] != "REPOSITORY_WORKFLOW_EXECUTION":
        errors.append("INVALID:evidence_kind")
    if receipt["repository_execution"] != "PROVEN_AT_THIS_STEP":
        errors.append("INVALID:repository_execution")
    if receipt["external_runtime_truth"] != "NOT_PROVEN":
        errors.append("DENY:external_runtime_truth_must_remain_not_proven")
    if receipt["independent_external_observation"] is not False:
        errors.append("DENY:independent_external_observation_must_be_false")

    for field in ("commit_sha", "workflow_run_id", "workflow_run_attempt", "receipt_generated_at"):
        if not isinstance(receipt[field], str) or not receipt[field].strip():
            errors.append(f"INVALID:{field}")

    return not errors, errors
