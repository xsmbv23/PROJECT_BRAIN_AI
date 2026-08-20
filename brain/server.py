from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

from brain import __version__
from tools.binding_probe import classify_database_binding

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_DIR = ROOT / "evidence" / "runtime"
PROBE = ROOT / "tools" / "transport_probe.py"


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_payload(self):
        binding = classify_database_binding()
        self._json(200, {
            "status": 200,
            "project": "XSMB_FORENSIC",
            "component": "PROJECT_BRAIN_AI",
            "version": __version__,
            "role": "GOVERNANCE_CONTROL_PLANE",
            "foundation": "IMPLEMENTED",
            "promotion": "DENY",
            "layer_1": "LOCKED",
            "mutation": "DENY",
            "evidence": "COMPACT_ENVELOPE_ONLY",
            "render": "READONLY_HEALTH_BOUNDARY",
            "liveness": "LIVE",
            "commit_sha": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
            "database_binding": binding["status"],
            "database_tls": binding["tls"],
        })

    def _probe_authorized(self) -> bool:
        expected = os.environ.get("FORENSIC_PROBE_TOKEN", "")
        supplied = self.headers.get("X-Forensic-Probe-Token", "")
        return bool(expected) and secrets.compare_digest(supplied, expected)

    def _run_fixed_probe(self) -> tuple[bool, str]:
        RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(
            [sys.executable, str(PROBE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        raw = proc.stdout.strip()
        # Persist the probe's exact stdout as the raw receipt. The bridge does
        # not parse, rewrite, or manufacture receipt fields.
        stamp = str(int(time.time() * 1000))
        raw_path = RECEIPT_DIR / f"transport_{stamp}.json"
        raw_path.write_text(raw + "\n", encoding="utf-8")
        return proc.returncode == 0, raw_path.name

    def do_GET(self):
        if self.path in ("/", "/health", "/governance"):
            self._send_payload()
            return
        if self.path == "/forensic/run-transport-probe":
            if not self._probe_authorized():
                self._json(403, {"status": 403, "verdict": "DENY_AUTHORIZATION"})
                return
            passed, receipt_name = self._run_fixed_probe()
            # Trigger response only. Never return the receipt itself.
            self._json(202 if passed else 409, {
                "status": 202 if passed else 409,
                "execution": "IN_CONTAINER",
                "action": "FIXED_TRANSPORT_PROBE",
                "probe": "tools/transport_probe.py",
                "receipt": "PERSISTED_SEPARATELY",
                "receipt_name": receipt_name,
                "verdict": "EXECUTED" if passed else "EXECUTED_DENY",
            })
            return
        self._json(404, {"status": 404, "verdict": "NOT_FOUND"})

    def do_HEAD(self):
        if self.path in ("/", "/health", "/governance"):
            self._send_payload()
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, *_args):
        return


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
