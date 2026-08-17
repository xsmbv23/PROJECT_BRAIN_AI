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
        if (
            not path.is_file()
            or path in {verifier_path, detector_path}
            or any(part in ignored_dirs for part in path.parts)
            or "tests" in path.parts
            or path.suffix.lower() in ignored_suffixes
        ):
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
    lease = CapabilityLease("test", Plane.COMMUNICATION, 1)
    request = PlaneRequest(Plane.COMMUNICATION, "test", "room", 1)
    assert brain.authorize(request, lease)


def room_lock_round_trip() -> None:
    lock = RoomLock("room-a", "key-a")
    assert authorize_room(lock, "key-a")
    assert not authorize_room(lock, "wrong-key")


def corridor_sensor_round_trip() -> None:
    assert sense_corridor_presence("corridor-a", expected="corridor-a").authorized
    assert not sense_corridor_presence("corridor-a", expected="corridor-b").authorized


def inner_latch_round_trip() -> None:
    policy = InnerLatchPolicy("room-owner")
    latch = InnerLatch(policy)
    assert latch.state == InnerLatchState.LATCHED
    assert not latch.open("room-owner")
    assert latch.ring_and_release("room-owner")
    assert latch.open("room-owner")


def unified_security_chain_round_trip() -> None:
    assert evaluate_entry_request(corridor_key="c", room_key="r", inner_release=True, requested_room="r").allowed


def run_tests() -> None:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise AssertionError("foundation unit tests failed")


def main() -> int:
    tracemalloc.start()
    started = time.monotonic()
    try:
        source_scan(); adapter_import_scan(); durable_round_trip(); brain_governance_round_trip(); room_lock_round_trip(); corridor_sensor_round_trip(); inner_latch_round_trip(); unified_security_chain_round_trip(); run_tests()
    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    print({"status": "PASS", "elapsed_seconds": round(time.monotonic() - started, 4), "tracemalloc_peak_bytes": peak, "memory_guard_bytes": 335544320})
    return 0


if __name__ == "__main__":
    sys.exit(main())
