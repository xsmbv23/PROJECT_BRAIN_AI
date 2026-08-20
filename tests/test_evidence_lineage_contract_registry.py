import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "contracts" / "evidence_lineage_contract_registry_v1.json"


class EvidenceLineageContractRegistryTests(unittest.TestCase):
    def test_exactly_one_current_authority(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        current = [x for x in data["contracts"] if x.get("classification") == "CURRENT_AUTHORITY"]
        self.assertEqual(len(current), 1)
        self.assertEqual(data["current_authority"], current[0]["path"])

    def test_legacy_lineage_contract_is_historical(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        legacy = next(x for x in data["contracts"] if x["path"] == "contracts/evidence_lineage_v1.json")
        self.assertEqual(legacy["classification"], "HISTORICAL_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
