import unittest

from tools.result_transport_probe import classify


class ResultTransportProbeTests(unittest.TestCase):
    def test_raw_html_result(self):
        result = classify('<table><tr><td>12345</td></tr></table>')
        self.assertEqual(result['status'], 'RAW_HTML_RESULT')
        self.assertTrue(result['raw_html_result'])

    def test_embedded_json(self):
        result = classify('<script type="application/json">{"results":[12345]}</script>')
        self.assertEqual(result['status'], 'EMBEDDED_JSON')
        self.assertTrue(result['embedded_json'])

    def test_secondary_transport_hint(self):
        result = classify('<script>fetch("/api/results.json").then(x => x.json())</script>')
        self.assertEqual(result['status'], 'SECONDARY_TRANSPORT_HINT')
        self.assertTrue(result['js_generated_hint'])
        self.assertTrue(result['secondary_endpoint_hint'])

    def test_no_transport_is_deny(self):
        result = classify('<html><body><div>DB G1 G2 G3 G4 G5 G6 G7</div></body></html>')
        self.assertEqual(result['status'], 'NO_RESULT_TRANSPORT_PROVEN')
        self.assertEqual(result['candidate_numbers'], 0)


if __name__ == '__main__':
    unittest.main()
