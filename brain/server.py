from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

from brain import __version__


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health", "/governance"):
            self.send_response(404)
            self.end_headers()
            return
        payload = {
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
        }
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
