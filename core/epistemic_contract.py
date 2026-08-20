"""Machine-readable epistemic contract for the Forensic FSM.

Invariant: doctrine, state, history, and hypothesis are never evidence merely
because they look authoritative. Only a concrete EVIDENCE artifact can satisfy
an evidence claim, and every gate must own fresh evidence.
"""
from __future__ import annotations

from enum import Enum


class EpistemicType(str, Enum):
    DOCTRINE = "DOCTRINE"
    EVIDENCE = "EVIDENCE"
    STATE = "STATE"
    HISTORY = "HISTORY"
    HYPOTHESIS = "HYPOTHESIS"


class InvalidEvidenceError(ValueError):
    """Raised when a non-evidence epistemic object is promoted as evidence."""


def validate_evidence_claim(source_type: EpistemicType) -> bool:
    if source_type is not EpistemicType.EVIDENCE:
        raise InvalidEvidenceError(
            f"Deny: {source_type.value} cannot be used as Evidence."
        )
    return True


def gate_pass_is_local(*, gate: str, evidence_type: EpistemicType) -> dict[str, object]:
    """Create a local gate result; it grants no downstream PASS inheritance."""
    validate_evidence_claim(evidence_type)
    return {
        "gate": gate,
        "status": "PASS",
        "evidence_type": evidence_type.value,
        "pass_is_local": True,
        "unlocks_only": f"evaluate_next_gate_after_{gate}",
        "promotes": False,
    }
