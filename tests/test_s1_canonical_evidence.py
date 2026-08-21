import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from tools.verify_s1_canonical_evidence import verify_manifest


class S1CanonicalEvidenceTests(unittest.TestCase):
    def _manifest(self, root: Path, artifact: Path, **overrides):
        raw_hash = sha256(artifact.read_bytes()).hexdigest()
        data = {
            "source_provenance": {
                "classification": "REAL_AND_TRACEABLE",
                "source": "TEST_ONLY",
                "operator_identity": "TEST_SUITE",
                "authorization_reference": "TEST_SUITE_AUTHORIZED_CAPTURE",
            },
            "acquisition_channel": "MANUAL_AUTHORIZED_CAPTURE",
            "acquisition_reference": "TEST_SUITE_AUTHORIZED_CAPTURE",
            "acquisition_timestamp_utc": "2026-08-12T10:00:00+00:00",
            "artifact_path": artifact.name,
            "raw_artifact_sha256": raw_hash,
            "raw_byte_sha256": raw_hash,
            "date_start": "2026-08-10",
            "date_end": "2026-08-12",
            "expected_consecutive_days": 3,
            "observed_consecutive_days": 3,
            "coverage_ratio": 1.0,
            "unresolved_conflicts": 0,
            "admission_receipt": {
                "receipt_id": "TEST-RECEIPT",
                "source": "TEST_ONLY",
                "observed_at": "2026-08-12T10:00:00+00:00",
                "event_type": "TEST_EXTERNAL_OBSERVATION",
                "synthetic": False,
            },
            "frozen_canonical_sha256": raw_hash,
            "synthetic_data": False,
        }
        data.update(overrides)
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return manifest

    def test_missing_manifest_denies(self):
        with tempfile.TemporaryDirectory() as td:
            result = verify_manifest(Path(td) / "missing.json")
            self.assertEqual(result["status"], "DENY")

    def test_authorized_complete_fixture_passes_unit_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "canonical.bin"
            artifact.write_bytes(b"TEST_ONLY_CANONICAL_ARTIFACT")
            result = verify_manifest(self._manifest(root, artifact))
            self.assertEqual(result["status"], "PASS")

    def test_wrong_artifact_hash_denies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "canonical.bin"
            artifact.write_bytes(b"TEST_ONLY_CANONICAL_ARTIFACT")
            result = verify_manifest(self._manifest(root, artifact, raw_artifact_sha256="0" * 64))
            self.assertEqual(result["status"], "DENY")
            self.assertIn("RAW_ARTIFACT_SHA256_MISMATCH", result["reasons"])

    def test_coverage_gap_denies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "canonical.bin"
            artifact.write_bytes(b"TEST_ONLY_CANONICAL_ARTIFACT")
            result = verify_manifest(self._manifest(root, artifact, coverage_ratio=0.99))
            self.assertEqual(result["status"], "DENY")
            self.assertIn("COVERAGE_NOT_1_0", result["reasons"])

    def test_synthetic_flag_denies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "canonical.bin"
            artifact.write_bytes(b"TEST_ONLY_CANONICAL_ARTIFACT")
            result = verify_manifest(self._manifest(root, artifact, synthetic_data=True))
            self.assertEqual(result["status"], "DENY")
            self.assertIn("SYNTHETIC_DATA_NOT_EXPLICITLY_FALSE", result["reasons"])


if __name__ == "__main__":
    unittest.main()
