import unittest

from tools.validate_multi_bot_deliberation import validate


class MultiBotDeliberationTests(unittest.TestCase):
    def base(self):
        return {
            "deliberation_id": "D001",
            "proposer": "BOT3_EXECUTION",
            "reviewers": ["BOT1_LEAD", "BOT2_QUANT"],
            "e2e_segment": "S1",
            "blocker": "runtime drift",
            "proposal": "reconcile runtime identity before evidence admission",
            "evidence_refs": ["receipt-1"],
            "assumptions": ["runtime evidence is fresh"],
            "positions": {"BOT1_LEAD": "AGREE", "BOT2_QUANT": "CONDITIONAL"},
            "objections_and_replies": ["BOT2 requires exact deploy evidence"],
            "synthesized_decision": "EXECUTE_RECONCILIATION",
            "chosen_owner": "BOT3_EXECUTION",
            "safe_parallel_work": ["Bot2 audits data provenance"],
            "unresolved_questions": ["fresh runtime receipt availability"],
            "next_action": "capture fresh receipt",
        }

    def test_valid_record(self):
        self.assertEqual(validate(self.base()), [])

    def test_challenge_requires_objection(self):
        record = self.base()
        record["positions"]["BOT1_LEAD"] = "CHALLENGE"
        record["objections_and_replies"] = []
        self.assertIn("CHALLENGE_REQUIRES_OBJECTION", validate(record))

    def test_deliberation_cannot_promote(self):
        record = self.base()
        record["synthesized_decision"] = "PROMOTE"
        self.assertIn("DELIBERATION_CANNOT_GRANT_PROMOTION", validate(record))

    def test_unknown_is_valid_position(self):
        record = self.base()
        record["positions"]["BOT2_QUANT"] = "UNKNOWN"
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
