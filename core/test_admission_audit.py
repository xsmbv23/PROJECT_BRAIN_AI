from core.admission_audit import admission_allowed, audit_decision

def test_rejects_provisional_promotion():
    d = {"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","provisional":True,"admission_eligible":True,"independent_verifier":True,"evidence_sha":"x"}
    assert admission_allowed(d) is False

def test_rejects_bypass():
    d = {"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","bypass":True,"independent_verifier":True,"evidence_sha":"x"}
    assert admission_allowed(d) is False

def test_rejects_missing_independent_verifier():
    d = {"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","independent_verifier":False,"evidence_sha":"x"}
    assert admission_allowed(d) is False

def test_accepts_only_explicit_valid_shape():
    d = {"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","errors":[],"independent_verifier":True,"evidence_sha":"abc"}
    assert admission_allowed(d) is True
