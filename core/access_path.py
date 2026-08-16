"""Explicit two-key access path for Fosennic foundation security.

A visitor needs a corridor capability/key AND a destination-room key.
Protected rooms add a third, human-mediated gate: ring and wait for an
authorized occupant to release the inner latch.
"""
from __future__ import annotations

from dataclasses import dataclass

from .foundation_hardening import GovernanceDeny
from .inner_latch import InnerLatch


@dataclass(frozen=True)
class CorridorKey:
    corridor_id: str
    fingerprint: str


@dataclass(frozen=True)
class RoomKey:
    room_id: str
    fingerprint: str


@dataclass(frozen=True)
class AccessPathPolicy:
    corridor_id: str
    destination_room: str
    corridor_key: CorridorKey
    room_key: RoomKey
    protected: bool


def verify_access_path(
    *,
    policy: AccessPathPolicy,
    corridor_key_fingerprint: str,
    room_key_fingerprint: str,
    latch: InnerLatch | None = None,
) -> str:
    """Return only the highest state actually proven; fail closed otherwise."""
    if corridor_key_fingerprint != policy.corridor_key.fingerprint:
        raise GovernanceDeny("CORRIDOR_KEY_DENY")
    if room_key_fingerprint != policy.room_key.fingerprint:
        raise GovernanceDeny("ROOM_KEY_DENY")
    if not policy.protected:
        return "ENTRY_AUTHORIZED"
    if latch is None:
        raise GovernanceDeny("INNER_LATCH_REQUIRED")
    latch.request_entry(room_id=policy.destination_room, external_authorized=True)
    return "DOORBELL_RUNG_WAITING_FOR_INSIDE_RELEASE"
