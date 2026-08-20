"""Single Forensic FSM for guarded admission.

PASS is local to a gate. No gate may inherit PASS from another gate.
UNKNOWN and any unmet prerequisite are DENY. This module contains no I/O,
network access, credentials, or source data.

ACTION_RECEIPT is intentionally separate from truth admission. It proves only
that one exact runtime action was executed for one exact commit/deployment.
It never proves source truth, canonical quorum, Edge, EV/P&L, or promotion.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Gate(str, Enum):
    EXISTENCE="DB_EXISTENCE"; BINDING="DB_BINDING"; SECURITY="DB_TLS_ADMISSION"; ROUND_TRIP="DB_ROUND_TRIP"; PROMOTION="PROMOTION"
class SourceGate(str, Enum):
    INDEPENDENCE="SOURCE_INDEPENDENCE"; NETWORK_ORIGIN="NETWORK_ORIGIN_PROOF"; EXCEL_WEB_MATCH="EXCEL_VS_WEB_MATCH"; CANONICAL_QUORUM="CANONICAL_QUORUM"; TRUTH_ADMISSION="TRUTH_ADMISSION"
class GateStatus(str, Enum): PASS="PASS"; DENY="DENY"; UNKNOWN="UNKNOWN"
@dataclass(frozen=True)
class GateEvidence: gate: Gate; status: GateStatus; receipt_id: str
@dataclass(frozen=True)
class SourceEvidence: gate: SourceGate; status: GateStatus; receipt_id: str
@dataclass(frozen=True)
class ForensicDecision: status: GateStatus; gate: str; reason: str


def admit_gate(evidence: GateEvidence, *, prerequisites: tuple[GateEvidence,...]=())->ForensicDecision:
    if evidence.status is not GateStatus.PASS: return ForensicDecision(evidence.status,evidence.gate.value,"LOCAL_GATE_NOT_PROVEN")
    if any(prior.status is not GateStatus.PASS for prior in prerequisites): return ForensicDecision(GateStatus.DENY,evidence.gate.value,"PREREQUISITE_NOT_PROVEN")
    if not evidence.receipt_id: return ForensicDecision(GateStatus.DENY,evidence.gate.value,"EVIDENCE_RECEIPT_MISSING")
    return ForensicDecision(GateStatus.PASS,evidence.gate.value,"LOCAL_PROPOSITION_PROVEN")


def admit_action_receipt(*, receipt_status: str, receipt_id: str) -> ForensicDecision:
    """Admit an exact action receipt locally; never promote downstream truth."""
    if receipt_status != "PASS_LOCAL":
        return ForensicDecision(GateStatus.DENY, "ACTION_RECEIPT", "ACTION_RECEIPT_NOT_PROVEN")
    if not receipt_id:
        return ForensicDecision(GateStatus.DENY, "ACTION_RECEIPT", "ACTION_RECEIPT_ID_MISSING")
    return ForensicDecision(GateStatus.PASS, "ACTION_RECEIPT", "LOCAL_ACTION_EXECUTION_PROVEN")


def admit_source_gate(evidence: SourceEvidence, *, prerequisites: tuple[SourceEvidence,...]=())->ForensicDecision:
    if evidence.status is not GateStatus.PASS: return ForensicDecision(evidence.status,evidence.gate.value,"LOCAL_SOURCE_GATE_NOT_PROVEN")
    if any(prior.status is not GateStatus.PASS for prior in prerequisites): return ForensicDecision(GateStatus.DENY,evidence.gate.value,"SOURCE_PREREQUISITE_NOT_PROVEN")
    if not evidence.receipt_id: return ForensicDecision(GateStatus.DENY,evidence.gate.value,"SOURCE_EVIDENCE_RECEIPT_MISSING")
    return ForensicDecision(GateStatus.PASS,evidence.gate.value,"LOCAL_SOURCE_PROPOSITION_PROVEN")


def promote(evidence_chain: tuple[GateEvidence,...])->ForensicDecision:
    """Promote only the DATABASE domain. Source gates can never satisfy DB gates."""
    required=(Gate.EXISTENCE,Gate.BINDING,Gate.SECURITY,Gate.ROUND_TRIP)
    by_gate={item.gate:item for item in evidence_chain}
    for gate in required:
        item=by_gate.get(gate)
        if item is None or item.status is not GateStatus.PASS or not item.receipt_id:
            return ForensicDecision(GateStatus.DENY,Gate.PROMOTION.value,f"{gate.value}_NOT_INDEPENDENTLY_PROVEN")
    return ForensicDecision(GateStatus.PASS,Gate.PROMOTION.value,"ALL_DATABASE_GATES_INDEPENDENTLY_PROVEN")
