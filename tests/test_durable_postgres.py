import unittest

from tools.durable_postgres import DurableEvidenceDeny, _require_tls_database_url


class DurablePostgresTests(unittest.TestCase):
    def test_database_url_requires_postgres_scheme(self):
        with self.assertRaises(DurableEvidenceDeny):
            _require_tls_database_url("https://example.invalid/db")

    def test_database_url_forces_tls_mode(self):
        value = _require_tls_database_url("postgresql://user:pass@example.invalid/db")
        self.assertIn("sslmode=require", value)

    def test_existing_secure_tls_modes_are_preserved(self):
        value = _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=verify-full")
        self.assertIn("sslmode=verify-full", value)

    def test_plaintext_sslmode_is_upgraded_to_required_tls(self):
        value = _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=disable")
        self.assertIn("sslmode=require", value)
        self.assertNotIn("sslmode=disable", value)


if __name__ == "__main__":
    unittest.main()
