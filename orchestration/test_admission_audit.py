from core.admission_audit import admission_allowed

BASE = {
    "status": "PASS",
    "contract_id": "S1_CANONICAL_EVIDENCE_V2",
    "independent_verifier": True,
    "evidence_sha": "sha-evidence",
    "fresh_evidence": True,
    "evidence": {
        "source_provenance": "primary",
        "acquisition_channel": "runtime",
        "acquisition_reference": "ref-1",
        "acquisition_timestamp_utc": "2026-08-22T00:00:00Z",
        "artifact_path": "a",
        "canonical_artifact_path": "c",
        "raw_artifact_sha256": "a" * 64,
        "raw_byte_sha256": "b" * 64,
        "date_start": "2026-01-01",
        "date_end": "2026-01-02",
        "expected_consecutive_days": 2,
        "observed_consecutive_days": 2,
        "coverage_ratio": 1.0,
        "unresolved_conflicts": 0,
        "admission_receipt": {"id": "receipt-1"},
        "frozen_canonical_sha256": "c" * 64,
        "synthetic_data": False,
    },
}


def test_complete_s1_evidence_is_allowed():
    assert admission_allowed(BASE)


def test_missing_required_evidence_is_denied():
    d = {**BASE, "evidence": {**BASE["evidence"]}}
    d["evidence"].pop("raw_byte_sha256")
    assert not admission_allowed(d)


def test_provisional_promotion_is_denied():
    d = {**BASE, "provisional": True, "admission_eligible": True}
    assert not admission_allowed(d)


def test_bypass_is_denied():
    d = {**BASE, "force_promote": True}
    assert not admission_allowed(d)


def test_stale_evidence_is_denied():
    d = {**BASE, "fresh_evidence": False}
    assert not admission_allowed(d)


def test_conflict_is_denied():
    d = {**BASE, "evidence": {**BASE["evidence"], "unresolved_conflicts": 1}}
    assert not admission_allowed(d)
