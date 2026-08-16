import unittest

from core.foundation_hardening import (
    AuditChain, CapabilityLease, CircuitBreaker, GovernanceDeny, PolicyPin,
    quarantine, validate_schema_major,
)


class FoundationHardeningTests(unittest.TestCase):
    def test_policy_pin_denies_mismatch(self):
        pin = PolicyPin("p1", "v1.0", "b1")
        with self.assertRaisesRegex(GovernanceDeny, "POLICY_PIN_MISMATCH"):
            pin.verify(policy_version="p2", schema_version="v1.0", brain_state_version="b1")

    def test_capability_lease_denies_expiry_and_replay(self):
        lease = CapabilityLease("cap", "corr", "L0", "L1", 0, 10, "n", "p1", 1)
        with self.assertRaisesRegex(GovernanceDeny, "CAPABILITY_EXPIRED"):
            lease.verify(now=10, corridor_id="corr", capability_id="cap", nonce="n", policy_version="p1", operation_count=0)

    def test_breaker_opens_after_threshold(self):
        b = CircuitBreaker(threshold=2, cooldown_seconds=10)
        b.failure(0)
        b.failure(1)
        with self.assertRaisesRegex(GovernanceDeny, "CIRCUIT_BREAKER_OPEN"):
            b.allow(2)

    def test_schema_major_mismatch_denies(self):
        with self.assertRaisesRegex(GovernanceDeny, "SCHEMA_MAJOR_MISMATCH"):
            validate_schema_major(received="v2.0", expected="v1.9")

    def test_quarantine_is_terminal_metadata_state(self):
        self.assertEqual(quarantine("lineage break"), {"state": "QUARANTINED", "reason": "lineage break"})

    def test_audit_chain_is_linked_and_deterministic(self):
        chain = AuditChain()
        a = chain.append(event_id="1", event_type="DENY", policy_version="p1", payload={"x": 1}, timestamp=100)
        b = chain.append(event_id="2", event_type="QUARANTINE", policy_version="p1", payload={"x": 2}, timestamp=101)
        self.assertEqual(a.previous_hash, "GENESIS")
        self.assertEqual(b.previous_hash, a.event_hash)
        self.assertEqual(chain.last_hash, b.event_hash)


if __name__ == "__main__":
    unittest.main()
