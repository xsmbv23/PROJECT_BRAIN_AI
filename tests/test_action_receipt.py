import unittest
from datetime import datetime, timezone, timedelta

from core.action_receipt import verify_action_receipt


class ActionReceiptTests(unittest.TestCase):
    ACTION = "RUNTIME_PROVENANCE_EXECUTION"
    COMMIT = "c99d5df15ce9707dd6f6b5fcad912c78b2d9d9e2"
    DEPLOY = "dep-da3875u1egvs73c31abg"
    EVIDENCE = "00e321acf7d1624c1c7eb7234590dcc60f1d75ad15f1bfb1354aa8f09e26e701"
    NONCE = "n113-execution-01"
    NOW = datetime(2026, 8, 20, 4, 0, tzinfo=timezone.utc)

    def receipt(self, **overrides):
        value = {
            "receipt_version": "ACTION_RECEIPT_V1",
            "action_id": self.ACTION,
            "commit_sha": self.COMMIT,
            "deployment_id": self.DEPLOY,
            "execution_nonce": self.NONCE,
            "issued_at": self.NOW.isoformat(),
            "evidence_sha": self.EVIDENCE,
        }
        value.update(overrides)
        return value

    def test_missing_denied(self):
        self.assertEqual(verify_action_receipt(None, action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)["reason"], "ACTION_RECEIPT_MISSING")

    def test_wrong_commit_denied(self):
        result = verify_action_receipt(self.receipt(commit_sha="old"), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["reason"], "ACTION_RECEIPT_COMMIT_SHA_MISMATCH")

    def test_wrong_deployment_denied(self):
        result = verify_action_receipt(self.receipt(deployment_id="old-deploy"), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["reason"], "ACTION_RECEIPT_DEPLOYMENT_ID_MISMATCH")

    def test_wrong_action_denied(self):
        result = verify_action_receipt(self.receipt(action_id="OTHER"), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["reason"], "ACTION_RECEIPT_ACTION_ID_MISMATCH")

    def test_replay_nonce_mismatch_denied(self):
        result = verify_action_receipt(self.receipt(execution_nonce="replayed"), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["reason"], "ACTION_RECEIPT_EXECUTION_NONCE_MISMATCH")

    def test_stale_denied(self):
        result = verify_action_receipt(self.receipt(issued_at=(self.NOW - timedelta(seconds=901)).isoformat()), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["reason"], "ACTION_RECEIPT_STALE_OR_FUTURE")

    def test_exact_current_is_local_only(self):
        result = verify_action_receipt(self.receipt(), action_id=self.ACTION, commit_sha=self.COMMIT, deployment_id=self.DEPLOY, evidence_sha=self.EVIDENCE, execution_nonce=self.NONCE, now=self.NOW)
        self.assertEqual(result["status"], "PASS_LOCAL")
        self.assertTrue(result["pass_is_local"])
        self.assertFalse(result["promotes"])
        self.assertTrue(result["receipt_sha"])


if __name__ == "__main__":
    unittest.main()
