"""Single ordered Forensic Database Admission Chain.

This is intentionally small: one state machine, explicit gates, no inherited
permissions. A PASS only permits evaluation of the next gate.
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

    @property
    def promotion(self) -> bool:
        return self.existence and self.binding and self.tls and self.round_trip


def evaluate(state: AdmissionState) -> dict[str, object]:
    gates = [
        (Gate.DB_EXISTENCE, state.existence),
        (Gate.DB_BINDING, state.binding),
        (Gate.DB_TLS_ADMISSION, state.tls),
        (Gate.DB_ROUND_TRIP, state.round_trip),
        (Gate.PROMOTION, state.promotion),
    ]
    first_failed = next((gate.value for gate, passed in gates if not passed), None)
    return {
        "chain": [gate.value for gate, _ in gates],
        "passed": [gate.value for gate, passed in gates if passed],
        "first_failed_gate": first_failed,
        "promotion": state.promotion,
        "semantics": "PASS_IS_PREREQUISITE_ONLY",
        "unknown_is_not_pass": True,
        "default_deny": True,
    }
