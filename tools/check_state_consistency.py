"""Check that persistent state and next-action pointers cannot silently drift."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    current = json.loads((ROOT / "state/current_state.json").read_text(encoding="utf-8"))
    nxt = json.loads((ROOT / "state/next_action.json").read_text(encoding="utf-8"))

    errors = []
    if current["next_action_id"] != nxt["action_id"]:
        errors.append(f"next_action mismatch: current={current['next_action_id']} state={nxt['action_id']}")
    if current["promotion"] != "DENY":
        errors.append("promotion must remain DENY during foundation")
    if current["layer_1"] != "LOCKED":
        errors.append("layer_1 must remain LOCKED during foundation")
    if current["staircase"] != "LOCKED":
        errors.append("staircase must remain LOCKED during foundation")
    if current["ci_status"] not in {"PENDING", "UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN", "PASS", "FAIL"}:
        errors.append("invalid ci_status")
    if errors:
        print({"status": "FAIL", "errors": errors})
        return 1
    print({"status": "PASS", "last_action_id": current["last_action_id"], "next_action_id": current["next_action_id"], "promotion": current["promotion"], "layer_1": current["layer_1"], "staircase": current["staircase"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
