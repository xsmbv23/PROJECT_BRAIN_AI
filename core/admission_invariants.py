"""Fail-closed invariants for admission/promotion state transitions."""
from __future__ import annotations
from typing import Any, Mapping

def validate_transition(before: Mapping[str, Any], after: Mapping[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    after_status = after.get("status")
    if before.get("provisional") is True and after_status in {"PASS", "ADMITTED", "PROMOTED", "FINAL"}:
        errors.append("PROVISIONAL_CANNOT_PROMOTE_DIRECTLY")
    if after_status in {"ADMITTED", "PROMOTED", "FINAL"}:
        if after.get("contract_id") != "S1_CANONICAL_EVIDENCE_V2": errors.append("PROMOTION_REQUIRES_S1_CONTRACT")
        if after.get("independent_verifier") is not True: errors.append("PROMOTION_REQUIRES_INDEPENDENT_VERIFIER")
        if not after.get("evidence_sha"): errors.append("PROMOTION_REQUIRES_EVIDENCE_SHA")
        if after.get("errors"): errors.append("PROMOTION_WITH_ERRORS_FORBIDDEN")
        if any(after.get(k) is True for k in ("bypass", "override", "force_promote")): errors.append("PROMOTION_BYPASS_FORBIDDEN")
    return (not errors, errors)
