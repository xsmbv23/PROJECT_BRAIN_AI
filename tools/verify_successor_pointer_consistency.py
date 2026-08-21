"""Detect disagreement between persistent successor state pointers.

Both current_state.json and next_action.json are authoritative. They must agree
on the next action. A disagreement is a forensic integrity problem and must not
be silently resolved by guessing which file is newer.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "state" / "current_state.json"
NEXT = ROOT / "state" / "next_action.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify() -> dict[str, object]:
    reasons: list[str] = []
    try:
        current = _load(CURRENT)
        nxt = _load(NEXT)
    except Exception as exc:
        return {"verifier": "successor_pointer_consistency", "status": "DENY", "reasons": [f"STATE_UNREADABLE:{type(exc).__name__}"]}

    current_next = current.get("next_action_id")
    next_id = nxt.get("action_id")
    if not current_next or not next_id:
        reasons.append("NEXT_ACTION_POINTER_MISSING")
    elif current_next != next_id:
        reasons.append(f"POINTER_MISMATCH:{current_next}!={next_id}")

    last_action = current.get("last_action_id")
    if last_action and next_id and last_action == next_id:
        reasons.append("LAST_ACTION_EQUALS_NEXT_ACTION")

    status = "PASS" if not reasons else "DENY"
    return {
        "verifier": "successor_pointer_consistency",
        "status": status,
        "current_next_action_id": current_next,
        "next_action_file_id": next_id,
        "last_action_id": last_action,
        "reasons": reasons,
        "policy": "DO_NOT_GUESS_ON_POINTER_DRIFT",
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
