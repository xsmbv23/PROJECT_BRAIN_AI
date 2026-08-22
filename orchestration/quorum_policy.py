"""Fault-tolerant worker quorum policy.

Worker availability controls deliberation capacity, not admission authority.
No worker identity is hard-coded as a mandatory dependency for ordinary work.
Critical admission still requires the independent verifier/evidence predicates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

WORKERS = ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION")


@dataclass(frozen=True)
class QuorumDecision:
    mode: str
    available: tuple[str, ...]
    required: int
    can_deliberate: bool
    admission_eligible: bool


def evaluate_quorum(available: Iterable[str], *, critical: bool = False) -> QuorumDecision:
    active = tuple(sorted(set(available) & set(WORKERS)))
    required = 2
    can_deliberate = len(active) >= required
    # Deliberation never grants admission authority. Critical work additionally
    # requires an independent verifier/evidence path at the admission gate.
    admission_eligible = False
    if critical:
        mode = "FULL" if len(active) == 3 else "DEGRADED"
    else:
        mode = "FULL" if len(active) == 3 else ("DEGRADED" if can_deliberate else "INSUFFICIENT_QUORUM")
    return QuorumDecision(mode, active, required, can_deliberate, admission_eligible)


def require_deliberation_quorum(available: Iterable[str]) -> QuorumDecision:
    decision = evaluate_quorum(available)
    if not decision.can_deliberate:
        raise RuntimeError("INSUFFICIENT_WORKER_QUORUM")
    return decision
