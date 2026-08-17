import unittest

from tools.verify_database_admission_chain import verify


class DatabaseAdmissionChainTests(unittest.TestCase):
    def test_contract_is_strict(self):
        result = verify()
        self.assertEqual(result["database_admission_contract"], "PASS")
        self.assertTrue(result["single_forensic_state"])
        self.assertTrue(result["non_inheritable_pass"])
        self.assertTrue(result["stop_on_first_failure"])
        self.assertEqual(result["failure_history"], "IMMUTABLE")
        self.assertFalse(result["credential_values_emitted"])
        self.assertEqual(result["render_memory_guard_bytes"], 320 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
