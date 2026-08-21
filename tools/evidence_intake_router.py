"""Forensic evidence intake router.

This is deliberately an intake/governance component, not a scraper.
Every acquisition channel must converge to the same immutable evidence contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AcquisitionChannel(str, Enum):
    AUTOMATED_EXPLICIT = "AUTOMATED_EXPLICIT"
    MANUAL_AUTHORIZED = "MANUAL_AUTHORIZED"
    DURABLE_ARCHIVE_EXPORT = "DURABLE_ARCHIVE_EXPORT"


@dataclass(frozen=True)
class EvidenceAdmission:
    channel: AcquisitionChannel
    provenance: str
    acquired_at: str
    raw_sha256: str
    raw_bytes: int
    coverage: float
    unresolved_conflicts: int
    synthetic_data: bool

    def admit(self) -> None:
        if not self.provenance.strip():
            raise ValueError("DENY_PROVENANCE_MISSING")
        if not self.acquired_at.strip():
            raise ValueError("DENY_TIMESTAMP_MISSING")
        if len(self.raw_sha256) != 64:
            raise ValueError("DENY_RAW_SHA256_INVALID")
        if self.raw_bytes <= 0:
            raise ValueError("DENY_RAW_BYTES_INVALID")
        if self.coverage != 1.0:
            raise ValueError("DENY_COVERAGE_NOT_COMPLETE")
        if self.unresolved_conflicts != 0:
            raise ValueError("DENY_UNRESOLVED_CONFLICTS")
        if self.synthetic_data:
            raise ValueError("DENY_SYNTHETIC_DATA")


def admission_channels() -> tuple[str, ...]:
    return tuple(channel.value for channel in AcquisitionChannel)
