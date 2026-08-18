import unittest

from tools.runtime_boot_gate import admission_summary


class RuntimeBootAdmissionTests(unittest.TestCase):
    def test_bound_tls_without_round_trip_must_deny_promotion(self):
        result = admission_summary("BOUND_TLS", round_trip_proven=False)
        self.assertEqual(result["db_binding"], "BOUND_TLS")
        self.assertEqual(result["db_tls_admission"], "PASS")
        self.assertEqual(result["db_round_trip"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")

    def test_bound_tls_with_real_round_trip_may_promote(self):
        result = admission_summary("BOUND_TLS", round_trip_proven=True)
        self.assertEqual(result["db_round_trip"], "PASS")
        self.assertEqual(result["promotion"], "DENY")
        # DB existence remains external evidence; this module cannot infer it.

    def test_unsafe_binding_denies_tls_and_promotion(self):
        result = admission_summary("DENY_TLS", round_trip_proven=True)
        self.assertEqual(result["db_tls_admission"], "DENY")
        self.assertEqual(result["promotion"], "DENY")


if __name__ == "__main__":
    unittest.main()
