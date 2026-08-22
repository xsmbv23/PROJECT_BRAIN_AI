"""Single explicit admission boundary for orchestration decisions."""
from __future__ import annotations
from typing import Any, Mapping
from core.admission_audit import admission_allowed, audit_decision

def gate(decision: Mapping[str, Any]) -> dict[str, Any]:
    findings = audit_decision(decision)
    allowed = admission_allowed(decision)
    return {
        "admission": "ALLOW" if allowed else "DENY",
        "findings": [f.code for f in findings],
        "reason": "EXPLICIT_S1_VERIFIER_EVIDENCE_REQUIRED" if not allowed else "EXPLICIT_VERIFIED_EVIDENCE",
    }
