import json
import unittest
from pathlib import Path

from tools.state_reconciliation import reconcile

ROOT = Path(__file__).resolve().parents[1]


class StateReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = json.loads((ROOT / "state" / "current_state.json").read_text(encoding="utf-8"))
        cls.expected_commit = cls.state.get("last_verified_runtime_commit") or cls.state.get("promotion_runtime_commit")

    def test_current_verified_commit_passes_only_when_verified_pointer_exists(self):
        result = reconcile(runtime_commit=self.expected_commit, deployment_id="new-deploy-id")
        if self.expected_commit in (None, "", "UNKNOWN"):
            self.assertEqual(result["state_consistency"], "HARD_DENY")
            self.assertFalse(result["runtime_commit_same_as_last_verified"])
        else:
            self.assertEqual(result["state_consistency"], "VERIFIED")
            self.assertTrue(result["runtime_commit_same_as_last_verified"])
        self.assertFalse(result["runtime_is_authority"])

    def test_new_runtime_commit_requires_hard_deny_without_verified_authority(self):
        result = reconcile(runtime_commit="NEW_RUNTIME_COMMIT", deployment_id="new-deploy-id")
        self.assertEqual(result["state_consistency"], "HARD_DENY")
        self.assertFalse(result["runtime_commit_same_as_last_verified"])

    def test_deployment_id_is_not_identity(self):
        result = reconcile(runtime_commit=self.expected_commit, deployment_id="different-but-valid-redeploy-id")
        if self.expected_commit in (None, "", "UNKNOWN"):
            self.assertEqual(result["state_consistency"], "HARD_DENY")
        else:
            self.assertEqual(result["state_consistency"], "VERIFIED")
        self.assertEqual(result["deployment_evidence"]["identity_rule"], "DEPLOYMENT_ID_IS_EVIDENCE_ONLY")


if __name__ == "__main__":
    unittest.main()
