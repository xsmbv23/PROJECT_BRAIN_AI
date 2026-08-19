"""Streaming network evidence collector.

The collector observes transport and payload evidence only. It never decides
whether the observed data is canonical. Large responses are streamed through
incremental SHA-256 so the Render worker does not accumulate bulk payloads in RAM.
"""
from __future__ import annotations

import hashlib
import socket
import ssl
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

CHUNK_SIZE = 64 * 1024


@dataclass(frozen=True)
class NetworkOriginReceipt:
    url: str
    resolved_ip: str
    tls_version: str
    tls_peer_certificate_sha256: str
    http_status: int
    response_sha256: str
    capture_timestamp_utc: str
    bytes_observed: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _resolve_ip(host: str) -> str:
    infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not infos:
        raise RuntimeError("NETWORK_ORIGIN_PROOF: unresolved host")
    return infos[0][4][0]


def collect(url: str, timeout: float = 20.0) -> NetworkOriginReceipt:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise RuntimeError("NETWORK_ORIGIN_PROOF: HTTPS URL required")

    resolved_ip = _resolve_ip(parsed.hostname)
    request = Request(url, headers={"User-Agent": "XSMB-Forensic-EvidenceCollector/1.0"})

    response_hash = hashlib.sha256()
    bytes_observed = 0
    cert_hash = ""
    tls_version = ""

    with urlopen(request, timeout=timeout) as response:
        sock = getattr(response, "fp", None)
        raw = getattr(sock, "raw", None) if sock else None
        connection = getattr(raw, "_sock", None) if raw else None
        if connection is not None and isinstance(connection, ssl.SSLSocket):
            tls_version = connection.version() or ""
            cert = connection.getpeercert(binary_form=True)
            cert_hash = hashlib.sha256(cert).hexdigest() if cert else ""

        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            response_hash.update(chunk)
            bytes_observed += len(chunk)

        status = int(getattr(response, "status", 0) or 0)

    if not tls_version or not cert_hash:
        raise RuntimeError("NETWORK_ORIGIN_PROOF: TLS certificate evidence missing")

    return NetworkOriginReceipt(
        url=url,
        resolved_ip=resolved_ip,
        tls_version=tls_version,
        tls_peer_certificate_sha256=cert_hash,
        http_status=status,
        response_sha256=response_hash.hexdigest(),
        capture_timestamp_utc=datetime.now(timezone.utc).isoformat(),
        bytes_observed=bytes_observed,
    )
