#!/usr/bin/env python3
"""Fail-closed, provider-neutral LLM adapter for background workers.

No credential is persisted by this module. Provider configuration comes only
from runtime environment variables. The adapter returns a typed BLOCKED result
when configuration or budget is unavailable and never grants forensic authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    base_url: str
    api_key: str
    model: str
    timeout_seconds: int
    max_output_tokens: int
    max_prompt_chars: int

    @classmethod
    def from_env(cls) -> "ProviderConfig":
        return cls(
            base_url=os.environ.get("LLM_BASE_URL", "").rstrip("/"),
            api_key=os.environ.get("LLM_API_KEY", ""),
            model=os.environ.get("LLM_MODEL", ""),
            timeout_seconds=int(os.environ.get("LLM_TIMEOUT_SECONDS", "45")),
            max_output_tokens=int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "1200")),
            max_prompt_chars=int(os.environ.get("LLM_MAX_PROMPT_CHARS", "12000")),
        )

    def configured(self) -> bool:
        return bool(self.base_url and self.api_key and self.model)


def _blocked(reason: str, proposed_next_action: str) -> dict:
    return {
        "status": "BLOCKED_PROVIDER",
        "reason": reason,
        "proposed_next_action": proposed_next_action,
        "forensic_gate": "NONE",
        "promotion": "DENY",
    }


def invoke(prompt: str, *, config: ProviderConfig | None = None) -> dict:
    cfg = config or ProviderConfig.from_env()
    if not cfg.configured():
        return _blocked(
            "LLM provider configuration is incomplete; no autonomous reasoning performed",
            "Configure LLM_BASE_URL, LLM_API_KEY and LLM_MODEL through secret management",
        )
    if len(prompt) > cfg.max_prompt_chars:
        return _blocked(
            "prompt exceeds configured safety budget",
            "Reduce prompt size or raise LLM_MAX_PROMPT_CHARS under explicit policy",
        )
    if cfg.max_output_tokens <= 0 or cfg.timeout_seconds <= 0:
        return _blocked(
            "LLM budget is invalid",
            "Set positive timeout and output-token budgets",
        )

    payload = json.dumps({
        "model": cfg.model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": cfg.max_output_tokens,
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{cfg.base_url}/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg.api_key}",
        },
        method="POST",
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=cfg.timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {
            "status": "RETRYABLE_PROVIDER_ERROR",
            "reason": f"provider request failed: {type(exc).__name__}",
            "forensic_gate": "NONE",
            "promotion": "DENY",
        }

    choices = body.get("choices") or []
    if not choices or not isinstance(choices[0], dict):
        return {
            "status": "PROVIDER_MALFORMED_RESPONSE",
            "reason": "provider returned no usable choice",
            "forensic_gate": "NONE",
            "promotion": "DENY",
        }
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        return {
            "status": "PROVIDER_MALFORMED_RESPONSE",
            "reason": "provider response has no textual message",
            "forensic_gate": "NONE",
            "promotion": "DENY",
        }

    return {
        "status": "LLM_COMPLETED",
        "model": cfg.model,
        "latency_ms": int((time.monotonic() - started) * 1000),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "response_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content": content,
        "forensic_gate": "NONE",
        "promotion": "DENY",
    }
