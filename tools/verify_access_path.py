"""Small deterministic verifier for the access-path security boundary."""
from __future__ import annotations

from core.access_path import AccessPathPolicy, CorridorKey, RoomKey, verify_access_path
from core.foundation_hardening import GovernanceDeny
from core.inner_latch import InnerLatch, InnerLatchPolicy, InnerLatchState


def main() -> int:
    policy = AccessPathPolicy(
        corridor_id="HALL_A",
        destination_room="OWNER_ROOM",
        corridor_key=CorridorKey("HALL_A", "CORRIDOR_KEY_A"),
        room_key=RoomKey("OWNER_ROOM", "ROOM_KEY_A"),
        protected=True,
    )
    latch = InnerLatch(InnerLatchPolicy("OWNER_ROOM", 3, True, ("OWNER_PRESENT",)))

    # Wrong corridor key: deny before the room key can matter.
    try:
        verify_access_path(policy=policy, corridor_key_fingerprint="BAD", room_key_fingerprint="ROOM_KEY_A", latch=latch)
    except GovernanceDeny:
        pass
    else:
        return 1

    # Both keys: request only. Protected room must remain latched.
    state = verify_access_path(
        policy=policy,
        corridor_key_fingerprint="CORRIDOR_KEY_A",
        room_key_fingerprint="ROOM_KEY_A",
        latch=latch,
    )
    if state != "DOORBELL_RUNG_WAITING_FOR_INSIDE_RELEASE":
        return 2
    if latch.state != InnerLatchState.RINGING:
        return 3

    try:
        latch.assert_entry_released()
    except GovernanceDeny:
        pass
    else:
        return 4

    latch.release_from_inside(occupant_capability="OWNER_PRESENT")
    latch.assert_entry_released()
    print({"status": "PASS", "protected_room": "OWNER_ROOM", "state": latch.state.value})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
