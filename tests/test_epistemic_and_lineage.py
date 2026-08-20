import unittest

from core.epistemic_contract import EpistemicType, InvalidEvidenceError, validate_evidence_claim
from tools.validate_lineage import validate_lineage


class EpistemicContractTests(unittest.TestCase):
    def test_only_evidence_can_be_evidence(self):
        self.assertTrue(validate_evidence_claim(EpistemicType.EVIDENCE))
        for kind in EpistemicType:
            if kind is not EpistemicType.EVIDENCE:
                with self.assertRaises(InvalidEvidenceError):
                    validate_evidence_claim(kind)


class LineageTests(unittest.TestCase):
    def test_missing_link_is_hard_deny(self):
        result = validate_lineage({
            "prediction_id": "p1",
            "feature_snapshot_sha": "a" * 64,
            "canonical_sha": "b" * 64,
            "raw_receipt_sha": "",
        })
        self.assertEqual(result["status"], "NOT_PROVEN")
        self.assertEqual(result["execution"], "CANCEL")

    def test_malformed_hash_is_hard_deny(self):
        result = validate_lineage({
            "prediction_id": "p1",
            "feature_snapshot_sha": "short",
            "canonical_sha": "b" * 64,
            "raw_receipt_sha": "c" * 64,
        })
        self.assertEqual(result["status"], "NOT_PROVEN")
        self.assertEqual(result["execution"], "CANCEL")

    def test_complete_lineage_is_local_pass_only(self):
        result = validate_lineage({
            "prediction_id": "p1",
            "feature_snapshot_sha": "a" * 64,
            "canonical_sha": "b" * 64,
            "raw_receipt_sha": "c" * 64,
        })
        self.assertEqual(result["status"], "PROVEN_LINEAGE")
        self.assertEqual(result["execution"], "ELIGIBLE_FOR_NEXT_GATE")


if __name__ == "__main__":
    unittest.main()
