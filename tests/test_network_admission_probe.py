import unittest
from unittest.mock import patch

from tools.network_admission_probe import probe


class NetworkAdmissionProbeTests(unittest.TestCase):
    def test_missing_binding_denies(self):
        self.assertEqual(probe(""), {"status": "NOT_BOUND"})

    def test_invalid_scheme_denies(self):
        self.assertEqual(probe("https://example.invalid/db"), {"status": "DENY_BINDING"})

    @patch("tools.network_admission_probe.socket.getaddrinfo")
    def test_dns_failure_is_network_deny(self, getaddrinfo):
        getaddrinfo.side_effect = OSError("hidden")
        result = probe("postgresql://u:p@example.invalid/db?sslmode=require")
        self.assertEqual(result["status"], "DENY_NETWORK_ORIGIN")
        self.assertEqual(result["dns"], "DENY")


if __name__ == "__main__":
    unittest.main()
