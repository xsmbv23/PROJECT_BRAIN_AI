"""Fail-closed validation for Bot 1/2/3 persistent handoffs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OWNERS = {"BOT_1", "BOT_2", "BOT_3"}
SEGMENTS = {
    "S1_REAL_DATA",
    "S2_VALID_RESEARCH",
    "S3_VALID_BACKTEST",
    "S4_EDGE",
    "S5_EV_PNL_ROI",
    "S6_ROBUSTNESS_RISK_DRIFT",
    "S7_CONTROLLED_ACTION",
}
CHALLENGES = {"ACK", "AGREE", "CHALLENGE", "UNKNOWN", "BLOCKED"}
REQUIRED = {
    "owner",
    "action_id",
    "e2e_segment",
    "blocker",
    "action",
    "evidence_refs",
    "result",
    "next_action",
    "peer_impact",
    "challenge_status",
}


def validate(payload: object) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not isinstance(payload, dict):
        return False, ["HANDOFF_NOT_OBJECT"]
    missing = sorted(REQUIRED - set(payload))
    if missing:
        reasons.append("MISSING:" + ",".join(missing))
    if payload.get("owner") not in OWNERS:
        reasons.append("OWNER_INVALID")
    if payload.get("e2e_segment") not in SEGMENTS:
        reasons.append("E2E_SEGMENT_INVALID")
    if payload.get("challenge_status") not in CHALLENGES:
        reasons.append("CHALLENGE_STATUS_INVALID")
    for field in ("action_id", "action", "result", "next_action"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            reasons.append(field.upper() + "_MISSING")
    if not isinstance(payload.get("evidence_refs"), list):
        reasons.append("EVIDENCE_REFS_NOT_LIST")
    elif any(not isinstance(item, str) or not item.strip() for item in payload["evidence_refs"]):
        reasons.append("EVIDENCE_REF_INVALID")
    if not isinstance(payload.get("blocker"), str):
        reasons.append("BLOCKER_NOT_STRING")
    if not isinstance(payload.get("peer_impact"), str):
        reasons.append("PEER_IMPACT_NOT_STRING")
    return not reasons, reasons


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"status": "DENY", "reasons": ["HANDOFF_ARGUMENT_REQUIRED"]}))
        return 2
    path = Path(sys.argv[1])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"status": "DENY", "reasons": ["HANDOFF_UNREADABLE"]}))
        return 1
    ok, reasons = validate(payload)
    print(json.dumps({"status": "PASS" if ok else "DENY", "reasons": reasons}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
