import unittest

from core.brain_role import BrainRole, Plane, PlaneRequest
from core.foundation_hardening import CapabilityLease, GovernanceDeny, PolicyPin


class BrainRoleTests(unittest.TestCase):
    def setUp(self):
        self.brain = BrainRole(PolicyPin("P1", "v1.0", "B1"))
        self.lease = CapabilityLease(
            capability_id="CAP",
            corridor_id="HALL_A",
            source_layer="CHAT",
            destination_layer="DATA",
            issued_at=90.0,
            expires_at=200.0,
            nonce="N1",
            policy_version="P1",
            max_operations=3,
        )

    def req(self, destination=Plane.DATA, **kw):
        values = dict(source=Plane.CHAT, destination=destination,
                      corridor_id="HALL_A", policy_version="P1",
                      schema_version="v1.2", brain_state_version="B1",
                      capability_id="CAP", nonce="N1")
        values.update(kw)
        return PlaneRequest(**values)

    def auth(self, request=None, lease=None):
        return self.brain.authorize(request or self.req(), lease=lease or self.lease,
                                    expected_schema_major="v1", now=100.0)

    def test_brain_can_gate_scoped_data_request(self):
        self.assertEqual(self.auth(), "ADMISSIBLE_FOR_NEXT_GATE")

    def test_brain_cannot_be_called_as_destination_service(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(Plane.BRAIN))

    def test_policy_pin_is_mandatory(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(policy_version="P2"))

    def test_capability_is_mandatory(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(capability_id=""))

    def test_nonce_is_mandatory(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(nonce=""))

    def test_major_schema_change_is_denied(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(schema_version="v2.0"))

    def test_expired_lease_is_denied(self):
        expired = CapabilityLease(**{**self.lease.__dict__, "expires_at": 100.0})
        with self.assertRaises(GovernanceDeny):
            self.auth(lease=expired)

    def test_wrong_corridor_is_denied(self):
        with self.assertRaises(GovernanceDeny):
            self.auth(self.req(corridor_id="HALL_B"))

    def test_wrong_destination_layer_is_denied(self):
        wrong = CapabilityLease(**{**self.lease.__dict__, "destination_layer": "ENGINE"})
        with self.assertRaises(GovernanceDeny):
            self.auth(lease=wrong)

    def test_brain_pass_is_not_final_authority(self):
        self.assertEqual(self.auth(), "ADMISSIBLE_FOR_NEXT_GATE")
