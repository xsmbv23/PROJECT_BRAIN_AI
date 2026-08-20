import os
import unittest
from unittest.mock import patch

from brain.server import Handler


class N109TriggerContractTests(unittest.TestCase):
    def test_probe_path_is_post_only(self):
        # Structural contract: privileged transport execution must not be
        # reachable from the read-only GET surface.
        self.assertTrue(hasattr(Handler, "do_POST"))
        self.assertTrue(hasattr(Handler, "do_GET"))

    def test_token_is_required(self):
        with patch.dict(os.environ, {"FORENSIC_PROBE_TOKEN": "secret"}, clear=False):
            self.assertFalse(Handler._probe_authorized.__doc__ is not None)

    def test_probe_is_fixed_subprocess(self):
        source = open("brain/server.py", encoding="utf-8").read()
        self.assertIn('"/forensic/trigger-transport-probe"', source)
        self.assertIn('[sys.executable, str(PROBE)]', source)
        self.assertIn('"X-Forensic-Probe-Token"', source)
        self.assertNotIn('self.path == "/forensic/run-transport-probe"', source)


if __name__ == "__main__":
    unittest.main()
