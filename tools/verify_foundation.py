"""Deterministic stdlib-only foundation verification runner."""
from __future__ import annotations

import pathlib
import re
import sys
import time
import tracemalloc
import unittest

from core.brain_role import BrainRole, Plane, PlaneRequest
from core.corridor_lock import RoomLock, authorize_room
from core.corridor_sensor import sense_corridor_presence
from core.durable_audit import seal_head
from core.durable_state import persist_audit_head, restore_audit_head
from core.foundation_gate import run_foundation_gate
from core.foundation_hardening import AuditChain, CapabilityLease, GovernanceDeny, PolicyPin
from core.inner_latch import InnerLatch, InnerLatchPolicy, InnerLatchState
from core.security_chain import evaluate_entry_request

ROOT = pathlib.Path(__file__).resolve().parents[1]


def source_scan() -> None:
    # Detector implementation and adversarial tests intentionally contain signatures.
    banned = re.compile(r"(?i)(postgres(?:ql)?://|redis://|-----BEGIN .*PRIVATE KEY-----)")
    verifier_path = pathlib.Path(__file__).resolve()
    detector_path = ROOT / "core" / "credential_guard.py"
    ignored_dirs = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
    ignored_suffixes = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".so", ".dylib", ".dll", ".whl"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path in {verifier_path, detector_path} or any(part in ignored_dirs for part in path.parts) or "tests" in path.parts or path.suffix.lower() in ignored_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeError):
            continue
        if banned.search(text):
            raise AssertionError(f"credential-like material detected: {path}")


def adapter_import_scan() -> None:
    forbidden = ("psycopg", "asyncpg", "redis", "requests", "httpx", "urllib.request")
    for path in (ROOT / "core").glob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if re.search(rf"^\s*(?:from|import)\s+{re.escape(token)}", text, re.MULTILINE):
                raise AssertionError(f"direct runtime adapter import in core: {path}: {token}")


def durable_round_trip() -> None:
    class Store:
        def __init__(self): self.data = {}
        def put(self, k, v): self.data[k] = v
        def get(self, k): return self.data.get(k)
    chain = AuditChain()
    chain.append(event_id="verify", event_type="VERIFIED", policy_version="p1", payload={}, timestamp=1)
    env = seal_head(chain, policy_version="p1", schema_version="v1.0", brain_state_version="b1", event_count=1, generated_at=2)
    store = Store(); persist_audit_head(store, env)
    restored = restore_audit_head(store, policy="p1", schema="v1.0", brain_state="b1", expected_head=env.audit_head)
    assert restored.envelope.audit_head == env.audit_head


def brain_governance_round_trip() -> None:
    brain = BrainRole(PolicyPin("P1", "v1.0", "B1"))
    lease = CapabilityLease(
        capability_id="CAP_A", corridor_id="HALL_A", source_layer="CHAT", destination_layer="SECURITY",
        issued_at=90.0, expires_at=200.0, nonce="N1", policy_version="P1", max_operations=3,
    )
    request = PlaneRequest(
        source=Plane.CHAT, destination=Plane.SECURITY, corridor_id="HALL_A",
        policy_version="P1", schema_version="v1.2", brain_state_version="B1",
        capability_id="CAP_A", nonce="N1",
    )
    assert brain.authorize(request, lease=lease, expected_schema_major="v1", now=100.0) == "ADMISSIBLE_FOR_NEXT_GATE"
    with unittest.TestCase().assertRaises(GovernanceDeny):
        brain.authorize(request, lease=lease, expected_schema_major="v1", now=201.0)
    with unittest.TestCase().assertRaises(GovernanceDeny):
        brain.authorize(request, lease=lease, expected_schema_major="v1", now=100.0, operation_count=3)
    with unittest.TestCase().assertRaises(GovernanceDeny):
        brain.authorize(
            PlaneRequest(**{**request.__dict__, "destination": Plane.BRAIN}),
            lease=lease, expected_schema_major="v1", now=100.0,
        )


def room_lock_round_trip() -> None:
    room = RoomLock("ROOM_A", 1, "CAP_A", "KEY_A", ("HALL_A",), ("ROOM_A",), ((0, 1),))
    authorize_room(room, presented_capability="CAP_A", key_fingerprint="KEY_A", source_room="HALL_A", destination_room="ROOM_A", source_layer=0, destination_layer=1)
    try:
        authorize_room(room, presented_capability="CAP_A", key_fingerprint="KEY_A", source_room="HALL_A", destination_room="ROOM_A", source_layer=-1, destination_layer=1)
    except GovernanceDeny:
        return
    raise AssertionError("unlisted layer edge must deny")


def corridor_sensor_round_trip() -> None:
    signal = sense_corridor_presence(corridor_id="HALL_A", sensor_id="SENSOR_A", source_room="HALL_X", destination_room="ROOM_A", authorized=False)
    assert signal.light_on is True
    assert signal.level == "WARNING"
    assert signal.event == "UNAUTHORIZED_CORRIDOR_APPROACH"


def inner_latch_round_trip() -> None:
    latch = InnerLatch(InnerLatchPolicy(
        room_id="OWNER_ROOM", security_level=3,
        requires_inner_release=True,
        authorized_occupant_capabilities=("OWNER_PRESENT",),
    ))
    latch.request_entry(room_id="OWNER_ROOM", external_authorized=True)
    assert latch.state == InnerLatchState.RINGING
    try:
        latch.assert_entry_released()
    except GovernanceDeny:
        pass
    else:
        raise AssertionError("high-security room must remain latched after ringing")
    latch.release_from_inside(occupant_capability="OWNER_PRESENT")
    latch.assert_entry_released()
    assert latch.state == InnerLatchState.RELEASED


def unified_security_chain_round_trip() -> None:
    lock = RoomLock("OWNER_ROOM", 3, "CAP_A", "KEY_A", ("HALL_A",), ("OWNER_ROOM",), ((2, 3),))
    latch = InnerLatch(InnerLatchPolicy("OWNER_ROOM", 3, True, ("OWNER_PRESENT",)))
    decision = evaluate_entry_request(
        lock=lock, latch=latch, corridor_id="HALL_A", sensor_id="SENSOR_A",
        source_room="HALL_A", destination_room="OWNER_ROOM",
        source_layer=2, destination_layer=3, capability="CAP_A", key_fingerprint="KEY_A",
    )
    assert decision.external_authorized is True
    assert decision.entry_authorized is False
    assert decision.reason == "INNER_LATCH_SECURED"
    assert latch.state == InnerLatchState.RINGING


def main() -> int:
    tracemalloc.start(); started = time.monotonic()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    source_scan(); adapter_import_scan(); durable_round_trip(); brain_governance_round_trip(); room_lock_round_trip(); corridor_sensor_round_trip(); inner_latch_round_trip(); unified_security_chain_round_trip()
    gate = run_foundation_gate()
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    report = {"tests_ok": result.wasSuccessful(), "gate": gate["status"], "source_scan": "PASS", "adapter_import_scan": "PASS", "durable_round_trip": "PASS", "brain_governance": "PASS", "room_lock": "PASS", "corridor_sensor": "PASS", "inner_latch": "PASS", "security_chain": "PASS", "tracemalloc_peak_bytes": peak, "elapsed_seconds": round(time.monotonic()-started, 4)}
    print(report)
    return 0 if result.wasSuccessful() and gate["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
