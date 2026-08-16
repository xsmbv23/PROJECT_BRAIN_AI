import unittest

from core.corridor_sensor import sense_corridor_presence


class CorridorSensorTests(unittest.TestCase):
    def test_authorized_approach_turns_light_on_without_granting_access(self):
        signal = sense_corridor_presence(
            corridor_id="HALL_A", sensor_id="SENSOR_A",
            source_room="HALL_A", destination_room="ROOM_A", authorized=True,
        )
        self.assertTrue(signal.light_on)
        self.assertEqual(signal.level, "INFO")
        self.assertEqual(signal.event, "CORRIDOR_ACCESS_ATTEMPT")

    def test_unauthorized_approach_turns_light_on_and_warns(self):
        signal = sense_corridor_presence(
            corridor_id="HALL_A", sensor_id="SENSOR_A",
            source_room="HALL_X", destination_room="ROOM_A", authorized=False,
        )
        self.assertTrue(signal.light_on)
        self.assertEqual(signal.level, "WARNING")
        self.assertEqual(signal.event, "UNAUTHORIZED_CORRIDOR_APPROACH")
