"""Verify the credential-free forensic database admission-chain contract.

This verifier checks architecture only. It never connects to PostgreSQL and
never reads or emits DATABASE_URL. Runtime binding/round-trip evidence remains
separate and cannot be manufactured by this verifier.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "architecture" / "FORENSIC_DATABASE_ADMISSION_CHAIN_V1.json"

EXPECTED_GATES = [
    ("DB_EXISTENCE", "DB_EXISTS", "DB_NOT_FOUND"),
    ("DB_BINDING", "BOUND", "NOT_BOUND"),
    ("DB_TLS_ADMISSION", "BOUND_TLS", "DENY_TLS"),
    ("DB_ROUND_TRIP", "SHA256_MATCH", "ROUND_TRIP_DENY"),
]


def verify() -> dict[str, object]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["schema"] == "FORENSIC_DATABASE_ADMISSION_CHAIN_V1"
    assert data["single_forensic_state"] is True
    assert data["non_inheritable_pass"] is True
    assert data["stop_on_first_failure"] is True
    assert data["later_gates_after_failure"] == "UNREACHED"
    assert data["failure_history"] == "IMMUTABLE"
    assert data["local_pass_equals_render_pass"] is False
    assert data["credential_values_are_evidence"] is False
    assert data["credential_storage"] == "RENDER_SECRET_ENV_ONLY"
    assert data["oom_guard_bytes"] == 320 * 1024 * 1024
    gates = [(x["id"], x["pass"], x["failure"]) for x in data["gates"]]
    assert gates == EXPECTED_GATES
    assert data["promotion_requires_all"] == [x[0] for x in EXPECTED_GATES]
    return {
        "database_admission_contract": "PASS",
        "single_forensic_state": True,
        "gate_count": len(gates),
        "non_inheritable_pass": True,
        "stop_on_first_failure": True,
        "failure_history": "IMMUTABLE",
        "credential_values_emitted": False,
        "render_memory_guard_bytes": data["oom_guard_bytes"],
    }


if __name__ == "__main__":
    print(verify())
