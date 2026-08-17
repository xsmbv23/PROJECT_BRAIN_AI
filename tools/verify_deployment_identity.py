"""Credential-free deployment identity admission gate.

The gate is intentionally control-plane code: it compares two independently
observed commit identities and never attempts to contact GitHub with a runtime
secret. A stale Render deployment is DENY even when its functional tests pass.
"""
from __future__ import annotations

import argparse
import os


def verify(canonical_commit: str, runtime_commit: str | None = None) -> dict[str, object]:
    runtime = runtime_commit or os.environ.get("RENDER_GIT_COMMIT", "")
    canonical = canonical_commit.strip()
    observed = runtime.strip()
    if not canonical or not observed:
        return {"status": "DENY", "reason": "IDENTITY_MISSING"}
    if canonical != observed:
        return {
            "status": "DENY",
            "reason": "DEPLOYMENT_DRIFT",
            "canonical_commit": canonical,
            "runtime_commit": observed,
        }
    return {
        "status": "PASS",
        "reason": "EXACT_CURRENT_COMMIT",
        "canonical_commit": canonical,
        "runtime_commit": observed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--runtime", default=None)
    args = parser.parse_args()
    result = verify(args.canonical, args.runtime)
    print(result, flush=True)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
