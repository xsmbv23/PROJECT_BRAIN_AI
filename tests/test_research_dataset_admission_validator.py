import unittest

from tools.research_dataset_admission_validator import validate_research_dataset_receipt


BASE = {
    "dataset_identity": "dataset-1",
    "source_provenance_reference": "prov-1",
    "canonical_input_reference": "full27-1",
    "temporal_evidence_reference": "temporal-1",
    "date_manifest_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "start_date": "2026-01-01",
    "end_date": "2026-02-10",
    "actual_days": 41,
    "required_days": 41,
    "contiguous": True,
    "missing_days": [],
    "train_observations": 20,
    "test_observations": 20,
    "temporal_policy": "DATE_ALIGNED_NO_LOOKAHEAD",
    "code_version": "abc123",
}


class ResearchDatasetAdmissionValidatorTests(unittest.TestCase):
    def test_valid_receipt_is_research_only(self):
        result = validate_research_dataset_receipt(BASE)
        self.assertEqual(result["status"], "ADMITTED")
        self.assertEqual(result["edge"], "NOT_PROVEN")
        self.assertEqual(result["ev_pnl"], "NOT_PROVEN")
        self.assertEqual(result["action"], "NOT_AUTHORIZED")

    def test_gap_denied(self):
        receipt = {**BASE, "contiguous": False, "missing_days": ["2026-01-08"]}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_short_history_denied(self):
        receipt = {**BASE, "actual_days": 40}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_required_history_cannot_be_lowered(self):
        receipt = {**BASE, "required_days": 1, "actual_days": 1}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_required_history_must_match_oos_split(self):
        receipt = {**BASE, "required_days": 42}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_date_span_must_match_actual_days(self):
        receipt = {**BASE, "end_date": "2026-02-11", "actual_days": 41}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_reversed_date_range_denied(self):
        receipt = {**BASE, "start_date": "2026-02-11"}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_empty_provenance_denied(self):
        receipt = {**BASE, "source_provenance_reference": ""}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_invalid_date_denied(self):
        receipt = {**BASE, "start_date": "not-a-date"}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_invalid_manifest_hash_denied(self):
        receipt = {**BASE, "date_manifest_sha256": "not-a-sha256"}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_lookahead_policy_denied(self):
        receipt = {**BASE, "temporal_policy": "POSITIONAL_LAG"}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_missing_field_denied(self):
        receipt = dict(BASE)
        del receipt["canonical_input_reference"]
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")


if __name__ == "__main__":
    unittest.main()
