"""Static admission-control audit: deny unsafe promotion paths."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class AuditFinding:
    code: str
    severity: str
    message: str

S1_REQUIRED = (
    "source_provenance",
    "acquisition_channel",
    "acquisition_reference",
    "acquisition_timestamp_utc",
    "artifact_path",
    "canonical_artifact_path",
    "raw_artifact_sha256",
    "raw_byte_sha256",
    "date_start",
    "date_end",
    "expected_consecutive_days",
    "observed_consecutive_days",
    "coverage_ratio",
    "unresolved_conflicts",
    "admission_receipt",
    "frozen_canonical_sha256",
    "synthetic_data",
)


def _evidence(decision: Mapping[str, Any]) -> Mapping[str, Any]:
    value = decision.get("evidence")
    return value if isinstance(value, Mapping) else decision


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
    if decision.get("synthetic_data") is True or _evidence(decision).get("synthetic_data") is True:
        findings.append(AuditFinding("SYNTHETIC_ADMISSION", "CRITICAL", "Synthetic evidence cannot be admitted"))

    if decision.get("status") == "PASS":
        evidence = _evidence(decision)
        missing = [k for k in S1_REQUIRED if k not in evidence]
        if missing:
            findings.append(AuditFinding("S1_REQUIRED_EVIDENCE_MISSING", "CRITICAL", f"Missing required S1 evidence: {','.join(missing)}"))
        if evidence.get("coverage_ratio") != 1.0:
            findings.append(AuditFinding("S1_COVERAGE_NOT_COMPLETE", "CRITICAL", "S1 coverage_ratio must equal 1.0"))
        if evidence.get("unresolved_conflicts") != 0:
            findings.append(AuditFinding("S1_UNRESOLVED_CONFLICTS", "CRITICAL", "S1 unresolved_conflicts must equal 0"))
        if evidence.get("synthetic_data") is not False:
            findings.append(AuditFinding("S1_SYNTHETIC_FLAG_INVALID", "CRITICAL", "S1 synthetic_data must be explicitly false"))
        if not evidence.get("admission_receipt"):
            findings.append(AuditFinding("S1_ADMISSION_RECEIPT_MISSING", "CRITICAL", "A real observable admission receipt is required"))
        if not evidence.get("frozen_canonical_sha256"):
            findings.append(AuditFinding("S1_FROZEN_HASH_MISSING", "CRITICAL", "A frozen canonical SHA-256 is required"))
        if decision.get("fresh_evidence") is not True:
            findings.append(AuditFinding("S1_FRESH_EVIDENCE_MISSING", "CRITICAL", "Promotion requires explicit fresh evidence"))

    return findings


def admission_allowed(decision: Mapping[str, Any]) -> bool:
    findings = audit_decision(decision)
    if findings:
        return False
    return (
        decision.get("status") == "PASS"
        and decision.get("contract_id") == "S1_CANONICAL_EVIDENCE_V2"
        and not decision.get("errors")
        and decision.get("independent_verifier") is True
        and bool(decision.get("evidence_sha"))
        and decision.get("fresh_evidence") is True
    )
