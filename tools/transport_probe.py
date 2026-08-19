"""Independent source transport probe for ketqua16.net.

This module is deliberately transport-only: it does not parse lottery meaning,
strip advertising, infer canonical truth, or promote data. It fetches a bounded
raw HTTP payload, records status/length/SHA-256, and fails closed on truncation,
oversize payloads, redirects, or non-200 responses.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from dataclasses import asdict, dataclass

URL = "https://ketqua16.net/"
MAX_BYTES = 128 * 1024
TIMEOUT_SECONDS = 15
USER_AGENT = "XSMB-FORENSIC-TRANSPORT-PROBE/1.0"
EXPECTED_MIN_BYTES = 1


@dataclass(frozen=True)
class TransportReceipt:
    action_id: str
    url: str
    status_code: int
    bytes_read: int
    sha256: str
    truncated: bool
    elapsed_ms: int
    verdict: str


def run_probe(action_id: str = "BRAIN-N104C.1_TRANSPORT_PROBE") -> TransportReceipt:
    started = time.monotonic()
    request = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            status = int(response.status)
            if status != 200:
                return TransportReceipt(action_id, URL, status, 0, "", False, int((time.monotonic()-started)*1000), "DENY_HTTP_STATUS")
            body = response.read(MAX_BYTES + 1)
            truncated = len(body) > MAX_BYTES
            if truncated:
                body = body[:MAX_BYTES]
            digest = hashlib.sha256(body).hexdigest()
            verdict = "DENY_TRUNCATED" if truncated else ("PASS" if len(body) >= EXPECTED_MIN_BYTES else "DENY_EMPTY")
            return TransportReceipt(action_id, URL, status, len(body), digest, truncated, int((time.monotonic()-started)*1000), verdict)
    except Exception as exc:
        return TransportReceipt(action_id, URL, 0, 0, "", False, int((time.monotonic()-started)*1000), "DENY_TRANSPORT_ERROR")


def main() -> int:
    receipt = run_probe()
    print(json.dumps(asdict(receipt), ensure_ascii=False, sort_keys=True), flush=True)
    return 0 if receipt.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
