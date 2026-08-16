import unittest

from core.foundation_gate import run_foundation_gate


class FoundationGateTests(unittest.TestCase):
    def test_foundation_gate_passes_bounded_metadata(self):
        result = run_foundation_gate()
        self.assertEqual(result["status"], "PASS")
        self.assertNotEqual(result["audit_head"], "GENESIS")
        self.assertTrue(result["checks"])


if __name__ == "__main__":
    unittest.main()
