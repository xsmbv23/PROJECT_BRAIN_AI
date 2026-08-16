import unittest

from core.corridor_lock import RoomLock, authorize_room
from core.foundation_hardening import GovernanceDeny


class CorridorLockTests(unittest.TestCase):
    def setUp(self):
        self.lock = RoomLock(
            room_id="ROOM_A", layer=0, capability_id="CAP_A",
            key_fingerprint="KEY_A", allowed_from=("HALL_A",),
            allowed_to=("ROOM_A",),
        )

    def test_correct_key_and_corridor_pass(self):
        authorize_room(self.lock, presented_capability="CAP_A", key_fingerprint="KEY_A",
                       source_room="HALL_A", destination_room="ROOM_A",
                       source_layer=0, destination_layer=0)

    def test_wrong_room_key_denies(self):
        with self.assertRaises(GovernanceDeny):
            authorize_room(self.lock, presented_capability="CAP_A", key_fingerprint="KEY_B",
                           source_room="HALL_A", destination_room="ROOM_A",
                           source_layer=0, destination_layer=0)

    def test_key_does_not_transfer_to_other_room(self):
        other = RoomLock("ROOM_B", 0, "CAP_B", "KEY_B", ("HALL_B",), ("ROOM_B",))
        with self.assertRaises(GovernanceDeny):
            authorize_room(other, presented_capability="CAP_A", key_fingerprint="KEY_A",
                           source_room="HALL_A", destination_room="ROOM_B",
                           source_layer=0, destination_layer=0)

    def test_wrong_layer_denies(self):
        with self.assertRaises(GovernanceDeny):
            authorize_room(self.lock, presented_capability="CAP_A", key_fingerprint="KEY_A",
                           source_room="HALL_A", destination_room="ROOM_A",
                           source_layer=1, destination_layer=0)
