import unittest
from unittest.mock import patch

from tools.network_evidence_collector import CHUNK_SIZE, collect


class NetworkEvidenceCollectorTests(unittest.TestCase):
    def test_chunk_size_is_render_safe(self):
        self.assertEqual(CHUNK_SIZE, 64 * 1024)

    def test_http_is_denied_before_network(self):
        with self.assertRaisesRegex(RuntimeError, "HTTPS URL required"):
            collect("http://example.invalid")

    def test_empty_host_is_denied(self):
        with self.assertRaisesRegex(RuntimeError, "HTTPS URL required"):
            collect("https://")

    def test_resolver_failure_is_fail_closed(self):
        with patch("tools.network_evidence_collector._resolve_ip", side_effect=RuntimeError("resolver fail")):
            with self.assertRaisesRegex(RuntimeError, "resolver fail"):
                collect("https://example.invalid")


if __name__ == "__main__":
    unittest.main()
