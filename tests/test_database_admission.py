import unittest

from tools.database_admission import AdmissionState, evaluate


class DatabaseAdmissionTests(unittest.TestCase):
    def test_empty_state_denies_at_existence(self):
        result = evaluate(AdmissionState())
        self.assertEqual(result["first_failed_gate"], "DB_EXISTENCE")
        self.assertFalse(result["promotion"])

    def test_existence_does_not_grant_binding(self):
        result = evaluate(AdmissionState(existence=True))
        self.assertEqual(result["first_failed_gate"], "DB_BINDING")
        self.assertFalse(result["promotion"])

    def test_binding_does_not_grant_tls(self):
        result = evaluate(AdmissionState(existence=True, binding=True))
        self.assertEqual(result["first_failed_gate"], "DB_TLS_ADMISSION")
        self.assertFalse(result["promotion"])

    def test_tls_does_not_grant_round_trip(self):
        result = evaluate(AdmissionState(existence=True, binding=True, tls=True))
        self.assertEqual(result["first_failed_gate"], "DB_ROUND_TRIP")
        self.assertFalse(result["promotion"])

    def test_only_complete_chain_promotes(self):
        result = evaluate(AdmissionState(True, True, True, True))
        self.assertIsNone(result["first_failed_gate"])
        self.assertTrue(result["promotion"])


if __name__ == "__main__":
    unittest.main()
