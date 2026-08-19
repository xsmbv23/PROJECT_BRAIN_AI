import os
import unittest

from brain.server import Handler


class _Headers:
    def __init__(self, token=""):
        self.token = token

    def get(self, key, default=""):
        if key == "X-Forensic-Probe-Token":
            return self.token
        return default


class _Request:
    def __init__(self, token=""):
        self.headers = _Headers(token)


class TransportExecutionPathTests(unittest.TestCase):
    def test_probe_token_is_required(self):
        old = os.environ.get("FORENSIC_PROBE_TOKEN")
        try:
            os.environ["FORENSIC_PROBE_TOKEN"] = "secret"
            self.assertFalse(Handler._probe_authorized(_Request("")))
            self.assertFalse(Handler._probe_authorized(_Request("wrong")))
            self.assertTrue(Handler._probe_authorized(_Request("secret")))
        finally:
            if old is None:
                os.environ.pop("FORENSIC_PROBE_TOKEN", None)
            else:
                os.environ["FORENSIC_PROBE_TOKEN"] = old

    def test_missing_server_token_denies(self):
        old = os.environ.pop("FORENSIC_PROBE_TOKEN", None)
        try:
            self.assertFalse(Handler._probe_authorized(_Request("anything")))
        finally:
            if old is not None:
                os.environ["FORENSIC_PROBE_TOKEN"] = old


if __name__ == "__main__":
    unittest.main()
