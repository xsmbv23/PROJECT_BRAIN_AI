"""Second-person / inner-latch authorization for high-security rooms.

A valid external capability is necessary but insufficient for protected rooms.
The room must explicitly require an inner-latch release, and that release must
be produced by an authorized presence inside the room after a doorbell/request.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .foundation_hardening import GovernanceDeny


class InnerLatchState(str, Enum):
    SECURED = "SECURED"
    RINGING = "RINGING"
    RELEASED = "RELEASED"


@dataclass(frozen=True)
class InnerLatchPolicy:
    room_id: str
    security_level: int
    requires_inner_release: bool
    authorized_occupant_capabilities: tuple[str, ...]


@dataclass
class InnerLatch:
    policy: InnerLatchPolicy
    state: InnerLatchState = InnerLatchState.SECURED

    def request_entry(self, *, room_id: str, external_authorized: bool) -> None:
        if room_id != self.policy.room_id:
            raise GovernanceDeny("INNER_LATCH_ROOM_DENY")
        if not external_authorized:
            raise GovernanceDeny("INNER_LATCH_EXTERNAL_AUTH_DENY")
        if not self.policy.requires_inner_release:
            self.state = InnerLatchState.RELEASED
            return
        self.state = InnerLatchState.RINGING

    def release_from_inside(self, *, occupant_capability: str) -> None:
        if not self.policy.requires_inner_release:
            raise GovernanceDeny("INNER_RELEASE_NOT_REQUIRED")
        if self.state != InnerLatchState.RINGING:
            raise GovernanceDeny("INNER_RELEASE_NO_ACTIVE_REQUEST")
        if occupant_capability not in self.policy.authorized_occupant_capabilities:
            raise GovernanceDeny("INNER_RELEASE_OCCUPANT_DENY")
        self.state = InnerLatchState.RELEASED

    def assert_entry_released(self) -> None:
        if self.state != InnerLatchState.RELEASED:
            raise GovernanceDeny("INNER_LATCH_SECURED")
