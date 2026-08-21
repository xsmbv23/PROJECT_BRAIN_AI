import json
import tempfile
import unittest
from pathlib import Path
from tools.verify_successor_pointer_consistency import verify


class SuccessorPointerConsistencyTests(unittest.TestCase):
    def test_matching_pointers_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            import tools.verify_successor_pointer_consistency as mod
            old_current, old_next = mod.CURRENT, mod.NEXT
            try:
                mod.CURRENT = root / "current.json"
                mod.NEXT = root / "next.json"
                mod.CURRENT.write_text(json.dumps({"last_action_id":"BRAIN-N163","next_action_id":"BRAIN-N164"}), encoding="utf-8")
                mod.NEXT.write_text(json.dumps({"action_id":"BRAIN-N164"}), encoding="utf-8")
                result = verify()
                self.assertEqual(result["status"], "PASS")
            finally:
                mod.CURRENT, mod.NEXT = old_current, old_next

    def test_mismatch_denies_without_guessing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            import tools.verify_successor_pointer_consistency as mod
            old_current, old_next = mod.CURRENT, mod.NEXT
            try:
                mod.CURRENT = root / "current.json"
                mod.NEXT = root / "next.json"
                mod.CURRENT.write_text(json.dumps({"last_action_id":"BRAIN-N163","next_action_id":"BRAIN-N164"}), encoding="utf-8")
                mod.NEXT.write_text(json.dumps({"action_id":"BRAIN-N162"}), encoding="utf-8")
                result = verify()
                self.assertEqual(result["status"], "DENY")
                self.assertIn("POINTER_MISMATCH:BRAIN-N164!=BRAIN-N162", result["reasons"])
            finally:
                mod.CURRENT, mod.NEXT = old_current, old_next


if __name__ == "__main__":
    unittest.main()
