"""Single Forensic FSM for guarded admission.

PASS is local to a gate. No gate may inherit PASS from another gate.
UNKNOWN and any unmet prerequisite are DENY. This module contains no I/O,
network access, credentials, or source data.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Gate(str, Enum):
    EXISTENCE = "DB_EXISTENCE"
    BINDING = "DB_BINDING"
    SECURITY = "DB_TLS_ADMISSION"
    ROUND_TRIP = "DB_ROUND_TRIP"
    PROMOTION = "PROMOTION"


class GateStatus(str, Enum):
    PASS = "PASS"
    DENY = "DENY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class GateEvidence:
    gate: Gate
    status: GateStatus
    receipt_id: str


@dataclass(frozen=True)
class ForensicDecision:
    status: GateStatus
    gate: Gate
    reason: str


def admit_gate(evidence: GateEvidence, *, prerequisites: tuple[GateEvidence, ...] = ()) -> ForensicDecision:
    """Evaluate one gate without inheriting status from any other gate."""
    if evidence.status is not GateStatus.PASS:
        return ForensicDecision(evidence.status, evidence.gate, "LOCAL_GATE_NOT_PROVEN")
    for prior in prerequisites:
        if prior.status is not GateStatus.PASS:
            return ForensicDecision(GateStatus.DENY, evidence.gate, "PREREQUISITE_NOT_PROVEN")
    if not evidence.receipt_id:
        return ForensicDecision(GateStatus.DENY, evidence.gate, "EVIDENCE_RECEIPT_MISSING")
    return ForensicDecision(GateStatus.PASS, evidence.gate, "LOCAL_PROPOSITION_PROVEN")


def promote(evidence_chain: tuple[GateEvidence, ...]) -> ForensicDecision:
    """Promotion is allowed only when every required proposition has its own receipt."""
    required = (Gate.EXISTENCE, Gate.BINDING, Gate.SECURITY, Gate.ROUND_TRIP)
    by_gate = {item.gate: item for item in evidence_chain}
    for gate in required:
        item = by_gate.get(gate)
        if item is None or item.status is not GateStatus.PASS or not item.receipt_id:
            return ForensicDecision(GateStatus.DENY, Gate.PROMOTION, f"{gate.value}_NOT_INDEPENDENTLY_PROVEN")
    return ForensicDecision(GateStatus.PASS, Gate.PROMOTION, "ALL_REQUIRED_GATES_INDEPENDENTLY_PROVEN")
