import unittest

from core.forensic_gate import (
    Gate,
    GateEvidence,
    GateStatus,
    SourceEvidence,
    SourceGate,
    admit_gate,
    admit_source_gate,
    promote,
)


class ForensicGateIndependenceTests(unittest.TestCase):
    def ev(self, gate, status=GateStatus.PASS, receipt="r"):
        return GateEvidence(gate, status, receipt)

    def src(self, gate, status=GateStatus.PASS, receipt="s"):
        return SourceEvidence(gate, status, receipt)

    def test_db_pass_is_local(self):
        existence = self.ev(Gate.EXISTENCE)
        result = admit_gate(self.ev(Gate.BINDING), prerequisites=(existence,))
        self.assertEqual(result.status, GateStatus.PASS)
        # The result proves BINDING, not PROMOTION.
        self.assertEqual(result.gate, Gate.BINDING.value)

    def test_db_pass_does_not_promote(self):
        result = promote((self.ev(Gate.EXISTENCE),))
        self.assertEqual(result.status, GateStatus.DENY)
        self.assertIn(Gate.BINDING.value, result.reason)

    def test_source_pass_does_not_satisfy_db(self):
        source = self.src(SourceGate.NETWORK_ORIGIN)
        # The DB promotion API accepts DB evidence only; a source receipt is not usable here.
        result = promote(())
        self.assertEqual(result.status, GateStatus.DENY)
        self.assertNotEqual(source.gate.value, Gate.EXISTENCE.value)

    def test_excel_web_match_does_not_grant_canonical_quorum(self):
        local = self.src(SourceGate.EXCEL_WEB_MATCH)
        result = admit_source_gate(
            self.src(SourceGate.CANONICAL_QUORUM),
            prerequisites=(local,),
        )
        self.assertEqual(result.status, GateStatus.PASS)
        self.assertEqual(result.gate, SourceGate.CANONICAL_QUORUM.value)
        # This is a local prerequisite chain, not a global truth decision.
        self.assertNotEqual(result.gate, SourceGate.TRUTH_ADMISSION.value)

    def test_missing_receipt_denies(self):
        result = admit_gate(self.ev(Gate.EXISTENCE, receipt=""))
        self.assertEqual(result.status, GateStatus.DENY)
        self.assertEqual(result.reason, "EVIDENCE_RECEIPT_MISSING")

    def test_unknown_never_becomes_pass(self):
        result = admit_source_gate(self.src(SourceGate.NETWORK_ORIGIN, GateStatus.UNKNOWN))
        self.assertEqual(result.status, GateStatus.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
