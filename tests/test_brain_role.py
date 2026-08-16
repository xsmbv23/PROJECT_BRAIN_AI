import unittest

from core.brain_role import BrainRole, Plane, PlaneRequest
from core.foundation_hardening import GovernanceDeny, PolicyPin


class BrainRoleTests(unittest.TestCase):
    def setUp(self):
        self.brain = BrainRole(PolicyPin("P1", "v1.0", "B1"))

    def req(self, destination=Plane.DATA, **kw):
        values = dict(source=Plane.CHAT, destination=destination,
                      policy_version="P1", schema_version="v1.2",
                      brain_state_version="B1", capability_id="CAP")
        values.update(kw)
        return PlaneRequest(**values)

    def test_brain_can_gate_data_request(self):
        self.assertEqual(self.brain.authorize(self.req(), expected_schema_major="v1"), "ADMISSIBLE_FOR_NEXT_GATE")

    def test_brain_cannot_be_called_as_destination_service(self):
        with self.assertRaises(GovernanceDeny):
            self.brain.authorize(self.req(Plane.BRAIN), expected_schema_major="v1")

    def test_policy_pin_is_mandatory(self):
        with self.assertRaises(GovernanceDeny):
            self.brain.authorize(self.req(policy_version="P2"), expected_schema_major="v1")

    def test_capability_is_mandatory(self):
        with self.assertRaises(GovernanceDeny):
            self.brain.authorize(self.req(capability_id=""), expected_schema_major="v1")

    def test_major_schema_change_is_denied(self):
        with self.assertRaises(GovernanceDeny):
            self.brain.authorize(self.req(schema_version="v2.0"), expected_schema_major="v1")
