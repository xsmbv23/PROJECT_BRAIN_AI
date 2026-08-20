"""Validate Quant Engine research-dataset admission receipts.

Consumer-side gate only: admission proves research eligibility at this gate;
it never proves canonical truth, edge, EV/P&L, or action authorization.
"""
from __future__ import annotations

from datetime import date

MIN_REQUIRED_DAYS = 41
MIN_TRAIN_OBSERVATIONS = 20
MIN_TEST_OBSERVATIONS = 20


def _nonempty_string(receipt: dict[str, object], key: str) -> bool:
    value = receipt.get(key)
    return isinstance(value, str) and bool(value.strip())


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

    for key in ("dataset_identity", "source_provenance_reference", "canonical_input_reference", "code_version"):
        if not _nonempty_string(receipt, key):
            return {"status": "DENY", "reason": "IDENTITY_OR_PROVENANCE_EMPTY", "field": key}

    if receipt["temporal_policy"] != "DATE_ALIGNED_NO_LOOKAHEAD":
        return {"status": "DENY", "reason": "TEMPORAL_POLICY_INVALID"}
    if receipt["contiguous"] is not True:
        return {"status": "DENY", "reason": "TEMPORAL_CONTIGUITY_NOT_PROVEN"}
    if receipt["missing_days"] != []:
        return {"status": "DENY", "reason": "MISSING_DAYS_PRESENT"}

    for key in ("actual_days", "required_days", "train_observations", "test_observations"):
        if type(receipt[key]) is not int:
            return {"status": "DENY", "reason": "COUNT_TYPE_INVALID", "field": key}

    if receipt["required_days"] < MIN_REQUIRED_DAYS:
        return {"status": "DENY", "reason": "REQUIRED_HISTORY_BELOW_POLICY_MINIMUM"}
    expected_required = receipt["train_observations"] + receipt["test_observations"] + 1
    if receipt["required_days"] != expected_required:
        return {"status": "DENY", "reason": "REQUIRED_HISTORY_INCONSISTENT_WITH_OOS_SPLIT"}
    if receipt["train_observations"] < MIN_TRAIN_OBSERVATIONS:
        return {"status": "DENY", "reason": "TRAIN_MINIMUM_NOT_MET"}
    if receipt["test_observations"] < MIN_TEST_OBSERVATIONS:
        return {"status": "DENY", "reason": "TEST_MINIMUM_NOT_MET"}
    if receipt["actual_days"] < receipt["required_days"]:
        return {"status": "DENY", "reason": "INSUFFICIENT_REAL_HISTORY"}

    parsed_dates: list[date] = []
    for key in ("start_date", "end_date"):
        try:
            parsed_dates.append(date.fromisoformat(receipt[key]))
        except (TypeError, ValueError):
            return {"status": "DENY", "reason": "DATE_FORMAT_INVALID", "field": key}
    start, end = parsed_dates
    if end < start:
        return {"status": "DENY", "reason": "DATE_RANGE_REVERSED"}
    span_days = (end - start).days + 1
    if receipt["actual_days"] != span_days:
        return {"status": "DENY", "reason": "DAY_COUNT_DOES_NOT_MATCH_DATE_SPAN"}

    return {
        "status": "ADMITTED",
        "reason": "RESEARCH_ELIGIBILITY_ONLY",
        "canonical_promotion": "NOT_PROVEN",
        "edge": "NOT_PROVEN",
        "ev_pnl": "NOT_PROVEN",
        "action": "NOT_AUTHORIZED",
    }
