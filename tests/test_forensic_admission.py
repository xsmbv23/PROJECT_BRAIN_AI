import math
import unittest

from tools.forensic_admission import admit_edge, admit_ev


class ForensicAdmissionTests(unittest.TestCase):
    def test_edge_requires_observable_evidence(self):
        self.assertFalse(admit_edge("DB_EXISTENCE", "DB_BINDING", False).allowed)
        self.assertEqual(admit_edge("DB_EXISTENCE", "DB_BINDING", False).reason, "EDGE_EVIDENCE_UNKNOWN")

    def test_edge_requires_endpoints(self):
        self.assertFalse(admit_edge("", "DB_BINDING", True).allowed)

    def test_explicit_edge_can_admit(self):
        self.assertTrue(admit_edge("DB_EXISTENCE", "DB_BINDING", True).allowed)

    def test_negative_ev_is_denied(self):
        result = admit_ev(-0.01)
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason, "EV_NEGATIVE")

    def test_unknown_ev_is_denied(self):
        self.assertFalse(admit_ev(None).allowed)

    def test_nonfinite_ev_is_denied(self):
        self.assertFalse(admit_ev(math.nan).allowed)
        self.assertFalse(admit_ev(math.inf).allowed)

    def test_zero_ev_is_not_negative(self):
        self.assertTrue(admit_ev(0).allowed)

    def test_positive_ev_is_admitted(self):
        self.assertTrue(admit_ev(1.0).allowed)


if __name__ == "__main__":
    unittest.main()
