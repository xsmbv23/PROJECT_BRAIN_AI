"""Deterministic fault matrix for worker/admission resilience tests."""
from __future__ import annotations
from orchestration.quorum_reconciliation import reconcile

WORKERS = ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION")

def matrix() -> list[dict[str, object]]:
    rows = []
    for mask in range(8):
        available = {w: bool(mask & (1 << i)) for i, w in enumerate(WORKERS)}
        r = reconcile(available)
        rows.append({"available": available, "mode": r.mode, "can_deliberate": r.can_deliberate, "provisional": r.provisional, "admission_eligible": r.admission_eligible})
    return rows
