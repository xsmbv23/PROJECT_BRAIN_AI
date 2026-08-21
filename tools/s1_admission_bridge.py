"""Bridge S1 canonical evidence into the single Forensic FSM.

This is a pure decision adapter. It cannot create evidence and cannot unlock
Room 02. It maps verifier output to the canonical gate state:

S1_CANONICAL_EVIDENCE_ADMITTED -> S1 PASS / next gate may be evaluated
anything else                  -> S1 DENY / downstream UNREACHED
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from tools.verify_s1_canonical_evidence import verify_manifest


def evaluate_s1(manifest_path: str | Path) -> dict[str, object]:
    evidence = verify_manifest(manifest_path)
    passed = evidence.get("status") == "PASS"
    return {
        "fsm": "ONE_FORENSIC_FSM",
        "gate": "S1_CANONICAL_EVIDENCE",
        "status": "PASS" if passed else "DENY",
        "pass_is_local": True,
        "pass_is_prerequisite_only": True,
        "no_pass_inheritance": True,
        "downstream": "S2_VALID_RESEARCH_EVALUABLE" if passed else "S2_VALID_RESEARCH_UNREACHED",
        "promotion": "DENY" if not passed else "NEXT_GATE_ONLY",
        "evidence": evidence,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"status": "DENY", "reason": "MANIFEST_ARGUMENT_REQUIRED"}))
        return 2
    result = evaluate_s1(argv[1])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
