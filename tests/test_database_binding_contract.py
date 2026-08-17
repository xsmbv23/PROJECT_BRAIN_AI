import unittest

from tools.verify_database_binding_contract import verify


class DatabaseBindingContractTests(unittest.TestCase):
    def test_contract_is_valid(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["contract_id"], "RENDER_DB_BINDING_V1")


if __name__ == "__main__":
    unittest.main()
