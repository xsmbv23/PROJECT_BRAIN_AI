import unittest

from tools.verify_admission_fsm import verify


class AdmissionFSMTests(unittest.TestCase):
    def test_fsm_contract_is_forensic_safe(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["states"], 5)
        self.assertEqual(result["external_event_path"], "ISOLATED")
        self.assertEqual(result["room_02"], "LOCKED")
        self.assertEqual(result["promotion"], "DENY_UNTIL_FRESH_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
