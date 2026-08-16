"""Fail-closed source/config guard against credential leakage.

The Brain core must never contain database URLs, tokens, passwords or private
keys. Runtime adapters receive secrets outside this package.
"""
from __future__ import annotations

import re

from .foundation_hardening import GovernanceDeny

_PATTERNS = (
    re.compile(r"(?i)postgres(?:ql)?://[^\s'\"]+"),
    re.compile(r"(?i)redis://[^\s'\"]+"),
    re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def assert_no_credentials(text: str) -> None:
    if any(pattern.search(text) for pattern in _PATTERNS):
        raise GovernanceDeny("CREDENTIAL_EXPOSURE")
