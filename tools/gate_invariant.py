"""Machine-checkable admission invariants for the Forensic gate chain.

Core rule: PASS is local to a gate. A predecessor PASS is a prerequisite for
reaching the next gate, never evidence for that next gate. Evidence must also
be fresh within the current reconciliation cycle.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Sequence


class GateInvariantViolationError(RuntimeError):
    pass


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: str
    evidence_hash: str
    created_at: float
    cycle_id: str


@dataclass(frozen=True)
class GateDefinition:
    gate_id: str
    depends_on: tuple[str, ...] = ()
    evidence_required: tuple[str, ...] = ()
    forbidden_evidence_sources: tuple[str, ...] = ()


def _valid_status(status: str) -> bool:
    return status in {"PASS", "FAIL", "UNKNOWN", "UNREACHED"}


def check_gate_invariant(
    current: GateDefinition,
    history: Sequence[GateResult],
    *,
    now: float | None = None,
    ttl_seconds: float = 300.0,
) -> tuple[bool, str]:
    """Validate whether *current* may be evaluated.

    This function checks only admission conditions. It never treats predecessor
    evidence as evidence for the current gate.
    """
    if not current.gate_id:
        return False, "GATE_ID_MISSING"
    if ttl_seconds <= 0:
        return False, "TTL_INVALID"
    now_value = datetime.now(timezone.utc).timestamp() if now is None else now

    by_id = {item.gate_id: item for item in history}
    for item in history:
        if not _valid_status(item.status):
            return False, f"INVALID_STATUS:{item.gate_id}"
        if not item.evidence_hash or not item.cycle_id:
            return False, f"EVIDENCE_IDENTITY_MISSING:{item.gate_id}"
        age = now_value - item.created_at
        if age < 0 or age > ttl_seconds:
            return False, f"STALE_EVIDENCE:{item.gate_id}"

    for dependency in current.depends_on:
        result = by_id.get(dependency)
        if result is None:
            return False, f"DEPENDENCY_MISSING:{dependency}"
        if result.status != "PASS":
            return False, f"DEPENDENCY_NOT_PASS:{dependency}"
        if result.cycle_id != history[-1].cycle_id if history else True:
            return False, f"CYCLE_MISMATCH:{dependency}"

    # No current gate may reuse any predecessor evidence hash.
    predecessor_hashes = {by_id[d].evidence_hash for d in current.depends_on if d in by_id}
    if len(predecessor_hashes) != len([d for d in current.depends_on if d in by_id]):
        return False, "DUPLICATE_PREDECESSOR_EVIDENCE"

    return True, "ADMITTED"


def assert_gate_admitted(
    current: GateDefinition,
    history: Sequence[GateResult],
    *,
    now: float | None = None,
    ttl_seconds: float = 300.0,
) -> None:
    ok, reason = check_gate_invariant(current, history, now=now, ttl_seconds=ttl_seconds)
    if not ok:
        raise GateInvariantViolationError(f"DENY:{current.gate_id}:{reason}")


def gate_chain_is_valid(
    history: Iterable[GateResult], *, now: float | None = None, ttl_seconds: float = 300.0
) -> tuple[bool, str]:
    """Validate a recorded chain without inventing missing evidence."""
    items = list(history)
    if not items:
        return False, "EMPTY_HISTORY"
    seen: set[str] = set()
    hashes: set[str] = set()
    for item in items:
        if item.gate_id in seen:
            return False, f"DUPLICATE_GATE:{item.gate_id}"
        if item.evidence_hash in hashes:
            return False, f"EVIDENCE_REUSE:{item.gate_id}"
        seen.add(item.gate_id)
        hashes.add(item.evidence_hash)
        if not _valid_status(item.status):
            return False, f"INVALID_STATUS:{item.gate_id}"
    return True, "CHAIN_RECORD_VALID"
