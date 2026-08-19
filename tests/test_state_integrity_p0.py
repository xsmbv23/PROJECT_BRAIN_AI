import unittest

from tools.state_reconciliation import _semantic_errors


class StateIntegrityP0Tests(unittest.TestCase):
    def base(self):
        return {
            "state_mode": "DATA_ADMISSION",
            "state": "SOURCE_PROVENANCE_CAPTURE",
            "action_space": 1,
            "action": "RUNTIME_PROVENANCE_EXECUTION",
            "promotion": "PASS_TO_ROOM_01_ONLY;CANONICAL_QUORUM_DENY",
            "layer_1": "ROOM_01_DATA_ADMISSION",
            "staircase": "LOCKED",
            "pass_inheritance": False,
            "unknown_is_not_pass": True,
            "default_deny": True,
            "database_admission_chain": "ONE_FORENSIC_FSM",
            "database_gate_noninheritance": True,
            "database_promotion_requires_fresh_evidence": True,
        }

    def test_current_data_admission_state_is_valid(self):
        self.assertEqual(_semantic_errors(self.base()), [])

    def test_gate_pass_cannot_be_inherited(self):
        state = self.base()
        state["pass_inheritance"] = True
        self.assertIn("pass_inheritance must be false", _semantic_errors(state))

    def test_unknown_is_not_pass(self):
        state = self.base()
        state["unknown_is_not_pass"] = False
        self.assertIn("unknown_is_not_pass must be true", _semantic_errors(state))

    def test_data_admission_cannot_unlock_staircase(self):
        state = self.base()
        state["staircase"] = "UNLOCKED"
        self.assertIn("DATA_ADMISSION requires staircase LOCKED", _semantic_errors(state))

    def test_data_admission_cannot_expand_to_room_02(self):
        state = self.base()
        state["layer_1"] = "ROOM_02_EDGE_RESEARCH"
        self.assertIn("DATA_ADMISSION requires Room 01 only", _semantic_errors(state))

    def test_promotion_scope_is_local(self):
        state = self.base()
        state["promotion"] = "PASS_TO_ROOM_02"
        self.assertIn("DATA_ADMISSION promotion scope is invalid", _semantic_errors(state))

    def test_fresh_evidence_required(self):
        state = self.base()
        state["database_promotion_requires_fresh_evidence"] = False
        self.assertIn("database promotion must require fresh evidence", _semantic_errors(state))


if __name__ == "__main__":
    unittest.main()
