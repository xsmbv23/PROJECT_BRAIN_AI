import unittest

from tools.evidence_lineage_validator import validate_evidence
from tools.lineage_bridge import source_evidence_from_network_receipt


class LineageBridgeTests(unittest.TestCase):
    def test_network_receipt_maps_to_canonical_source_evidence(self):
        receipt = {
            "url": "https://ketqua16.net/",
            "capture_timestamp_utc": "2026-08-21T00:00:00Z",
            "response_sha256": "raw-response-sha",
        }
        evidence = source_evidence_from_network_receipt(receipt, producer_component="n104c1_transport_inspection")
        self.assertEqual(validate_evidence(evidence)["status"], "PASS")
        self.assertEqual(evidence["raw_artifact_sha256"], "raw-response-sha")
        self.assertFalse(evidence["derived"])

    def test_incomplete_network_receipt_denied(self):
        with self.assertRaisesRegex(ValueError, "NETWORK_RECEIPT_LINEAGE_INCOMPLETE"):
            source_evidence_from_network_receipt({"url": "https://ketqua16.net/"}, producer_component="n104c1_transport_inspection")


if __name__ == "__main__":
    unittest.main()
