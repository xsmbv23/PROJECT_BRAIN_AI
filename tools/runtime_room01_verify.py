"""Exact-current runtime verification for Room 01.

The canonical source remains owned by xsmbv23/xsmb-quant. Brain carries only
an explicitly sealed VERIFICATION_ONLY vector so the exact-current runtime can
exercise the real-source parsing/derivation path even when runtime egress/DNS
is unavailable. This vector is never promoted to canonical truth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rooms.room_01_data_admission import admit_manifest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures/room_01/2026-08-12/full27_fixture.json"
EXPECTED_FILE_SHA256 = "96328e7808165f60fd4513f2dbe77936c12e3fc3f918896c62e3f0049306e225"
EXPECTED_PAYLOAD_SHA256 = "d80bff3b3d8576263f9eb9c103656a8512360a8376b0d30b8ea1b5680291b76a"
EXPECTED_RECEIPT_SHA256 = "ed52d57f9e2b307a679b4fb0fbcc4088c40592e9a66bf786fcec69a97941f468"
EXPECTED_FIXTURE_ID = "XSMB-2026-08-12-REAL-SOURCE-001"


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> dict:
    try:
        raw = FIXTURE_PATH.read_bytes()
        manifest = json.loads(raw.decode("utf-8"))

        if manifest.get("fixture_id") != EXPECTED_FIXTURE_ID:
            raise RuntimeError("ROOM01_FIXTURE_ID_CHANGED")
        if manifest.get("source_file_sha256") != EXPECTED_FILE_SHA256:
            raise RuntimeError("ROOM01_SOURCE_HASH_CHANGED")
        if manifest.get("fixture_payload_sha256") != EXPECTED_PAYLOAD_SHA256:
            raise RuntimeError("ROOM01_FIXTURE_HASH_CHANGED")
        if manifest.get("fixture_status") != "VERIFICATION_ONLY":
            raise RuntimeError("ROOM01_SOURCE_STATUS_DENY")
        if manifest.get("provenance_owner") != "xsmbv23/xsmb-quant":
            raise RuntimeError("ROOM01_PROVENANCE_DENY")
        if manifest.get("canonical_eligibility") != "DENY_QUORUM_LT_2":
            raise RuntimeError("ROOM01_CANONICAL_STATUS_CHANGED")

        receipt = admit_manifest(manifest)
        if receipt.get("receipt_sha256") != EXPECTED_RECEIPT_SHA256:
            raise RuntimeError("ROOM01_RECEIPT_HASH_CHANGED")

        return {
            "status": "PASS",
            "action": "BRAIN-N090_DATA_ADMISSION_RUNTIME_VERIFY",
            "room": receipt["room"],
            "runtime": "EXACT_CURRENT",
            "source_fixture": manifest["fixture_id"],
            "source_owner": manifest["provenance_owner"],
            "source_file_sha256": manifest["source_file_sha256"],
            "fixture_payload_sha256": manifest["fixture_payload_sha256"],
            "receipt_sha256": receipt["receipt_sha256"],
            "admission": receipt["admission"],
            "canonical_eligibility": receipt["canonical_eligibility"],
            "research_admission": receipt["research_admission"],
            "staircase": receipt["staircase"],
            "verification_vector_sha256": _sha_bytes(raw),
            "verification_vector_policy": "SEALED_REAL_SOURCE_VECTOR;NOT_CANONICAL_TRUTH",
        }
    except Exception as exc:
        reason = str(exc)
        safe_reason = reason if reason.startswith("ROOM01_") else "RUNTIME_ROOM01_VERIFY_FAILURE"
        return {
            "status": "DENY",
            "action": "BRAIN-N090_DATA_ADMISSION_RUNTIME_VERIFY",
            "runtime": "EXACT_CURRENT",
            "reason": safe_reason,
            "exception_class": type(exc).__name__,
            "fixture_owner": "xsmbv23/xsmb-quant",
            "canonical_eligibility": "DENY_QUORUM_LT_2",
            "research_admission": "LOCKED",
            "staircase": "LOCKED",
        }


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True), flush=True)
