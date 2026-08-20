import unittest
from datetime import date

from core.epistemic_contract import EpistemicType, InvalidEvidenceError
from core.runtime_admission import admit_evidence, admit_prediction


VALID = {
    "prediction_id": "P-001",
    "feature_snapshot_sha": "a" * 64,
    "canonical_sha": "b" * 64,
    "raw_receipt_sha": "c" * 64,
}


class RuntimeAdmissionTests(unittest.TestCase):
    def test_only_evidence_can_satisfy_evidence_claim(self):
        with self.assertRaises(InvalidEvidenceError):
            admit_evidence(gate="G1", source_type=EpistemicType.HYPOTHESIS)

    def test_gate_pass_is_local(self):
        result = admit_evidence(gate="G1", source_type=EpistemicType.EVIDENCE)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["pass_is_local"])
        self.assertFalse(result["promotes"])

    def test_missing_lineage_cancels_execution(self):
        result = admit_prediction({}, feature_input_date=date(2026, 8, 19), prediction_date=date(2026, 8, 20), prediction_frozen=True, result_revealed=False)
        self.assertEqual(result["status"], "NOT_PROVEN")
        self.assertEqual(result["execution"], "CANCEL")

    def test_future_feature_input_is_temporal_violation(self):
        result = admit_prediction(VALID, feature_input_date=date(2026, 8, 20), prediction_date=date(2026, 8, 20), prediction_frozen=True, result_revealed=False)
        self.assertEqual(result["status"], "TEMPORAL_VIOLATION")
        self.assertEqual(result["execution"], "CANCEL")

    def test_prediction_must_freeze_before_result_reveal(self):
        result = admit_prediction(VALID, feature_input_date=date(2026, 8, 19), prediction_date=date(2026, 8, 20), prediction_frozen=False, result_revealed=True)
        self.assertEqual(result["status"], "NOT_PROVEN")
        self.assertEqual(result["execution"], "CANCEL")

    def test_valid_lineage_is_only_next_gate_eligible(self):
        result = admit_prediction(VALID, feature_input_date=date(2026, 8, 19), prediction_date=date(2026, 8, 20), prediction_frozen=True, result_revealed=False)
        self.assertEqual(result["status"], "PROVEN_LINEAGE")
        self.assertEqual(result["execution"], "ELIGIBLE_FOR_NEXT_GATE")
        self.assertFalse(result["promotes"])


if __name__ == "__main__":
    unittest.main()
