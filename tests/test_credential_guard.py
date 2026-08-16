import unittest

from core.credential_guard import assert_no_credentials
from core.foundation_hardening import GovernanceDeny


class CredentialGuardTests(unittest.TestCase):
    def test_clean_text_passes(self):
        assert_no_credentials("policy_version=v1; adapter receives secret externally")

    def test_database_url_denies(self):
        with self.assertRaises(GovernanceDeny):
            assert_no_credentials("DATABASE_URL=postgresql://user:password@example/db")

    def test_private_key_denies(self):
        with self.assertRaises(GovernanceDeny):
            assert_no_credentials("-----BEGIN PRIVATE KEY-----")
