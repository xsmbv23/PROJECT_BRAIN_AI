import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/forensic/FORENSIC_GATE_SEMANTICS_V1.json"


class ForensicGateSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_pass_inheritance_is_forbidden(self):
        laws = self.contract["laws"]
        self.assertTrue(laws["pass_is_local"])
        self.assertTrue(laws["pass_is_prerequisite_only"])
        self.assertFalse(laws["pass_inheritance"])
        self.assertEqual(laws["pass_inheritance_policy"], "FORBIDDEN")

    def test_unknown_and_blocked_are_not_pass(self):
        laws = self.contract["laws"]
        self.assertTrue(laws["unknown_is_not_pass"])
        self.assertTrue(laws["blocked_is_valid_forensic_state"])
        self.assertTrue(laws["blocked_is_success_state"])

    def test_database_chain_is_ordered(self):
        self.assertEqual(
            self.contract["database_chain"],
            ["DB_EXISTENCE", "DB_BINDING", "DB_TLS_ADMISSION", "DB_ROUND_TRIP", "PROMOTION"],
        )

    def test_non_implication_is_explicit(self):
        items = set(self.contract["non_implication"])
        self.assertIn("DB_EXISTENCE(PASS) !=> DB_BINDING(PASS)", items)
        self.assertIn("DB_BINDING(PASS) !=> DB_ROUND_TRIP(PASS)", items)
        self.assertIn("DB_ROUND_TRIP(PASS) !=> PROMOTION(PASS)", items)

    def test_exact_runtime_substitution_is_forbidden(self):
        laws = self.contract["laws"]
        self.assertEqual(laws["local_substitution_for_exact_runtime"], "FORBIDDEN")
        self.assertEqual(laws["proxy_evidence"], "FORBIDDEN")

    def test_layer_one_and_staircase_remain_locked(self):
        layer = self.contract["layer_policy"]
        self.assertEqual(layer["layer_1"], "LOCKED")
        self.assertEqual(layer["staircase"], "LOCKED")


if __name__ == "__main__":
    unittest.main()
