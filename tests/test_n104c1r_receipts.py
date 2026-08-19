import unittest

from tools.validate_n104c1r_receipts import reconcile, validate_network_origin, validate_state_drift


class N104C1RReceiptTests(unittest.TestCase):
    def test_missing_receipt_is_not_pass(self):
        result = reconcile({}, {})
        self.assertEqual(result["reconciliation"], "MISMATCH")
        self.assertEqual(result["promotion"], "DENY")

    def test_network_requires_tls_and_hashes(self):
        receipt = {
            "source": "ketqua16.net",
            "resolved_ip": "203.0.113.1",
            "tls_version": "TLSv1.3",
            "certificate_sha256": "a" * 64,
            "http_status": 200,
            "response_sha256": "b" * 64,
            "timestamp_utc": "2026-08-20T00:00:00Z",
        }
        self.assertEqual(validate_network_origin(receipt), [])

    def test_state_drift_requires_exact_match(self):
        receipt = {
            "repo": {"last_action": "A", "next_action": "B", "state_mode": "DATA_ADMISSION"},
            "runtime": {"last_action": "A", "next_action": "B", "state_mode": "DATA_ADMISSION"},
            "match": True,
            "timestamp_utc": "2026-08-20T00:00:00Z",
        }
        self.assertEqual(validate_state_drift(receipt), [])

    def test_gate_pass_does_not_inherit(self):
        network = {
            "source": "ketqua16.net",
            "resolved_ip": "203.0.113.1",
            "tls_version": "TLSv1.3",
            "certificate_sha256": "a" * 64,
            "http_status": 200,
            "response_sha256": "b" * 64,
            "timestamp_utc": "2026-08-20T00:00:00Z",
        }
        drift = {
            "repo": {"last_action": "A"},
            "runtime": {"last_action": "A"},
            "match": True,
            "timestamp_utc": "2026-08-20T00:00:00Z",
        }
        result = reconcile(network, drift)
        self.assertEqual(result["reconciliation"], "MATCH")
        self.assertEqual(result["promotion"], "ADMIT")


if __name__ == "__main__":
    unittest.main()
