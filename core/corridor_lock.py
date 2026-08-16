"""Fail-closed per-room lock model.

Every Brain room has an independent lock/capability. Possessing one key never
implies access to another room. Parent/child layer direction is explicit.
"""
from __future__ import annotations

from dataclasses import dataclass
from .foundation_hardening import GovernanceDeny


@dataclass(frozen=True)
class RoomLock:
    room_id: str
    layer: int
    capability_id: str
    key_fingerprint: str
    allowed_from: tuple[str, ...]
    allowed_to: tuple[str, ...]


def authorize_room(lock: RoomLock, *, presented_capability: str,
                   key_fingerprint: str, source_room: str,
                   destination_room: str, source_layer: int,
                   destination_layer: int) -> None:
    if presented_capability != lock.capability_id:
        raise GovernanceDeny("ROOM_CAPABILITY_DENY")
    if key_fingerprint != lock.key_fingerprint:
        raise GovernanceDeny("ROOM_KEY_DENY")
    if source_room not in lock.allowed_from:
        raise GovernanceDeny("CORRIDOR_SOURCE_DENY")
    if destination_room not in lock.allowed_to:
        raise GovernanceDeny("CORRIDOR_DESTINATION_DENY")
    if source_layer != lock.layer:
        raise GovernanceDeny("SOURCE_LAYER_DENY")
    if destination_layer != lock.layer:
        raise GovernanceDeny("DESTINATION_LAYER_DENY")
