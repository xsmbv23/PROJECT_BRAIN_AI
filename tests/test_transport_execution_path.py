import os
import unittest

from brain.server import Handler


class TransportExecutionPathTests(unittest.TestCase):
    def test_probe_token_is_required(self):
        old = os.environ.get("FORENSIC_PROBE_TOKEN")
        try:
            os.environ["FORENSIC_PROBE_TOKEN"] = "secret"
            self.assertFalse(Handler._probe_authorized)
        finally:
            if old is None:
                os.environ.pop("FORENSIC_PROBE_TOKEN", None)
            else:
                os.environ["FORENSIC_PROBE_TOKEN"] = old


if __name__ == "__main__":
    unittest.main()
