import unittest

from tools.durable_postgres import DurableEvidenceDeny, _require_tls_database_url


class DurablePostgresTests(unittest.TestCase):
    def test_database_url_requires_postgres_scheme(self):
        with self.assertRaises(DurableEvidenceDeny):
            _require_tls_database_url("https://example.invalid/db")

    def test_database_url_without_explicit_tls_is_denied(self):
        with self.assertRaises(DurableEvidenceDeny) as ctx:
            _require_tls_database_url("postgresql://user:pass@example.invalid/db")
        self.assertEqual(str(ctx.exception), "DATABASE_TLS_NOT_EXPLICIT")

    def test_existing_secure_tls_modes_are_preserved(self):
        value = _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=verify-full")
        self.assertIn("sslmode=verify-full", value)

    def test_plaintext_sslmode_is_denied_not_upgraded(self):
        with self.assertRaises(DurableEvidenceDeny) as ctx:
            _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=disable")
        self.assertEqual(str(ctx.exception), "DATABASE_TLS_NOT_EXPLICIT")


if __name__ == "__main__":
    unittest.main()
