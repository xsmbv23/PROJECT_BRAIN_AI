import unittest
from unittest.mock import patch

from brain.server import _governance_payload


class GovernanceEnvelopeTests(unittest.TestCase):
    def test_governance_exposes_canonical_admission_state(self):
        with patch("brain.server.classify_database_binding", return_value={"status": "BOUND_TLS", "tls": "PASS"}), patch(
            "brain.server._current_action_receipt_evidence",
            return_value={"status": "DENY", "reason": "ACTION_RECEIPT_MISSING", "pass_is_local": True, "promotes": False},
        ):
            payload = _governance_payload()

        self.assertEqual(payload["forensic_fsm"], "ONE_FORENSIC_FSM")
        self.assertEqual(payload["action_space"], 0)
        self.assertEqual(payload["action"], "MANDATORY_NO_OP")
        self.assertEqual(payload["promotion"], "DENY")
        self.assertEqual(payload["layer_1"], "LOCKED")
        self.assertEqual(payload["room_02"], "LOCKED")
        self.assertEqual(payload["staircase"], "LOCKED")
        self.assertTrue(payload["next_action_id"])


if __name__ == "__main__":
    unittest.main()
