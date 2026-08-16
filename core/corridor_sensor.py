"""Passive corridor warning sensor.

A sensor may illuminate a corridor and emit a security event, but it never
creates access. Observation and authorization are deliberately separate.
"""
from __future__ import annotations

from dataclasses import dataclass
from .foundation_hardening import GovernanceDeny


@dataclass(frozen=True)
class CorridorSignal:
    corridor_id: str
    sensor_id: str
    level: str
    light_on: bool
    event: str


def sense_corridor_presence(*, corridor_id: str, sensor_id: str,
                            source_room: str, destination_room: str,
                            authorized: bool) -> CorridorSignal:
    if not corridor_id or not sensor_id:
        raise GovernanceDeny("CORRIDOR_SENSOR_ID_DENY")
    level = "INFO" if authorized else "WARNING"
    event = "CORRIDOR_ACCESS_ATTEMPT" if authorized else "UNAUTHORIZED_CORRIDOR_APPROACH"
    return CorridorSignal(corridor_id, sensor_id, level, True, event)
