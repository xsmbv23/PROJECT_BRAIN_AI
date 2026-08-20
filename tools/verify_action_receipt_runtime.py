"""Exact-current read-only action receipt gate.

The verifier only reads receipts emitted by a prior runtime execution boundary.
It never creates or modifies evidence/state. Durable receipts are preferred;
legacy repository receipts remain a compatibility path.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from tools.action_receipt_validator import validate_action_receipt
from tools.action_receipt_store import find_exact_action_receipt

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "evidence" / "receipts"


def main() -> int:
    try:
        state = json.loads((ROOT / "state" / "current_state.json").read_text(encoding="utf-8"))
        action = state.get("last_action_id")
        next_action = state.get("next_action_id")
        runtime_commit = os.environ.get("RENDER_GIT_COMMIT", "")
        deployment_id = os.environ.get("RENDER_DEPLOY_ID", "")
        if not action or not next_action or not runtime_commit or not deployment_id:
            print(json.dumps({"status": "DENY", "reason": "RUNTIME_ACTION_IDENTITY_MISSING"}, ensure_ascii=False))
            return 1

        receipt = None
        receipt_origin = "NONE"
        try:
            receipt = find_exact_action_receipt(action_id=action, commit_sha=runtime_commit, deployment_id=deployment_id)
            if receipt:
                receipt_origin = "DURABLE_POSTGRES_PRIOR_RUNTIME"
        except Exception:
            receipt = None

        if receipt is None and RECEIPTS.exists():
            candidates = []
            for path in RECEIPTS.rglob("*.json"):
                try:
                    obj = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError, json.JSONDecodeError):
                    continue
                if isinstance(obj, dict) and obj.get("action_id") == action:
                    candidates.append((path, obj))
            if len(candidates) == 1:
                receipt_origin = "REPOSITORY_LEGACY"
                receipt = candidates[0][1]
            elif len(candidates) > 1:
                print(json.dumps({"status": "DENY", "reason": "RECEIPT_AMBIGUOUS", "action_id": action, "count": len(candidates)}, ensure_ascii=False))
                return 1

        if receipt is None:
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_MISSING", "action_id": action, "commit_sha": runtime_commit, "deployment_id": deployment_id}, ensure_ascii=False))
            return 1

        canonical_state = {"last_action_id": action, "next_action_id": next_action}
        result = validate_action_receipt(receipt, canonical_state, {"commit_sha": runtime_commit})
        result["receipt_origin"] = receipt_origin
        result["deployment_id"] = deployment_id
        result["pass_is_local"] = True
        result["promotes"] = False
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("status") == "PASS" else 1
    except Exception as exc:
        print(json.dumps({"status": "DENY", "reason": "VERIFIER_EXCEPTION", "exception_type": type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
