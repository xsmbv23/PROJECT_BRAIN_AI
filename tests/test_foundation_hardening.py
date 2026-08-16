from core.foundation_hardening import (
    AuditChain, CapabilityLease, CircuitBreaker, GovernanceDeny, PolicyPin,
    quarantine, validate_schema_major,
)


def test_policy_pin_denies_mismatch():
    pin = PolicyPin("p1", "v1.0", "b1")
    try:
        pin.verify(policy_version="p2", schema_version="v1.0", brain_state_version="b1")
    except GovernanceDeny as exc:
        assert str(exc) == "POLICY_PIN_MISMATCH"
    else:
        raise AssertionError("policy mismatch must deny")


def test_capability_lease_denies_expiry_and_replay():
    lease = CapabilityLease("cap", "corr", "L0", "L1", 0, 10, "n", "p1", 1)
    try:
        lease.verify(now=10, corridor_id="corr", capability_id="cap", nonce="n", policy_version="p1", operation_count=0)
    except GovernanceDeny as exc:
        assert str(exc) == "CAPABILITY_EXPIRED"
    else:
        raise AssertionError("expired lease must deny")


def test_breaker_opens_after_threshold():
    b = CircuitBreaker(threshold=2, cooldown_seconds=10)
    b.failure(0)
    b.failure(1)
    try:
        b.allow(2)
    except GovernanceDeny as exc:
        assert str(exc) == "CIRCUIT_BREAKER_OPEN"
    else:
        raise AssertionError("open breaker must deny")


def test_schema_major_mismatch_denies():
    try:
        validate_schema_major(received="v2.0", expected="v1.9")
    except GovernanceDeny as exc:
        assert str(exc) == "SCHEMA_MAJOR_MISMATCH"
    else:
        raise AssertionError("schema major mismatch must deny")


def test_quarantine_is_terminal_metadata_state():
    assert quarantine("lineage break") == {"state": "QUARANTINED", "reason": "lineage break"}


def test_audit_chain_is_linked_and_deterministic():
    chain = AuditChain()
    a = chain.append(event_id="1", event_type="DENY", policy_version="p1", payload={"x": 1}, timestamp=100)
    b = chain.append(event_id="2", event_type="QUARANTINE", policy_version="p1", payload={"x": 2}, timestamp=101)
    assert a.previous_hash == "GENESIS"
    assert b.previous_hash == a.event_hash
    assert chain.last_hash == b.event_hash
