import unittest

from core.access_path import AccessPathPolicy, CorridorKey, RoomKey, verify_access_path
from core.foundation_hardening import GovernanceDeny
from core.inner_latch import InnerLatch, InnerLatchPolicy, InnerLatchState


class AccessPathTests(unittest.TestCase):
    def policy(self, protected=True):
        return AccessPathPolicy(
            corridor_id="HALL_A",
            destination_room="OWNER_ROOM",
            corridor_key=CorridorKey("HALL_A", "CORRIDOR_KEY_A"),
            room_key=RoomKey("OWNER_ROOM", "ROOM_KEY_A"),
            protected=protected,
        )

    def latch(self):
        return InnerLatch(InnerLatchPolicy("OWNER_ROOM", 3, True, ("OWNER_PRESENT",)))

    def test_both_keys_are_required(self):
        with self.assertRaises(GovernanceDeny):
            verify_access_path(policy=self.policy(False), corridor_key_fingerprint="BAD", room_key_fingerprint="ROOM_KEY_A")
        with self.assertRaises(GovernanceDeny):
            verify_access_path(policy=self.policy(False), corridor_key_fingerprint="CORRIDOR_KEY_A", room_key_fingerprint="BAD")
        self.assertEqual(verify_access_path(policy=self.policy(False), corridor_key_fingerprint="CORRIDOR_KEY_A", room_key_fingerprint="ROOM_KEY_A"), "ENTRY_AUTHORIZED")

    def test_protected_room_only_rings_after_both_keys(self):
        latch = self.latch()
        result = verify_access_path(policy=self.policy(True), corridor_key_fingerprint="CORRIDOR_KEY_A", room_key_fingerprint="ROOM_KEY_A", latch=latch)
        self.assertEqual(result, "DOORBELL_RUNG_WAITING_FOR_INSIDE_RELEASE")
        self.assertEqual(latch.state, InnerLatchState.RINGING)

    def test_protected_room_cannot_bypass_latch(self):
        latch = self.latch()
        verify_access_path(policy=self.policy(True), corridor_key_fingerprint="CORRIDOR_KEY_A", room_key_fingerprint="ROOM_KEY_A", latch=latch)
        with self.assertRaises(GovernanceDeny):
            latch.assert_entry_released()
