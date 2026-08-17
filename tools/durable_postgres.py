"""TLS-only metadata evidence sink for the Brain foundation.

This is an infrastructure adapter, deliberately outside ``core/`` so the Brain
control plane remains dataset-free and dependency-isolated.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


class DurableEvidenceDeny(RuntimeError):
    """Fail-closed error for unsafe or unavailable durable evidence."""


@dataclass(frozen=True)
class EvidenceReceipt:
    evidence_id: str
    envelope_sha: str
    recorded_at: str


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _require_tls_database_url(url: str) -> str:
    if not url:
        raise DurableEvidenceDeny("DATABASE_URL_MISSING")
    parsed = urlsplit(url)
    if parsed.scheme not in {"postgresql", "postgres"}:
        raise DurableEvidenceDeny("DATABASE_URL_SCHEME_DENIED")
    params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    sslmode = params.get("sslmode", "")
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        params["sslmode"] = "require"
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(params), parsed.fragment))


def _load_psycopg():
    try:
        import psycopg  # type: ignore
    except ImportError as exc:
        raise DurableEvidenceDeny("PSYCOPG_UNAVAILABLE") from exc
    return psycopg


def record_envelope(envelope: dict[str, object], *, database_url: str | None = None) -> EvidenceReceipt:
    forbidden = {"password", "secret", "token", "api_key", "database_url", "DATABASE_URL"}
    if forbidden.intersection(str(k).lower() for k in envelope):
        raise DurableEvidenceDeny("CREDENTIAL_FIELD_IN_EVIDENCE")
    canonical = _canonical(envelope)
    envelope_sha = hashlib.sha256(canonical).hexdigest()
    evidence_id = hashlib.sha256((envelope_sha + "|brain-foundation").encode()).hexdigest()[:32]
    recorded_at = datetime.now(timezone.utc).isoformat()
    url = _require_tls_database_url(database_url or os.environ.get("DATABASE_URL", ""))
    psycopg = _load_psycopg()
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS brain_forensic_evidence (
                        evidence_id TEXT PRIMARY KEY,
                        envelope_sha TEXT NOT NULL,
                        recorded_at TIMESTAMPTZ NOT NULL,
                        envelope_json JSONB NOT NULL
                    )
                """)
                cur.execute("""
                    INSERT INTO brain_forensic_evidence
                        (evidence_id, envelope_sha, recorded_at, envelope_json)
                    VALUES (%s, %s, %s, %s::jsonb)
                    ON CONFLICT (evidence_id) DO NOTHING
                """, (evidence_id, envelope_sha, recorded_at, canonical.decode("utf-8")))
            conn.commit()
    except Exception as exc:
        raise DurableEvidenceDeny("DURABLE_EVIDENCE_WRITE_FAILED") from exc
    return EvidenceReceipt(evidence_id=evidence_id, envelope_sha=envelope_sha, recorded_at=recorded_at)


def verify_receipt(receipt: EvidenceReceipt, *, database_url: str | None = None) -> bool:
    url = _require_tls_database_url(database_url or os.environ.get("DATABASE_URL", ""))
    psycopg = _load_psycopg()
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT envelope_sha, envelope_json FROM brain_forensic_evidence WHERE evidence_id=%s", (receipt.evidence_id,))
                row = cur.fetchone()
    except Exception as exc:
        raise DurableEvidenceDeny("DURABLE_EVIDENCE_READ_FAILED") from exc
    if not row:
        raise DurableEvidenceDeny("DURABLE_EVIDENCE_NOT_FOUND")
    stored_sha, payload = row
    actual_sha = hashlib.sha256(_canonical(payload)).hexdigest()
    if stored_sha != receipt.envelope_sha or actual_sha != receipt.envelope_sha:
        raise DurableEvidenceDeny("DURABLE_EVIDENCE_HASH_MISMATCH")
    return True
