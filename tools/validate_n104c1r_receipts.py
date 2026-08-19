"""Strict validator for N104C.1R receipts.

This validator never creates evidence and never promotes a gate. It only
accepts already-produced receipts and returns PASS/FAIL for their local
structural and reconciliation assertions. Missing runtime evidence is DENY.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
TLS = {"TLSv1.2", "TLSv1.3"}


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def validate_network_origin(receipt: dict) -> list[str]:
    errors: list[str] = []
    required = ("source", "resolved_ip", "tls_version", "certificate_sha256", "http_status", "response_sha256", "timestamp_utc")
    for key in required:
        if key not in receipt:
            errors.append(f"NETWORK_MISSING:{key}")
    if receipt.get("source") != "ketqua16.net": errors.append("NETWORK_SOURCE")
    if not receipt.get("resolved_ip"): errors.append("NETWORK_IP")
    if receipt.get("tls_version") not in TLS: errors.append("NETWORK_TLS")
    if not _is_sha(receipt.get("certificate_sha256")): errors.append("NETWORK_CERT_SHA")
    if receipt.get("http_status") != 200: errors.append("NETWORK_HTTP_STATUS")
    if not _is_sha(receipt.get("response_sha256")): errors.append("NETWORK_RESPONSE_SHA")
    if not receipt.get("timestamp_utc"): errors.append("NETWORK_TIMESTAMP")
    return errors


def validate_state_drift(receipt: dict) -> list[str]:
    errors: list[str] = []
    for key in ("repo", "runtime", "match", "timestamp_utc"):
        if key not in receipt: errors.append(f"DRIFT_MISSING:{key}")
    if receipt.get("match") is not True: errors.append("DRIFT_MATCH_FALSE")
    repo = receipt.get("repo")
    runtime = receipt.get("runtime")
    if not isinstance(repo, dict) or not isinstance(runtime, dict):
        errors.append("DRIFT_SHAPE")
    elif repo != runtime:
        errors.append("DRIFT_FIELDS_MISMATCH")
    return errors


def reconcile(network: dict, drift: dict) -> dict:
    errors = validate_network_origin(network) + validate_state_drift(drift)
    return {
        "reconciliation": "MATCH" if not errors else "MISMATCH",
        "errors": errors,
        "promotion": "ADMIT" if not errors else "DENY",
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    evidence = root / "evidence" / "N104C.1R"
    network_path = evidence / "network_origin_receipt.json"
    drift_path = evidence / "state_drift_receipt.json"
    if not network_path.exists() or not drift_path.exists():
        print(json.dumps({"reconciliation": "MISMATCH", "errors": ["RECEIPT_MISSING"], "promotion": "DENY"}, sort_keys=True))
        return 1
    network = json.loads(network_path.read_text(encoding="utf-8"))
    drift = json.loads(drift_path.read_text(encoding="utf-8"))
    result = reconcile(network, drift)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["reconciliation"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
