"""Minimal durable-state boundary for Brain governance metadata.

The Brain owns only compact governance state. A production adapter must be
injected by the runtime; this module deliberately has no credentials and no
network/database dependency.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .durable_audit import AuditHeadEnvelope, restore_and_verify, serialize
from .foundation_hardening import GovernanceDeny


class DurableStateStore(Protocol):
    def put(self, key: str, value: str) -> None: ...
    def get(self, key: str) -> str | None: ...


@dataclass(frozen=True)
class RestoredAuditState:
    envelope: AuditHeadEnvelope
    restored: bool


def persist_audit_head(store: DurableStateStore, envelope: AuditHeadEnvelope) -> None:
    store.put("brain.audit_head.v1", serialize(envelope))


def restore_audit_head(store: DurableStateStore, *, policy: str, schema: str,
                       brain_state: str, expected_head: str) -> RestoredAuditState:
    raw = store.get("brain.audit_head.v1")
    if raw is None:
        raise GovernanceDeny("DURABLE_AUDIT_HEAD_MISSING")
    envelope = restore_and_verify(
        raw,
        expected_policy=policy,
        expected_schema=schema,
        expected_brain_state=brain_state,
        expected_head=expected_head,
    )
    return RestoredAuditState(envelope=envelope, restored=True)
