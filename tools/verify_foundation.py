"""Deterministic stdlib-only foundation verification runner."""
from __future__ import annotations

import pathlib
import re
import sys
import time
import tracemalloc
import unittest

from core.corridor_lock import RoomLock, authorize_room
from core.corridor_sensor import sense_corridor_presence
from core.durable_audit import seal_head
from core.durable_state import persist_audit_head, restore_audit_head
from core.foundation_gate import run_foundation_gate
from core.foundation_hardening import AuditChain, GovernanceDeny

ROOT = pathlib.Path(__file__).resolve().parents[1]


def source_scan() -> None:
    banned = re.compile(r"(?i)(postgres(?:ql)?://|redis://|-----BEGIN .*PRIVATE KEY-----)")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix in {".pyc", ".png", ".jpg", ".zip"}:
            continue
        if banned.search(path.read_text(encoding="utf-8", errors="ignore")):
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
    # Sensor output is telemetry only. It has no capability/key and therefore
    # cannot be substituted for authorize_room().


def main() -> int:
    tracemalloc.start(); started = time.monotonic()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    source_scan(); adapter_import_scan(); durable_round_trip(); room_lock_round_trip(); corridor_sensor_round_trip()
    gate = run_foundation_gate()
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    report = {"tests_ok": result.wasSuccessful(), "gate": gate["status"], "source_scan": "PASS", "adapter_import_scan": "PASS", "durable_round_trip": "PASS", "room_lock": "PASS", "corridor_sensor": "PASS", "tracemalloc_peak_bytes": peak, "elapsed_seconds": round(time.monotonic()-started, 4)}
    print(report)
    return 0 if result.wasSuccessful() and gate["status"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
