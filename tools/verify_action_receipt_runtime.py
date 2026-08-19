"""Exact-current read-only action receipt gate.

The command searches persisted evidence/receipts for a receipt whose action_id
matches state.last_action_id. It never creates or modifies evidence/state.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from tools.action_receipt_validator import validate_action_receipt

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "current_state.json"
RECEIPTS = ROOT / "evidence" / "receipts"


def main() -> int:
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
        action = state.get("last_action_id") or state.get("last_action")
        next_action = state.get("next_action_id") or state.get("next_action")
        if not action or not next_action:
            raise ValueError("STATE_POINTER_MISSING")

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
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_MISSING", "action_id": action}, ensure_ascii=False))
            return 1
        if len(candidates) != 1:
            print(json.dumps({"status": "DENY", "reason": "RECEIPT_AMBIGUOUS", "action_id": action, "count": len(candidates)}, ensure_ascii=False))
            return 1

        path, receipt = candidates[0]
        runtime_commit = os.environ.get("RENDER_GIT_COMMIT", "")
        canonical_state = {
            "last_action_id": action,
            "next_action_id": next_action,
        }
        result = validate_action_receipt(receipt, canonical_state, {"commit_sha": runtime_commit})
        result["receipt_path"] = str(path.relative_to(ROOT))
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("status") == "PASS" else 1
    except Exception as exc:
        print(json.dumps({"status": "DENY", "reason": "VERIFIER_EXCEPTION", "exception_type": type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
