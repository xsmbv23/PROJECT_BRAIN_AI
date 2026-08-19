"""Bounded canonical identity probe for N102.

Only the first bounded metadata window is inspected. The page is never
archived, persisted, or treated as source truth. Ads and application links
are excluded from identity evidence.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import ssl
import time
from dataclasses import asdict, dataclass
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

DECLARED_SOURCES = ("https://ketqua16.net", "https://xsmb.com.vn")
MAX_DOCUMENT_BYTES = 262_144
MAX_REDIRECTS = 3


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass(frozen=True)
class IdentityReceipt:
    requested_url: str
    requested_host: str
    final_url: str
    final_host: str
    status_code: int
    redirect_chain: tuple[str, ...]
    response_bytes_observed: int
    bounded_window_sha256: str
    canonical_links: tuple[str, ...]
    og_urls: tuple[str, ...]
    titles: tuple[str, ...]
    site_names: tuple[str, ...]
    tls_version: str | None
    tls_cipher: str | None
    identity_decision: str
    reason: str


def _tls_metadata(response) -> tuple[str | None, str | None]:
    try:
        sock = response.fp.raw._sock
        if isinstance(sock, ssl.SSLSocket):
            cipher = sock.cipher()
            return sock.version(), cipher[0] if cipher else None
    except (AttributeError, OSError, TypeError):
        pass
    return None, None


def _extract(text: str, pattern: str) -> tuple[str, ...]:
    values = []
    for match in re.finditer(pattern, text, flags=re.I | re.S):
        value = html.unescape(match.group(1)).strip()
        if value and value not in values:
            values.append(value[:512])
    return tuple(values[:8])


def _host(value: str) -> str:
    parsed = urlsplit(value)
    return (parsed.hostname or "").lower()


def probe_identity(url: str, timeout: float = 8.0) -> IdentityReceipt:
    requested_host = _host(url)
    current = url
    chain: list[str] = []
    response = None
    status = 0
    tls_version = None
    tls_cipher = None
    body = b""
    started = time.perf_counter()

    for _ in range(MAX_REDIRECTS + 1):
        req = Request(current, method="GET", headers={"User-Agent": "XSMB-Forensic-CanonicalProbe/1.0", "Accept": "text/html,application/xhtml+xml", "Accept-Encoding": "identity", "Range": f"bytes=0-{MAX_DOCUMENT_BYTES - 1}"})
        opener = build_opener(NoRedirect())
        try:
            response = opener.open(req, timeout=timeout)
            status = response.status
            tls_version, tls_cipher = _tls_metadata(response)
            body = response.read(MAX_DOCUMENT_BYTES)
            final_url = current
            break
        except Exception as exc:
            code = int(getattr(exc, "code", 0) or 0)
            location = getattr(getattr(exc, "headers", None), "get", lambda *_: None)("Location")
            if 300 <= code < 400 and location:
                chain.append(current)
                current = urljoin(current, location)
                continue
            final_url = current
            status = code
            break
        finally:
            if response is not None:
                try:
                    response.close()
                except Exception:
                    pass
                response = None
    else:
        final_url = current
        status = 310

    elapsed = round((time.perf_counter() - started) * 1000, 3)
    text = body.decode("utf-8", errors="ignore")
    canonical_links = _extract(text, r'<link[^>]+rel=["\'][^"\']*canonical[^"\']*["\'][^>]+href=["\']([^"\']+)')
    canonical_links += tuple(v for v in _extract(text, r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\'][^"\']*canonical[^"\']*') if v not in canonical_links)
    og_urls = _extract(text, r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)')
    og_urls += tuple(v for v in _extract(text, r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:url["\']') if v not in og_urls)
    titles = _extract(text, r'<title[^>]*>(.*?)</title>')
    site_names = _extract(text, r'<meta[^>]+(?:property|name)=["\'](?:og:site_name|application-name)["\'][^>]+content=["\']([^"\']+)')
    site_names += tuple(v for v in _extract(text, r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:site_name|application-name)["\']') if v not in site_names)

    identity_hosts = {requested_host}
    canonical_hosts = {_host(urljoin(final_url, x)) for x in canonical_links if _host(urljoin(final_url, x))}
    og_hosts = {_host(urljoin(final_url, x)) for x in og_urls if _host(urljoin(final_url, x))}
    markers = int(bool(canonical_hosts & identity_hosts)) + int(bool(og_hosts & identity_hosts))
    if status not in {200, 206}:
        decision, reason = "DENY", "HTTP_STATUS_NOT_200_OR_206"
    elif markers >= 2:
        decision, reason = "PASS_LOCAL", "CANONICAL_AND_OG_URL_MATCH_DECLARED_HOST"
    elif markers == 1:
        decision, reason = "NOT_PROVEN", "ONLY_ONE_EXPLICIT_IDENTITY_MARKER"
    else:
        decision, reason = "DENY", "NO_EXPLICIT_IDENTITY_MARKER"

    return IdentityReceipt(requested_url=url, requested_host=requested_host, final_url=final_url, final_host=_host(final_url), status_code=status, redirect_chain=tuple(chain), response_bytes_observed=len(body), bounded_window_sha256=hashlib.sha256(body).hexdigest(), canonical_links=tuple(canonical_links), og_urls=tuple(og_urls), titles=titles, site_names=site_names, tls_version=tls_version, tls_cipher=tls_cipher, identity_decision=decision, reason=f"{reason}; elapsed_ms={elapsed}")


def run_probe() -> dict[str, object]:
    receipts = [asdict(probe_identity(url)) for url in DECLARED_SOURCES]
    return {"probe": "BRAIN-N102_CANONICAL_SOURCE_IDENTITY_PROOF", "mode": "DATA_ADMISSION", "source_count": len(receipts), "receipts": receipts, "promotion": "DENY", "independence": "NOT_PROVEN", "payload_policy": "BOUNDED_METADATA_WINDOW_ONLY"}


if __name__ == "__main__":
    print(json.dumps(run_probe(), ensure_ascii=False, sort_keys=True))
