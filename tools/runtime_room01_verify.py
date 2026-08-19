"""Exact-current runtime verification for Room 01.

The fixture remains owned by xsmbv23/xsmb-quant. Brain fetches only the
credential-free JSON fixture over HTTPS, verifies its immutable content hashes,
then executes Room 01 locally in the Render runtime. No fixture is copied into
Brain as a second source of truth.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

from rooms.room_01_data_admission import admit_manifest

FIXTURE_URL = "https://raw.githubusercontent.com/xsmbv23/xsmb-quant/main/fixtures/2026-08-12/full27_fixture.json"
EXPECTED_FILE_SHA256 = "96328e7808165f60fd4513f2dbe77936c12e3fc3f918896c62e3f0049306e225"
EXPECTED_PAYLOAD_SHA256 = "d80bff3b3d8576263f9eb9c103656a8512360a8376b0d30b8ea1b5680291b76a"
EXPECTED_RECEIPT_SHA256 = "ed52d57f9e2b307a679b4fb0fbcc4088c40592e9a66bf786fcec69a97941f468"


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> dict:
    with urllib.request.urlopen(FIXTURE_URL, timeout=15) as response:
        raw = response.read()
    manifest = json.loads(raw.decode("utf-8"))

    if manifest.get("source_file_sha256") != EXPECTED_FILE_SHA256:
        raise RuntimeError("ROOM01_SOURCE_HASH_CHANGED")
    if manifest.get("fixture_payload_sha256") != EXPECTED_PAYLOAD_SHA256:
        raise RuntimeError("ROOM01_FIXTURE_HASH_CHANGED")
    if manifest.get("fixture_status") != "VERIFICATION_ONLY":
        raise RuntimeError("ROOM01_SOURCE_STATUS_DENY")

    receipt = admit_manifest(manifest)
    if receipt.get("receipt_sha256") != EXPECTED_RECEIPT_SHA256:
        raise RuntimeError("ROOM01_RECEIPT_HASH_CHANGED")

    return {
        "action": "BRAIN-N090_DATA_ADMISSION_RUNTIME_VERIFY",
        "room": receipt["room"],
        "runtime": "EXACT_CURRENT",
        "source_fixture": manifest["fixture_id"],
        "source_file_sha256": manifest["source_file_sha256"],
        "fixture_payload_sha256": manifest["fixture_payload_sha256"],
        "receipt_sha256": receipt["receipt_sha256"],
        "admission": receipt["admission"],
        "canonical_eligibility": receipt["canonical_eligibility"],
        "research_admission": receipt["research_admission"],
        "staircase": receipt["staircase"],
        "fixture_transport_sha256": _sha_bytes(raw),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True), flush=True)
