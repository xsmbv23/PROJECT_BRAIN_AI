"""Bounded streaming HTTP provenance capture.

The adapter captures exact response bytes to a local artifact path while
hashing incrementally. It never stores credentials in receipts and never
claims source independence from domain names alone.
"""
from __future__ import annotations

import hashlib
import json
import socket
import time
from http.client import HTTPResponse
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

CHUNK = 64 * 1024
MAX_ARTIFACT_BYTES = 32 * 1024 * 1024


def _safe_source_identity(url: str) -> dict[str, object]:
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    ips: list[str] = []
    if host:
        try:
            ips = sorted({item[4][0] for item in socket.getaddrinfo(host, None)})
        except OSError:
            ips = []
    return {
        "scheme": parsed.scheme,
        "hostname": host,
        "resolved_ips": ips,
    }


def capture(url: str, artifact_path: str, *, source_id: str, parser_version: str) -> dict[str, object]:
    if not url.startswith(("https://", "http://")):
        raise ValueError("unsupported URL scheme")

    request_timestamp = time.time()
    req = Request(url, headers={"User-Agent": "XSMB-Forensic-Provenance/1.0"})
    opener = build_opener()
    response: HTTPResponse = opener.open(req, timeout=20)
    redirect_chain = [getattr(item, "url", "") for item in getattr(response, "history", [])]
    redirect_chain.append(response.geturl())

    target = Path(artifact_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    total = 0
    try:
        with target.open("wb") as handle:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARTIFACT_BYTES:
                    raise ValueError("artifact exceeds bounded capture limit")
                digest.update(chunk)
                handle.write(chunk)
    except Exception:
        target.unlink(missing_ok=True)
        raise

    source_identity = _safe_source_identity(response.geturl())
    return {
        "source_id": source_id,
        "request_url": url,
        "request_timestamp": request_timestamp,
        "http_status": int(response.status),
        "content_type": response.headers.get("Content-Type", ""),
        "redirect_chain": redirect_chain,
        "raw_artifact_path": str(target),
        "raw_response_bytes": total,
        "raw_sha256": digest.hexdigest(),
        "normalized_full27_sha256": "NOT_COMPUTED",
        "parser_version": parser_version,
        "source_identity": source_identity,
        "anti_ad_collision_identity": {
            "hostname": source_identity["hostname"],
            "resolved_ips": source_identity["resolved_ips"],
            "independence_status": "NOT_PROVEN",
        },
        "independence_status": "NOT_PROVEN",
        "credentials_present": False,
    }


def write_receipt(receipt: dict[str, object], path: str) -> None:
    clean = dict(receipt)
    clean.pop("credentials_present", None)
    Path(path).write_text(json.dumps(clean, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
