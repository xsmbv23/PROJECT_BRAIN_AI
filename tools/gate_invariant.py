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

    seen_gate_ids: set[str] = set()
    by_id: dict[str, GateResult] = {}
    for item in history:
        if item.gate_id in seen_gate_ids:
            return False, f"DUPLICATE_GATE:{item.gate_id}"
        seen_gate_ids.add(item.gate_id)
        by_id[item.gate_id] = item
        if not _valid_status(item.status):
            return False, f"INVALID_STATUS:{item.gate_id}"
        if not item.evidence_hash or not item.cycle_id:
            return False, f"EVIDENCE_IDENTITY_MISSING:{item.gate_id}"
        age = now_value - item.created_at
        if age < 0 or age > ttl_seconds:
            return False, f"STALE_EVIDENCE:{item.gate_id}"
        if item.status != "PASS":
            return False, f"BLOCKED_HISTORY:{item.gate_id}:{item.status}"

    for dependency in current.depends_on:
        result = by_id.get(dependency)
        if result is None:
            return False, f"DEPENDENCY_MISSING:{dependency}"
        if result.status != "PASS":
            return False, f"DEPENDENCY_NOT_PASS:{dependency}"
        if result.cycle_id != history[-1].cycle_id if history else True:
            return False, f"CYCLE_MISMATCH:{dependency}"

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
    """Validate a recorded chain without inventing missing evidence.

    A recorded chain is not trusted merely because its gate IDs and hashes are
    unique. Every recorded result must belong to one cycle, remain within the
    same freshness window used for live admission, and be recorded in temporal
    order. Once a gate is FAIL/UNKNOWN/UNREACHED, no later gate may claim PASS;
    the later gates must remain UNREACHED. Dependency semantics are checked by
    ``check_gate_invariant`` when the next gate is evaluated because this
    function intentionally receives results, not gate definitions.
    """
    items = list(history)
    if not items:
        return False, "EMPTY_HISTORY"
    now_value = datetime.now(timezone.utc).timestamp() if now is None else now
    if ttl_seconds <= 0:
        return False, "TTL_INVALID"

    seen: set[str] = set()
    hashes: set[str] = set()
    cycle_id = items[0].cycle_id
    previous_created_at: float | None = None
    blocked_seen = False
    for item in items:
        if item.gate_id in seen:
            return False, f"DUPLICATE_GATE:{item.gate_id}"
        if item.evidence_hash in hashes:
            return False, f"EVIDENCE_REUSE:{item.gate_id}"
        if not item.evidence_hash or not item.cycle_id:
            return False, f"EVIDENCE_IDENTITY_MISSING:{item.gate_id}"
        if not _valid_status(item.status):
            return False, f"INVALID_STATUS:{item.gate_id}"
        if item.cycle_id != cycle_id:
            return False, f"CYCLE_MISMATCH:{item.gate_id}"
        if previous_created_at is not None and item.created_at < previous_created_at:
            return False, f"OUT_OF_ORDER_EVIDENCE:{item.gate_id}"
        age = now_value - item.created_at
        if age < 0 or age > ttl_seconds:
            return False, f"STALE_EVIDENCE:{item.gate_id}"

        if blocked_seen and item.status == "PASS":
            return False, f"PASS_AFTER_BLOCK:{item.gate_id}"
        if item.status != "PASS":
            blocked_seen = True

        seen.add(item.gate_id)
        hashes.add(item.evidence_hash)
        previous_created_at = item.created_at
    return True, "CHAIN_RECORD_VALID"
