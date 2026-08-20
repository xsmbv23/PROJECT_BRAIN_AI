import unittest

from tools.research_dataset_admission_validator import validate_research_dataset_receipt


BASE = {
    "dataset_identity": "dataset-1",
    "source_provenance_reference": "prov-1",
    "canonical_input_reference": "full27-1",
    "temporal_evidence_reference": "temporal-1",
    "date_manifest_sha256": "a" * 64,
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


class ResearchTemporalEvidenceTests(unittest.TestCase):
    def test_temporal_evidence_reference_required(self):
        receipt = dict(BASE)
        del receipt["temporal_evidence_reference"]
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_date_manifest_hash_required(self):
        receipt = dict(BASE)
        del receipt["date_manifest_sha256"]
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_date_manifest_hash_must_be_sha256(self):
        receipt = {**BASE, "date_manifest_sha256": "not-a-sha256"}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")

    def test_temporal_evidence_reference_must_be_nonempty(self):
        receipt = {**BASE, "temporal_evidence_reference": ""}
        self.assertEqual(validate_research_dataset_receipt(receipt)["status"], "DENY")


if __name__ == "__main__":
    unittest.main()
