from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ALLOWED_EPISTEMIC = {"REPORTED", "INFERRED", "VERIFIED", "UNKNOWN"}
ALLOWED_STATUS = {"NOT_STARTED", "ACKNOWLEDGED", "IN_DELIBERATION", "ACTION_QUEUED", "CLOSED"}


def validate(payload: dict) -> tuple[bool, str]:
    required = {
        "bridge_id", "message_id", "source", "target_bots", "relayed_at",
        "content_sha256", "content", "interpretation", "next_action_status"
    }
    missing = sorted(required - payload.keys())
    if missing:
        return False, f"MISSING:{','.join(missing)}"
    if payload["bridge_id"] != "CHAT_TO_DELIBERATION_V1":
        return False, "INVALID_BRIDGE_ID"
    if payload["source"] != "USER_RELAY":
        return False, "INVALID_SOURCE"
    actual = hashlib.sha256(payload["content"].encode("utf-8")).hexdigest()
    if actual != payload["content_sha256"]:
        return False, "CONTENT_SHA256_MISMATCH"
    interp = payload["interpretation"]
    for key in ("claims", "proposals", "challenges", "requested_actions", "evidence_refs", "epistemic_status"):
        if key not in interp:
            return False, f"MISSING_INTERPRETATION:{key}"
    if interp["epistemic_status"] not in ALLOWED_EPISTEMIC:
        return False, "INVALID_EPISTEMIC_STATUS"
    if payload["next_action_status"] not in ALLOWED_STATUS:
        return False, "INVALID_NEXT_ACTION_STATUS"
    if interp["epistemic_status"] == "REPORTED" and not payload["content"].strip():
        return False, "EMPTY_REPORTED_CONTENT"
    return True, "OK"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    ok, reason = validate(payload)
    print(json.dumps({"valid": ok, "reason": reason}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
