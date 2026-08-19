"""One-shot reality collector with candidate-only admission handoff.

Fetches the target source once. The same response produces transport evidence
and, when explicitly enabled, candidate-only extraction. No canonical truth,
quorum, normalization, prediction, or classification is performed.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

try:
    from tools.source_evidence_adapter import extract_xsmb_candidate
except ModuleNotFoundError:
    from source_evidence_adapter import extract_xsmb_candidate

SOURCE = "https://ketqua16.net/"
ARTIFACT_DIR = Path(os.environ.get("FORENSIC_ARTIFACT_DIR", "/tmp/forensic_artifacts"))
MAX_CAPTURE_BYTES = 8 * 1024 * 1024
CHUNK_SIZE = 64 * 1024


def collect() -> dict[str, object]:
    started = time.time()
    observed_at = datetime.now(timezone.utc).isoformat()
    parsed = urlsplit(SOURCE)
    infos = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not infos:
        raise RuntimeError("NETWORK_ORIGIN_PROOF: unresolved host")
    resolved_ip = infos[0][4][0]
    request = Request(
        SOURCE,
        headers={
            "User-Agent": "Project_Brain_AI-ForensicCollector/1.1",
            "Accept": "text/html,application/xhtml+xml",
        },
        method="GET",
    )
    raw_bytes = bytearray()
    response_hash = hashlib.sha256()
    tls_version = ""
    cert_hash = ""
    with urlopen(request, timeout=20) as response:
        raw = getattr(getattr(response, "fp", None), "raw", None)
        connection = getattr(raw, "_sock", None) if raw else None
        if isinstance(connection, ssl.SSLSocket):
            tls_version = connection.version() or ""
            cert = connection.getpeercert(binary_form=True)
            cert_hash = hashlib.sha256(cert).hexdigest() if cert else ""
        status = int(response.status)
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            if len(raw_bytes) + len(chunk) > MAX_CAPTURE_BYTES:
                raise RuntimeError("N104B: bounded capture exceeded 8MiB")
            response_hash.update(chunk)
            raw_bytes.extend(chunk)

    if not tls_version or not cert_hash:
        raise RuntimeError("NETWORK_ORIGIN_PROOF: TLS certificate evidence missing")

    raw = bytes(raw_bytes)
    sha256 = response_hash.hexdigest()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"ketqua16_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{sha256[:16]}.raw"
    artifact = ARTIFACT_DIR / filename
    artifact.write_bytes(raw)

    receipt: dict[str, object] = {
        "receipt_version": "2",
        "source": SOURCE,
        "final_url": final_url,
        "observed_at_utc": observed_at,
        "http_status": status,
        "content_type": content_type,
        "raw_bytes": len(raw),
        "sha256": sha256,
        "resolved_ip": resolved_ip,
        "tls_version": tls_version,
        "tls_peer_certificate_sha256": cert_hash,
        "artifact_path": str(artifact),
        "artifact_persistence": "EPHEMERAL_RENDER_FILESYSTEM",
        "parse_performed": False,
        "normalization_performed": False,
        "classification_performed": False,
        "elapsed_seconds": round(time.time() - started, 4),
    }

    if os.environ.get("RUN_N104B_ADAPTER") == "1":
        html = raw.decode("utf-8", errors="replace")
        candidate = extract_xsmb_candidate(html, SOURCE, observed_at)
        receipt["candidate"] = {
            "source_sha256": candidate.source_sha256,
            "row_count": candidate.row_count,
            "grade_rows": candidate.grade_rows,
            "status": candidate.status,
        }
        receipt["candidate_only"] = True
        receipt["excel_web_match"] = "NOT_RUN"
        receipt["canonical_quorum"] = "DENY"
        receipt["truth_admission"] = "DENY"

    return receipt


if __name__ == "__main__":
    try:
        print(json.dumps({"collector": "KETQUA16", "status": "PASS", "receipt": collect()}, ensure_ascii=False, separators=(",", ":")), flush=True)
    except Exception as exc:
        print(json.dumps({"collector": "KETQUA16", "status": "DENY", "error_type": type(exc).__name__, "error": str(exc), "canonical_quorum": "DENY", "truth_admission": "DENY"}, ensure_ascii=False), flush=True)
        raise
