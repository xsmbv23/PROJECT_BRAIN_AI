from orchestration.worker_result_reconciler import reconcile_results

def test_bot3_missing_is_provisional_not_failure():
    r = reconcile_results({"BOT2_QUANT": {"result": "PASS"}, "BOT4_EXECUTION": {"result": "PASS"}}, {"BOT2_QUANT": True, "BOT3_REALITY": False, "BOT4_EXECUTION": True})
    assert r["decision"] == "PROVISIONAL"
    assert r["mode"] == "DEGRADED"
    assert r["admission_eligible"] is False

def test_conflict_holds():
    r = reconcile_results({"BOT2_QUANT": {"result": "PASS"}, "BOT4_EXECUTION": {"result": "HOLD"}}, {"BOT2_QUANT": True, "BOT3_REALITY": False, "BOT4_EXECUTION": True})
    assert r["decision"] == "HOLD_CONFLICT"

def test_critical_never_admits():
    r = reconcile_results({"BOT2_QUANT": {"result": "PASS"}, "BOT3_REALITY": {"result": "PASS"}, "BOT4_EXECUTION": {"result": "PASS"}}, {"BOT2_QUANT": True, "BOT3_REALITY": True, "BOT4_EXECUTION": True}, critical=True)
    assert r["decision"] == "HOLD_CRITICAL_ADMISSION"
