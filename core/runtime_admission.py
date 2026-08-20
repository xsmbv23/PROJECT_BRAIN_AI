"""Exact runtime admission semantics for Forensic evidence and predictions.

This module is intentionally small and deterministic. It never manufactures
missing evidence, never promotes PASS across gates, and never permits future
feature inputs into a T-day prediction.
"""
from __future__ import annotations

from datetime import date
from typing import Mapping

from core.epistemic_contract import EpistemicType, gate_pass_is_local, validate_evidence_claim
from tools.validate_lineage import validate_lineage


def admit_evidence(*, gate: str, source_type: EpistemicType) -> dict[str, object]:
    """Admit one gate's evidence; PASS remains local to that gate."""
    validate_evidence_claim(source_type)
    return gate_pass_is_local(gate=gate, evidence_type=source_type)


def admit_prediction(
    record: Mapping[str, object],
    *,
    feature_input_date: date,
    prediction_date: date,
    prediction_frozen: bool,
    result_revealed: bool,
) -> dict[str, object]:
    """Apply lineage + temporal + freeze gates without changing the record."""
    lineage = validate_lineage(record)
    if lineage["status"] != "PROVEN_LINEAGE":
        return {
            "status": "NOT_PROVEN",
            "execution": "CANCEL",
            "reason": "LINEAGE_INVALID",
            "lineage": lineage,
        }

    if feature_input_date >= prediction_date:
        return {
            "status": "TEMPORAL_VIOLATION",
            "execution": "CANCEL",
            "reason": "FEATURE_INPUT_MUST_BE_T_MINUS_1_OR_EARLIER",
            "lineage": lineage,
        }

    if result_revealed and not prediction_frozen:
        return {
            "status": "NOT_PROVEN",
            "execution": "CANCEL",
            "reason": "PREDICTION_NOT_FROZEN_BEFORE_RESULT_REVEAL",
            "lineage": lineage,
        }

    return {
        "status": "PROVEN_LINEAGE",
        "execution": "ELIGIBLE_FOR_NEXT_GATE",
        "reason": "TEMPORAL_AND_FREEZE_GATES_PASS",
        "lineage": lineage,
        "pass_is_local": True,
        "promotes": False,
    }
