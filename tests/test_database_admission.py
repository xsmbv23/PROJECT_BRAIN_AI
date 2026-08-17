import unittest

from tools.database_admission import AdmissionState, evaluate


class DatabaseAdmissionTests(unittest.TestCase):
    def test_empty_state_denies_at_existence(self):
        result = evaluate(AdmissionState())
        self.assertEqual(result["first_failed_gate"], "DB_EXISTENCE")
        self.assertEqual(result["reached"], ["DB_EXISTENCE"])
        self.assertEqual(result["passed"], [])
        self.assertFalse(result["promotion"])

    def test_existence_does_not_grant_binding(self):
        result = evaluate(AdmissionState(existence=True))
        self.assertEqual(result["first_failed_gate"], "DB_BINDING")
        self.assertEqual(result["reached"], ["DB_EXISTENCE", "DB_BINDING"])
        self.assertEqual(result["passed"], ["DB_EXISTENCE"])
        self.assertFalse(result["promotion"])

    def test_existence_does_not_infer_deeper_raw_flags(self):
        result = evaluate(AdmissionState(existence=True, binding=True, tls=True, round_trip=True))
        # This case is complete and may promote.
        self.assertTrue(result["promotion"])

        blocked = evaluate(AdmissionState(existence=False, binding=True, tls=True, round_trip=True))
        self.assertEqual(blocked["reached"], ["DB_EXISTENCE"])
        self.assertEqual(blocked["passed"], [])
        self.assertEqual(blocked["first_failed_gate"], "DB_EXISTENCE")
        self.assertFalse(blocked["promotion"])

    def test_binding_does_not_grant_tls(self):
        result = evaluate(AdmissionState(existence=True, binding=True))
        self.assertEqual(result["first_failed_gate"], "DB_TLS_ADMISSION")
        self.assertEqual(result["passed"], ["DB_EXISTENCE", "DB_BINDING"])
        self.assertFalse(result["promotion"])

    def test_tls_does_not_grant_round_trip(self):
        result = evaluate(AdmissionState(existence=True, binding=True, tls=True))
        self.assertEqual(result["first_failed_gate"], "DB_ROUND_TRIP")
        self.assertEqual(result["passed"], ["DB_EXISTENCE", "DB_BINDING", "DB_TLS_ADMISSION"])
        self.assertFalse(result["promotion"])

    def test_only_complete_chain_promotes(self):
        result = evaluate(AdmissionState(True, True, True, True))
        self.assertIsNone(result["first_failed_gate"])
        self.assertEqual(result["reached"], [
            "DB_EXISTENCE",
            "DB_BINDING",
            "DB_TLS_ADMISSION",
            "DB_ROUND_TRIP",
            "PROMOTION",
        ])
        self.assertTrue(result["promotion"])
        self.assertEqual(result["passed"], result["reached"])


if __name__ == "__main__":
    unittest.main()
