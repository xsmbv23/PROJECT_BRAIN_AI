from orchestration.quorum_reconciliation import reconcile

def test_bot3_down_keeps_two_worker_deliberation():
    r = reconcile({"BOT2_QUANT": True, "BOT3_REALITY": False, "BOT4_EXECUTION": True})
    assert r.mode == "DEGRADED"
    assert r.can_deliberate is True
    assert r.provisional is True
    assert r.admission_eligible is False

def test_all_three_full():
    r = reconcile({"BOT2_QUANT": True, "BOT3_REALITY": True, "BOT4_EXECUTION": True})
    assert r.mode == "FULL"
    assert r.can_deliberate is True

def test_one_worker_stops_deliberation():
    r = reconcile({"BOT2_QUANT": True, "BOT3_REALITY": False, "BOT4_EXECUTION": False})
    assert r.mode == "INSUFFICIENT_QUORUM"
    assert r.can_deliberate is False

def test_critical_never_gets_admission_from_quorum():
    r = reconcile({"BOT2_QUANT": True, "BOT3_REALITY": True, "BOT4_EXECUTION": True}, critical=True)
    assert r.admission_eligible is False
