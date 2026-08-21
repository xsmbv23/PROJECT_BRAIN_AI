import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools.verify_s1_canonical_evidence import verify_manifest


class S1AcquisitionChannelTests(unittest.TestCase):
    def _manifest(self, root: Path, channel: str, provenance: dict) -> Path:
        artifact = root / "raw.bin"
        payload = b"real-evidence-fixture"
        artifact.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        manifest = {
            "source_provenance": {
                "classification": "REAL_AND_TRACEABLE",
                **provenance,
            },
            "acquisition_channel": channel,
            "acquisition_reference": provenance.get("permission_reference")
            or provenance.get("authorization_reference")
            or provenance.get("archive_identity")
            or "fixture-reference",
            "acquisition_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "artifact_path": "raw.bin",
            "raw_artifact_sha256": digest,
            "raw_byte_sha256": digest,
            "date_start": "2026-01-01",
            "date_end": "2026-01-03",
            "expected_consecutive_days": 3,
            "observed_consecutive_days": 3,
            "coverage_ratio": 1.0,
            "unresolved_conflicts": 0,
            "admission_receipt": {
                "receipt_id": "receipt-fixture",
                "source": "fixture-source",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "event_type": "S1_ADMISSION",
                "synthetic": False,
            },
            "frozen_canonical_sha256": digest,
            "synthetic_data": False,
        }
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def test_manual_authorized_capture_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self._manifest(
                root,
                "MANUAL_AUTHORIZED_CAPTURE",
                {
                    "operator_identity": "authorized-operator",
                    "authorization_reference": "AUTH-001",
                },
            )
            result = verify_manifest(path)
            self.assertEqual(result["status"], "PASS")

    def test_archive_export_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self._manifest(
                root,
                "DURABLE_ARCHIVE_EXPORT",
                {
                    "archive_identity": "archive-001",
                    "archive_provenance": "durable-archive-source",
                },
            )
            result = verify_manifest(path)
            self.assertEqual(result["status"], "PASS")

    def test_automated_source_requires_permission_and_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self._manifest(root, "AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION", {})
            result = verify_manifest(path)
            self.assertEqual(result["status"], "DENY")
            self.assertIn("AUTOMATED_PERMISSION_REFERENCE_MISSING", result["reasons"])
            self.assertIn("AUTOMATED_SOURCE_IDENTITY_MISSING", result["reasons"])


if __name__ == "__main__":
    unittest.main()
