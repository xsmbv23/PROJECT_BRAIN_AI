"""Single ordered Forensic Database Admission Chain.

A PASS only permits evaluation of the next gate. Later gates are never
implicitly evaluated or inherited from raw booleans.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Gate(str, Enum):
    DB_EXISTENCE = "DB_EXISTENCE"
    DB_BINDING = "DB_BINDING"
    DB_TLS_ADMISSION = "DB_TLS_ADMISSION"
    DB_ROUND_TRIP = "DB_ROUND_TRIP"
    PROMOTION = "PROMOTION"


@dataclass(frozen=True)
class AdmissionState:
    existence: bool = False
    binding: bool = False
    tls: bool = False
    round_trip: bool = False


def evaluate(state: AdmissionState) -> dict[str, object]:
    """Evaluate gates strictly from left to right.

    Once a gate fails, all deeper gates remain UNREACHED regardless of their
    raw boolean inputs. This prevents a successor from interpreting a later
    raw flag as evidence-backed PASS.
    """
    checks = (
        (Gate.DB_EXISTENCE, state.existence),
        (Gate.DB_BINDING, state.binding),
        (Gate.DB_TLS_ADMISSION, state.tls),
        (Gate.DB_ROUND_TRIP, state.round_trip),
    )

    passed: list[str] = []
    first_failed: str | None = None
    reached: list[str] = []

    for gate, value in checks:
        if first_failed is not None:
            break
        reached.append(gate.value)
        if value:
            passed.append(gate.value)
        else:
            first_failed = gate.value

    promotion = first_failed is None and len(passed) == len(checks)
    if promotion:
        reached.append(Gate.PROMOTION.value)
        passed.append(Gate.PROMOTION.value)
    else:
        # Promotion is never evaluated when an admission gate fails.
        # It is therefore UNREACHED, not merely FALSE.
        pass

    return {
        "chain": [gate.value for gate in (*checks, (Gate.PROMOTION, promotion))],
        "reached": reached,
        "passed": passed,
        "first_failed_gate": first_failed,
        "promotion": promotion,
        "semantics": "PASS_IS_PREREQUISITE_ONLY",
        "unknown_is_not_pass": True,
        "default_deny": True,
    }
