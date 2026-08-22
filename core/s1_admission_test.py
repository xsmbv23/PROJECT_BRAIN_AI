from __future__ import annotations

import hashlib
import json
from pathlib import Path

from s1_admission import verify


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(root: Path) -> Path:
    raw = root / "raw.bin"
    canonical = root / "canonical.bin"
    receipt = root / "receipt.json"
    raw.write_bytes(b"real source bytes")
    canonical.write_bytes(b"canonical frozen bytes")
    receipt.write_text('{"receipt":"fresh"}', encoding="utf-8")
    data = {
        "contract_id": "S1_CANONICAL_EVIDENCE_V2",
        "source_provenance": "REAL_AND_TRACEABLE",
        "acquisition_channel": "DURABLE_ARCHIVE_EXPORT",
        "acquisition_reference": "authorized://source/2026-08-21",
        "acquisition_timestamp_utc": "2026-08-21T16:00:00+00:00",
        "artifact_path": "raw.bin",
        "canonical_artifact_path": "canonical.bin",
        "raw_artifact_sha256": _sha(raw),
        "raw_byte_sha256": _sha(raw),
        "date_start": "2026-08-01",
        "date_end": "2026-08-21",
        "expected_consecutive_days": 21,
        "observed_consecutive_days": 21,
        "coverage_ratio": 1.0,
        "unresolved_conflicts": 0,
        "admission_receipt": "receipt.json",
        "frozen_canonical_sha256": _sha(canonical),
        "synthetic_data": False,
    }
    manifest = root / "manifest.json"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    return manifest


def test_valid_manifest_passes(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    result = verify(manifest, tmp_path)
    assert result.status == "PASS", result.errors


def test_coverage_gap_denies(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    data = json.loads(manifest.read_text())
    data["observed_consecutive_days"] = 20
    data["coverage_ratio"] = 20 / 21
    manifest.write_text(json.dumps(data))
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"


def test_synthetic_data_denies(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    data = json.loads(manifest.read_text())
    data["synthetic_data"] = True
    manifest.write_text(json.dumps(data))
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"


def test_canonical_hash_mismatch_denies(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path)
    data = json.loads(manifest.read_text())
    data["frozen_canonical_sha256"] = "0" * 64
    manifest.write_text(json.dumps(data))
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"
