import unittest

from tools.source_adapters.ketqua16 import extract_candidates


class Ketqua16AdapterTests(unittest.TestCase):
    def test_empty_allowlist_extracts_nothing(self):
        html = b'<div class="official"><span>12345</span></div>'
        self.assertEqual(extract_candidates(html, []), ())

    def test_only_explicit_selector_is_candidate_source(self):
        html = b'''
        <div class="ad"><span>99999</span></div>
        <div class="official"><span>12345</span></div>
        '''
        rows = extract_candidates(html, ["div.official"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].selector, "div.official")
        self.assertEqual(rows[0].five_digit_values, ("12345",))

    def test_adapter_has_no_judgement_field(self):
        html = b'<div class="official">12345</div>'
        row = extract_candidates(html, ["div.official"])[0]
        self.assertFalse(hasattr(row, "status"))
        self.assertFalse(hasattr(row, "truth"))


if __name__ == "__main__":
    unittest.main()
