#!/usr/bin/env python3
"""Regression tests for the BOT2/BOT3/BOT4 quorum degradation contract."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "orchestration" / "worker_reconcile.py"
spec = importlib.util.spec_from_file_location("worker_reconcile", path)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
BASE = lambda wid, status="LLM_COMPLETED": {"worker_id": wid, "status": status, "result": {"status": status}}
def check(results, expected):
    got = mod.reconcile("TEST-QUORUM", results)
    assert got["decision"] == expected, (expected, got)
    assert got["promotion"] == "DENY"
    assert got["canonical_next_action_mutation"] == "FORBIDDEN"
check([BASE("BOT2_QUANT"), BASE("BOT3_REALITY"), BASE("BOT4_EXECUTION")], "REVIEW_REQUIRED")
check([BASE("BOT2_QUANT"), BASE("BOT3_REALITY")], "PROVISIONAL")
check([BASE("BOT2_QUANT")], "INSUFFICIENT_QUORUM")
check([], "INSUFFICIENT_QUORUM")
check([{"status": "STALE_REJECTED", "worker_id": "BOT2_QUANT"}, BASE("BOT3_REALITY"), BASE("BOT4_EXECUTION")], "HOLD")
check([BASE("BOT2_QUANT", "CONFLICT"), BASE("BOT3_REALITY"), BASE("BOT4_EXECUTION")], "HOLD")
check([BASE("BOT2_QUANT", "BLOCKED_PROVIDER_NOT_CONFIGURED"), BASE("BOT3_REALITY"), BASE("BOT4_EXECUTION")], "HOLD")
print("WORKER_QUORUM_CONTRACT_PASS")
