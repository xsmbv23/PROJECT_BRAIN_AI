import unittest

from tools.e2e_segment_guard import SegmentState, segment_reachable


class E2ESegmentGuardTests(unittest.TestCase):
    def test_root_segment_is_reachable(self):
        ok, reason = segment_reachable("S1", [])
        self.assertTrue(ok)
        self.assertEqual(reason, "ROOT_SEGMENT")

    def test_missing_predecessor_denies(self):
        ok, reason = segment_reachable("S3", [])
        self.assertFalse(ok)
        self.assertEqual(reason, "PREDECESSOR_MISSING:S2")

    def test_unverified_predecessor_denies(self):
        states = [SegmentState("S2", "PREPARED", "manifest-ref")]
        ok, reason = segment_reachable("S3", states)
        self.assertFalse(ok)
        self.assertEqual(reason, "PREDECESSOR_NOT_VERIFIED:S2:PREPARED")

    def test_verified_predecessor_without_exit_evidence_denies(self):
        states = [SegmentState("S2", "VERIFIED", "")]
        ok, reason = segment_reachable("S3", states)
        self.assertFalse(ok)
        self.assertEqual(reason, "PREDECESSOR_EXIT_EVIDENCE_MISSING:S2")

    def test_verified_predecessor_allows_reachability(self):
        states = [SegmentState("S2", "VERIFIED", "evidence://s2/exit")]
        ok, reason = segment_reachable("S3", states)
        self.assertTrue(ok)
        self.assertEqual(reason, "SEGMENT_REACHABLE")

    def test_duplicate_segment_denies(self):
        states = [
            SegmentState("S2", "VERIFIED", "evidence://1"),
            SegmentState("S2", "VERIFIED", "evidence://2"),
        ]
        ok, reason = segment_reachable("S3", states)
        self.assertFalse(ok)
        self.assertEqual(reason, "DUPLICATE_SEGMENT:S2")

    def test_invalid_segment_status_denies(self):
        states = [SegmentState("S2", "PASS", "evidence://s2")]
        ok, reason = segment_reachable("S3", states)
        self.assertFalse(ok)
        self.assertEqual(reason, "INVALID_SEGMENT_STATUS:S2")


if __name__ == "__main__":
    unittest.main()
