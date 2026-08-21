"""Fail-closed reconciliation of persistent Brain state and next action.

State artifacts are forensic truth, not transport envelopes. The verifier never
infers a gate transition from another gate's PASS. Every downstream admission
requires its own explicit evidence/state/action tuple.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CURRENT = (
    "next_action_id", "promotion", "layer_1", "staircase", "ci_status",
    "last_action_id", "pass_inheritance", "unknown_is_not_pass", "default_deny",
    "action_space", "action", "state_mode", "state",
)
REQUIRED_NEXT = ("action_id", "status", "mode", "action_space", "promotion", "layer_1", "staircase")
VALID_CI = {"PENDING", "UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN", "PASS", "FAIL"}


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

    errors: list[str] = []
    missing = [key for key in REQUIRED_CURRENT if key not in current]
    if missing:
        errors.append(f"missing required current_state keys: {','.join(missing)}")
    missing_next = [key for key in REQUIRED_NEXT if key not in nxt]
    if missing_next:
        errors.append(f"missing required next_action keys: {','.join(missing_next)}")

    if not errors:
        if current["next_action_id"] != nxt["action_id"]:
            errors.append(f"next_action mismatch: current={current['next_action_id']} state={nxt['action_id']}")
        if current["action_space"] != nxt["action_space"]:
            errors.append("action_space mismatch between current_state and next_action")
        if current["state_mode"] != nxt["mode"]:
            errors.append("state_mode/mode mismatch between current_state and next_action")
        if current["promotion"] != nxt["promotion"]:
            errors.append("promotion mismatch between current_state and next_action")
        if current["layer_1"] != nxt["layer_1"]:
            errors.append("layer_1 mismatch between current_state and next_action")
        if current["staircase"] != nxt["staircase"]:
            errors.append("staircase mismatch between current_state and next_action")

    mode = current.get("state_mode")
    if mode == "FOUNDATION_LOCKED":
        if current.get("promotion") != "DENY" or nxt.get("promotion") != "HARD_DENY":
            errors.append("foundation mode requires promotion DENY/HARD_DENY")
        if current.get("layer_1") not in {"LOCKED", "ROOM_01_GATE_LOCKED"} or nxt.get("layer_1") != "LOCKED":
            errors.append("foundation mode requires layer_1 LOCKED")
        if current.get("staircase") != "LOCKED" or nxt.get("staircase") != "LOCKED":
            errors.append("foundation mode requires staircase LOCKED")
        if current.get("action_space") != 0 or nxt.get("action_space") != 0:
            errors.append("foundation mode requires action_space zero")
        if current.get("action") != "MANDATORY_NO_OP" or nxt.get("mode") != "MANDATORY_NO_OP":
            errors.append("foundation mode requires MANDATORY_NO_OP")
    elif mode == "DATA_ADMISSION":
        if current.get("promotion") != "PASS_TO_ROOM_01_ONLY;CANONICAL_QUORUM_DENY":
            errors.append("DATA_ADMISSION requires promotion limited to Room 01 with canonical quorum denied")
        if nxt.get("promotion") != current.get("promotion"):
            errors.append("DATA_ADMISSION promotion must remain locally scoped")
        if current.get("layer_1") != "ROOM_01_DATA_ADMISSION" or nxt.get("layer_1") != "ROOM_01_DATA_ADMISSION":
            errors.append("DATA_ADMISSION requires Room 01 only")
        if current.get("staircase") != "LOCKED" or nxt.get("staircase") != "LOCKED":
            errors.append("DATA_ADMISSION requires staircase LOCKED")
        if current.get("action_space") != 1 or nxt.get("action_space") != 1:
            errors.append("DATA_ADMISSION requires exactly one admitted action slot")
        allowed_actions = {"RUNTIME_PROVENANCE_EXECUTION", "PERMITTED_INDEPENDENT_SOURCE_ADMISSION"}
        allowed_states = {"SOURCE_PROVENANCE_CAPTURE", "SOURCE_INDEPENDENCE_AUDIT"}
        if current.get("action") not in allowed_actions:
            errors.append("DATA_ADMISSION current action is outside the admitted Room 01 action set")
        if nxt.get("mode") != "DATA_ADMISSION" or nxt.get("status") != "READY":
            errors.append("DATA_ADMISSION next action must be READY in DATA_ADMISSION mode")
        if current.get("state") not in allowed_states:
            errors.append("DATA_ADMISSION current state is outside the admitted provenance states")
    else:
        errors.append(f"unknown state_mode: {mode}")

    if current.get("pass_inheritance") is not False:
        errors.append("pass_inheritance must be false")
    if current.get("unknown_is_not_pass") is not True:
        errors.append("unknown_is_not_pass must be true")
    if current.get("default_deny") is not True:
        errors.append("default_deny must be true")
    if current.get("ci_status") not in VALID_CI:
        errors.append("invalid ci_status")

    if errors:
        print({"status": "FAIL", "errors": errors})
        return 1
    print({
        "status": "PASS",
        "state_mode": mode,
        "state": current["state"],
        "last_action_id": current["last_action_id"],
        "next_action_id": current["next_action_id"],
        "promotion": current["promotion"],
        "layer_1": current["layer_1"],
        "staircase": current["staircase"],
        "action_space": current["action_space"],
        "action": current["action"],
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
