"""Fail-closed admission boundary for Brain state reconciliation.

This boundary does not invent Quant projections or runtime receipts. Missing
projection evidence is explicitly NOT_PROVEN and therefore cannot promote.
Runtime commit drift is treated as version/reconciliation evidence, never as
proof that logical state changed. Logical authority/protocol violations are
HARD_DENY.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from tools.state_reconciliation import reconcile

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "state_reconciliation_admission_v1.json"


def evaluate_admission(runtime_commit: str | None = None, deployment_id: str | None = None, quant_projection: dict | None = None) -> dict[str, object]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    rec = reconcile(runtime_commit=runtime_commit, deployment_id=deployment_id)

    projection_present = isinstance(quant_projection, dict)
    projection_status = "PROVEN" if projection_present else "NOT_PROVEN"

    if rec["state_consistency"] == "HARD_DENY":
        decision = "HARD_DENY"
    elif not projection_present:
        decision = "RECONCILE_REQUIRED"
    elif rec["state_consistency"] == "RECONCILE_REQUIRED":
        decision = "RECONCILE_REQUIRED"
    else:
        decision = "VERIFIED"

    return {
        "contract_id": contract["contract_id"],
        "decision": decision,
        "brain_state": rec["state_consistency"],
        "quant_projection": projection_status,
        "runtime_evidence": {
            "known": rec["runtime_commit_known"],
            "commit": rec["runtime_commit"],
            "last_verified_commit": rec["runtime_last_verified_commit"],
            "same_as_last_verified": rec["runtime_commit_same_as_last_verified"],
        },
        "runtime_is_authority": False,
        "projection_is_authority": False,
        "unknown_is_not_pass": True,
        "default_deny": True,
        "promotion_allowed": decision == "VERIFIED",
    }


if __name__ == "__main__":
    result = evaluate_admission()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0)
