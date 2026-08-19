"""Bounded infrastructure comparison for N103.

No credentials, no application actions, no bulk content. IPs are hashed. ASN
is intentionally not guessed; absence of an explicit owner signal is DENY.
"""
from __future__ import annotations

import hashlib
import json
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit

DECLARED_SOURCES = ("https://ketqua16.net", "https://xsmb.com.vn")


@dataclass(frozen=True)
class InfrastructureReceipt:
    requested_host: str
    resolved_ip_sha256_16: tuple[str, ...]
    tls_version: str | None
    tls_cipher: str | None
    certificate_subject: str | None
    certificate_issuer: str | None
    certificate_san_sha256_16: str | None
    server_hint: str | None
    network_owner: str
    network_owner_observed: bool
    decision: str
    reason: str
    transfer_ms: float


def _ip_hashes(host: str, port: int) -> tuple[str, ...]:
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)})
    return tuple(hashlib.sha256(ip.encode()).hexdigest()[:16] for ip in addresses)


def _flatten_name(value) -> str | None:
    if not value:
        return None
    parts = []
    for section in value:
        for key, item in section:
            parts.append(f"{key}={item}")
    return ";".join(parts)[:512] or None


def probe_infrastructure(url: str, timeout: float = 8.0) -> InfrastructureReceipt:
    parsed = urlsplit(url)
    started = time.perf_counter()
    host = parsed.hostname or ""
    port = parsed.port or 443
    ips: tuple[str, ...] = ()
    tls_version = None
    tls_cipher = None
    subject = None
    issuer = None
    san_hash = None
    server_hint = None
    owner = "NOT_OBSERVED"
    owner_observed = False
    try:
        ips = _ip_hashes(host, port)
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as sock:
                tls_version = sock.version()
                cipher = sock.cipher()
                tls_cipher = cipher[0] if cipher else None
                cert = sock.getpeercert()
                subject = _flatten_name(cert.get("subject"))
                issuer = _flatten_name(cert.get("issuer"))
                sans = tuple(v for key, v in cert.get("subjectAltName", ()) if key == "DNS")
                san_hash = hashlib.sha256("|".join(sorted(sans)).encode()).hexdigest()[:16] if sans else None
        # Network ownership is deliberately not inferred from IP ranges or CDN names.
        decision = "DENY"
        reason = "NETWORK_OWNER_NOT_OBSERVED"
    except (OSError, ssl.SSLError, ValueError):
        decision = "DENY"
        reason = "INFRASTRUCTURE_METADATA_NOT_PROVEN"

    return InfrastructureReceipt(
        requested_host=host,
        resolved_ip_sha256_16=ips,
        tls_version=tls_version,
        tls_cipher=tls_cipher,
        certificate_subject=subject,
        certificate_issuer=issuer,
        certificate_san_sha256_16=san_hash,
        server_hint=None,
        network_owner=owner,
        network_owner_observed=owner_observed,
        decision=decision,
        reason=reason,
        transfer_ms=round((time.perf_counter() - started) * 1000, 3),
    )


def run_probe() -> dict[str, object]:
    receipts = [asdict(probe_infrastructure(url)) for url in DECLARED_SOURCES]
    return {
        "probe": "BRAIN-N103_SOURCE_INDEPENDENCE_PROOF",
        "mode": "DATA_ADMISSION",
        "source_count": len(receipts),
        "receipts": receipts,
        "independence": "DENY",
        "canonical_quorum": "DENY",
        "promotion": "DENY",
        "policy": "HOSTNAME_DIFFERENCE_IS_NOT_INDEPENDENCE_PROOF;NETWORK_OWNER_REQUIRED",
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), ensure_ascii=False, sort_keys=True))
