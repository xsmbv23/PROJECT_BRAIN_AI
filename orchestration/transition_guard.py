"""Mandatory fail-closed guard for orchestration state transitions."""
from __future__ import annotations
from typing import Any, Mapping
from core.admission_invariants import validate_transition

FINAL_STATES = frozenset({"ADMITTED", "PROMOTED", "FINAL"})

def guard_transition(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    ok, errors = validate_transition(before, after)
    if not ok:
        return {"allowed": False, "state": "DENY", "errors": errors}
    if after.get("status") in FINAL_STATES and after.get("admission") != "ALLOW":
        return {"allowed": False, "state": "DENY", "errors": ["FINAL_STATE_REQUIRES_ADMISSION_ALLOW"]}
    return {"allowed": True, "state": after.get("status", "UNSET"), "errors": []}
