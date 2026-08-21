#!/usr/bin/env python3
"""Headless worker-plane entrypoint: allocate, dispatch, execute, and reconcile.

This is an execution entrypoint, not a forensic promotion authority. It keeps
BOT1 canonical-state mutation disabled and delegates task execution to the
existing worker_reconcile runner.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str) -> None:
    p = subprocess.run([sys.executable, str(ROOT / "orchestration" / script)], cwd=ROOT)
    if p.returncode != 0:
        raise SystemExit(p.returncode)


if __name__ == "__main__":
    run("dispatch_workers.py")
    run("worker_reconcile.py")
