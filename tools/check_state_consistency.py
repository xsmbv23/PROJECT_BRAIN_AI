"""Check that persistent state and next-action pointers cannot silently drift.

State files are forensic artifacts, not transport envelopes. A valid state file
must be direct JSON with the required keys at the top level. Any wrapper such as
{\"content\": \"{...}\"} is a hard integrity failure.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CURRENT = (
    "next_action_id", "promotion", "layer_1", "staircase", "ci_status",
    "last_action_id", "pass_inheritance", "unknown_is_not_pass", "default_deny",
    "action_space", "action",
)
REQUIRED_NEXT = ("action_id", "status", "mode", "action_space", "promotion", "layer_1", "staircase")


def _read_direct_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be a JSON object")
    if "content" in value or "encoding" in value or "sha" in value:
        raise ValueError(f"{path.name} is a transport envelope, not a direct state artifact")
    return value


def main() -> int:
    try:
        current = _read_direct_json(ROOT / "state/current_state.json")
        nxt = _read_direct_json(ROOT / "state/next_action.json")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print({"status": "FAIL", "errors": [f"state integrity failure: {exc}"]})
        return 1

    errors = []
    missing = [key for key in REQUIRED_CURRENT if key not in current]
    if missing:
        errors.append(f"missing required current_state keys: {','.join(missing)}")
    missing_next = [key for key in REQUIRED_NEXT if key not in nxt]
    if missing_next:
        errors.append(f"missing required next_action keys: {','.join(missing_next)}")

    if not errors and current["next_action_id"] != nxt["action_id"]:
        errors.append(f"next_action mismatch: current={current['next_action_id']} state={nxt['action_id']}")
    if current.get("promotion") != "DENY" or nxt.get("promotion") != "HARD_DENY":
        errors.append("promotion must remain denied during foundation")
    if current.get("layer_1") not in {"LOCKED", "ROOM_01_GATE_LOCKED"} or nxt.get("layer_1") != "LOCKED":
        errors.append("layer_1 must remain LOCKED during foundation")
    if current.get("staircase") != "LOCKED" or nxt.get("staircase") != "LOCKED":
        errors.append("staircase must remain LOCKED during foundation")
    if current.get("pass_inheritance") is not False:
        errors.append("pass_inheritance must be false")
    if current.get("unknown_is_not_pass") is not True:
        errors.append("unknown_is_not_pass must be true")
    if current.get("default_deny") is not True:
        errors.append("default_deny must be true")
    if current.get("action_space") != 0 or nxt.get("action_space") != 0:
        errors.append("action_space must remain zero")
    if current.get("action") != "MANDATORY_NO_OP" or nxt.get("mode") != "MANDATORY_NO_OP":
        errors.append("action must remain MANDATORY_NO_OP")
    if current.get("ci_status") not in {"PENDING", "UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN", "PASS", "FAIL"}:
        errors.append("invalid ci_status")
    if errors:
        print({"status": "FAIL", "errors": errors})
        return 1
    print({"status": "PASS", "last_action_id": current["last_action_id"], "next_action_id": current["next_action_id"], "promotion": current["promotion"], "layer_1": current["layer_1"], "staircase": current["staircase"], "action_space": current["action_space"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
