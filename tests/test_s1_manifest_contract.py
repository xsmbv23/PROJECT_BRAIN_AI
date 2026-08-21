import unittest

from tools.verify_s1_manifest_contract import verify


class S1ManifestContractTests(unittest.TestCase):
    def test_contract_pass_does_not_admit_data(self):
        result = verify()
        self.assertEqual(result["status"], "PASS_CONTRACT")
        self.assertEqual(result["s1_admission"], "NOT_PROVEN")
        self.assertEqual(result["promotion"], "DENY")


if __name__ == "__main__":
    unittest.main()
