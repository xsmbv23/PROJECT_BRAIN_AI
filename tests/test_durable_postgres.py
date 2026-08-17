import pytest

from core.durable_postgres import DurableEvidenceDeny, _require_tls_database_url


def test_database_url_requires_postgres_scheme():
    with pytest.raises(DurableEvidenceDeny):
        _require_tls_database_url("https://example.invalid/db")


def test_database_url_forces_tls_mode():
    value = _require_tls_database_url("postgresql://user:pass@example.invalid/db")
    assert "sslmode=require" in value


def test_existing_secure_tls_modes_are_preserved():
    value = _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=verify-full")
    assert "sslmode=verify-full" in value


def test_plaintext_sslmode_is_upgraded_to_required_tls():
    value = _require_tls_database_url("postgresql://user:pass@example.invalid/db?sslmode=disable")
    assert "sslmode=require" in value
    assert "sslmode=disable" not in value
