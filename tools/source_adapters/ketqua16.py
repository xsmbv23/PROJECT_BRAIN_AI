"""KETQUA16 source adapter.

This module is intentionally split into two responsibilities:
1) collect raw network evidence without judging truth;
2) optionally extract candidate records from an explicitly supplied selector allowlist.

No function in this module can emit PASS, PROMOTE, TRUTH, or MATCH.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import ssl
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from urllib.parse import urlsplit

ORIGIN = "https://ketqua16.net"
MAX_BODY_BYTES = 8 * 1024 * 1024
CHUNK_BYTES = 64 * 1024
DIGITS5 = re.compile(r"(?<!\d)\d{5}(?!\d)")


@dataclass(frozen=True)
class NetworkEvidenceReceipt:
    origin: str
    resolved_ips: tuple[str, ...]
    tls_version: str
    peer_certificate_sha256: str
    http_status: int
    content_type: str
    content_length: int
    body_sha256: str
    truncated: bool


@dataclass(frozen=True)
class CandidateRecord:
    source: str
    selector: str
    text: str
    five_digit_values: tuple[str, ...]


class _AllowlistParser(HTMLParser):
    def __init__(self, selectors: set[str]):
        super().__init__(convert_charrefs=True)
        self.selectors = selectors
        self.stack: list[tuple[str, str | None]] = []
        self.buffers: dict[str, list[str]] = {}
        self.records: list[CandidateRecord] = []

    @staticmethod
    def _selector(tag: str, attrs: list[tuple[str, str | None]]) -> str:
        d = dict(attrs)
        ident = d.get("id")
        classes = [x for x in (d.get("class") or "").split() if x]
        if ident:
            return f"{tag}#{ident}"
        if classes:
            return f"{tag}.{'.'.join(classes)}"
        return tag

    def handle_starttag(self, tag, attrs):
        selector = self._selector(tag, attrs)
        self.stack.append((tag, selector if selector in self.selectors else None))
        if selector in self.selectors:
            self.buffers[selector] = []

    def handle_data(self, data):
        for _tag, selector in self.stack:
            if selector:
                self.buffers.setdefault(selector, []).append(data)

    def handle_endtag(self, tag):
        if not self.stack:
            return
        _tag, selector = self.stack.pop()
        if selector and _tag == tag:
            text = " ".join(" ".join(self.buffers.get(selector, [])).split())
            values = tuple(DIGITS5.findall(text))
            self.records.append(CandidateRecord(ORIGIN, selector, text, values))
            self.buffers.pop(selector, None)


def collect_network_evidence(url: str = ORIGIN) -> tuple[NetworkEvidenceReceipt, bytes]:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != urlsplit(ORIGIN).netloc:
        raise ValueError("DENY_ORIGIN")

    port = parsed.port or 443
    ips = tuple(sorted({item[4][0] for item in socket.getaddrinfo(parsed.hostname, port, type=socket.SOCK_STREAM)}))
    context = ssl.create_default_context()
    with socket.create_connection((parsed.hostname, port), timeout=20) as raw:
        with context.wrap_socket(raw, server_hostname=parsed.hostname) as tls:
            cert = tls.getpeercert(binary_form=True)
            request = (
                f"GET {parsed.path or '/'}{('?' + parsed.query) if parsed.query else ''} HTTP/1.1\r\n"
                f"Host: {parsed.hostname}\r\n"
                "User-Agent: XSMB-FORENSIC-EvidenceCollector/1.0\r\n"
                "Accept: text/html\r\n"
                "Connection: close\r\n\r\n"
            ).encode()
            tls.sendall(request)
            chunks: list[bytes] = []
            total = 0
            header = b""
            while b"\r\n\r\n" not in header and len(header) < 64 * 1024:
                part = tls.recv(CHUNK_BYTES)
                if not part:
                    break
                header += part
            marker = header.find(b"\r\n\r\n")
            if marker < 0:
                raise RuntimeError("DENY_MALFORMED_HTTP")
            raw_headers = header[:marker].decode("iso-8859-1", errors="replace").split("\r\n")
            status = int(raw_headers[0].split()[1])
            headers = {}
            for line in raw_headers[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.lower()] = v.strip()
            body = header[marker + 4 :]
            if body:
                chunks.append(body[:MAX_BODY_BYTES])
                total += len(chunks[-1])
            truncated = total > MAX_BODY_BYTES
            while total < MAX_BODY_BYTES and not truncated:
                part = tls.recv(CHUNK_BYTES)
                if not part:
                    break
                room = MAX_BODY_BYTES - total
                take = part[:room]
                chunks.append(take)
                total += len(take)
                if len(part) > room:
                    truncated = True
                    break
            payload = b"".join(chunks)
            receipt = NetworkEvidenceReceipt(
                origin=url,
                resolved_ips=ips,
                tls_version=tls.version() or "UNKNOWN",
                peer_certificate_sha256=hashlib.sha256(cert).hexdigest(),
                http_status=status,
                content_type=headers.get("content-type", ""),
                content_length=len(payload),
                body_sha256=hashlib.sha256(payload).hexdigest(),
                truncated=truncated,
            )
            return receipt, payload


def extract_candidates(html: bytes, selectors: list[str]) -> tuple[CandidateRecord, ...]:
    # Empty allowlist means no parsing. This is deliberate DEFAULT DENY behavior.
    if not selectors:
        return ()
    parser = _AllowlistParser(set(selectors))
    parser.feed(html.decode("utf-8", errors="replace"))
    return tuple(parser.records)


def collect(url: str = ORIGIN) -> dict[str, object]:
    receipt, body = collect_network_evidence(url)
    selectors = json.loads(os.environ.get("KETQUA16_SELECTORS_JSON", "[]"))
    candidates = extract_candidates(body, selectors)
    return {
        "evidence_receipt": asdict(receipt),
        "candidates": [asdict(x) for x in candidates],
        "truth_status": "UNJUDGED",
        "next_gate": "EXCEL_VS_WEB_MATCH",
    }
