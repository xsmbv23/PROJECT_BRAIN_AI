"""N104B one-shot real-source capture.

This runner is intentionally opt-in via RUN_N104B_CAPTURE=1. It performs one
bounded HTTPS capture, computes transport evidence and candidate-only XSMB
extraction, then emits compact JSON to the Render application log. It never
writes credentials, raw HTML, or bulk source data to logs.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from tools.source_evidence_adapter import extract_xsmb_candidate

URL = "https://ketqua16.net/"
CHUNK_SIZE = 64 * 1024
MAX_CAPTURE_BYTES = 8 * 1024 * 1024


def run() -> dict[str, object]:
    parsed = urlsplit(URL)
    if parsed.scheme != "https" or not parsed.hostname:
        raise RuntimeError("N104B: HTTPS URL required")
    infos = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not infos:
        raise RuntimeError("N104B: unresolved host")
    resolved_ip = infos[0][4][0]
    req = Request(URL, headers={"User-Agent": "XSMB-Forensic-EvidenceCollector/1.0"})
    body = bytearray()
    response_hash = hashlib.sha256()
    cert_hash = ""
    tls_version = ""
    status = 0
    with urlopen(req, timeout=20.0) as response:
        raw = getattr(getattr(response, "fp", None), "raw", None)
        connection = getattr(raw, "_sock", None) if raw else None
        if isinstance(connection, ssl.SSLSocket):
            tls_version = connection.version() or ""
            cert = connection.getpeercert(binary_form=True)
            cert_hash = hashlib.sha256(cert).hexdigest() if cert else ""
        status = int(getattr(response, "status", 0) or 0)
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            response_hash.update(chunk)
            if len(body) + len(chunk) > MAX_CAPTURE_BYTES:
                raise RuntimeError("N104B: bounded capture exceeded 8MiB")
            body.extend(chunk)
    if not tls_version or not cert_hash:
        raise RuntimeError("N104B: TLS evidence missing")
    captured_at = datetime.now(timezone.utc).isoformat()
    html = bytes(body).decode("utf-8", errors="replace")
    candidate = extract_xsmb_candidate(html, URL, captured_at)
    return {
        "action_id": "BRAIN-N104B",
        "source": "ketqua16.net",
        "network_origin": {
            "url": URL,
            "resolved_ip": resolved_ip,
            "tls_version": tls_version,
            "tls_peer_certificate_sha256": cert_hash,
            "http_status": status,
            "response_sha256": response_hash.hexdigest(),
            "capture_timestamp_utc": captured_at,
            "bytes_observed": len(body),
        },
        "candidate": {
            "source_sha256": candidate.source_sha256,
            "capture_timestamp_utc": candidate.capture_timestamp_utc,
            "grade_rows": candidate.grade_rows,
            "row_count": candidate.row_count,
            "status": candidate.status,
        },
        "canonical_quorum": "DENY",
        "truth_admission": "DENY",
    }


def main() -> int:
    if os.environ.get("RUN_N104B_CAPTURE") != "1":
        return 0
    try:
        print(json.dumps(run(), ensure_ascii=False, separators=(",", ":")), flush=True)
        return 0
    except Exception as exc:
        print(json.dumps({"action_id":"BRAIN-N104B","status":"DENY","error":str(exc),"canonical_quorum":"DENY","truth_admission":"DENY"}, ensure_ascii=False), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
