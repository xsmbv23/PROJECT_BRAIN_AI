import unittest

from tools.quant_workflow_receipt_validator import validate_quant_workflow_receipt


class TestQuantWorkflowReceiptValidator(unittest.TestCase):
    def valid_receipt(self):
        return {
            "evidence_kind": "REPOSITORY_WORKFLOW_EXECUTION",
            "repository_execution": "PROVEN_AT_THIS_STEP",
            "external_runtime_truth": "NOT_PROVEN",
            "independent_external_observation": False,
            "commit_sha": "abc123",
            "workflow_run_id": "42",
            "workflow_run_attempt": "1",
            "receipt_generated_at": "2026-08-21T00:00:00+00:00",
        }

    def test_accepts_repository_execution_only(self):
        ok, errors = validate_quant_workflow_receipt(self.valid_receipt())
        self.assertTrue(ok)
        self.assertEqual(errors, [])

    def test_rejects_runtime_truth_claim(self):
        receipt = self.valid_receipt()
        receipt["external_runtime_truth"] = "PROVEN"
        ok, errors = validate_quant_workflow_receipt(receipt)
        self.assertFalse(ok)
        self.assertIn("DENY:external_runtime_truth_must_remain_not_proven", errors)

    def test_rejects_missing_execution_identity(self):
        receipt = self.valid_receipt()
        receipt["workflow_run_id"] = ""
        ok, errors = validate_quant_workflow_receipt(receipt)
        self.assertFalse(ok)
        self.assertIn("INVALID:workflow_run_id", errors)

    def test_rejects_independent_observation_claim(self):
        receipt = self.valid_receipt()
        receipt["independent_external_observation"] = True
        ok, errors = validate_quant_workflow_receipt(receipt)
        self.assertFalse(ok)
        self.assertIn("DENY:independent_external_observation_must_be_false", errors)


if __name__ == "__main__":
    unittest.main()
