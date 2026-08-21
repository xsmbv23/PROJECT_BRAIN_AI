import unittest

from tools.validate_multi_bot_handoff import validate


class MultiBotHandoffTests(unittest.TestCase):
    def valid(self, **overrides):
        payload = {
            "owner": "BOT_3",
            "action_id": "BOT3-E2E-001",
            "e2e_segment": "S2_VALID_RESEARCH",
            "blocker": "",
            "action": "Run bounded implementation test",
            "evidence_refs": ["commit:abc123"],
            "result": "IMPLEMENTED",
            "next_action": "Persist runtime receipt",
            "peer_impact": "Bot 1 reviews only if gate state changes",
            "challenge_status": "ACK",
        }
        payload.update(overrides)
        return payload

    def test_valid_handoff(self):
        ok, reasons = validate(self.valid())
        self.assertTrue(ok)
        self.assertEqual(reasons, [])

    def test_invalid_owner_denied(self):
        ok, reasons = validate(self.valid(owner="BOT_9"))
        self.assertFalse(ok)
        self.assertIn("OWNER_INVALID", reasons)

    def test_missing_evidence_list_denied(self):
        ok, reasons = validate(self.valid(evidence_refs="commit:abc123"))
        self.assertFalse(ok)
        self.assertIn("EVIDENCE_REFS_NOT_LIST", reasons)

    def test_unknown_challenge_is_allowed(self):
        ok, reasons = validate(self.valid(challenge_status="UNKNOWN"))
        self.assertTrue(ok)
        self.assertEqual(reasons, [])

    def test_invalid_segment_denied(self):
        ok, reasons = validate(self.valid(e2e_segment="NOT_A_SEGMENT"))
        self.assertFalse(ok)
        self.assertIn("E2E_SEGMENT_INVALID", reasons)


if __name__ == "__main__":
    unittest.main()
