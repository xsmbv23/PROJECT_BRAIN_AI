import unittest

from core.forensic_gate import Gate, GateEvidence, GateStatus, admit_gate, promote


class ForensicGateTests(unittest.TestCase):
    def test_pass_is_local(self):
        existence = GateEvidence(Gate.EXISTENCE, GateStatus.PASS, "r-exists")
        binding = GateEvidence(Gate.BINDING, GateStatus.DENY, "r-binding")
        self.assertEqual(admit_gate(existence).status, GateStatus.PASS)
        self.assertEqual(admit_gate(binding, prerequisites=(existence,)).status, GateStatus.DENY)

    def test_unknown_is_not_pass(self):
        unknown = GateEvidence(Gate.SECURITY, GateStatus.UNKNOWN, "r-unknown")
        self.assertEqual(admit_gate(unknown).status, GateStatus.UNKNOWN)

    def test_missing_receipt_denies(self):
        evidence = GateEvidence(Gate.EXISTENCE, GateStatus.PASS, "")
        self.assertEqual(admit_gate(evidence).status, GateStatus.DENY)

    def test_promotion_requires_every_gate(self):
        chain = (
            GateEvidence(Gate.EXISTENCE, GateStatus.PASS, "a"),
            GateEvidence(Gate.BINDING, GateStatus.PASS, "b"),
            GateEvidence(Gate.SECURITY, GateStatus.PASS, "c"),
        )
        decision = promote(chain)
        self.assertEqual(decision.status, GateStatus.DENY)
        self.assertIn("DB_ROUND_TRIP", decision.reason)

    def test_full_chain_promotes(self):
        chain = tuple(GateEvidence(gate, GateStatus.PASS, gate.value) for gate in (
            Gate.EXISTENCE, Gate.BINDING, Gate.SECURITY, Gate.ROUND_TRIP
        ))
        self.assertEqual(promote(chain).status, GateStatus.PASS)


if __name__ == "__main__":
    unittest.main()
