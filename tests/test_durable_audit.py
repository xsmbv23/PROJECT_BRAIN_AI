import json
import unittest

from core.durable_audit import restore_and_verify, seal_head, serialize
from core.foundation_hardening import AuditChain, GovernanceDeny


class DurableAuditTests(unittest.TestCase):
    def test_roundtrip_survives_simulated_restart(self):
        chain = AuditChain()
        chain.append(event_id="e1", event_type="VERIFIED", policy_version="p1", payload={"x": 1}, timestamp=100)
        envelope = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=101)
        restored = restore_and_verify(serialize(envelope), expected_policy="p1", expected_schema="v1.0", expected_brain_state="b1", expected_head=chain.last_hash)
        self.assertEqual(restored.audit_head, chain.last_hash)
        self.assertEqual(restored.envelope_sha, envelope.envelope_sha)

    def test_tamper_denies(self):
        chain = AuditChain()
        chain.append(event_id="e1", event_type="VERIFIED", policy_version="p1", payload={}, timestamp=100)
        envelope = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=101)
        data = json.loads(serialize(envelope))
        data["audit_head"] = "tampered"
        with self.assertRaisesRegex(GovernanceDeny, "AUDIT_ENVELOPE_HASH_MISMATCH"):
            restore_and_verify(json.dumps(data), expected_policy="p1", expected_schema="v1.0", expected_brain_state="b1", expected_head=chain.last_hash)

    def test_wrong_policy_denies(self):
        chain = AuditChain()
        chain.append(event_id="e1", event_type="VERIFIED", policy_version="p1", payload={}, timestamp=100)
        envelope = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=101)
        with self.assertRaisesRegex(GovernanceDeny, "AUDIT_ENVELOPE_POLICY_MISMATCH"):
            restore_and_verify(serialize(envelope), expected_policy="p2", expected_schema="v1.0", expected_brain_state="b1", expected_head=chain.last_hash)
