from tools.evidence_lineage_validator import validate_evidence


def base():
    return {
        "source_identity": "ketqua16.net",
        "observation_timestamp": "2026-08-21T00:00:00Z",
        "observation_origin": "external_source",
    }


def test_semantic_fingerprint_without_validated_domain_denies():
    evidence = base() | {"semantic_fingerprint": "semantic-123"}
    result = validate_evidence(evidence)
    assert result["status"] == "DENY"
    assert result["reason"] == "SEMANTIC_HASH_REQUIRES_VALIDATED_DOMAIN"


def test_semantic_fingerprint_requires_domain_validation_even_for_quorum():
    evidence = base() | {
        "semantic_fingerprint": "semantic-123",
        "semantic_quorum": True,
    }
    result = validate_evidence(evidence)
    assert result["status"] == "DENY"
    assert result["reason"] == "SEMANTIC_HASH_REQUIRES_VALIDATED_DOMAIN"


def test_semantic_fingerprint_passes_after_domain_validation():
    evidence = base() | {
        "semantic_fingerprint": "semantic-123",
        "validated_canonical_domain": True,
    }
    assert validate_evidence(evidence)["status"] == "PASS"
