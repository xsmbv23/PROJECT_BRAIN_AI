from orchestration.transition_guard import guard_transition

def test_final_requires_admission_allow():
    r = guard_transition({}, {"status":"FINAL","contract_id":"S1_CANONICAL_EVIDENCE_V2","independent_verifier":True,"evidence_sha":"x","errors":[]})
    assert not r["allowed"]

def test_provisional_cannot_promote():
    r = guard_transition({"provisional":True}, {"status":"PROMOTED","admission":"ALLOW","contract_id":"S1_CANONICAL_EVIDENCE_V2","independent_verifier":True,"evidence_sha":"x","errors":[]})
    assert not r["allowed"]

def test_valid_final_transition():
    r = guard_transition({}, {"status":"FINAL","admission":"ALLOW","contract_id":"S1_CANONICAL_EVIDENCE_V2","independent_verifier":True,"evidence_sha":"x","errors":[]})
    assert r["allowed"]
