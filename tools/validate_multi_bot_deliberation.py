"""Validate a persistent multi-Bot deliberation record."""
from __future__ import annotations

import json
import sys

ALLOWED_BOTS = {"BOT1_LEAD", "BOT2_QUANT", "BOT3_EXECUTION"}
ALLOWED_POSITIONS = {"AGREE", "CHALLENGE", "CONDITIONAL", "UNKNOWN"}
REQUIRED = {
    "deliberation_id", "proposer", "reviewers", "e2e_segment", "blocker",
    "proposal", "evidence_refs", "assumptions", "positions",
    "objections_and_replies", "synthesized_decision", "chosen_owner",
    "safe_parallel_work", "unresolved_questions", "next_action",
}


def validate(record: dict) -> list[str]:
    reasons: list[str] = []
    missing = sorted(REQUIRED - set(record))
    if missing:
        reasons.append("MISSING:" + ",".join(missing))
    proposer = record.get("proposer")
    if proposer not in ALLOWED_BOTS:
        reasons.append("INVALID_PROPOSER")
    owner = record.get("chosen_owner")
    if owner not in ALLOWED_BOTS:
        reasons.append("INVALID_OWNER")
    reviewers = record.get("reviewers")
    if not isinstance(reviewers, list) or not reviewers:
        reasons.append("REVIEWERS_REQUIRED")
    else:
        bad = [r for r in reviewers if r not in ALLOWED_BOTS]
        if bad:
            reasons.append("INVALID_REVIEWER")
    positions = record.get("positions")
    if not isinstance(positions, dict) or not positions:
        reasons.append("POSITIONS_REQUIRED")
    else:
        for bot, position in positions.items():
            if bot not in ALLOWED_BOTS:
                reasons.append("INVALID_POSITION_BOT")
            if position not in ALLOWED_POSITIONS:
                reasons.append("INVALID_POSITION")
        if any(v == "CHALLENGE" for v in positions.values()):
            if not record.get("objections_and_replies"):
                reasons.append("CHALLENGE_REQUIRES_OBJECTION")
    if record.get("synthesized_decision") in {"PASS", "PROMOTE"}:
        reasons.append("DELIBERATION_CANNOT_GRANT_PROMOTION")
    return reasons


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"status": "DENY", "reasons": ["RECORD_ARGUMENT_REQUIRED"]}))
        return 2
    try:
        record = json.loads(open(argv[1], encoding="utf-8").read())
    except Exception:
        print(json.dumps({"status": "DENY", "reasons": ["RECORD_UNREADABLE"]}))
        return 1
    reasons = validate(record if isinstance(record, dict) else {})
    result = {"status": "PASS" if not reasons else "DENY", "reasons": reasons}
    print(json.dumps(result, sort_keys=True))
    return 0 if not reasons else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
