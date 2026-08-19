import unittest

from tools.state_reconciliation_admission import evaluate_admission


class StateReconciliationAdmissionTests(unittest.TestCase):
    def test_missing_projection_cannot_promote(self):
        result = evaluate_admission(runtime_commit="UNKNOWN", deployment_id="unknown", quant_projection=None)
        self.assertEqual(result["decision"], "RECONCILE_REQUIRED")
        self.assertFalse(result["promotion_allowed"])
        self.assertEqual(result["quant_projection"], "NOT_PROVEN")

    def test_runtime_version_drift_is_not_logical_state_authority(self):
        result = evaluate_admission(runtime_commit="new-runtime", deployment_id="dep-new", quant_projection={"projection": "receipt"})
        self.assertEqual(result["decision"], "RECONCILE_REQUIRED")
        self.assertFalse(result["promotion_allowed"])
        self.assertFalse(result["runtime_is_authority"])
        self.assertFalse(result["projection_is_authority"])


if __name__ == "__main__":
    unittest.main()
