#!/usr/bin/env python3
"""Fail-closed tests for the guarded LLM provider adapter."""
from __future__ import annotations

from llm_provider import ProviderConfig, invoke


def test_missing_provider_is_blocked() -> None:
    cfg = ProviderConfig("", "", "", 45, 1200, 12000)
    result = invoke("hello", config=cfg)
    assert result["status"] == "BLOCKED_PROVIDER"
    assert result["promotion"] == "DENY"
    assert result["forensic_gate"] == "NONE"


def test_prompt_budget_is_blocked() -> None:
    cfg = ProviderConfig("https://example.invalid", "secret-not-used", "model", 45, 1200, 4)
    result = invoke("12345", config=cfg)
    assert result["status"] == "BLOCKED_PROVIDER"
    assert "prompt exceeds" in result["reason"]
    assert result["promotion"] == "DENY"


def test_invalid_budget_is_blocked() -> None:
    cfg = ProviderConfig("https://example.invalid", "secret-not-used", "model", 0, 1200, 12000)
    result = invoke("hello", config=cfg)
    assert result["status"] == "BLOCKED_PROVIDER"
    assert result["promotion"] == "DENY"


def test_provider_config_never_exposes_key() -> None:
    cfg = ProviderConfig("https://example.invalid", "SUPER_SECRET", "model", 45, 1200, 12000)
    result = invoke("hello", config=cfg)
    assert "SUPER_SECRET" not in str(result)


if __name__ == "__main__":
    test_missing_provider_is_blocked()
    test_prompt_budget_is_blocked()
    test_invalid_budget_is_blocked()
    test_provider_config_never_exposes_key()
    print("llm_provider fail-closed tests: PASS")
