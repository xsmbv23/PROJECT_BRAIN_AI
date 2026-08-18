"""Credential-free, fail-closed network admission probe.

Runs only when FORENSIC_NETWORK_PROBE=1. It never emits DATABASE_URL, user,
password, host, or raw exception text. The result is compact forensic metadata.
A failed probe is evidence and DENY; it must never terminate the normal service.
"""
from __future__ import annotations

import hashlib
import os
import socket
import time
from urllib.parse import urlsplit

import psycopg


def _host_hash(host: str) -> str:
    return hashlib.sha256(host.encode("utf-8")).hexdigest()[:16]


def probe(database_url: str | None = None) -> dict[str, object]:
    raw = database_url if database_url is not None else os.environ.get("DATABASE_URL", "")
    if not raw:
        return {"status": "NOT_BOUND"}

    parsed = urlsplit(raw)
    if parsed.scheme not in {"postgres", "postgresql"} or not parsed.hostname:
        return {"status": "DENY_BINDING"}

    host = parsed.hostname
    port = parsed.port or 5432
    result: dict[str, object] = {
        "status": "NOT_PROVEN",
        "host_sha256_16": _host_hash(host),
        "port": port,
        "dns": "NOT_PROVEN",
        "tls": "NOT_PROVEN",
        "connection": "NOT_PROVEN",
    }

    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)})
        result["dns"] = "PASS"
        result["resolved_count"] = len(addresses)
        result["resolved_ip_sha256_16"] = [hashlib.sha256(ip.encode()).hexdigest()[:16] for ip in addresses]
    except (OSError, ValueError):
        result["dns"] = "DENY"
        result["status"] = "DENY_NETWORK_ORIGIN"
        return result

    started = time.perf_counter()
    conn = None
    try:
        conn = psycopg.connect(raw, connect_timeout=10)
        result["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        info = conn.info
        result["connection"] = "PASS"
        result["server_version"] = int(info.server_version)
        result["tls"] = "PASS" if bool(getattr(info, "ssl_in_use", False)) else "DENY"
        if result["tls"] != "PASS":
            result["status"] = "DENY_TLS"
            return result
        result["ssl_cipher"] = str(info.ssl_attribute("cipher") or "UNKNOWN")
        result["ssl_protocol"] = str(info.ssl_attribute("protocol") or "UNKNOWN")
        result["status"] = "PASS"
        return result
    except psycopg.OperationalError:
        result["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        result["connection"] = "DENY"
        result["status"] = "DENY_NETWORK_ORIGIN"
        return result
    except Exception as exc:
        result["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        result["connection"] = "DENY"
        result["exception_class"] = exc.__class__.__name__
        result["status"] = "DENY_NETWORK_ORIGIN"
        return result
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    if os.environ.get("FORENSIC_NETWORK_PROBE") != "1":
        print('{"status":"DISABLED"}', flush=True)
    else:
        print(probe(), flush=True)
