"""Static admission-control audit: deny unsafe promotion paths."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class AuditFinding:
    code: str
    severity: str
    message: str

def audit_decision(decision: Mapping[str, Any]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    if decision.get("status") == "PASS" and decision.get("contract_id") != "S1_CANONICAL_EVIDENCE_V2":
        findings.append(AuditFinding("ADMISSION_CONTRACT_MISMATCH", "CRITICAL", "PASS without the canonical S1 contract is forbidden"))
    if decision.get("status") == "PASS" and decision.get("errors"):
        findings.append(AuditFinding("ADMISSION_PASS_WITH_ERRORS", "CRITICAL", "PASS with verifier errors is forbidden"))
    if decision.get("provisional") is True and decision.get("admission_eligible") is True:
        findings.append(AuditFinding("PROVISIONAL_PROMOTION", "CRITICAL", "Provisional decisions cannot become admission"))
    if decision.get("bypass") is True or decision.get("override") is True or decision.get("force_promote") is True:
        findings.append(AuditFinding("PROMOTION_BYPASS", "CRITICAL", "Bypass/override/force promotion is forbidden"))
    if decision.get("synthetic_data") is True:
        findings.append(AuditFinding("SYNTHETIC_ADMISSION", "CRITICAL", "Synthetic evidence cannot be admitted"))
    return findings

def admission_allowed(decision: Mapping[str, Any]) -> bool:
    findings = audit_decision(decision)
    if findings:
        return False
    return (decision.get("status") == "PASS" and decision.get("contract_id") == "S1_CANONICAL_EVIDENCE_V2" and not decision.get("errors") and decision.get("independent_verifier") is True and bool(decision.get("evidence_sha")))
