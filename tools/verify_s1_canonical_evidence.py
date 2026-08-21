"""Machine-checkable S1 canonical evidence admission.

This verifier is intentionally fail-closed. It validates a real evidence
manifest and, when present, the referenced artifact bytes and receipt. It never
creates evidence, hashes missing data, or promotes an unproven dataset.

Usage:
    python tools/verify_s1_canonical_evidence.py path/to/manifest.json

Exit 0 only when every S1 condition is independently proven.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = {
    "source_provenance",
    "artifact_path",
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


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _is_real_receipt(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    required = {"receipt_id", "source", "observed_at", "event_type"}
    if not required.issubset(value):
        return False
    if not all(isinstance(value[k], str) and value[k].strip() for k in required):
        return False
    if value.get("synthetic") is True:
        return False
    return True


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(manifest_path: str | Path) -> dict[str, object]:
    path = Path(manifest_path)
    result: dict[str, object] = {
        "gate": "S1_CANONICAL_EVIDENCE",
        "status": "DENY",
        "manifest": str(path),
        "reasons": [],
    }

    if not path.is_file():
        result["reasons"] = ["MANIFEST_MISSING"]
        return result

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        result["reasons"] = ["MANIFEST_UNREADABLE"]
        return result

    if not isinstance(manifest, dict):
        result["reasons"] = ["MANIFEST_NOT_OBJECT"]
        return result

    reasons: list[str] = []
    missing = sorted(REQUIRED - set(manifest))
    if missing:
        reasons.append("MISSING:" + ",".join(missing))

    if manifest.get("synthetic_data") is not False:
        reasons.append("SYNTHETIC_DATA_NOT_EXPLICITLY_FALSE")

    provenance = manifest.get("source_provenance")
    if not isinstance(provenance, dict) or provenance.get("classification") != "REAL_AND_TRACEABLE":
        reasons.append("SOURCE_PROVENANCE_NOT_REAL_AND_TRACEABLE")

    for field in ("raw_artifact_sha256", "raw_byte_sha256", "frozen_canonical_sha256"):
        value = manifest.get(field)
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            reasons.append(field.upper() + "_INVALID")

    try:
        start = _parse_date(str(manifest.get("date_start")))
        end = _parse_date(str(manifest.get("date_end")))
        expected = int(manifest.get("expected_consecutive_days"))
        observed = int(manifest.get("observed_consecutive_days"))
        coverage = float(manifest.get("coverage_ratio"))
        conflicts = int(manifest.get("unresolved_conflicts"))
    except (TypeError, ValueError):
        reasons.append("DATE_OR_COVERAGE_FIELDS_INVALID")
    else:
        expected_from_dates = (end - start).days + 1
        if end < start or expected != expected_from_dates:
            reasons.append("CONSECUTIVE_DATE_RANGE_INVALID")
        if observed != expected:
            reasons.append("OBSERVED_DAYS_NOT_COMPLETE")
        if coverage != 1.0:
            reasons.append("COVERAGE_NOT_1_0")
        if conflicts != 0:
            reasons.append("UNRESOLVED_CONFLICTS_PRESENT")

    receipt = manifest.get("admission_receipt")
    if not _is_real_receipt(receipt):
        reasons.append("REAL_ADMISSION_RECEIPT_NOT_PROVEN")
    else:
        try:
            observed_at = datetime.fromisoformat(str(receipt["observed_at"]).replace("Z", "+00:00"))
            if observed_at.tzinfo is None:
                reasons.append("RECEIPT_TIMESTAMP_NOT_TIMEZONE_AWARE")
            elif observed_at > datetime.now(timezone.utc) + timedelta(minutes=5):
                reasons.append("RECEIPT_TIMESTAMP_IN_FUTURE")
        except ValueError:
            reasons.append("RECEIPT_TIMESTAMP_INVALID")

    artifact_path = manifest.get("artifact_path")
    if not isinstance(artifact_path, str) or not artifact_path.strip():
        reasons.append("CANONICAL_ARTIFACT_PATH_MISSING")
    else:
        artifact = (path.parent / artifact_path).resolve()
        try:
            artifact.relative_to(path.parent.resolve())
        except ValueError:
            reasons.append("ARTIFACT_PATH_ESCAPES_EVIDENCE_ROOT")
        else:
            if not artifact.is_file():
                reasons.append("CANONICAL_ARTIFACT_MISSING")
            else:
                computed = _sha256_file(artifact)
                expected_raw_artifact = manifest.get("raw_artifact_sha256")
                expected_raw_byte = manifest.get("raw_byte_sha256")
                if isinstance(expected_raw_artifact, str) and SHA256_RE.fullmatch(expected_raw_artifact):
                    if computed != expected_raw_artifact:
                        reasons.append("RAW_ARTIFACT_SHA256_MISMATCH")
                if isinstance(expected_raw_byte, str) and SHA256_RE.fullmatch(expected_raw_byte):
                    if computed != expected_raw_byte:
                        reasons.append("RAW_BYTE_SHA256_MISMATCH")

    result["reasons"] = reasons
    if not reasons:
        result["status"] = "PASS"
        result["admission"] = "S1_CANONICAL_EVIDENCE_ADMITTED"
    else:
        result["admission"] = "S1_CANONICAL_EVIDENCE_BLOCKED"
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"status": "DENY", "reasons": ["MANIFEST_ARGUMENT_REQUIRED"]}))
        return 2
    result = verify_manifest(argv[1])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
