import hashlib
import json
import unittest

from tools.action_receipt_validator import expected_receipt_sha, validate_action_receipt


class ActionReceiptValidatorTests(unittest.TestCase):
    def make_receipt(self, action="N104C.1", commit="1b337d9e", status="HOLD"):
        receipt = {"action_id": action, "commit_sha": commit, "status": status, "evidence_type": "RUNTIME"}
        receipt["receipt_sha256"] = expected_receipt_sha(receipt)
        return receipt

    def test_matching_state_runtime_and_receipt_pass(self):
        state = {"last_action": "N104C.1", "next_action": "N104C.1R"}
        runtime = {"commit_sha": "1b337d9e"}
        result = validate_action_receipt(self.make_receipt(), state, runtime)
        self.assertEqual(result["status"], "PASS")

    def test_missing_receipt_sha_denies(self):
        receipt = self.make_receipt()
        del receipt["receipt_sha256"]
        result = validate_action_receipt(receipt, {"last_action": "N104C.1", "next_action": "N104C.1R"}, {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_SHA_MISMATCH")

    def test_action_mismatch_denies(self):
        result = validate_action_receipt(self.make_receipt(action="N999"), {"last_action": "N104C.1", "next_action": "N104C.1R"}, {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_ACTION_MISMATCH")

    def test_runtime_commit_mismatch_denies(self):
        result = validate_action_receipt(self.make_receipt(), {"last_action": "N104C.1", "next_action": "N104C.1R"}, {"commit_sha": "different"})
        self.assertEqual(result["reason"], "RUNTIME_COMMIT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
