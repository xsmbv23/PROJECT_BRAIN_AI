import json
import unittest
from pathlib import Path

from tools.state_reconciliation import reconcile

ROOT = Path(__file__).resolve().parents[1]


class StateReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        outer = json.loads((ROOT / "state" / "current_state.json").read_text(encoding="utf-8"))
        cls.state = json.loads(outer["content"])
        cls.expected_commit = cls.state.get("last_verified_runtime_commit") or cls.state.get("promotion_runtime_commit")

    def test_current_verified_commit_passes(self):
        result = reconcile(runtime_commit=self.expected_commit, deployment_id="new-deploy-id")
        self.assertEqual(result["state_consistency"], "VERIFIED")
        self.assertTrue(result["runtime_commit_match"])
        self.assertFalse(result["runtime_is_authority"])

    def test_wrong_runtime_commit_hard_denies(self):
        result = reconcile(runtime_commit="WRONG_COMMIT", deployment_id="whatever")
        self.assertEqual(result["state_consistency"], "HARD_DENY")
        self.assertFalse(result["runtime_commit_match"])

    def test_deployment_id_is_not_identity(self):
        result = reconcile(runtime_commit=self.expected_commit, deployment_id="different-but-valid-redeploy-id")
        self.assertEqual(result["state_consistency"], "VERIFIED")
        self.assertEqual(result["deployment_evidence"]["identity_rule"], "DEPLOYMENT_ID_IS_EVIDENCE_ONLY")


if __name__ == "__main__":
    unittest.main()
