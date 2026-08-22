#!/usr/bin/env python3
"""Regression tests for canonical quorum denominator binding."""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))


def run_with_workers(value: str) -> str:
    env = os.environ.copy()
    env["WORKERS"] = value
    code = (
        "import orchestration.worker_reconcile as w; "
        "print(w.WORKERS); "
        "print(w.CANONICAL_WORKERS)"
    )
    return subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, env=env, text=True)


def main() -> int:
    checks = {}
    full = run_with_workers("BOT2_QUANT,BOT3_REALITY,BOT4_EXECUTION")
    degraded = run_with_workers("BOT2_QUANT,BOT4_EXECUTION")
    unknown = run_with_workers("BOT2_QUANT,EVIL_WORKER")
    checks["canonical_set_is_three"] = all(x in full for x in ("BOT2_QUANT", "BOT3_REALITY", "BOT4_EXECUTION"))
    checks["execution_subset_can_be_two"] = all(x in degraded for x in ("BOT2_QUANT", "BOT4_EXECUTION"))
    checks["canonical_denominator_remains_three"] = "('BOT2_QUANT', 'BOT3_REALITY', 'BOT4_EXECUTION')" in degraded
    checks["unknown_worker_excluded"] = "EVIL_WORKER" not in unknown
    result = "PASS" if all(checks.values()) else "FAIL"
    print({"schema": "canonical-quorum-denominator/v1", "checks": checks, "result": result})
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
