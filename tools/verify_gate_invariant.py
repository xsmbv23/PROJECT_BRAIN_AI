"""Executable regression verifier for FORENSIC_GATE_INVARIANT_V1."""
from __future__ import annotations

import json
from pathlib import Path

from tools.gate_invariant import GateDefinition, GateResult, check_gate_invariant, gate_chain_is_valid

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "forensic_gate_invariant_v1.json"


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    rules = contract["rules"]
    if not all(rules.values()):
        print({"gate_invariant": "DENY", "reason": "CONTRACT_RULE_FALSE"})
        return 1

    now = 1_000_000.0
    first = GateResult("DB_EXISTENCE", "PASS", "evidence-a", now, "cycle-1")
    second = GateDefinition("DB_BINDING", depends_on=("DB_EXISTENCE",))
    ok, reason = check_gate_invariant(second, [first], now=now)
    if not ok or reason != "ADMITTED":
        print({"gate_invariant": "DENY", "reason": "VALID_CHAIN_REJECTED", "detail": reason})
        return 1

    reused = [first, GateResult("DB_BINDING", "PASS", "evidence-a", now, "cycle-1")]
    ok, reason = gate_chain_is_valid(reused, now=now)
    if ok or reason != "EVIDENCE_REUSE:DB_BINDING":
        print({"gate_invariant": "DENY", "reason": "EVIDENCE_REUSE_NOT_DETECTED", "detail": reason})
        return 1

    stale = GateResult("DB_EXISTENCE", "PASS", "evidence-stale", now - 301, "cycle-1")
    ok, reason = check_gate_invariant(second, [stale], now=now)
    if ok or reason != "STALE_EVIDENCE:DB_EXISTENCE":
        print({"gate_invariant": "DENY", "reason": "STALE_EVIDENCE_NOT_DETECTED", "detail": reason})
        return 1

    print({"gate_invariant": "PASS", "contract": contract["contract_id"], "ttl_seconds": rules["EVIDENCE_TTL_SECONDS"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
