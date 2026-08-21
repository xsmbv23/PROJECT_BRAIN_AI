import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from tools.s1_admission_bridge import evaluate_s1


class S1AdmissionBridgeTests(unittest.TestCase):
    def test_missing_manifest_stays_terminal_deny(self):
        with tempfile.TemporaryDirectory() as td:
            result = evaluate_s1(Path(td) / "missing.json")
            self.assertEqual(result["status"], "DENY")
            self.assertEqual(result["downstream"], "S2_VALID_RESEARCH_UNREACHED")
            self.assertTrue(result["no_pass_inheritance"])

    def test_complete_test_manifest_only_unlocks_next_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "canonical.bin"
            artifact.write_bytes(b"TEST_ONLY")
            digest = sha256(artifact.read_bytes()).hexdigest()
            manifest = {
                "source_provenance": {"classification": "REAL_AND_TRACEABLE", "source": "TEST_ONLY"},
                "artifact_path": artifact.name,
                "raw_artifact_sha256": digest,
                "raw_byte_sha256": digest,
                "date_start": "2026-08-10",
                "date_end": "2026-08-12",
                "expected_consecutive_days": 3,
                "observed_consecutive_days": 3,
                "coverage_ratio": 1.0,
                "unresolved_conflicts": 0,
                "admission_receipt": {"receipt_id":"T","source":"TEST_ONLY","observed_at":"2026-08-12T10:00:00+00:00","event_type":"TEST","synthetic":False},
                "frozen_canonical_sha256": digest,
                "synthetic_data": False,
            }
            mp = root / "manifest.json"
            mp.write_text(json.dumps(manifest), encoding="utf-8")
            result = evaluate_s1(mp)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["downstream"], "S2_VALID_RESEARCH_EVALUABLE")
            self.assertEqual(result["promotion"], "NEXT_GATE_ONLY")


if __name__ == "__main__":
    unittest.main()
