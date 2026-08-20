import os
import unittest
from unittest.mock import patch

from brain.server import _deployment_identity
from tools.verify_deployment_identity import verify


class DeploymentIdentityTests(unittest.TestCase):
    def test_missing_identity_denies(self):
        self.assertEqual(verify("", "abc")["status"], "DENY")
        self.assertEqual(verify("abc", "")["status"], "DENY")

    def test_stale_runtime_denies(self):
        result = verify("canonical", "stale")
        self.assertEqual(result["status"], "DENY")
        self.assertEqual(result["reason"], "DEPLOYMENT_DRIFT")

    def test_exact_runtime_passes(self):
        result = verify("canonical", "canonical")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["reason"], "EXACT_CURRENT_COMMIT")

    def test_instance_id_never_falls_back_to_deployment_identity(self):
        with patch.dict(
            os.environ,
            {"RENDER_DEPLOY_ID": "", "RENDER_INSTANCE_ID": "instance-only"},
            clear=False,
        ):
            deployment, identity_type = _deployment_identity()
        self.assertEqual(deployment, "")
        self.assertEqual(identity_type, "NONE")

    def test_deploy_id_is_authoritative_over_instance_id(self):
        with patch.dict(
            os.environ,
            {"RENDER_DEPLOY_ID": "deploy-123", "RENDER_INSTANCE_ID": "instance-456"},
            clear=False,
        ):
            deployment, identity_type = _deployment_identity()
        self.assertEqual(deployment, "deploy-123")
        self.assertEqual(identity_type, "RENDER_DEPLOY_ID")


if __name__ == "__main__":
    unittest.main()
