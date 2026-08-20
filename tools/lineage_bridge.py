"""Bridge non-authoritative network receipts into the canonical lineage schema.

The bridge copies only observed metadata. It does not fetch data, invent hashes,
classify truth, promote state, or persist credentials.
"""
from __future__ import annotations

from typing import Any


def source_evidence_from_network_receipt(receipt: dict[str, Any], *, producer_component: str) -> dict[str, Any]:
    source_identity = receipt.get("url")
    observed_at = receipt.get("capture_timestamp_utc")
    raw_sha = receipt.get("response_sha256")
    if not source_identity or not observed_at or not raw_sha:
        raise ValueError("NETWORK_RECEIPT_LINEAGE_INCOMPLETE")

    return {
        "source_identity": source_identity,
        "observation_timestamp": observed_at,
        "observation_origin": "external_source",
        "raw_artifact_exists": True,
        "raw_artifact_sha256": raw_sha,
        "producer_component": producer_component,
        "derived": False,
        "authority": "source_observation",
    }
