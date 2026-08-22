"""Fault-tolerant worker reconciliation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

WORKERS = ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION")

@dataclass(frozen=True)
class Reconciliation:
    mode: str
    available_workers: tuple[str, ...]
    can_deliberate: bool
    provisional: bool
    admission_eligible: bool
    reason: str

def reconcile(available: Mapping[str, bool], *, critical: bool = False) -> Reconciliation:
    active = tuple(w for w in WORKERS if available.get(w, False))
    n = len(active)
    if n >= 3:
        return Reconciliation("FULL", active, True, False, False if critical else True, "FULL_QUORUM")
    if n == 2:
        return Reconciliation("DEGRADED", active, True, True, False, "DEGRADED_TWO_WORKER_QUORUM")
    return Reconciliation("INSUFFICIENT_QUORUM", active, False, True, False, "LESS_THAN_TWO_WORKERS")
