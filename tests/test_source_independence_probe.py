import unittest

from tools.source_independence_probe import probe_infrastructure


class SourceIndependenceProbeTests(unittest.TestCase):
    def test_hostname_difference_is_not_independence(self):
        receipt = probe_infrastructure("https://example.com")
        self.assertNotEqual(receipt.decision, "PASS")
        self.assertIn(receipt.reason, {"NETWORK_OWNER_NOT_OBSERVED", "INDEPENDENCE_REQUIRES_CROSS_OWNER_AND_FRESH_COMPARISON", "INFRASTRUCTURE_METADATA_NOT_PROVEN"})


if __name__ == "__main__":
    unittest.main()
