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

    def test_database_promotion_does_not_require_network_origin(self):
        chain = tuple(GateEvidence(gate, GateStatus.PASS, gate.value) for gate in (
            Gate.EXISTENCE, Gate.BINDING, Gate.SECURITY, Gate.ROUND_TRIP
        ))
        self.assertEqual(promote(chain).status, GateStatus.PASS)

    def test_source_network_origin_is_separate_domain(self):
        source = SourceEvidence(SourceGate.NETWORK_ORIGIN, GateStatus.PASS, "network-receipt")
        self.assertEqual(admit_source_gate(source).status, GateStatus.PASS)

    def test_source_gate_does_not_inherit_database_pass(self):
        source = SourceEvidence(SourceGate.EXCEL_WEB_MATCH, GateStatus.PASS, "match-receipt")
        db = GateEvidence(Gate.EXISTENCE, GateStatus.PASS, "db-receipt")
        # Database evidence cannot be passed as a source prerequisite.
        self.assertEqual(admit_source_gate(source).status, GateStatus.PASS)
        self.assertNotEqual(source.gate.value, db.gate.value)

    def test_source_prerequisite_is_local(self):
        origin = SourceEvidence(SourceGate.NETWORK_ORIGIN, GateStatus.DENY, "origin-deny")
        match = SourceEvidence(SourceGate.EXCEL_WEB_MATCH, GateStatus.PASS, "match-receipt")
        decision = admit_source_gate(match, prerequisites=(origin,))
        self.assertEqual(decision.status, GateStatus.DENY)
        self.assertEqual(decision.reason, "SOURCE_PREREQUISITE_NOT_PROVEN")

    def test_promotion_requires_every_database_gate(self):
        chain = (
            GateEvidence(Gate.EXISTENCE, GateStatus.PASS, "a"),
            GateEvidence(Gate.BINDING, GateStatus.PASS, "b"),
            GateEvidence(Gate.SECURITY, GateStatus.PASS, "c"),
        )
        decision = promote(chain)
        self.assertEqual(decision.status, GateStatus.DENY)
        self.assertIn("DB_ROUND_TRIP", decision.reason)


if __name__ == "__main__":
    unittest.main()
