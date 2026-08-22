from orchestration.quorum_policy import evaluate_quorum, require_deliberation_quorum


def test_all_workers_full():
    d = evaluate_quorum(["BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION"])
    assert d.mode == "FULL"
    assert d.can_deliberate is True
    assert d.admission_eligible is False


def test_bot3_down_two_worker_degraded():
    d = require_deliberation_quorum(["BOT2_QUANT", "BOT4_EXECUTION"])
    assert d.mode == "DEGRADED"
    assert d.available == ("BOT2_QUANT", "BOT4_EXECUTION")
    assert d.can_deliberate is True
    assert d.admission_eligible is False


def test_one_worker_is_not_quorum():
    d = evaluate_quorum(["BOT2_QUANT"])
    assert d.mode == "INSUFFICIENT_QUORUM"
    assert d.can_deliberate is False


def test_unknown_workers_are_ignored():
    d = evaluate_quorum(["BOT2_QUANT", "UNKNOWN"])
    assert d.available == ("BOT2_QUANT",)
    assert d.can_deliberate is False


def test_critical_never_gets_admission_from_quorum():
    d = evaluate_quorum(["BOT2_QUANT", "BOT4_EXECUTION"], critical=True)
    assert d.mode == "DEGRADED"
    assert d.can_deliberate is True
    assert d.admission_eligible is False
