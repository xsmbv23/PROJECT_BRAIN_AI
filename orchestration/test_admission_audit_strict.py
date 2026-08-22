#!/usr/bin/env python3
"""Regression tests for fail-closed S1 admission auditing."""
from __future__ import annotations

from core.admission_audit import admission_allowed, audit_decision


def base() -> dict:
    return {
        "status": "PASS",
        "contract_id": "S1_CANONICAL_EVIDENCE_V2",
        "independent_verifier": True,
        "evidence_sha": "abc123",
        "fresh_evidence": True,
        "evidence": {
            "source_provenance": "REAL_AND_TRACEABLE",
            "acquisition_channel": "DURABLE_ARCHIVE_EXPORT",
            "acquisition_reference": "archive://2026-08-22",
            "acquisition_timestamp_utc": "2026-08-22T00:00:00Z",
            "artifact_path": "evidence/raw.json",
            "canonical_artifact_path": "evidence/canonical.json",
            "raw_artifact_sha256": "raw-artifact-sha",
            "raw_byte_sha256": "raw-byte-sha",
            "date_start": "2026-08-17",
            "date_end": "2026-08-21",
            "expected_consecutive_days": 5,
            "observed_consecutive_days": 5,
            "coverage_ratio": 1.0,
            "unresolved_conflicts": 0,
            "admission_receipt": "receipt-2026-08-22",
            "frozen_canonical_sha256": "canonical-sha",
            "synthetic_data": False,
        },
    }


def main() -> int:
    valid = base()
    assert admission_allowed(valid), audit_decision(valid)

    stale = base()
    stale["fresh_evidence"] = False
    assert not admission_allowed(stale)

    incomplete = base()
    del incomplete["evidence"]["frozen_canonical_sha256"]
    assert not admission_allowed(incomplete)

    conflicts = base()
    conflicts["evidence"]["unresolved_conflicts"] = 1
    assert not admission_allowed(conflicts)

    provisional = base()
    provisional["provisional"] = True
    provisional["admission_eligible"] = True
    assert not admission_allowed(provisional)

    print({"schema": "strict-s1-admission-audit/v1", "result": "PASS"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
