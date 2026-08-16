from core.foundation_gate import run_foundation_gate


def test_foundation_gate_passes_bounded_metadata():
    result = run_foundation_gate()
    assert result["status"] == "PASS"
    assert result["audit_head"] != "GENESIS"
    assert result["checks"]
