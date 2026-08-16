"""Fail-closed composition of Fosennic foundation security boundaries."""
from __future__ import annotations

from dataclasses import dataclass

from .corridor_lock import RoomLock, authorize_room
from .corridor_sensor import CorridorSignal, sense_corridor_presence
from .foundation_hardening import GovernanceDeny
from .inner_latch import InnerLatch


@dataclass(frozen=True)
class SecurityDecision:
    corridor_signal: CorridorSignal
    external_authorized: bool
    entry_authorized: bool
    reason: str


def evaluate_entry_request(
    *,
    lock: RoomLock,
    latch: InnerLatch,
    corridor_id: str,
    sensor_id: str,
    source_room: str,
    destination_room: str,
    source_layer: int,
    destination_layer: int,
    capability: str,
    key_fingerprint: str,
) -> SecurityDecision:
    """Evaluate a request without ever allowing a sensor to grant access.

    The function is deliberately ordered: observe -> authorize request ->
    request inner release -> assert release. No later state may be inferred
    from an earlier signal.
    """
    signal = sense_corridor_presence(
        corridor_id=corridor_id,
        sensor_id=sensor_id,
        source_room=source_room,
        destination_room=destination_room,
        authorized=False,
    )
    try:
        authorize_room(
            lock,
            presented_capability=capability,
            key_fingerprint=key_fingerprint,
            source_room=source_room,
            destination_room=destination_room,
            source_layer=source_layer,
            destination_layer=destination_layer,
        )
    except GovernanceDeny as exc:
        return SecurityDecision(signal, False, False, str(exc))

    latch.request_entry(room_id=destination_room, external_authorized=True)
    try:
        latch.assert_entry_released()
    except GovernanceDeny as exc:
        return SecurityDecision(signal, True, False, str(exc))
    return SecurityDecision(signal, True, True, "ENTRY_RELEASED")
