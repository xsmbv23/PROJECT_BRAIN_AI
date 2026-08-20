"""Durable ACTION_RECEIPT store.

This is an infrastructure adapter, not a verifier and not Brain core. The
issuer is called only after the runtime execution boundary completes. The
admission verifier reads prior receipts; it never calls the issuer.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from tools.durable_postgres import DurableEvidenceDeny, _canonical, _load_psycopg, _require_tls_database_url


def latest_evidence_sha() -> str:
    url = _require_tls_database_url(os.environ.get("DATABASE_URL", ""))
    psycopg = _load_psycopg()
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT envelope_sha FROM brain_forensic_evidence ORDER BY recorded_at DESC LIMIT 1")
                row = cur.fetchone()
    except Exception as exc:
        raise DurableEvidenceDeny(f"ACTION_RECEIPT_EVIDENCE_HEAD_READ_FAILED:{type(exc).__name__}") from exc
    if not row or not row[0]:
        raise DurableEvidenceDeny("ACTION_RECEIPT_EVIDENCE_HEAD_MISSING")
    return str(row[0])


def issue_action_receipt(*, action_id: str, commit_sha: str, deployment_id: str, evidence_sha: str | None = None) -> dict[str, Any]:
    if not all((action_id, commit_sha, deployment_id)):
        raise DurableEvidenceDeny("ACTION_RECEIPT_IDENTITY_INCOMPLETE")
    evidence_sha = evidence_sha or latest_evidence_sha()
    issued_at = datetime.now(timezone.utc).isoformat()
    nonce_seed = f"{action_id}|{commit_sha}|{deployment_id}|{issued_at}"
    import hashlib
    execution_nonce = hashlib.sha256(nonce_seed.encode("utf-8")).hexdigest()
    body = {
        "receipt_version": "ACTION_RECEIPT_V1",
        "action_id": action_id,
        "commit_sha": commit_sha,
        "deployment_id": deployment_id,
        "execution_nonce": execution_nonce,
        "issued_at": issued_at,
        "evidence_sha": evidence_sha,
        "status": "PASS",
    }
    receipt_sha256 = hashlib.sha256(_canonical(body)).hexdigest()
    receipt = dict(body, receipt_sha256=receipt_sha256)
    url = _require_tls_database_url(os.environ.get("DATABASE_URL", ""))
    psycopg = _load_psycopg()
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS brain_forensic_action_receipts (
                        receipt_sha256 TEXT PRIMARY KEY,
                        action_id TEXT NOT NULL,
                        commit_sha TEXT NOT NULL,
                        deployment_id TEXT NOT NULL,
                        execution_nonce TEXT NOT NULL UNIQUE,
                        issued_at TIMESTAMPTZ NOT NULL,
                        evidence_sha TEXT NOT NULL,
                        receipt_json JSONB NOT NULL
                    )
                """)
                cur.execute("""
                    INSERT INTO brain_forensic_action_receipts
                    (receipt_sha256, action_id, commit_sha, deployment_id, execution_nonce, issued_at, evidence_sha, receipt_json)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
                    ON CONFLICT (receipt_sha256) DO NOTHING
                """, (receipt_sha256, action_id, commit_sha, deployment_id, execution_nonce, issued_at, evidence_sha, json.dumps(receipt, sort_keys=True, separators=(",", ":"))))
            conn.commit()
    except Exception as exc:
        raise DurableEvidenceDeny(f"ACTION_RECEIPT_WRITE_FAILED:{type(exc).__name__}") from exc
    return receipt


def find_exact_action_receipt(*, action_id: str, commit_sha: str, deployment_id: str) -> dict[str, Any] | None:
    url = _require_tls_database_url(os.environ.get("DATABASE_URL", ""))
    psycopg = _load_psycopg()
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT receipt_json
                    FROM brain_forensic_action_receipts
                    WHERE action_id=%s AND commit_sha=%s AND deployment_id=%s
                    ORDER BY issued_at DESC
                    LIMIT 1
                """, (action_id, commit_sha, deployment_id))
                row = cur.fetchone()
    except Exception as exc:
        raise DurableEvidenceDeny(f"ACTION_RECEIPT_READ_FAILED:{type(exc).__name__}") from exc
    return dict(row[0]) if row else None
