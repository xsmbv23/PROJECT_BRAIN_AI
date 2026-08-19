import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.source_provenance_capture import _safe_source_identity, write_receipt


class SourceProvenanceTests(unittest.TestCase):
    def test_identity_does_not_claim_independence(self):
        with patch("tools.source_provenance_capture.socket.getaddrinfo", return_value=[]):
            identity = _safe_source_identity("https://ketqua16.net/xsmb")
        self.assertEqual(identity["hostname"], "ketqua16.net")
        self.assertEqual(identity["resolved_ips"], [])

    def test_receipt_writer_does_not_persist_credential_marker(self):
        receipt = {
            "source_id": "test",
            "raw_sha256": "abc",
            "credentials_present": True,
            "independence_status": "NOT_PROVEN",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "receipt.json"
            write_receipt(receipt, str(path))
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("credentials_present", text)
            self.assertIn("NOT_PROVEN", text)


if __name__ == "__main__":
    unittest.main()
