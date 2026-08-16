"""Restart-safe compact audit-head envelope.

The envelope contains metadata only. It is intentionally not a bulk-data
store and does not become a second source of truth.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json

from .foundation_hardening import AuditChain, GovernanceDeny


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class AuditHeadEnvelope:
    envelope_version: str
    policy_version: str
    schema_version: str
    brain_state_version: str
    audit_head: str
    previous_audit_head: str
    event_count: int
    generated_at: float
    envelope_sha: str


def seal_head(chain: AuditChain, *, policy_version: str, schema_version: str,
              brain_state_version: str, event_count: int, generated_at: float) -> AuditHeadEnvelope:
    if event_count < 1 or chain.last_hash == "GENESIS":
        raise GovernanceDeny("AUDIT_HEAD_NOT_ESTABLISHED")
    body = {
        "envelope_version": "v1",
        "policy_version": policy_version,
        "schema_version": schema_version,
        "brain_state_version": brain_state_version,
        "audit_head": chain.last_hash,
        "previous_audit_head": "GENESIS",
        "event_count": event_count,
        "generated_at": generated_at,
    }
    digest = hashlib.sha256(_canonical(body)).hexdigest()
    return AuditHeadEnvelope(**body, envelope_sha=digest)


def serialize(envelope: AuditHeadEnvelope) -> str:
    return json.dumps(asdict(envelope), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def restore_and_verify(raw: str, *, expected_policy: str, expected_schema: str,
                       expected_brain_state: str, expected_head: str) -> AuditHeadEnvelope:
    try:
        data = json.loads(raw)
        supplied_sha = data.pop("envelope_sha")
    except (TypeError, ValueError, KeyError) as exc:
        raise GovernanceDeny("AUDIT_ENVELOPE_MALFORMED") from exc
    digest = hashlib.sha256(_canonical(data)).hexdigest()
    if digest != supplied_sha:
        raise GovernanceDeny("AUDIT_ENVELOPE_HASH_MISMATCH")
    if data["policy_version"] != expected_policy or data["schema_version"] != expected_schema or data["brain_state_version"] != expected_brain_state:
        raise GovernanceDeny("AUDIT_ENVELOPE_POLICY_MISMATCH")
    if data["audit_head"] != expected_head:
        raise GovernanceDeny("AUDIT_HEAD_RESTORE_MISMATCH")
    if data["event_count"] < 1:
        raise GovernanceDeny("AUDIT_EVENT_COUNT_INVALID")
    data["envelope_sha"] = supplied_sha
    return AuditHeadEnvelope(**data)
