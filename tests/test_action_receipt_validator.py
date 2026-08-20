import unittest

from tools.action_receipt_validator import expected_receipt_sha, validate_action_receipt


class ActionReceiptValidatorTests(unittest.TestCase):
    def make_receipt(self, action="N104C.1", commit="1b337d9e", status="HOLD"):
        receipt = {
            "action_id": action,
            "commit_sha": commit,
            "deployment_id": "deploy-123",
            "execution_nonce": "",
            "issued_at": "2026-08-20T19:00:00+00:00",
            "status": status,
            "evidence_type": "RUNTIME",
        }
        import hashlib
        seed = f"{action}|{commit}|deploy-123|{receipt['issued_at']}"
        receipt["execution_nonce"] = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        receipt["receipt_sha256"] = expected_receipt_sha(receipt)
        return receipt

    def state(self, last="N104C.1", nxt="N104C.1R"):
        return {"last_action_id": last, "next_action_id": nxt}

    def test_matching_state_runtime_and_receipt_pass(self):
        result = validate_action_receipt(self.make_receipt(), self.state(), {"commit_sha": "1b337d9e"})
        self.assertEqual(result["status"], "PASS")

    def test_missing_receipt_sha_denies(self):
        receipt = self.make_receipt()
        del receipt["receipt_sha256"]
        result = validate_action_receipt(receipt, self.state(), {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_SHA_MISMATCH")

    def test_action_mismatch_denies(self):
        result = validate_action_receipt(self.make_receipt(action="N999"), self.state(), {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_ACTION_MISMATCH")

    def test_runtime_commit_mismatch_denies(self):
        result = validate_action_receipt(self.make_receipt(), self.state(), {"commit_sha": "different"})
        self.assertEqual(result["reason"], "RUNTIME_COMMIT_MISMATCH")

    def test_missing_issued_at_denies(self):
        receipt = self.make_receipt()
        del receipt["issued_at"]
        receipt["receipt_sha256"] = expected_receipt_sha(receipt)
        result = validate_action_receipt(receipt, self.state(), {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_ISSUED_AT_MISSING")

    def test_nonce_mismatch_denies(self):
        receipt = self.make_receipt()
        receipt["execution_nonce"] = "wrong"
        receipt["receipt_sha256"] = expected_receipt_sha(receipt)
        result = validate_action_receipt(receipt, self.state(), {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "RECEIPT_NONCE_MISMATCH")

    def test_legacy_pointer_names_are_not_accepted(self):
        legacy = {"last_action": "N104C.1", "next_action": "N104C.1R"}
        result = validate_action_receipt(self.make_receipt(), legacy, {"commit_sha": "1b337d9e"})
        self.assertEqual(result["reason"], "STATE_POINTER_MISSING")


if __name__ == "__main__":
    unittest.main()
