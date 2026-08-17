import unittest

from tools.binding_probe import classify_database_binding


class BindingProbeTests(unittest.TestCase):
    def test_missing_binding_is_not_bound(self):
        self.assertEqual(classify_database_binding(""), {"bound": False, "tls": False, "status": "NOT_BOUND"})

    def test_non_postgres_scheme_denied(self):
        result = classify_database_binding("https://example.invalid/db")
        self.assertEqual(result["status"], "DENY_SCHEME")
        self.assertFalse(result["tls"])

    def test_postgres_without_tls_denied(self):
        result = classify_database_binding("postgresql://u:p@example.invalid/db?sslmode=disable")
        self.assertEqual(result["status"], "DENY_TLS")
        self.assertFalse(result["tls"])

    def test_postgres_tls_is_bound(self):
        result = classify_database_binding("postgresql://u:p@example.invalid/db?sslmode=require")
        self.assertEqual(result["status"], "BOUND_TLS")
        self.assertTrue(result["bound"])
        self.assertTrue(result["tls"])


if __name__ == "__main__":
    unittest.main()
