import unittest

from core.corridor_lock import RoomLock
from core.foundation_hardening import GovernanceDeny
from core.inner_latch import InnerLatch, InnerLatchPolicy, InnerLatchState
from core.security_chain import evaluate_entry_request


class SecurityChainTests(unittest.TestCase):
    def room(self):
        return RoomLock("OWNER_ROOM", 3, "CAP_A", "KEY_A", ("HALL_A",), ("OWNER_ROOM",), ((2, 3),))

    def protected_latch(self):
        return InnerLatch(InnerLatchPolicy("OWNER_ROOM", 3, True, ("OWNER_PRESENT",)))

    def test_correct_external_credentials_still_require_inner_release(self):
        latch = self.protected_latch()
        decision = evaluate_entry_request(
            lock=self.room(), latch=latch,
            corridor_id="HALL_A", sensor_id="S1",
            source_room="HALL_A", destination_room="OWNER_ROOM",
            source_layer=2, destination_layer=3,
            capability="CAP_A", key_fingerprint="KEY_A",
        )
        self.assertTrue(decision.external_authorized)
        self.assertFalse(decision.entry_authorized)
        self.assertEqual(latch.state, InnerLatchState.RINGING)

    def test_wrong_credentials_never_activate_inner_release(self):
        latch = self.protected_latch()
        decision = evaluate_entry_request(
            lock=self.room(), latch=latch,
            corridor_id="HALL_A", sensor_id="S1",
            source_room="HALL_A", destination_room="OWNER_ROOM",
            source_layer=2, destination_layer=3,
            capability="CAP_X", key_fingerprint="KEY_X",
        )
        self.assertFalse(decision.external_authorized)
        self.assertFalse(decision.entry_authorized)
        self.assertEqual(latch.state, InnerLatchState.SECURED)

    def test_wrong_direction_is_denied_before_latch_request(self):
        latch = self.protected_latch()
        decision = evaluate_entry_request(
            lock=self.room(), latch=latch,
            corridor_id="HALL_A", sensor_id="S1",
            source_room="HALL_A", destination_room="OWNER_ROOM",
            source_layer=3, destination_layer=2,
            capability="CAP_A", key_fingerprint="KEY_A",
        )
        self.assertFalse(decision.external_authorized)
        self.assertEqual(latch.state, InnerLatchState.SECURED)

    def test_sensor_signal_never_becomes_authority(self):
        latch = self.protected_latch()
        decision = evaluate_entry_request(
            lock=self.room(), latch=latch,
            corridor_id="HALL_A", sensor_id="S1",
            source_room="HALL_A", destination_room="OWNER_ROOM",
            source_layer=2, destination_layer=3,
            capability="CAP_A", key_fingerprint="KEY_A",
        )
        self.assertTrue(decision.corridor_signal.light_on)
        self.assertFalse(decision.entry_authorized)

    def test_inner_release_is_the_only_final_step(self):
        latch = self.protected_latch()
        evaluate_entry_request(
            lock=self.room(), latch=latch,
            corridor_id="HALL_A", sensor_id="S1",
            source_room="HALL_A", destination_room="OWNER_ROOM",
            source_layer=2, destination_layer=3,
            capability="CAP_A", key_fingerprint="KEY_A",
        )
        with self.assertRaises(GovernanceDeny):
            latch.release_from_inside(occupant_capability="GUEST")
        latch.release_from_inside(occupant_capability="OWNER_PRESENT")
        latch.assert_entry_released()
