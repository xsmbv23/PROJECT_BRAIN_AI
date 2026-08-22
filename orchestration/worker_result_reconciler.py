"""Reconcile worker results without treating an unavailable worker as failure."""
from __future__ import annotations
from typing import Any, Mapping
from orchestration.quorum_reconciliation import reconcile

def reconcile_results(results: Mapping[str, Mapping[str, Any]], available: Mapping[str, bool], *, critical: bool = False) -> dict[str, Any]:
    q = reconcile(available, critical=critical)
    bound = []
    conflicts = []
    for worker, result in results.items():
        if not available.get(worker, False):
            continue
        if result.get("status") in ("HOLD", "FAIL", "ERROR") or result.get("result") in ("HOLD", "FAIL"):
            conflicts.append(worker)
        bound.append(worker)
    if not q.can_deliberate:
        decision = "INSUFFICIENT_QUORUM"
    elif conflicts:
        decision = "HOLD_CONFLICT"
    elif q.provisional:
        decision = "PROVISIONAL"
    else:
        decision = "RECONCILED"
    if critical:
        decision = "HOLD_CRITICAL_ADMISSION" if decision in ("RECONCILED", "PROVISIONAL") else decision
    return {"decision": decision, "mode": q.mode, "available_workers": list(q.available_workers), "bound_results": bound, "conflicts": conflicts, "provisional": q.provisional, "admission_eligible": False}
