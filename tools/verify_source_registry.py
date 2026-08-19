"""Validate source registry structure without promoting any source."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "contracts" / "source_registry.json"
REQUIRED = {"source_id", "display_name", "endpoint_type", "target_date", "raw_preservation_policy", "last_verified_status", "independence_status"}


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["promotion_status"] == "DENY"
    assert data["rules"]["source_registration_is_not_source_verification"] is True
    assert data["rules"]["source_registration_is_not_quorum"] is True
    assert data["rules"]["independence_requires_observable_evidence"] is True
    assert data["rules"]["credentials_in_registry"] is False
    assert len(data["sources"]) >= 2
    for source in data["sources"]:
        assert REQUIRED.issubset(source)
        assert source["last_verified_status"] in {"pending", "verified", "failed"}
        assert source["independence_status"] in {"not_proven", "proven", "collision"}
    print({"source_registry": "PASS", "sources": len(data["sources"]), "promotion": "DENY"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
