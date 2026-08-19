import unittest

from core.forensic_gate import Gate, GateEvidence, GateStatus, SourceGate, SourceEvidence, admit_gate, admit_source_gate, promote


class ForensicGateChainTests(unittest.TestCase):
    def ev(self, gate, status=GateStatus.PASS, receipt="r-1"):
        return GateEvidence(gate=gate, status=status, receipt_id=receipt)

    def test_pass_does_not_inherit_to_next_gate(self):
        existence = self.ev(Gate.EXISTENCE)
        binding = self.ev(Gate.BINDING, GateStatus.UNKNOWN)
        decision = admit_gate(binding, prerequisites=(existence,))
        self.assertEqual(decision.status, GateStatus.UNKNOWN)

    def test_missing_prerequisite_denies_local_pass(self):
        binding = self.ev(Gate.BINDING)
        decision = admit_gate(binding, prerequisites=(self.ev(Gate.EXISTENCE, GateStatus.DENY),))
        self.assertEqual(decision.status, GateStatus.DENY)
        self.assertEqual(decision.reason, "PREREQUISITE_NOT_PROVEN")

    def test_db_promotion_is_not_granted_by_source_network_gate(self):
        source = SourceEvidence(SourceGate.NETWORK_ORIGIN, GateStatus.PASS, "n")
        source_decision = admit_source_gate(source)
        self.assertEqual(source_decision.status, GateStatus.PASS)
        chain = (self.ev(Gate.EXISTENCE), self.ev(Gate.BINDING), self.ev(Gate.SECURITY), self.ev(Gate.ROUND_TRIP))
        decision = promote(chain)
        self.assertEqual(decision.status, GateStatus.PASS)

    def test_db_promotion_requires_independent_db_receipts(self):
        chain = (
            self.ev(Gate.EXISTENCE, receipt="e"),
            self.ev(Gate.BINDING, receipt="b"),
            self.ev(Gate.SECURITY, receipt="s"),
            self.ev(Gate.ROUND_TRIP, receipt="r"),
        )
        decision = promote(chain)
        self.assertEqual(decision.status, GateStatus.PASS)


if __name__ == "__main__":
    unittest.main()
