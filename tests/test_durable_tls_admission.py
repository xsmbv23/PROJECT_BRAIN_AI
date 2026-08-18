import unittest

from tools.durable_postgres import DurableEvidenceDeny, _require_tls_database_url


class DurableTLSAdmissionTests(unittest.TestCase):
    def test_missing_sslmode_denies(self):
        with self.assertRaisesRegex(DurableEvidenceDeny, "DATABASE_TLS_NOT_EXPLICIT"):
            _require_tls_database_url("postgresql://u:p@example.invalid/db")

    def test_disabled_tls_denies(self):
        with self.assertRaisesRegex(DurableEvidenceDeny, "DATABASE_TLS_NOT_EXPLICIT"):
            _require_tls_database_url("postgresql://u:p@example.invalid/db?sslmode=disable")

    def test_require_tls_passes(self):
        url = "postgresql://u:p@example.invalid/db?sslmode=require"
        self.assertEqual(_require_tls_database_url(url), url)

    def test_verify_full_tls_passes(self):
        url = "postgresql://u:p@example.invalid/db?sslmode=verify-full"
        self.assertEqual(_require_tls_database_url(url), url)


if __name__ == "__main__":
    unittest.main()
