import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVER = (ROOT / "brain" / "server.py").read_text(encoding="utf-8")
PROBE = (ROOT / "tools" / "transport_probe.py").read_text(encoding="utf-8")


class ExecutionBridgeContractTests(unittest.TestCase):
    def test_fixed_probe_only(self):
        self.assertIn('PROBE = ROOT / "tools" / "transport_probe.py"', SERVER)
        self.assertIn('[sys.executable, str(PROBE)]', SERVER)
        self.assertNotIn('subprocess.run([sys.executable, str(PROBE),', SERVER)

    def test_probe_is_not_modified_by_bridge(self):
        self.assertIn('TransportReceipt', PROBE)
        self.assertNotIn('FORENSIC_PROBE_TOKEN', PROBE)

    def test_receipt_is_not_returned(self):
        self.assertIn('receipt": "PERSISTED_SEPARATELY"', SERVER)
        self.assertNotIn('receipt.__dict__', SERVER)

    def test_authorization_is_explicit(self):
        self.assertIn('FORENSIC_PROBE_TOKEN', SERVER)
        self.assertIn('secrets.compare_digest', SERVER)

    def test_no_generic_execution_surface(self):
        self.assertNotIn('command =', SERVER)
        self.assertNotIn('cmd = self.headers', SERVER)


if __name__ == "__main__":
    unittest.main()
