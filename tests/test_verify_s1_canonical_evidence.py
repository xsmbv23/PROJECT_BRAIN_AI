from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.verify_s1_canonical_evidence import verify_manifest


def _manifest(artifact_rel: str, digest: str, **overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "source_provenance": {"classification": "REAL_AND_TRACEABLE", "source": "ketqua16"},
        "artifact_path": artifact_rel,
        "raw_artifact_sha256": digest,
        "raw_byte_sha256": digest,
        "date_start": "2026-08-17",
        "date_end": "2026-08-17",
        "expected_consecutive_days": 1,
        "observed_consecutive_days": 1,
        "coverage_ratio": 1.0,
        "unresolved_conflicts": 0,
        "admission_receipt": {
            "receipt_id": "receipt-1",
            "source": "ketqua16",
            "observed_at": "2026-08-17T12:00:00Z",
            "event_type": "external_observation",
        },
        "frozen_canonical_sha256": "a" * 64,
        "synthetic_data": False,
    }
    base.update(overrides)
    return base


def _write_fixture(tmp_path: Path, manifest: dict[str, object], payload: bytes = b"REAL") -> Path:
    root = tmp_path / "evidence"
    root.mkdir()
    artifact = root / "artifact.bin"
    artifact.write_bytes(payload)
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def test_v2_requires_artifact_identity_fields(tmp_path: Path) -> None:
    payload = b"REAL"
    digest = hashlib.sha256(payload).hexdigest()
    manifest = _manifest("artifact.bin", digest)
    manifest.pop("artifact_path")
    manifest.pop("raw_artifact_sha256")
    manifest.pop("raw_byte_sha256")
    result = verify_manifest(_write_fixture(tmp_path, manifest, payload))
    assert result["status"] == "DENY"
    assert "MISSING:artifact_path,raw_artifact_sha256,raw_byte_sha256" in result["reasons"]


def test_raw_byte_sha256_must_match_artifact_bytes(tmp_path: Path) -> None:
    payload = b"REAL"
    digest = hashlib.sha256(payload).hexdigest()
    manifest = _manifest("artifact.bin", digest, raw_byte_sha256="b" * 64)
    result = verify_manifest(_write_fixture(tmp_path, manifest, payload))
    assert result["status"] == "DENY"
    assert "RAW_BYTE_SHA256_MISMATCH" in result["reasons"]


def test_raw_artifact_sha256_must_match_artifact_bytes(tmp_path: Path) -> None:
    payload = b"REAL"
    digest = hashlib.sha256(payload).hexdigest()
    manifest = _manifest("artifact.bin", "c" * 64, raw_byte_sha256=digest)
    result = verify_manifest(_write_fixture(tmp_path, manifest, payload))
    assert result["status"] == "DENY"
    assert "RAW_ARTIFACT_SHA256_MISMATCH" in result["reasons"]


def test_valid_v2_manifest_passes(tmp_path: Path) -> None:
    payload = b"REAL"
    digest = hashlib.sha256(payload).hexdigest()
    manifest = _manifest("artifact.bin", digest)
    result = verify_manifest(_write_fixture(tmp_path, manifest, payload))
    assert result["status"] == "PASS"
    assert result["admission"] == "S1_CANONICAL_EVIDENCE_ADMITTED"
