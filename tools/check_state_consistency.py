"""Check that persistent state and next-action pointers cannot silently drift."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CURRENT = ("next_action_id", "promotion", "layer_1", "staircase", "ci_status", "last_action_id")


def main() -> int:
    try:
        current = json.loads((ROOT / "state/current_state.json").read_text(encoding="utf-8"))
        nxt = json.loads((ROOT / "state/next_action.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print({"status": "FAIL", "errors": [f"state read/parse failure: {exc.__class__.__name__}"]})
        return 1

    errors = []
    missing = [key for key in REQUIRED_CURRENT if key not in current]
    if missing:
        errors.append(f"missing required current_state keys: {','.join(missing)}")
    if "action_id" not in nxt:
        errors.append("next_action missing action_id")

    if not errors and current["next_action_id"] != nxt["action_id"]:
        errors.append(f"next_action mismatch: current={current['next_action_id']} state={nxt['action_id']}")
    if current.get("promotion") != "DENY":
        errors.append("promotion must remain DENY during foundation")
    if current.get("layer_1") not in {"LOCKED", "ROOM_01_GATE_LOCKED"}:
        errors.append("layer_1 must remain LOCKED during foundation")
    if current.get("staircase") != "LOCKED":
        errors.append("staircase must remain LOCKED during foundation")
    if current.get("ci_status") not in {"PENDING", "UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN", "PASS", "FAIL"}:
        errors.append("invalid ci_status")
    if errors:
        print({"status": "FAIL", "errors": errors})
        return 1
    print({"status": "PASS", "last_action_id": current["last_action_id"], "next_action_id": current["next_action_id"], "promotion": current["promotion"], "layer_1": current["layer_1"], "staircase": current["staircase"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
