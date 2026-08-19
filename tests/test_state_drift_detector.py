import unittest

from tools.state_drift_detector import detect_drift


class StateDriftDetectorTests(unittest.TestCase):
    def test_current_repository_state_has_no_structural_drift(self):
        result = detect_drift()
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertFalse(result["drift"])


if __name__ == "__main__":
    unittest.main()
