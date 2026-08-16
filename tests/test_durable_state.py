import unittest

from core.durable_audit import seal_head
from core.durable_state import persist_audit_head, restore_audit_head
from core.foundation_hardening import AuditChain, GovernanceDeny


class MemoryStore:
    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


class DurableStateTests(unittest.TestCase):
    def test_round_trip_after_simulated_restart(self):
        chain = AuditChain()
        chain.append(event_id="e1", event_type="VERIFIED", policy_version="p1", payload={}, timestamp=1)
        envelope = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=2)
        store = MemoryStore()
        persist_audit_head(store, envelope)

        del chain
        restored = restore_audit_head(store, policy="p1", schema="v1.0", brain_state="b1", expected_head=envelope.audit_head)
        self.assertTrue(restored.restored)
        self.assertEqual(restored.envelope.audit_head, envelope.audit_head)

    def test_missing_state_denies(self):
        with self.assertRaises(GovernanceDeny):
            restore_audit_head(MemoryStore(), policy="p1", schema="v1.0", brain_state="b1", expected_head="x")

    def test_tamper_denies(self):
        chain = AuditChain()
        chain.append(event_id="e1", event_type="VERIFIED", policy_version="p1", payload={}, timestamp=1)
        envelope = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=2)
        store = MemoryStore()
        persist_audit_head(store, envelope)
        store.data["brain.audit_head.v1"] = store.data["brain.audit_head.v1"].replace('"event_count":1', '"event_count":2')
        with self.assertRaises(GovernanceDeny):
            restore_audit_head(store, policy="p1", schema="v1.0", brain_state="b1", expected_head=envelope.audit_head)
