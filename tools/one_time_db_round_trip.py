"""Explicit, opt-in durable DB round-trip proof for BRAIN-N081.

This is NOT part of the normal boot gate. It runs only when the explicit
FORENSIC_DB_ROUND_TRIP_ONCE flag is enabled in the Render service environment.
It never prints or persists credentials. The envelope is compact and
credential-free. A failed proof is evidence and must not take the web service
down.
"""
from __future__ import annotations

import hashlib
import json
import os

from tools.durable_postgres import DurableEvidenceDeny, probe_tls_connection, record_envelope, verify_receipt


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def run() -> int:
    if os.environ.get("FORENSIC_DB_ROUND_TRIP_ONCE") != "1":
        return 0

    try:
        network = probe_tls_connection()
    except DurableEvidenceDeny as exc:
        print(json.dumps({
            "db_round_trip_action": "DENY",
            "network_origin_proof": "NOT_PROVEN",
            "network_reason": str(exc),
            "write_read_hash_match": False,
            "promotion": "DENY",
            "mutation": "NONE",
        }, ensure_ascii=False), flush=True)
        return 0

    envelope = {
        "schema": "FORENSIC_DB_ROUND_TRIP_V1",
        "action_id": "BRAIN-N081",
        "purpose": "DURABLE_WRITE_READ_HASH_PROOF",
        "service": os.environ.get("RENDER_SERVICE_NAME", "project-brain-ai"),
        "commit": os.environ.get("RENDER_GIT_COMMIT", "UNKNOWN"),
        "payload": "COMPACT_FORENSIC_METADATA_ONLY",
    }
    expected_sha = hashlib.sha256(canonical(envelope)).hexdigest()
    try:
        receipt = record_envelope(envelope)
        read_ok = verify_receipt(receipt)
    except DurableEvidenceDeny as exc:
        print(json.dumps({
            "db_round_trip_action": "DENY",
            "network_origin_proof": network["network_origin_proof"],
            "write_read_hash_match": False,
            "reason": str(exc),
            "promotion": "DENY",
            "mutation": "ATTEMPTED_EXPLICITLY",
        }, ensure_ascii=False), flush=True)
        return 0

    print(json.dumps({
        "db_round_trip_action": "PASS",
        "network_origin_proof": network["network_origin_proof"],
        "write": "PASS",
        "read": "PASS",
        "canonical_sha": expected_sha,
        "stored_sha": receipt.envelope_sha,
        "sha_match": expected_sha == receipt.envelope_sha and read_ok,
        "evidence_id": receipt.evidence_id,
        "promotion": "DENY",
        "mutation": "EXPLICIT_ONE_TIME_PROOF",
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
