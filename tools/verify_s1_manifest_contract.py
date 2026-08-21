"""Verify the S1 admission contract without admitting any dataset.

This verifier proves only that the contract is internally coherent. It must
never promote S1, inspect a fabricated fixture as canonical truth, or infer
real-world evidence from repository scaffolding.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "s1_canonical_evidence_manifest.schema.json"
REQUIRED = {
    "source_provenance",
    "artifact_path",
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
}


def verify() -> dict[str, object]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["contract_id"] == "S1_CANONICAL_EVIDENCE_V2"
    assert set(data["required"]) == REQUIRED
    conditions = data["admission_conditions"]
    assert conditions["coverage_ratio"] == 1.0
    assert conditions["unresolved_conflicts"] == 0
    assert conditions["synthetic_data"] is False
    assert data["failure_policy"] == "DEFAULT_DENY"
    assert data["unknown_policy"] == "NOT_PASS"
    assert data["pass_inheritance"] is False
    assert data["correction_policy"] == "NEW_VERSION_NEW_HASH_NEW_ADMISSION_EVENT"
    assert data["credential_policy"] == "NO_CREDENTIALS_IN_MANIFEST"
    # Contract coherence is PASS; actual S1 admission remains a separate gate.
    return {
        "status": "PASS_CONTRACT",
        "s1_admission": "NOT_PROVEN",
        "promotion": "DENY",
    }


if __name__ == "__main__":
    print(verify())
