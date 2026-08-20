import copy
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

    def test_raw_artifact_requires_raw_sha256(self):
        result = validate_evidence(self.base() | {"raw_artifact_exists": True})
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "RAW_ARTIFACT_SHA256_MISSING")

    def test_semantic_quorum_requires_semantic_fingerprint(self):
        result = validate_evidence(self.base() | {"semantic_quorum": True})
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "SEMANTIC_FINGERPRINT_MISSING")

    def test_raw_and_semantic_identity_are_not_conflated(self):
        evidence = self.base() | {
            "raw_artifact_sha256": "raw-bytes",
            "semantic_fingerprint": "meaning",
            "semantic_quorum": True,
        }
        self.assertEqual(validate_evidence(evidence)["status"], "PASS")

    def test_same_value_for_raw_and_semantic_hash_denies_without_explicit_distinction(self):
        evidence = self.base() | {
            "raw_artifact_sha256": "same",
            "semantic_fingerprint": "same",
        }
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "RAW_AND_SEMANTIC_HASH_CONFLATED")

    def test_legacy_alias_requires_explicit_fixture(self):
        evidence = self.base() | {
            "raw_artifact_exists": True,
            "raw_sha256": "legacy-raw",
        }
        result = validate_evidence(evidence)
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "LEGACY_ALIAS_REQUIRES_EXPLICIT_FIXTURE")

    def test_legacy_fixture_can_be_read_without_becoming_canonical(self):
        evidence = self.base() | {
            "raw_artifact_exists": True,
            "raw_sha256": "legacy-raw",
            "legacy_fixture": True,
        }
        self.assertEqual(validate_evidence(evidence)["status"], "PASS")

    def test_canonical_field_wins_over_legacy_alias(self):
        evidence = self.base() | {
            "raw_artifact_exists": True,
            "raw_artifact_sha256": "canonical",
            "raw_sha256": "legacy",
        }
        self.assertEqual(validate_evidence(evidence)["status"], "PASS")

    def test_validator_does_not_mutate_evidence(self):
        evidence = self.base() | {
            "derived": True,
            "upstream_evidence_ids": ["E1"],
            "derivation_contract": "DERIVATION_V1",
        }
        before = copy.deepcopy(evidence)
        validate_evidence(evidence)
        self.assertEqual(evidence, before)
