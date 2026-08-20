import unittest

from tools.evidence_lineage_validator import validate_evidence


class EvidenceLineageValidatorTests(unittest.TestCase):
    def base(self):
        return {
            "source_identity": "ketqua16.net",
            "observation_timestamp": "2026-08-21T00:00:00Z",
            "observation_origin": "external_source",
        }

    def test_minimal_source_evidence_passes(self):
        self.assertEqual(validate_evidence(self.base())["status"], "PASS")

    def test_missing_source_provenance_denies(self):
        evidence = self.base()
        del evidence["observation_origin"]
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "REQUIRED_PROVENANCE_MISSING")

    def test_derived_source_truth_masquerade_denies(self):
        evidence = self.base() | {"authority": "source_truth", "derived": True}
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "DERIVED_CANNOT_BE_SOURCE_TRUTH")

    def test_local_receipt_cannot_claim_external_independence(self):
        evidence = self.base() | {"observation_origin": "local_receipt", "independent_external": True}
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "LOCAL_RECEIPT_CANNOT_BE_INDEPENDENT_EXTERNAL_OBSERVATION")

    def test_derived_evidence_requires_upstream_lineage(self):
        evidence = self.base() | {"derived": True}
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "DERIVED_PROVENANCE_MISSING")

    def test_runtime_admission_requires_runtime_identity_and_gate_evidence(self):
        evidence = self.base() | {"runtime_admission": True}
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "RUNTIME_ADMISSION_PROVENANCE_MISSING")

    def test_canonical_promotion_requires_payload_hash(self):
        evidence = self.base() | {"promoted_canonical": True}
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "CANONICAL_PROVENANCE_MISSING")
