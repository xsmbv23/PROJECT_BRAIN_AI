"""Bounded origin metadata probe for N101.

Policy: metadata only. Never download, parse, hash, or persist source-truth
payloads. Redirects are observed but never promoted to canonical identity.
"""
from __future__ import annotations

import hashlib
import json
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from http.client import HTTPResponse
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

DECLARED_SOURCES = (
    "https://ketqua16.net",
    "https://xsmb.com.vn",
)
SAFE_HEADERS = {
    "content-type", "content-length", "content-encoding", "date",
    "server", "cache-control", "etag", "last-modified", "vary",
    "strict-transport-security", "content-security-policy",
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass(frozen=True)
class OriginReceipt:
    requested_url: str
    requested_host: str
    final_url: str
    final_host: str
    status_code: int
    redirect_chain: tuple[str, ...]
    transfer_ms: float
    tls_version: str | None
    tls_cipher: str | None
    safe_headers: dict[str, str]
    payload_downloaded: bool
    payload_hash: str
    canonical_identity: str


def _tls_metadata(response: HTTPResponse) -> tuple[str | None, str | None]:
    try:
        sock = response.fp.raw._sock  # CPython HTTPResponse/socket path
        if isinstance(sock, ssl.SSLSocket):
            cipher = sock.cipher()
            return sock.version(), cipher[0] if cipher else None
    except (AttributeError, OSError, TypeError):
        pass
    return None, None


def _safe_headers(response: HTTPResponse) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in response.headers.items():
        if key.lower() in SAFE_HEADERS:
            out[key.lower()] = value[:512]
    return dict(sorted(out.items()))


def probe_origin(url: str, timeout: float = 8.0) -> OriginReceipt:
    requested = urlsplit(url)
    started = time.perf_counter()
    chain: list[str] = []
    opener = build_opener(NoRedirect())
    current = url
    response: HTTPResponse | None = None
    status = 0
    headers: dict[str, str] = {}
    tls_version = None
    tls_cipher = None

    for _ in range(6):
        req = Request(current, method="HEAD", headers={"User-Agent": "XSMB-Forensic-OriginProbe/1.0"})
        try:
            response = opener.open(req, timeout=timeout)
            status = response.status
            headers = _safe_headers(response)
            tls_version, tls_cipher = _tls_metadata(response)
            final_url = current
            break
        except Exception as exc:
            # RedirectError exposes the Location header while keeping payload untouched.
            if hasattr(exc, "code") and hasattr(exc, "headers") and hasattr(exc, "geturl"):
                code = int(exc.code)
                location = exc.headers.get("Location")
                if 300 <= code < 400 and location:
                    chain.append(current)
                    current = location
                    continue
            final_url = current
            status = int(getattr(exc, "code", 0) or 0)
            break
    else:
        final_url = current
        status = 310

    elapsed = round((time.perf_counter() - started) * 1000, 3)
    final = urlsplit(final_url)
    if response is not None:
        try:
            response.close()
        except Exception:
            pass

    # The probe deliberately has no payload bytes. A fixed digest of the empty
    # byte string makes that fact machine-checkable without hashing source data.
    empty_payload_hash = hashlib.sha256(b"").hexdigest()
    return OriginReceipt(
        requested_url=url,
        requested_host=requested.hostname or "",
        final_url=final_url,
        final_host=final.hostname or "",
        status_code=status,
        redirect_chain=tuple(chain),
        transfer_ms=elapsed,
        tls_version=tls_version,
        tls_cipher=tls_cipher,
        safe_headers=headers,
        payload_downloaded=False,
        payload_hash=empty_payload_hash,
        canonical_identity="DENY_UNPROVEN",
    )


def run_probe() -> dict[str, object]:
    receipts = [asdict(probe_origin(url)) for url in DECLARED_SOURCES]
    return {
        "probe": "BRAIN-N101_ORIGIN_METADATA_PROBE",
        "mode": "DATA_ADMISSION",
        "source_count": len(receipts),
        "receipts": receipts,
        "canonical_identity": "DENY_UNPROVEN",
        "payload_policy": "NO_DOWNLOAD_NO_PARSE_NO_SOURCE_HASH",
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), ensure_ascii=False, sort_keys=True))
