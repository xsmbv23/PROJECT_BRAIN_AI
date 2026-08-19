import unittest

from tools.canonical_identity_probe import MAX_DOCUMENT_BYTES, probe_identity


class CanonicalIdentityProbeTests(unittest.TestCase):
    def test_document_window_is_bounded(self):
        self.assertLessEqual(MAX_DOCUMENT_BYTES, 262144)

    def test_identity_probe_never_reports_full_payload(self):
        receipt = probe_identity("https://example.com")
        self.assertLessEqual(receipt.response_bytes_observed, MAX_DOCUMENT_BYTES)
        self.assertTrue(receipt.bounded_window_sha256)

    def test_hostname_alone_cannot_pass_identity(self):
        receipt = probe_identity("https://example.com")
        self.assertNotEqual(receipt.identity_decision, "PASS")


if __name__ == "__main__":
    unittest.main()
