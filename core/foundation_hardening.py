"""Compact executable Brain governance primitives.

This module is intentionally independent of the chat UI and data plane.
It provides deterministic policy pinning, expiring capability leases,
quarantine, circuit breaking, schema-major validation, and tamper-evident
append-only audit events. It stores metadata only.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import time
from typing import Any


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class GovernanceDeny(Exception):
    pass


def _schema_major(version: str) -> str:
    parts = version.strip().split(".")
    if len(parts) < 2 or not parts[0].startswith("v") or not parts[0][1:].isdigit() or not parts[1].isdigit():
        raise GovernanceDeny("SCHEMA_VERSION_INVALID")
    return f"{parts[0]}.0"


@dataclass(frozen=True)
class PolicyPin:
    policy_version: str
    schema_version: str
    brain_state_version: str

    def verify(self, *, policy_version: str, schema_version: str, brain_state_version: str) -> None:
        if policy_version != self.policy_version or brain_state_version != self.brain_state_version:
            raise GovernanceDeny("POLICY_PIN_MISMATCH")
        if _schema_major(schema_version) != _schema_major(self.schema_version):
            raise GovernanceDeny("SCHEMA_MAJOR_PIN_MISMATCH")


@dataclass(frozen=True)
class CapabilityLease:
    capability_id: str
    corridor_id: str
    source_layer: str
    destination_layer: str
    issued_at: float
    expires_at: float
    nonce: str
    policy_version: str
    max_operations: int

    def verify(self, *, now: float, corridor_id: str, capability_id: str,
               nonce: str, policy_version: str, operation_count: int) -> None:
        if now >= self.expires_at:
            raise GovernanceDeny("CAPABILITY_EXPIRED")
        if corridor_id != self.corridor_id or capability_id != self.capability_id:
            raise GovernanceDeny("CAPABILITY_SCOPE_MISMATCH")
        if nonce != self.nonce or policy_version != self.policy_version:
            raise GovernanceDeny("CAPABILITY_REPLAY_OR_POLICY_MISMATCH")
        if operation_count >= self.max_operations:
            raise GovernanceDeny("CAPABILITY_OPERATION_LIMIT")


class CircuitBreaker:
    def __init__(self, *, threshold: int = 3, cooldown_seconds: float = 300.0) -> None:
        if threshold < 1 or cooldown_seconds <= 0:
            raise ValueError("invalid circuit breaker configuration")
        self.threshold = threshold
        self.cooldown_seconds = cooldown_seconds
        self.failures = 0
        self.opened_at: float | None = None

    @property
    def open(self) -> bool:
        return self.opened_at is not None

    def allow(self, now: float) -> None:
        if self.opened_at is None:
            return
        if now - self.opened_at >= self.cooldown_seconds:
            self.failures = 0
            self.opened_at = None
            return
        raise GovernanceDeny("CIRCUIT_BREAKER_OPEN")

    def failure(self, now: float) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.opened_at = now


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    event_type: str
    policy_version: str
    payload: dict[str, Any]
    timestamp: float
    prev_hash: str
    event_hash: str


class AuditChain:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, *, event_id: str, event_type: str, policy_version: str,
               payload: dict[str, Any], timestamp: float) -> AuditEvent:
        prev = self.events[-1].event_hash if self.events else "GENESIS"
        material = _canonical({"event_id": event_id, "event_type": event_type,
                               "policy_version": policy_version, "payload": payload,
                               "timestamp": timestamp, "prev_hash": prev})
        digest = hashlib.sha256(material).hexdigest()
        event = AuditEvent(event_id, event_type, policy_version, payload, timestamp, prev, digest)
        self.events.append(event)
        return event

    @property
    def head(self) -> str:
        return self.events[-1].event_hash if self.events else "GENESIS"
