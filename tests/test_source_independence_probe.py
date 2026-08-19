import unittest

from tools.source_independence_probe import probe_infrastructure


class SourceIndependenceProbeTests(unittest.TestCase):
    def test_hostname_difference_is_not_independence(self):
        receipt = probe_infrastructure("https://example.com")
        self.assertNotEqual(receipt.decision, "PASS")
        self.assertFalse(receipt.network_owner_observed)


if __name__ == "__main__":
    unittest.main()
