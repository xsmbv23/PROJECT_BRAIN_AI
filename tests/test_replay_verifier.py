import unittest

from tools.replay_verifier import replay


class ReplayVerifierTests(unittest.TestCase):
    def test_replay_passes(self):
        result = replay()
        self.assertEqual(result["replay"], "PASS")
        self.assertTrue(all(result["assertions"].values()))

    def test_external_path_remains_frozen(self):
        result = replay()
        self.assertEqual(result["external_before"], result["external_after"])
        self.assertEqual(result["external_after"]["action_space"], 0)
        self.assertEqual(result["external_after"]["action"], "MANDATORY_NO_OP")

    def test_protected_rooms_remain_closed(self):
        result = replay()
        self.assertFalse(result["room_02_unlocked"])
        self.assertFalse(result["staircase_unlocked"])
        self.assertEqual(result["promotion"], "DENY")

    def test_negative_and_invalid_ev_are_denied(self):
        result = replay()
        self.assertEqual(result["ev_decisions"]["negative"], "DENY")
        self.assertEqual(result["ev_decisions"]["unknown"], "DENY")
        self.assertEqual(result["ev_decisions"]["nan"], "DENY")
        self.assertEqual(result["ev_decisions"]["infinite"], "DENY")
        self.assertEqual(result["ev_decisions"]["zero"], "NOT_SUFFICIENT")

    def test_contract_hash_is_deterministic(self):
        result = replay()
        self.assertEqual(result["contract_hash"], result["contract_hash_repeat"])


if __name__ == "__main__":
    unittest.main()
