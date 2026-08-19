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
        self.assertTrue(laws["state_transition_requires_own_gate_evidence"])
        self.assertTrue(laws["one_gate_cannot_set_another_gate_pass"])

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

    def test_database_gate_meanings_are_distinct(self):
        meanings = self.contract["database_gate_meanings"]
        self.assertNotEqual(meanings["DB_EXISTENCE"], meanings["DB_BINDING"])
        self.assertNotEqual(meanings["DB_BINDING"], meanings["DB_TLS_ADMISSION"])
        self.assertNotEqual(meanings["DB_TLS_ADMISSION"], meanings["DB_ROUND_TRIP"])
        self.assertNotEqual(meanings["DB_ROUND_TRIP"], meanings["PROMOTION"])

    def test_non_implication_is_explicit(self):
        items = set(self.contract["non_implication"])
        self.assertIn("DB_EXISTENCE(PASS) !=> DB_BINDING(PASS)", items)
        self.assertIn("DB_BINDING(PASS) !=> DB_TLS_ADMISSION(PASS)", items)
        self.assertIn("DB_TLS_ADMISSION(PASS) !=> DB_ROUND_TRIP(PASS)", items)
        self.assertIn("DB_ROUND_TRIP(PASS) !=> PROMOTION(PASS)", items)

    def test_source_chain_is_ordered(self):
        self.assertEqual(
            self.contract["source_admission_chain"],
            [
                "SOURCE_INDEPENDENCE",
                "NETWORK_ORIGIN_PROOF",
                "RESULT_TRANSPORT",
                "OFFICIAL_RESULT_PANEL",
                "CANDIDATE",
                "EXCEL_VS_WEB_MATCH",
                "CANONICAL_QUORUM",
                "TRUTH_ADMISSION",
            ],
        )

    def test_source_non_implication_is_explicit(self):
        items = set(self.contract["source_non_implication"])
        expected = [
            "SOURCE_INDEPENDENCE(PASS) !=> NETWORK_ORIGIN_PROOF(PASS)",
            "NETWORK_ORIGIN_PROOF(PASS) !=> RESULT_TRANSPORT(PASS)",
            "RESULT_TRANSPORT(PASS) !=> OFFICIAL_RESULT_PANEL(PASS)",
            "OFFICIAL_RESULT_PANEL(PASS) !=> CANDIDATE(PASS)",
            "CANDIDATE(PASS) !=> EXCEL_VS_WEB_MATCH(PASS)",
            "EXCEL_VS_WEB_MATCH(PASS) !=> CANONICAL_QUORUM(PASS)",
            "CANONICAL_QUORUM(PASS) !=> TRUTH_ADMISSION(PASS)",
        ]
        for item in expected:
            self.assertIn(item, items)

    def test_exact_runtime_substitution_is_forbidden(self):
        laws = self.contract["laws"]
        self.assertEqual(laws["local_substitution_for_exact_runtime"], "FORBIDDEN")
        self.assertEqual(laws["proxy_evidence"], "FORBIDDEN")

    def test_history_is_append_only(self):
        laws = self.contract["laws"]
        self.assertTrue(laws["historical_records_append_only"])
        self.assertTrue(laws["historical_deny_meaning_is_immutable"])

    def test_layer_one_and_staircase_remain_locked(self):
        layer = self.contract["layer_policy"]
        self.assertEqual(layer["layer_1"], "LOCKED")
        self.assertEqual(layer["staircase"], "LOCKED")


if __name__ == "__main__":
    unittest.main()
