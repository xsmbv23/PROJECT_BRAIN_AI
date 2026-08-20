"""Boot-time ACTION_RECEIPT gate.

Boot must never depend on a durable receipt query. It reads only repository
historical receipts and remains DENY when the exact prior runtime receipt is
not present there. The live read-only governance boundary performs the durable
same-deployment receipt verification after the service is up.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from tools.action_receipt_validator import validate_action_receipt

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

        candidates = []
        if RECEIPTS.exists():
            for path in RECEIPTS.rglob("*.json"):
                try:
                    obj = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError, json.JSONDecodeError):
                    continue
                if isinstance(obj, dict) and obj.get("action_id") == action:
                    candidates.append((path, obj))
        if not candidates:
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_MISSING", "action_id": action, "commit_sha": runtime_commit, "deployment_id": deployment_id, "deployment_identity_type": identity_type}, ensure_ascii=False))
            return 1
        if len(candidates) != 1:
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_AMBIGUOUS", "action_id": action, "count": len(candidates)}, ensure_ascii=False))
            return 1

        _, receipt = candidates[0]
        result = validate_action_receipt(receipt, {"last_action_id": action, "next_action_id": next_action}, {"commit_sha": runtime_commit})
        if receipt.get("deployment_id") != deployment_id:
            result = {"status": "DENY", "reason": "RECEIPT_DEPLOYMENT_ID_MISMATCH"}
        result["receipt_origin"] = "REPOSITORY_LEGACY"
        result["deployment_identity_type"] = identity_type
        result["pass_is_local"] = True
        result["promotes"] = False
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("status") == "PASS" else 1
    except Exception as exc:
        print(json.dumps({"status": "DENY", "reason": "VERIFIER_EXCEPTION", "exception_type": type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
