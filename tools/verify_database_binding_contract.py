"""Validate the immutable, credential-free Render database admission contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "render_database_binding.json"

GATES = ("DB_EXISTENCE", "DB_BINDING", "DB_TLS_ADMISSION", "DB_ROUND_TRIP", "PROMOTION")


def verify() -> dict[str, object]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    required = {
        "contract_id": "RENDER_DB_BINDING_V1",
        "required_runtime_binding": "DATABASE_URL",
        "credential_storage": "RENDER_SECRET_ENV_ONLY",
        "github_credential_storage": False,
        "promotion_gate": "DENY_UNTIL_BOUND_TLS_AND_ROUND_TRIP_PROVEN",
    }
    for key, value in required.items():
        if data.get(key) != value:
            raise AssertionError(f"binding contract mismatch: {key}")
    if set(data.get("required_tls_modes", [])) != {"require", "verify-ca", "verify-full"}:
        raise AssertionError("TLS admission contract mismatch")
    if set(data.get("required_scheme", [])) != {"postgresql", "postgres"}:
        raise AssertionError("PostgreSQL scheme contract mismatch")
    if data.get("round_trip_payload_policy") != "NO_SOURCE_DATA_NO_CREDENTIALS_NO_BULK_DATA":
        raise AssertionError("round-trip payload policy mismatch")
    if data.get("oom_guard_bytes") != 335544320:
        raise AssertionError("OOM guard contract mismatch")
    return {
        "status": "PASS",
        "contract_id": data["contract_id"],
        "ordered_gates": list(GATES),
        "rule": "PASS_AT_GATE_IS_PREREQUISITE_ONLY; NEVER_INFER_DEEPER_PASS",
        "unknown_is_not_pass": True,
        "promotion_requires": ["BOUND_TLS", "COMPACT_WRITE_READ", "SHA256_MATCH"],
    }


if __name__ == "__main__":
    print(verify())
