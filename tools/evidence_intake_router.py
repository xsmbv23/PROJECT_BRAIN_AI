"""Channel-agnostic forensic evidence intake boundary.

This component is an intake/governance boundary, not a scraper. Every lawful
acquisition channel converges on the same evidence semantics used by S1 V2.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class AcquisitionChannel(str, Enum):
    AUTOMATED_EXPLICIT = "AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION"
    MANUAL_AUTHORIZED = "MANUAL_AUTHORIZED_CAPTURE"
    DURABLE_ARCHIVE_EXPORT = "DURABLE_ARCHIVE_EXPORT"


@dataclass(frozen=True)
class EvidenceAdmission:
    channel: AcquisitionChannel
    provenance: str
    acquisition_reference: str
    acquired_at: str
    raw_sha256: str
    raw_bytes: int
    date_start: str
    date_end: str
    expected_consecutive_days: int
    observed_consecutive_days: int
    coverage: float
    unresolved_conflicts: int
    frozen_canonical_sha256: str
    synthetic_data: bool

    def admit(self) -> None:
        if not self.provenance.strip():
            raise ValueError("DENY_PROVENANCE_MISSING")
        if not self.acquisition_reference.strip():
            raise ValueError("DENY_ACQUISITION_REFERENCE_MISSING")
        if not self.acquired_at.strip():
            raise ValueError("DENY_TIMESTAMP_MISSING")
        try:
            captured_at = datetime.fromisoformat(self.acquired_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("DENY_TIMESTAMP_INVALID") from exc
        if captured_at.tzinfo is None:
            raise ValueError("DENY_TIMESTAMP_NOT_TIMEZONE_AWARE")
        if captured_at > datetime.now(timezone.utc) + __import__("datetime").timedelta(minutes=5):
            raise ValueError("DENY_TIMESTAMP_IN_FUTURE")
        if not SHA256_RE.fullmatch(self.raw_sha256):
            raise ValueError("DENY_RAW_SHA256_INVALID")
        if not SHA256_RE.fullmatch(self.frozen_canonical_sha256):
            raise ValueError("DENY_FROZEN_CANONICAL_SHA256_INVALID")
        if self.raw_bytes <= 0:
            raise ValueError("DENY_RAW_BYTES_INVALID")
        try:
            start = date.fromisoformat(self.date_start)
            end = date.fromisoformat(self.date_end)
        except ValueError as exc:
            raise ValueError("DENY_DATE_RANGE_INVALID") from exc
        expected_from_dates = (end - start).days + 1
        if end < start or self.expected_consecutive_days != expected_from_dates:
            raise ValueError("DENY_CONSECUTIVE_DATE_RANGE_INVALID")
        if self.observed_consecutive_days != self.expected_consecutive_days:
            raise ValueError("DENY_OBSERVED_DAYS_NOT_COMPLETE")
        if self.coverage != 1.0:
            raise ValueError("DENY_COVERAGE_NOT_COMPLETE")
        if self.unresolved_conflicts != 0:
            raise ValueError("DENY_UNRESOLVED_CONFLICTS")
        if self.synthetic_data:
            raise ValueError("DENY_SYNTHETIC_DATA")


def admission_channels() -> tuple[str, ...]:
    return tuple(channel.value for channel in AcquisitionChannel)
