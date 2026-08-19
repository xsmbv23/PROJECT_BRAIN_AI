import unittest
from unittest.mock import patch

from tools.transport_probe import MAX_BYTES, run_probe


class _Response:
    status = 200
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, n=-1):
        return b"x" * min(n, 1024)


class TransportProbeTests(unittest.TestCase):
    @patch("tools.transport_probe.urllib.request.urlopen", return_value=_Response())
    def test_bounded_200_probe_passes(self, _mock):
        receipt = run_probe()
        self.assertEqual(receipt.status_code, 200)
        self.assertFalse(receipt.truncated)
        self.assertEqual(receipt.bytes_read, 1024)
        self.assertEqual(receipt.verdict, "PASS")
        self.assertEqual(len(receipt.sha256), 64)

    def test_maximum_is_bounded(self):
        self.assertEqual(MAX_BYTES, 128 * 1024)


if __name__ == "__main__":
    unittest.main()
