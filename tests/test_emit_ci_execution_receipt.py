import unittest

from tools.emit_ci_execution_receipt import build_receipt


class TestCiExecutionReceipt(unittest.TestCase):
    def test_repository_execution_is_explicitly_non_promotional(self):
        receipt = build_receipt(
            {
                "GITHUB_SHA": "abc123",
                "GITHUB_RUN_ID": "42",
                "GITHUB_RUN_ATTEMPT": "1",
                "GITHUB_RUN_STARTED_AT": "2026-08-21T00:00:00Z",
            }
        )
        self.assertEqual(receipt["evidence_kind"], "REPOSITORY_WORKFLOW_EXECUTION")
        self.assertEqual(receipt["repository_execution"], "PROVEN_AT_THIS_STEP")
        self.assertEqual(receipt["external_runtime_truth"], "NOT_PROVEN")
        self.assertFalse(receipt["independent_external_observation"])

    def test_missing_execution_identity_is_not_hidden(self):
        receipt = build_receipt({})
        self.assertEqual(receipt["commit_sha"], "")
        self.assertEqual(receipt["workflow_run_id"], "")
        self.assertEqual(receipt["external_runtime_truth"], "NOT_PROVEN")


if __name__ == "__main__":
    unittest.main()
