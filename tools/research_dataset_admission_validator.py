"""Validate Quant Engine research-dataset admission receipts.

This is a consumer-side evidence gate. A valid receipt proves only research
eligibility at this gate; it never proves canonical truth, edge, EV/P&L, or
action authorization.
"""
from __future__ import annotations


def validate_research_dataset_receipt(receipt: dict[str, object]) -> dict[str, object]:
    required = (
        "dataset_identity", "source_provenance_reference", "canonical_input_reference",
        "start_date", "end_date", "actual_days", "required_days", "contiguous",
        "missing_days", "train_observations", "test_observations", "temporal_policy",
        "code_version",
    )
    missing = [key for key in required if key not in receipt]
    if missing:
        return {"status": "DENY", "reason": "RECEIPT_FIELDS_MISSING", "missing": missing}

    if receipt["temporal_policy"] != "DATE_ALIGNED_NO_LOOKAHEAD":
        return {"status": "DENY", "reason": "TEMPORAL_POLICY_INVALID"}
    if receipt["contiguous"] is not True:
        return {"status": "DENY", "reason": "TEMPORAL_CONTIGUITY_NOT_PROVEN"}
    if receipt["missing_days"] != []:
        return {"status": "DENY", "reason": "MISSING_DAYS_PRESENT"}
    if not isinstance(receipt["actual_days"], int) or not isinstance(receipt["required_days"], int):
        return {"status": "DENY", "reason": "DAY_COUNTS_INVALID"}
    if receipt["actual_days"] < receipt["required_days"]:
        return {"status": "DENY", "reason": "INSUFFICIENT_REAL_HISTORY"}
    if not isinstance(receipt["train_observations"], int) or receipt["train_observations"] < 20:
        return {"status": "DENY", "reason": "TRAIN_MINIMUM_NOT_MET"}
    if not isinstance(receipt["test_observations"], int) or receipt["test_observations"] < 20:
        return {"status": "DENY", "reason": "TEST_MINIMUM_NOT_MET"}

    return {
        "status": "ADMITTED",
        "reason": "RESEARCH_ELIGIBILITY_ONLY",
        "canonical_promotion": "NOT_PROVEN",
        "edge": "NOT_PROVEN",
        "ev_pnl": "NOT_PROVEN",
        "action": "NOT_AUTHORIZED",
    }
