import unittest

from tools.origin_metadata_probe import DECLARED_SOURCES, probe_origin


class OriginMetadataProbeTests(unittest.TestCase):
    def test_declared_sources_are_https(self):
        self.assertEqual(len(DECLARED_SOURCES), 2)
        self.assertTrue(all(url.startswith("https://") for url in DECLARED_SOURCES))

    def test_probe_never_downloads_payload(self):
        receipt = probe_origin("https://example.com")
        self.assertFalse(receipt.payload_downloaded)
        self.assertEqual(receipt.payload_hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertEqual(receipt.canonical_identity, "DENY_UNPROVEN")

    def test_requested_host_is_preserved(self):
        receipt = probe_origin("https://example.com")
        self.assertEqual(receipt.requested_host, "example.com")


if __name__ == "__main__":
    unittest.main()
