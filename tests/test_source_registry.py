import unittest
from tools.verify_source_registry import main


class SourceRegistryTests(unittest.TestCase):
    def test_registry_is_valid_and_stays_denied(self):
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
