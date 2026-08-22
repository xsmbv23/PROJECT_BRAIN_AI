"""Strict S1 canonical-evidence admission verifier.

This module verifies an already-produced evidence manifest. It does not fetch
sources, infer business dates, parse source content, or mutate canonical state.
A PASS means only that the supplied manifest satisfies the S1 contract and
that every referenced local artifact/hash is verifiable at execution time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT_ID = "S1_CANONICAL_EVIDENCE_V2"
REQUIRED = {
    "source_provenance",
    "acquisition_channel",
    "acquisition_reference",
    "acquisition_timestamp_utc",
    "artifact_path",
    "canonical_artifact_path",
    "raw_artifact_sha256",
    "raw_byte_sha256",
    "date_start",
    "date_end",
    "expected_consecutive_days",
    "observed_consecutive_days",
    "coverage_ratio",
    "unresolved_conflicts",
    "admission_receipt",
    "frozen_canonical_sha256",
    "synthetic_data",
}
ALLOWED_CHANNELS = {
    "AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION",
    "MANUAL_AUTHORIZED_CAPTURE",
    "DURABLE_ARCHIVE_EXPORT",
}


@dataclass(frozen=True)
class Result:
    status: str
    contract_id: str
    checked_at_utc: str
    manifest: str
    errors: list[str]
    verified: list[str]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_timestamp(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: missing")
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field}: timezone required")


def _parse_date(value: Any, field: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field}: YYYY-MM-DD required")
    return date.fromisoformat(value)


def _resolve(root: Path, value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: path required")
    root = root.resolve()
    candidate = (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"{field}: path escapes evidence root")
    if not candidate.is_file():
        raise ValueError(f"{field}: file not found: {value}")
    return candidate


def verify(manifest_path: Path, evidence_root: Path) -> Result:
    errors: list[str] = []
    verified: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - CLI boundary
        return Result("DENY", CONTRACT_ID, datetime.now(timezone.utc).isoformat(), str(manifest_path), [f"manifest: invalid JSON: {exc}"], [])

    if manifest.get("contract_id") not in (CONTRACT_ID, None):
        errors.append(f"contract_id: expected {CONTRACT_ID}")
    missing = sorted(REQUIRED - set(manifest))
    errors.extend(f"missing required field: {field}" for field in missing)
    if errors:
        return Result("DENY", CONTRACT_ID, datetime.now(timezone.utc).isoformat(), str(manifest_path), errors, verified)

    if manifest.get("synthetic_data") is not False:
        errors.append("synthetic_data: must be false")
    if manifest.get("source_provenance") != "REAL_AND_TRACEABLE":
        errors.append("source_provenance: must be REAL_AND_TRACEABLE")
    channel = manifest.get("acquisition_channel")
    if channel not in ALLOWED_CHANNELS:
        errors.append("acquisition_channel: unsupported or missing explicit authorized channel")
    if not isinstance(manifest.get("acquisition_reference"), str) or not manifest["acquisition_reference"].strip():
        errors.append("acquisition_reference: present and non-empty")
    try:
        _parse_timestamp(manifest.get("acquisition_timestamp_utc"), "acquisition_timestamp_utc")
    except ValueError as exc:
        errors.append(str(exc))

    try:
        start = _parse_date(manifest["date_start"], "date_start")
        end = _parse_date(manifest["date_end"], "date_end")
        if end < start:
            errors.append("date range: date_end precedes date_start")
        expected = int(manifest["expected_consecutive_days"])
        observed = int(manifest["observed_consecutive_days"])
        ratio = float(manifest["coverage_ratio"])
        if expected <= 0:
            errors.append("expected_consecutive_days: must be > 0")
        if observed < 0 or observed > expected:
            errors.append("observed_consecutive_days: outside expected range")
        if ratio != 1.0:
            errors.append("coverage_ratio: must equal 1.0")
        if observed != expected:
            errors.append("coverage: observed_consecutive_days must equal expected_consecutive_days")
        if (end - start).days + 1 != expected:
            errors.append("coverage: date range length does not equal expected_consecutive_days")
    except (TypeError, ValueError) as exc:
        errors.append(f"coverage: invalid value: {exc}")

    try:
        conflicts = int(manifest["unresolved_conflicts"])
        if conflicts != 0:
            errors.append("unresolved_conflicts: must equal 0")
    except (TypeError, ValueError):
        errors.append("unresolved_conflicts: integer required")

    try:
        artifact = _resolve(evidence_root, manifest["artifact_path"], "artifact_path")
        raw_digest = _sha256(artifact)
        if raw_digest != str(manifest["raw_artifact_sha256"]).lower():
            errors.append("raw_artifact_sha256: does not match artifact bytes")
        else:
            verified.append("raw_artifact_sha256")
        if raw_digest != str(manifest["raw_byte_sha256"]).lower():
            errors.append("raw_byte_sha256: does not match artifact bytes")
        else:
            verified.append("raw_byte_sha256")
    except ValueError as exc:
        errors.append(str(exc))

    try:
        receipt = _resolve(evidence_root, manifest["admission_receipt"], "admission_receipt")
        verified.append(f"admission_receipt:{receipt.relative_to(evidence_root.resolve())}")
    except ValueError as exc:
        errors.append(str(exc))

    try:
        canonical = _resolve(evidence_root, manifest["canonical_artifact_path"], "canonical_artifact_path")
        canonical_digest = _sha256(canonical)
        if canonical_digest != str(manifest["frozen_canonical_sha256"]).lower():
            errors.append("frozen_canonical_sha256: does not match canonical artifact bytes")
        else:
            verified.append("frozen_canonical_sha256")
    except ValueError as exc:
        errors.append(str(exc))

    status = "PASS" if not errors else "DENY"
    return Result(status, CONTRACT_ID, datetime.now(timezone.utc).isoformat(), str(manifest_path), errors, verified)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify S1 canonical evidence without mutating state")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args(argv)
    result = verify(args.manifest, args.evidence_root)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.status == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
