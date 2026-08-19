"""Brain-level state drift detector.

Purpose: prevent a successor Bot or runtime from silently moving backward to an
older checkpoint, or from treating repository state as proof of runtime state.
This detector checks structural identity only. It never upgrades a gate.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_state(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or any(k in obj for k in ("content", "encoding", "sha")):
        raise ValueError(f"{path.name} must be a direct JSON state artifact")
    return obj


def detect_drift() -> dict[str, object]:
    current = read_state(ROOT / "state/current_state.json")
    nxt = read_state(ROOT / "state/next_action.json")
    errors: list[str] = []

    pairs = (
        ("next_action_id", "action_id"),
        ("action_space", "action_space"),
        ("state_mode", "mode"),
        ("promotion", "promotion"),
        ("layer_1", "layer_1"),
        ("staircase", "staircase"),
    )
    for left, right in pairs:
        if current.get(left) != nxt.get(right):
            errors.append(f"state/next mismatch: {left}={current.get(left)!r}, next.{right}={nxt.get(right)!r}")

    if current.get("last_action_id") == current.get("next_action_id"):
        errors.append("last_action_id must not equal next_action_id")

    if current.get("pass_inheritance") is not False:
        errors.append("pass_inheritance must remain false")
    if current.get("unknown_is_not_pass") is not True:
        errors.append("unknown_is_not_pass must remain true")
    if current.get("default_deny") is not True:
        errors.append("default_deny must remain true")

    # Repository state can describe the expected runtime, but cannot certify it.
    # A runtime identity mismatch is therefore a DENY condition, never an auto-fix.
    if current.get("runtime_boot_gate") == "PASS" and current.get("last_verified_runtime_commit") in {None, "", "UNKNOWN"}:
        errors.append("runtime_boot_gate PASS requires an explicit verified runtime commit")

    # Guard against an accidental return to a pre-admission phase.
    if current.get("state_mode") == "DATA_ADMISSION":
        forbidden = {"FOUNDATION_LOCKED", "FOUNDATION", "BOOTSTRAP"}
        if current.get("state") in forbidden:
            errors.append("DATA_ADMISSION cannot regress to foundation/bootstrap state")
        if current.get("layer_1") != "ROOM_01_DATA_ADMISSION":
            errors.append("DATA_ADMISSION cannot regress or jump layer_1")
        if current.get("staircase") != "LOCKED":
            errors.append("DATA_ADMISSION staircase must remain locked")

    return {
        "status": "PASS" if not errors else "DENY",
        "drift": bool(errors),
        "errors": errors,
        "last_action_id": current.get("last_action_id"),
        "next_action_id": current.get("next_action_id"),
        "state_mode": current.get("state_mode"),
        "state": current.get("state"),
        "promotion": current.get("promotion"),
        "layer_1": current.get("layer_1"),
        "staircase": current.get("staircase"),
    }


if __name__ == "__main__":
    print(detect_drift())
