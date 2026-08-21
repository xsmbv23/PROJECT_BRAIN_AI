import unittest

from tools.evidence_intake_router import AcquisitionChannel, EvidenceAdmission, admission_channels


class EvidenceIntakeRouterTests(unittest.TestCase):
    def valid(self, channel):
        return EvidenceAdmission(
            channel=channel,
            provenance="authorized-source",
            acquired_at="2026-08-21T03:00:00Z",
            raw_sha256="a" * 64,
            raw_bytes=123,
            coverage=1.0,
            unresolved_conflicts=0,
            synthetic_data=False,
        )

    def test_all_channels_share_same_gate(self):
        self.assertEqual(set(admission_channels()), {c.value for c in AcquisitionChannel})
        for channel in AcquisitionChannel:
            self.valid(channel).admit()

    def test_missing_provenance_denied(self):
        evidence = self.valid(AcquisitionChannel.MANUAL_AUTHORIZED)
        with self.assertRaisesRegex(ValueError, "DENY_PROVENANCE_MISSING"):
            evidence.__class__(**{**evidence.__dict__, "provenance": ""}).admit()

    def test_incomplete_coverage_denied(self):
        evidence = self.valid(AcquisitionChannel.DURABLE_ARCHIVE_EXPORT)
        with self.assertRaisesRegex(ValueError, "DENY_COVERAGE_NOT_COMPLETE"):
            evidence.__class__(**{**evidence.__dict__, "coverage": 0.99}).admit()

    def test_synthetic_data_denied(self):
        evidence = self.valid(AcquisitionChannel.AUTOMATED_EXPLICIT)
        with self.assertRaisesRegex(ValueError, "DENY_SYNTHETIC_DATA"):
            evidence.__class__(**{**evidence.__dict__, "synthetic_data": True}).admit()

    def test_conflict_denied(self):
        evidence = self.valid(AcquisitionChannel.AUTOMATED_EXPLICIT)
        with self.assertRaisesRegex(ValueError, "DENY_UNRESOLVED_CONFLICTS"):
            evidence.__class__(**{**evidence.__dict__, "unresolved_conflicts": 1}).admit()


if __name__ == "__main__":
    unittest.main()
