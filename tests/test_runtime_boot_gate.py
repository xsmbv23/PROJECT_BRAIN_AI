import unittest

from tools.runtime_boot_gate import admission_summary


class RuntimeBootAdmissionTests(unittest.TestCase):
    def test_bound_tls_without_network_or_round_trip_must_deny_promotion(self):
        result = admission_summary("BOUND_TLS", "NOT_PROVEN", round_trip_proven=False)
        self.assertEqual(result["db_binding"], "BOUND_TLS")
        self.assertEqual(result["db_tls_admission"], "PASS")
        self.assertEqual(result["network_origin_proof"], "NOT_PROVEN")
        self.assertEqual(result["db_round_trip"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")

    def test_network_pass_is_local_and_does_not_infer_round_trip(self):
        result = admission_summary("BOUND_TLS", "PASS", round_trip_proven=False)
        self.assertEqual(result["network_origin_proof"], "PASS")
        self.assertEqual(result["db_round_trip"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")

    def test_bound_tls_with_round_trip_still_requires_external_existence(self):
        result = admission_summary("BOUND_TLS", "PASS", round_trip_proven=True)
        self.assertEqual(result["db_round_trip"], "PASS")
        self.assertEqual(result["promotion"], "DENY")
        # DB existence remains external evidence; this module cannot infer it.

    def test_unsafe_binding_denies_tls_and_promotion(self):
        result = admission_summary("DENY_TLS", "PASS", round_trip_proven=True)
        self.assertEqual(result["db_tls_admission"], "DENY")
        self.assertEqual(result["network_origin_proof"], "PASS")
        self.assertEqual(result["promotion"], "DENY")


if __name__ == "__main__":
    unittest.main()
