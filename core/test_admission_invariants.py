from core.admission_invariants import validate_transition

def test_provisional_cannot_promote():
    ok, errors = validate_transition({"provisional": True}, {"status": "PROMOTED"})
    assert not ok
    assert "PROVISIONAL_CANNOT_PROMOTE_DIRECTLY" in errors

def test_promotion_requires_full_evidence():
    ok, errors = validate_transition({}, {"status":"PROMOTED"})
    assert not ok
    assert len(errors) >= 3

def test_valid_promotion_shape():
    ok, errors = validate_transition({}, {"status":"PROMOTED","contract_id":"S1_CANONICAL_EVIDENCE_V2","independent_verifier":True,"evidence_sha":"abc","errors":[]})
    assert ok
    assert errors == []
