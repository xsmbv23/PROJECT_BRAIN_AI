"""S1 evidence-closure audit.

Fail-closed local audit. It never fetches data, invents provenance, or promotes
state. A PASS requires complete consecutive coverage, valid per-day receipts,
explicit acquisition metadata, raw/canonical byte hashes, zero unresolved
conflicts, and a real admission receipt reference.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

REQUIRED_MANIFEST = {
    "source_provenance", "acquisition_channel", "acquisition_reference",
    "acquisition_timestamp_utc", "artifact_path", "canonical_artifact_path",
    "raw_artifact_sha256", "raw_byte_sha256", "date_start", "date_end",
    "expected_consecutive_days", "observed_consecutive_days", "coverage_ratio",
    "unresolved_conflicts", "admission_receipt", "frozen_canonical_sha256",
    "synthetic_data",
}
ALLOWED_CHANNELS = {
    "AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION",
    "MANUAL_AUTHORIZED_CAPTURE",
    "DURABLE_ARCHIVE_EXPORT",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _days(start: str, end: str) -> list[str]:
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    if e < s:
        return []
    return [(s + timedelta(days=i)).isoformat() for i in range((e - s).days + 1)]


def _inside(root: Path, relative: str, errors: list[str], code: str) -> Path | None:
    if not relative:
        errors.append(code + "_missing")
        return None
    p = (root / relative).resolve()
    try:
        p.relative_to(root)
    except ValueError:
        errors.append(code + "_outside_evidence_root")
        return None
    return p


def audit(manifest: dict[str, Any], evidence_root: str | Path) -> dict[str, Any]:
    root = Path(evidence_root).resolve()
    errors: list[str] = []
    missing = sorted(REQUIRED_MANIFEST - manifest.keys())
    if missing:
        errors.append("missing_manifest_fields:" + ",".join(missing))
    if manifest.get("synthetic_data") is not False:
        errors.append("synthetic_data_not_false")
    if manifest.get("source_provenance") != "REAL_AND_TRACEABLE":
        errors.append("source_provenance_not_real_and_traceable")
    if manifest.get("acquisition_channel") not in ALLOWED_CHANNELS:
        errors.append("invalid_acquisition_channel")
    if not str(manifest.get("acquisition_reference", "")).strip():
        errors.append("missing_acquisition_reference")
    if not str(manifest.get("acquisition_timestamp_utc", "")).strip():
        errors.append("missing_acquisition_timestamp")
    if manifest.get("unresolved_conflicts") != 0:
        errors.append("unresolved_conflicts_nonzero")
    if not str(manifest.get("admission_receipt", "")).strip():
        errors.append("missing_admission_receipt")

    try:
        expected_days = _days(manifest["date_start"], manifest["date_end"])
    except Exception:
        expected_days = []
        errors.append("invalid_date_range")

    if manifest.get("expected_consecutive_days") != len(expected_days):
        errors.append("expected_day_count_mismatch")

    artifact = _inside(root, str(manifest.get("artifact_path", "")), errors, "raw_artifact")
    canonical = _inside(root, str(manifest.get("canonical_artifact_path", "")), errors, "canonical_artifact")
    if artifact is not None and not artifact.is_file():
        errors.append("raw_artifact_missing")
    if canonical is not None and not canonical.is_file():
        errors.append("canonical_artifact_missing")

    if artifact is not None and artifact.is_file():
        actual_raw = sha256_file(artifact)
        if actual_raw != manifest.get("raw_artifact_sha256"):
            errors.append("raw_artifact_sha256_mismatch")
        if actual_raw != manifest.get("raw_byte_sha256"):
            errors.append("raw_byte_sha256_mismatch")

    observed_days: set[str] = set()
    for receipt_path in root.rglob("*.receipt.json"):
        try:
            rec = json.loads(receipt_path.read_text(encoding="utf-8"))
        except Exception:
            errors.append(f"invalid_receipt_json:{receipt_path.relative_to(root)}")
            continue
        day = rec.get("business_date")
        if day not in expected_days:
            continue
        observed_days.add(day)
        if rec.get("source_provenance") != "REAL_AND_TRACEABLE":
            errors.append(f"non_real_receipt:{day}")
        if rec.get("synthetic_data") is True or rec.get("source_provenance") == "SYNTHETIC":
            errors.append(f"synthetic_receipt:{day}")
        if not str(rec.get("raw_bytes_sha256", "")).strip():
            errors.append(f"missing_raw_hash:{day}")
        if rec.get("truncated") is True:
            errors.append(f"truncated_capture:{day}")
        if rec.get("acquisition_channel") not in ALLOWED_CHANNELS:
            errors.append(f"invalid_acquisition_channel:{day}")
        if not str(rec.get("acquisition_reference", "")).strip():
            errors.append(f"missing_acquisition_reference:{day}")
        if not str(rec.get("acquisition_timestamp_utc", "")).strip():
            errors.append(f"missing_acquisition_timestamp:{day}")

    missing_days = [d for d in expected_days if d not in observed_days]
    if missing_days:
        errors.append("missing_consecutive_days:" + ",".join(missing_days))
    if manifest.get("observed_consecutive_days") != len(observed_days):
        errors.append("observed_day_count_mismatch")
    if manifest.get("coverage_ratio") != 1.0:
        errors.append("coverage_ratio_not_one")

    if canonical is not None and canonical.is_file():
        actual_canonical = sha256_file(canonical)
        if actual_canonical != manifest.get("frozen_canonical_sha256"):
            errors.append("frozen_canonical_sha256_mismatch")

    return {
        "schema": "s1-evidence-closure-audit/v2",
        "status": "PASS" if not errors else "DENY",
        "evidence_root": str(root),
        "expected_days": expected_days,
        "observed_days": sorted(observed_days),
        "missing_days": missing_days,
        "errors": sorted(set(errors)),
        "promotion": "DENY",
    }


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("evidence_root")
    args = p.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    report = audit(manifest, args.evidence_root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
