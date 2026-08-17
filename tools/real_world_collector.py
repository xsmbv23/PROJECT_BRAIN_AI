"""One-shot reality collector.

Fetches the target source as raw bytes only. It does not parse, normalize,
interpret, or map lottery results. It writes the raw response to an ephemeral
artifact directory and emits a compact forensic receipt.

Durable artifact persistence is deliberately NOT claimed here because the
Render service has no persistent disk and the PostgreSQL binding is not yet
proven. The receipt therefore distinguishes ephemeral artifact capture from
durable evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = "https://ketqua16.net/"
ARTIFACT_DIR = Path(os.environ.get("FORENSIC_ARTIFACT_DIR", "/tmp/forensic_artifacts"))


def collect() -> dict[str, object]:
    started = time.time()
    observed_at = datetime.now(timezone.utc).isoformat()
    request = Request(
        SOURCE,
        headers={
            "User-Agent": "Project_Brain_AI-ForensicCollector/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
        method="GET",
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read()
        status = int(response.status)
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()

    sha256 = hashlib.sha256(raw).hexdigest()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"ketqua16_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{sha256[:16]}.raw"
    artifact = ARTIFACT_DIR / filename
    artifact.write_bytes(raw)

    return {
        "receipt_version": "1",
        "source": SOURCE,
        "final_url": final_url,
        "observed_at_utc": observed_at,
        "http_status": status,
        "content_type": content_type,
        "raw_bytes": len(raw),
        "sha256": sha256,
        "artifact_path": str(artifact),
        "artifact_persistence": "EPHEMERAL_RENDER_FILESYSTEM",
        "parse_performed": False,
        "normalization_performed": False,
        "classification_performed": False,
        "elapsed_seconds": round(time.time() - started, 4),
    }


if __name__ == "__main__":
    try:
        print(json.dumps({"collector": "KETQUA16", "status": "PASS", "receipt": collect()}, ensure_ascii=False), flush=True)
    except Exception as exc:
        print(json.dumps({"collector": "KETQUA16", "status": "DENY", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False), flush=True)
        raise
