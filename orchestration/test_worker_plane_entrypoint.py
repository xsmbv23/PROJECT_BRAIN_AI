#!/usr/bin/env python3
"""Static contract test for the headless worker-plane entrypoint."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "orchestration" / "run_worker_plane.py").read_text(encoding="utf-8")
assert 'run("dispatch_workers.py")' in text
assert 'run("worker_reconcile.py")' in text
assert 'canonical' in text.lower()
print("WORKER_PLANE_ENTRYPOINT_CONTRACT_PASS")
