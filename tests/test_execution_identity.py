import json
import unittest
from pathlib import Path

from tools.verify_execution_identity import canonical_without_execution_id

ROOT = Path(__file__).resolve().parents[1]


class ExecutionIdentityTests(unittest.TestCase):
    def test_requested_pair_is_fresh_and_distinct_from_legacy(self):
        doc = json.loads((ROOT / "state" / "execution_identity_manifest_N099.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["target_date"], "2026-08-12")
        self.assertNotEqual(doc["source_a"]["identity"], doc["historical_pair"]["source_a"])
        self.assertNotEqual(doc["source_b"]["identity"], doc["historical_pair"]["source_b"])

    def test_manifest_has_default_deny_capture(self):
        doc = json.loads((ROOT / "state" / "execution_identity_manifest_N099.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["capture_admission"], "DENY_UNTIL_NETWORK_ORIGIN_PROOF")
        self.assertEqual(doc["promotion"], "DENY")

    def test_canonicalization_is_deterministic(self):
        doc = json.loads((ROOT / "state" / "execution_identity_manifest_N099.json").read_text(encoding="utf-8"))
        self.assertEqual(canonical_without_execution_id(doc), canonical_without_execution_id(json.loads(json.dumps(doc))))


if __name__ == "__main__":
    unittest.main()
