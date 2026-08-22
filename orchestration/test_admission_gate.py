from orchestration.admission_gate import gate

def test_gate_denies_provisional():
    r = gate({"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","provisional":True,"admission_eligible":True,"independent_verifier":True,"evidence_sha":"x"})
    assert r["admission"] == "DENY"

def test_gate_denies_without_evidence():
    r = gate({"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","errors":[],"independent_verifier":True})
    assert r["admission"] == "DENY"

def test_gate_allows_only_explicit_verified_evidence():
    r = gate({"status":"PASS","contract_id":"S1_CANONICAL_EVIDENCE_V2","errors":[],"independent_verifier":True,"evidence_sha":"abc"})
    assert r["admission"] == "ALLOW"
