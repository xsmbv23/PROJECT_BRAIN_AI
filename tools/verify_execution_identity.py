"""Verify an execution identity manifest without performing network capture.

The verifier treats source identity as chain-of-custody state. It deliberately
cannot promote a source to PROVEN; that requires a later network-origin gate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "state" / "execution_identity_manifest_N099.json"


def canonical_without_execution_id(doc: dict) -> bytes:
    copy = dict(doc)
    copy.pop("execution_id", None)
    return json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def main() -> int:
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    required = ["manifest_schema_version", "target_date", "source_a", "source_b", "parser_version", "canonicalization_version", "selection_policy", "capture_admission"]
    missing = [k for k in required if k not in doc]
    if missing:
        print(json.dumps({"execution_identity":"DENY","reason":"MISSING_FIELDS","fields":missing}))
        return 1
    if doc["manifest_status"] != "REGISTERED_NOT_PROVEN":
        print(json.dumps({"execution_identity":"DENY","reason":"INVALID_STATUS"}))
        return 1
    if doc["capture_admission"] != "DENY_UNTIL_NETWORK_ORIGIN_PROOF":
        print(json.dumps({"execution_identity":"DENY","reason":"CAPTURE_NOT_DEFAULT_DENY"}))
        return 1
    if doc["source_a"]["identity"] == doc["source_b"]["identity"]:
        print(json.dumps({"execution_identity":"DENY","reason":"SOURCE_PAIR_NOT_DISTINCT"}))
        return 1
    execution_id = "EXEC-" + hashlib.sha256(canonical_without_execution_id(doc)).hexdigest()
    print(json.dumps({
        "execution_identity":"PASS_REGISTRATION",
        "execution_id":execution_id,
        "target_date":doc["target_date"],
        "source_a":doc["source_a"]["identity"],
        "source_b":doc["source_b"]["identity"],
        "capture_admission":doc["capture_admission"],
        "canonical_quorum":doc["canonical_quorum"],
        "promotion":doc["promotion"]
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
