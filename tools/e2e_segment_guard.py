"""Machine-checkable end-to-end segment reachability rules.

This is a planning/admission guard, not a promotion authority.  A downstream
segment can be prepared safely, but it cannot be marked reachable until its
immediate predecessor has independently verified exit evidence.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SegmentState:
    segment_id: str
    status: str
    exit_evidence_ref: str = ""


_ORDER = ("S1", "S2", "S3", "S4", "S5", "S6", "S7")
_VALID = {"UNKNOWN", "PREPARED", "VERIFIED", "UNREACHED", "BLOCKED"}


def segment_reachable(current: str, states: list[SegmentState]) -> tuple[bool, str]:
    """Return whether *current* may be reached from the E2E chain.

    VERIFIED is local to the predecessor segment.  It never grants PASS,
    promotion, or authorization to the current segment.
    """
    if current not in _ORDER:
        return False, "SEGMENT_UNKNOWN"
    by_id: dict[str, SegmentState] = {}
    for item in states:
        if item.segment_id in by_id:
            return False, f"DUPLICATE_SEGMENT:{item.segment_id}"
        if item.status not in _VALID:
            return False, f"INVALID_SEGMENT_STATUS:{item.segment_id}"
        by_id[item.segment_id] = item

    idx = _ORDER.index(current)
    if idx == 0:
        return True, "ROOT_SEGMENT"

    predecessor = _ORDER[idx - 1]
    prev = by_id.get(predecessor)
    if prev is None:
        return False, f"PREDECESSOR_MISSING:{predecessor}"
    if prev.status != "VERIFIED":
        return False, f"PREDECESSOR_NOT_VERIFIED:{predecessor}:{prev.status}"
    if not prev.exit_evidence_ref:
        return False, f"PREDECESSOR_EXIT_EVIDENCE_MISSING:{predecessor}"

    return True, "SEGMENT_REACHABLE"
