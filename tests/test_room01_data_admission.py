import unittest

from rooms.room_01_data_admission import admit_manifest


FIXTURE = {
    "fixture_status": "VERIFICATION_ONLY",
    "fixture_id": "XSMB-2026-08-12-REAL-SOURCE-001",
    "source_file": "Ket_Qua_Loto27.xlsx",
    "source_file_sha256": "96328e7808165f60fd4513f2dbe77936c12e3fc3f918896c62e3f0049306e225",
    "fixture_payload_sha256": "d80bff3b3d8576263f9eb9c103656a8512360a8376b0d30b8ea1b5680291b76a",
    "source_row_date": "12/08/2026",
    "source_count": 1,
    "source_prizes": ["82326","31773","64497","88592","50195","46812","80982","66597","76120","13434","0172","0162","3526","0188","3050","2194","4509","7308","9434","6888","540","059","081","21","97","42","00"],
    "semantic_lengths": [5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,3,3,3,2,2,2,2],
}


class Room01Tests(unittest.TestCase):
    def test_admits_artifact_but_denies_canonical_promotion(self):
        receipt = admit_manifest(FIXTURE)
        self.assertEqual(receipt["admission"], "PASS")
        self.assertEqual(receipt["full27_count"], 27)
        self.assertEqual(receipt["canonical_eligibility"], "DENY_QUORUM_LT_2")
        self.assertEqual(receipt["research_admission"], "LOCKED")
        self.assertEqual(receipt["staircase"], "LOCKED")
        self.assertTrue(receipt["receipt_sha256"])

    def test_tail_derivation_is_deterministic(self):
        receipt = admit_manifest(FIXTURE)
        self.assertEqual(receipt["tail27"], ["26","73","97","92","95","12","82","97","20","34","72","62","26","88","50","94","09","08","34","88","40","59","81","21","97","42","00"])

    def test_future_date_is_denied(self):
        bad = dict(FIXTURE)
        bad["source_row_date"] = "12/08/2099"
        with self.assertRaisesRegex(ValueError, "ROOM01_FUTURE_DATE_DENY"):
            admit_manifest(bad)


if __name__ == "__main__":
    unittest.main()
