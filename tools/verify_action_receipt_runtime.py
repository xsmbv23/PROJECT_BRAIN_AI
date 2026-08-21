"""Boot-time ACTION_RECEIPT gate.

The verifier reads the durable PostgreSQL receipt store written by the prior
runtime boundary. Repository receipts remain a legacy fallback only. A prior
receipt is never required to match the current runtime commit or deployment
identity; instead it must belong to a different prior runtime boundary.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from tools.action_receipt_validator import validate_action_receipt
from tools.durable_postgres import DurableEvidenceDeny

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "evidence" / "receipts"


def deployment_identity() -> tuple[str, str]:
    value = os.environ.get("RENDER_DEPLOY_ID", "")
    if value:
        return value, "RENDER_DEPLOY_ID"
    value = os.environ.get("RENDER_INSTANCE_ID", "")
    if value:
        return value, "RENDER_INSTANCE_ID"
    return "", "NONE"


def _load_prior_receipt_from_db(action_id: str) -> dict | None:
    from tools.action_receipt_store import find_latest_action_receipt
    return find_latest_action_receipt(action_id=action_id)


def _load_legacy_receipts(action_id: str) -> list[dict]:
    candidates = []
    if not RECEIPTS.exists():
        return candidates
    for path in RECEIPTS.rglob("*.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if isinstance(obj, dict) and obj.get("action_id") == action_id:
            candidates.append(obj)
    return candidates


def main() -> int:
    try:
        state = json.loads((ROOT / "state" / "current_state.json").read_text(encoding="utf-8"))
        action = state.get("last_action_id")
        next_action = state.get("next_action_id")
        runtime_commit = os.environ.get("RENDER_GIT_COMMIT", "")
        deployment_id, identity_type = deployment_identity()
        if not action or not next_action or not runtime_commit or not deployment_id:
            print(json.dumps({"status": "DENY", "reason": "RUNTIME_ACTION_IDENTITY_MISSING", "deployment_identity_type": identity_type}, ensure_ascii=False))
            return 1

        receipt = None
        receipt_origin = ""
        try:
            receipt = _load_prior_receipt_from_db(action)
            if receipt:
                receipt_origin = "DURABLE_POSTGRES"
        except DurableEvidenceDeny:
            receipt = None

        if receipt is None:
            legacy = _load_legacy_receipts(action)
            if len(legacy) == 1:
                receipt = legacy[0]
                receipt_origin = "REPOSITORY_LEGACY"
            elif len(legacy) > 1:
                print(json.dumps({"status": "DENY", "reason": "RECEIPT_AMBIGUOUS", "action_id": action, "count": len(legacy)}, ensure_ascii=False))
                return 1

        if receipt is None:
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_MISSING", "action_id": action, "commit_sha": runtime_commit, "deployment_id": deployment_id, "deployment_identity_type": identity_type}, ensure_ascii=False))
            return 1

        result = validate_action_receipt(
            receipt,
            {"last_action_id": action, "next_action_id": next_action},
            {"commit_sha": runtime_commit},
            prior_runtime=True,
        )
        if receipt.get("deployment_id") == deployment_id:
            result = {"status": "DENY", "reason": "RECEIPT_IS_CURRENT_RUNTIME_NOT_PRIOR"}
        result["receipt_origin"] = receipt_origin
        result["deployment_identity_type"] = identity_type
        result["current_runtime_commit"] = runtime_commit
        result["prior_runtime_commit"] = receipt.get("commit_sha", "UNKNOWN")
        result["prior_runtime_deployment_id"] = receipt.get("deployment_id", "UNKNOWN")
        result["pass_is_local"] = True
        result["promotes"] = False
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("status") == "PASS" else 1
    except Exception as exc:
        print(json.dumps({"status": "DENY", "reason": "VERIFIER_EXCEPTION", "exception_type": type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
