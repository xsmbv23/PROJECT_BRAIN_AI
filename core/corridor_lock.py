"""Fail-closed per-room lock and corridor authorization.

Every room has its own capability/key. Layer transitions are explicit edges;
a key never grants an implicit jump to another layer or room.
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
    allowed_layer_edges: tuple[tuple[int, int], ...] = ()


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
    if (source_layer, destination_layer) not in lock.allowed_layer_edges:
        raise GovernanceDeny("LAYER_EDGE_DENY")
    if destination_layer != lock.layer:
        raise GovernanceDeny("DESTINATION_LAYER_DENY")
