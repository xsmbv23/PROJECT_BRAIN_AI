from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s1_admission import CONTRACT_ID, verify  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_manifest(root: Path, *, coverage: float = 1.0, synthetic: bool = False) -> Path:
    raw = root / "raw.bin"
    canonical = root / "canonical.bin"
    receipt = root / "receipt.json"
    raw.write_bytes(b"real raw capture")
    canonical.write_bytes(b"frozen canonical dataset")
    receipt.write_text(json.dumps({"receipt": "observable"}), encoding="utf-8")
    manifest = {
        "contract_id": CONTRACT_ID,
        "source_provenance": "REAL_AND_TRACEABLE",
        "acquisition_channel": "DURABLE_ARCHIVE_EXPORT",
        "acquisition_reference": "archive://source/export/2026-08-21",
        "acquisition_timestamp_utc": "2026-08-21T09:00:00Z",
        "artifact_path": "raw.bin",
        "canonical_artifact_path": "canonical.bin",
        "raw_artifact_sha256": _sha(raw),
        "raw_byte_sha256": _sha(raw),
        "date_start": "2026-08-17",
        "date_end": "2026-08-21",
        "expected_consecutive_days": 5,
        "observed_consecutive_days": 5,
        "coverage_ratio": coverage,
        "unresolved_conflicts": 0,
        "admission_receipt": "receipt.json",
        "frozen_canonical_sha256": _sha(canonical),
        "synthetic_data": synthetic,
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_valid_manifest_passes(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    result = verify(manifest, tmp_path)
    assert result.status == "PASS"
    assert result.errors == []


def test_partial_coverage_denies(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path, coverage=0.8)
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"
    assert any("coverage_ratio" in error for error in result.errors)


def test_synthetic_data_denies(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path, synthetic=True)
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"
    assert any("synthetic_data" in error for error in result.errors)


def test_canonical_hash_mismatch_denies(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["frozen_canonical_sha256"] = "0" * 64
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    result = verify(manifest, tmp_path)
    assert result.status == "DENY"
    assert any("frozen_canonical_sha256" in error for error in result.errors)
