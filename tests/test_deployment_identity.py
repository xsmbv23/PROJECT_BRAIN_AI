import unittest

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


if __name__ == "__main__":
    unittest.main()
