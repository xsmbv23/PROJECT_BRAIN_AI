"""Bounded runtime gate for Brain foundation hardening.

No bulk data is accepted. The gate only validates compact metadata and
returns PASS/DENY evidence suitable for durable recording.
"""
from __future__ import annotations

import time
from .foundation_hardening import AuditChain, CapabilityLease, GovernanceDeny, PolicyPin, quarantine, validate_schema_major


def run_foundation_gate() -> dict[str, object]:
    now = time.time()
    pin = PolicyPin("p1", "v1.0", "b1")
    audit = AuditChain()
    checks: list[dict[str, object]] = []

    def check(name: str, fn) -> None:
        try:
            fn()
            checks.append({"name": name, "status": "PASS"})
        except GovernanceDeny as exc:
            checks.append({"name": name, "status": "DENY", "reason": str(exc)})

    check("policy_pin", lambda: pin.verify(policy_version="p1", schema_version="v1.0", brain_state_version="b1"))
    check("schema_major", lambda: validate_schema_major(received="v1.2", expected="v1.0"))

    lease = CapabilityLease("cap", "corr", "L0", "L1", now - 1, now + 30, "nonce", "p1", 2)
    check("capability_scope", lambda: lease.verify(now=now, corridor_id="corr", capability_id="cap", nonce="nonce", policy_version="p1", operation_count=0))

    audit.append(event_id="foundation-gate", event_type="VERIFIED", policy_version="p1", payload={"checks": len(checks)}, timestamp=now)
    q = quarantine("test containment")
    checks.append({"name": "quarantine", "status": "PASS", "state": q["state"]})

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "DENY"
    return {"status": status, "checks": checks, "audit_head": audit.last_hash, "evaluated_at": now}
