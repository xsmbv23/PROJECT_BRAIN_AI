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
from tools.action_receipt_store import find_exact_action_receipt
from tools.action_receipt_validator import validate_action_receipt

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_DIR = ROOT / "evidence" / "runtime"
PROBE = ROOT / "tools" / "transport_probe.py"


def _deployment_identity() -> tuple[str, str]:
    value = os.environ.get("RENDER_DEPLOY_ID", "")
    if value:
        return value, "RENDER_DEPLOY_ID"
    value = os.environ.get("RENDER_INSTANCE_ID", "")
    if value:
        return value, "RENDER_INSTANCE_ID"
    return "", "NONE"


def _runtime_observation_identity() -> dict:
    deployment, identity_type = _deployment_identity()
    return {
        "repository": "xsmbv23/Project_Brain_AI",
        "commit": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "deployment": deployment or "UNKNOWN",
        "instance": os.environ.get("RENDER_INSTANCE_ID", "UNKNOWN"),
        "identity_type": identity_type,
    }


def _current_action_receipt_evidence() -> dict:
    try:
        state = json.loads((ROOT / "state" / "current_state.json").read_text(encoding="utf-8"))
        action = state.get("last_action_id")
        next_action = state.get("next_action_id")
        commit = os.environ.get("RENDER_GIT_COMMIT", "")
        deployment, identity_type = _deployment_identity()
        if not action or not next_action or not commit or not deployment:
            return {"status": "DENY", "reason": "RUNTIME_ACTION_IDENTITY_MISSING", "identity_type": identity_type, "pass_is_local": True, "promotes": False}
        receipt = find_exact_action_receipt(action_id=action, commit_sha=commit, deployment_id=deployment)
        if not receipt:
            return {"status": "DENY", "reason": "ACTION_RECEIPT_MISSING", "identity_type": identity_type, "pass_is_local": True, "promotes": False}
        result = validate_action_receipt(receipt, {"last_action_id": action, "next_action_id": next_action}, {"commit_sha": commit})
        if receipt.get("deployment_id") != deployment:
            return {"status": "DENY", "reason": "ACTION_RECEIPT_DEPLOYMENT_ID_MISMATCH", "identity_type": identity_type, "pass_is_local": True, "promotes": False}
        return {
            "status": "PASS_LOCAL" if result.get("status") == "PASS" else "DENY",
            "reason": "EXACT_CURRENT_PRIOR_RUNTIME_RECEIPT" if result.get("status") == "PASS" else result.get("reason", "ACTION_RECEIPT_NOT_PROVEN"),
            "action_id": action,
            "commit_sha": commit,
            "deployment_identity_type": identity_type,
            "receipt_sha256": receipt.get("receipt_sha256"),
            "evidence_sha": receipt.get("evidence_sha"),
            "pass_is_local": True,
            "promotes": False,
        }
    except Exception as exc:
        return {"status": "DENY", "reason": f"ACTION_RECEIPT_READ_FAILED:{type(exc).__name__}", "pass_is_local": True, "promotes": False}


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
        observation_timestamp = time.time()
        request_identity = secrets.token_hex(16)
        runtime_identity = _runtime_observation_identity()
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
            "commit_sha": runtime_identity["commit"],
            "runtime_identity": runtime_identity,
            "observation_timestamp": observation_timestamp,
            "request_identity": request_identity,
            "database_binding": binding["status"],
            "database_tls": binding["tls"],
            "action_receipt": _current_action_receipt_evidence(),
        })

    def _probe_authorized(self) -> bool:
        expected = os.environ.get("FORENSIC_PROBE_TOKEN", "")
        supplied = self.headers.get("X-Forensic-Probe-Token", "")
        return bool(expected) and secrets.compare_digest(supplied, expected)

    def _run_fixed_probe(self) -> tuple[bool, str]:
        RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run([sys.executable, str(PROBE)], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
        raw = proc.stdout.strip()
        stamp = str(int(time.time() * 1000))
        raw_path = RECEIPT_DIR / f"transport_{stamp}.json"
        raw_path.write_text(raw + "\n", encoding="utf-8")
        return proc.returncode == 0, raw_path.name

    def do_GET(self):
        if self.path in ("/", "/health", "/governance"):
            self._send_payload()
            return
        self._json(404, {"status": 404, "verdict": "NOT_FOUND"})

    def do_POST(self):
        if self.path != "/forensic/trigger-transport-probe":
            self._json(404, {"status": 404, "verdict": "NOT_FOUND"})
            return
        if not self._probe_authorized():
            self._json(401, {"status": 401, "verdict": "UNAUTHORIZED_FORENSIC_TRIGGER"})
            return
        try:
            passed, receipt_name = self._run_fixed_probe()
        except Exception:
            self._json(500, {"status": 500, "verdict": "EXECUTION_FAILED"})
            return
        self._json(202 if passed else 409, {
            "status": 202 if passed else 409,
            "execution": "IN_CONTAINER",
            "action": "FIXED_TRANSPORT_PROBE",
            "probe": "tools/transport_probe.py",
            "receipt": "PERSISTED_SEPARATELY",
            "receipt_name": receipt_name,
            "verdict": "EXECUTED" if passed else "EXECUTED_DENY",
            "promotion": "DENY_UNTIL_INDEPENDENT_VERIFIER_PASS",
        })

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
