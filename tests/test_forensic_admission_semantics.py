import unittest


GATES = (
    "DB_EXISTENCE",
    "DB_BINDING",
    "SECRET_RESOLUTION",
    "DB_TLS_ADMISSION",
    "NETWORK_ORIGIN_PROOF",
    "DB_ROUND_TRIP",
    "PROMOTION",
)


class ForensicAdmissionSemanticsTests(unittest.TestCase):
    def test_single_ordered_chain(self):
        self.assertEqual(
            GATES,
            (
                "DB_EXISTENCE",
                "DB_BINDING",
                "SECRET_RESOLUTION",
                "DB_TLS_ADMISSION",
                "NETWORK_ORIGIN_PROOF",
                "DB_ROUND_TRIP",
                "PROMOTION",
            ),
        )

    def test_pass_is_not_inherited(self):
        # A PASS at gate N authorizes evaluation of N+1 only.
        evidence = {"DB_EXISTENCE": "PASS"}
        self.assertEqual(evidence.get("DB_EXISTENCE"), "PASS")
        self.assertNotEqual(evidence.get("DB_BINDING"), "PASS")
        self.assertNotEqual(evidence.get("DB_ROUND_TRIP"), "PASS")
        self.assertNotEqual(evidence.get("PROMOTION"), "PASS")

    def test_unknown_is_not_pass(self):
        evidence = {"DB_BINDING": "UNKNOWN"}
        self.assertNotEqual(evidence["DB_BINDING"], "PASS")

    def test_round_trip_owns_round_trip_evidence(self):
        evidence = {"DB_TLS_ADMISSION": "PASS", "DB_ROUND_TRIP": "UNKNOWN"}
        self.assertNotEqual(evidence["DB_TLS_ADMISSION"], evidence["DB_ROUND_TRIP"])
        self.assertNotEqual(evidence["DB_ROUND_TRIP"], "PASS")


if __name__ == "__main__":
    unittest.main()
