import unittest

from tools.runtime_boot_gate import admission_summary


class NetworkGateLocalityTests(unittest.TestCase):
    def test_bound_tls_does_not_inherit_network_pass(self):
        result = admission_summary("BOUND_TLS", "DENY_NETWORK_ORIGIN", False)
        self.assertEqual(result["db_binding"], "BOUND_TLS")
        self.assertEqual(result["db_tls_admission"], "PASS")
        self.assertEqual(result["network_origin_proof"], "NOT_PROVEN")
        self.assertEqual(result["db_round_trip"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")

    def test_network_pass_is_still_not_round_trip_pass(self):
        result = admission_summary("BOUND_TLS", "PASS", False)
        self.assertEqual(result["network_origin_proof"], "PASS")
        self.assertEqual(result["db_round_trip"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")


if __name__ == "__main__":
    unittest.main()
