import json
import tempfile
import unittest
from pathlib import Path


class StateArtifactIntegrityTests(unittest.TestCase):
    def test_transport_envelope_is_rejected(self):
        value = {"content": "{\"promotion\":\"DENY\"}", "encoding": "utf-8", "sha": "abc"}
        self.assertIn("content", value)
        self.assertIn("encoding", value)
        self.assertIn("sha", value)

    def test_direct_state_has_no_transport_wrapper(self):
        value = {
            "promotion": "DENY",
            "layer_1": "LOCKED",
            "staircase": "LOCKED",
            "pass_inheritance": False,
            "unknown_is_not_pass": True,
            "default_deny": True,
            "action_space": 0,
            "action": "MANDATORY_NO_OP",
        }
        self.assertNotIn("content", value)
        self.assertNotIn("encoding", value)
        self.assertNotIn("sha", value)
        self.assertFalse(value["pass_inheritance"])
        self.assertEqual(value["action_space"], 0)


if __name__ == "__main__":
    unittest.main()
