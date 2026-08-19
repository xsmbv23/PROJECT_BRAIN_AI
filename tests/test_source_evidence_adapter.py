import unittest

from tools.source_evidence_adapter import ALLOWED_GRADES, EXPECTED_COUNTS, extract_xsmb_candidate


class SourceEvidenceAdapterTests(unittest.TestCase):
    def test_allowed_grades_are_exact(self):
        self.assertEqual(ALLOWED_GRADES, ("ĐB", "G1", "G2", "G3", "G4", "G5", "G6", "G7"))

    def test_non_result_tables_cannot_become_candidates(self):
        html = "<table><tr><td>Quảng cáo</td><td>12345</td></tr></table>"
        result = extract_xsmb_candidate(html, "https://ketqua16.net/", "2026-08-19T00:00:00+00:00")
        self.assertEqual(result.status, "NO_RESULT_TABLE_CANDIDATE")
        self.assertEqual(result.grade_rows, {})

    def test_candidate_never_has_canonical_authority(self):
        rows = []
        widths = {"ĐB": 5, "G1": 5, "G2": 5, "G3": 5, "G4": 4, "G5": 4, "G6": 3, "G7": 2}
        for grade in ALLOWED_GRADES:
            for i in range(EXPECTED_COUNTS[grade]):
                rows.append(f"<tr><td>{grade}</td><td>{str(i + 1).zfill(widths[grade])}</td></tr>")
        result = extract_xsmb_candidate("<table>" + "".join(rows) + "</table>", "https://ketqua16.net/", "2026-08-19T00:00:00+00:00")
        self.assertEqual(result.status, "CANDIDATE_ONLY")
        self.assertEqual(result.row_count, 27)
        self.assertFalse(hasattr(result, "canonical_truth"))
        self.assertFalse(hasattr(result, "signal"))
        self.assertFalse(hasattr(result, "prediction"))


if __name__ == "__main__":
    unittest.main()
