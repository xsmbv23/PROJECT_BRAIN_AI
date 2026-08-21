"""Bounded read-only HTTP wrapper around source_independence_probe.

This service exists because the forensic source-independence probe is a
one-shot function, while Render Web Services require a long-lived process.
No credentials, mutation, scraping storage, or promotion is exposed.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tools.source_independence_probe import run_probe


class Handler(BaseHTTPRequestHandler):
    server_version = "XSMB-Forensic-Independence/1.0"

    def _send(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "authority": "OBSERVATION_ONLY", "promotion": "DENY"})
            return
        if self.path == "/probe":
            try:
                result = run_probe()
                result["authority"] = "OBSERVATION_ONLY"
                result["promotion"] = "DENY"
                self._send(200, result)
            except Exception as exc:  # fail closed
                self._send(503, {
                    "probe": "BRAIN-N103_SOURCE_INDEPENDENCE_PROOF",
                    "independence": "DENY",
                    "canonical_quorum": "DENY",
                    "promotion": "DENY",
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:512],
                })
            return
        self._send(404, {"status": "not_found"})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
