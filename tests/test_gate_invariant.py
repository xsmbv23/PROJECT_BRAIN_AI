import unittest

from tools.gate_invariant import GateDefinition, GateResult, check_gate_invariant, gate_chain_is_valid


class GateInvariantTests(unittest.TestCase):
    def setUp(self):
        self.now = 1_000_000.0
        self.prev = GateResult("DB_EXISTENCE", "PASS", "hash-a", self.now, "cycle-1")

    def test_dependency_pass_is_prerequisite_not_current_evidence(self):
        gate = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
        ok, reason = check_gate_invariant(gate, [self.prev], now=self.now)
        self.assertTrue(ok)
        self.assertEqual(reason, "ADMITTED")

    def test_missing_dependency_denies(self):
        gate = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
        ok, reason = check_gate_invariant(gate, [], now=self.now)
        self.assertFalse(ok)
        self.assertEqual(reason, "DEPENDENCY_MISSING:DB_EXISTENCE")

    def test_non_pass_dependency_denies(self):
        prev = GateResult("DB_EXISTENCE", "UNKNOWN", "hash-a", self.now, "cycle-1")
        gate = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
        ok, reason = check_gate_invariant(gate, [prev], now=self.now)
        self.assertFalse(ok)
        self.assertEqual(reason, "DEPENDENCY_NOT_PASS:DB_EXISTENCE")

    def test_stale_evidence_denies(self):
        gate = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
        ok, reason = check_gate_invariant(gate, [self.prev], now=self.now + 301)
        self.assertFalse(ok)
        self.assertEqual(reason, "STALE_EVIDENCE:DB_EXISTENCE")

    def test_cycle_mismatch_denies(self):
        prev = GateResult("DB_EXISTENCE", "PASS", "hash-a", self.now, "cycle-old")
        later = GateResult("OTHER", "PASS", "hash-b", self.now, "cycle-new")
        gate = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
        ok, reason = check_gate_invariant(gate, [prev, later], now=self.now)
        self.assertFalse(ok)
        self.assertEqual(reason, "CYCLE_MISMATCH:DB_EXISTENCE")

    def test_chain_rejects_evidence_reuse(self):
        history = [
            self.prev,
            GateResult("DB_BINDING", "PASS", "hash-a", self.now, "cycle-1"),
        ]
        ok, reason = gate_chain_is_valid(history, now=self.now)
        self.assertFalse(ok)
        self.assertEqual(reason, "EVIDENCE_REUSE:DB_BINDING")

    def test_chain_rejects_duplicate_gate(self):
        history = [
            self.prev,
            GateResult("DB_EXISTENCE", "PASS", "hash-b", self.now, "cycle-1"),
        ]
        ok, reason = gate_chain_is_valid(history, now=self.now)
        self.assertFalse(ok)
        self.assertEqual(reason, "DUPLICATE_GATE:DB_EXISTENCE")


if __name__ == "__main__":
    unittest.main()
