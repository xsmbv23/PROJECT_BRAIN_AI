"""Non-secret database binding probe.

This module never prints, returns, hashes, or persists a database credential.
It only classifies whether the service runtime has a PostgreSQL binding and
whether that binding declares an accepted TLS mode.
"""
from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlsplit


def classify_database_binding(database_url: str | None = None) -> dict[str, str | bool]:
    raw = database_url if database_url is not None else os.environ.get("DATABASE_URL", "")
    if not raw:
        return {"bound": False, "tls": False, "status": "NOT_BOUND"}
    parsed = urlsplit(raw)
    if parsed.scheme not in {"postgresql", "postgres"}:
        return {"bound": True, "tls": False, "status": "DENY_SCHEME"}
    params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    sslmode = params.get("sslmode", "")
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        return {"bound": True, "tls": False, "status": "DENY_TLS"}
    return {"bound": True, "tls": True, "status": "BOUND_TLS"}
