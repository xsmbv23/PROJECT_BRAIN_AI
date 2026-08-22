import hashlib
import json
from pathlib import Path
from core.s1_closure_audit import audit


def test_s1_denies_incomplete_coverage_and_missing_canonical(tmp_path: Path):
    raw = tmp_path / "raw.json"
    raw.write_text("{}", encoding="utf-8")
    receipt_dir = tmp_path / "2026-08-21"
    receipt_dir.mkdir()
    (receipt_dir / "a.receipt.json").write_text(json.dumps({
        "business_date":"2026-08-21",
        "raw_bytes_sha256": hashlib.sha256(b"{}").hexdigest(),
        "truncated": False,
        "acquisition_channel":"AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION",
        "acquisition_reference":"ref-1"
    }), encoding="utf-8")
    manifest = {
        "source_provenance":"REAL_AND_TRACEABLE",
        "acquisition_channel":"AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION",
        "acquisition_reference":"ref-1",
        "acquisition_timestamp_utc":"2026-08-21T00:00:00Z",
        "artifact_path":"raw.json",
        "canonical_artifact_path":"canonical.json",
        "raw_artifact_sha256":"0"*64,
        "raw_byte_sha256":"0"*64,
        "date_start":"2026-08-20",
        "date_end":"2026-08-21",
        "expected_consecutive_days":2,
        "observed_consecutive_days":1,
        "coverage_ratio":0.5,
        "unresolved_conflicts":0,
        "admission_receipt":"receipt.json",
        "frozen_canonical_sha256":"0"*64,
        "synthetic_data":False,
    }
    report = audit(manifest, tmp_path)
    assert report["status"] == "DENY"
    assert any(e.startswith("missing_consecutive_days:") for e in report["errors"])
    assert "canonical_artifact_missing" in report["errors"]
