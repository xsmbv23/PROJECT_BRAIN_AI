import unittest

from core.foundation_hardening import GovernanceDeny
from core.inner_latch import InnerLatch, InnerLatchPolicy, InnerLatchState


class InnerLatchTests(unittest.TestCase):
    def setUp(self):
        self.latch = InnerLatch(InnerLatchPolicy(
            room_id="OWNER_ROOM",
            security_level=3,
            requires_inner_release=True,
            authorized_occupant_capabilities=("OWNER_PRESENT",),
        ))

    def test_valid_request_only_rings(self):
        self.latch.request_entry(room_id="OWNER_ROOM", external_authorized=True)
        self.assertEqual(self.latch.state, InnerLatchState.RINGING)

    def test_valid_key_does_not_bypass_inner_latch(self):
        self.latch.request_entry(room_id="OWNER_ROOM", external_authorized=True)
        with self.assertRaises(GovernanceDeny):
            self.latch.assert_entry_released()

    def test_unauthorized_occupant_cannot_release(self):
        self.latch.request_entry(room_id="OWNER_ROOM", external_authorized=True)
        with self.assertRaises(GovernanceDeny):
            self.latch.release_from_inside(occupant_capability="GUEST")

    def test_authorized_occupant_releases(self):
        self.latch.request_entry(room_id="OWNER_ROOM", external_authorized=True)
        self.latch.release_from_inside(occupant_capability="OWNER_PRESENT")
        self.latch.assert_entry_released()
        self.assertEqual(self.latch.state, InnerLatchState.RELEASED)

    def test_no_request_means_no_release(self):
        with self.assertRaises(GovernanceDeny):
            self.latch.release_from_inside(occupant_capability="OWNER_PRESENT")
