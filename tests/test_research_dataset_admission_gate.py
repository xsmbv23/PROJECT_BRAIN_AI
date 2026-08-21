from tools.research_dataset_admission_gate import admit_research_dataset_receipt


def _receipt():
    return {
        "dataset_identity": "dataset-1",
        "source_provenance_reference": "prov-1",
        "canonical_input_reference": "canon-1",
        "temporal_evidence_reference": "temporal-1",
        "date_manifest_reference": "manifest-1",
        "date_manifest_sha256": "a" * 64,
        "start_date": "2026-01-01",
        "end_date": "2026-02-10",
        "actual_days": 41,
        "required_days": 41,
        "contiguous": True,
        "missing_days": [],
        "train_observations": 20,
        "test_observations": 20,
        "temporal_policy": "DATE_ALIGNED_NO_LOOKAHEAD",
        "code_version": "commit-1",
    }


def test_claimant_receipt_alone_is_not_admission():
    result = admit_research_dataset_receipt(_receipt(), None)
    assert result["status"] == "UNKNOWN"


def test_unverified_external_resolution_is_not_admission():
    result = admit_research_dataset_receipt(
        _receipt(),
        {"status": "UNKNOWN", "verifier_reference": "resolver-1"},
    )
    assert result["status"] == "UNKNOWN"


def test_verified_matching_manifest_can_admit_research_only():
    result = admit_research_dataset_receipt(
        _receipt(),
        {
            "status": "VERIFIED",
            "verifier_reference": "resolver-1",
            "resolved_manifest_sha256": "a" * 64,
        },
    )
    assert result["status"] == "ADMITTED"
    assert result["canonical_promotion"] == "NOT_PROVEN"
    assert result["edge"] == "NOT_PROVEN"
    assert result["ev_pnl"] == "NOT_PROVEN"
    assert result["action"] == "NOT_AUTHORIZED"
