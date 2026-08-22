from orchestration.quorum_reconciliation import reconcile

def test_two_of_three_matrix():
    workers = ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION")
    for missing in workers:
        available = {w: w != missing for w in workers}
        r = reconcile(available)
        assert r.mode == "DEGRADED"
        assert r.can_deliberate
        assert r.provisional
        assert not r.admission_eligible

def test_zero_and_one_worker_matrix():
    workers = ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION")
    assert not reconcile({w: False for w in workers}).can_deliberate
    for only in workers:
        available = {w: w == only for w in workers}
        assert not reconcile(available).can_deliberate
