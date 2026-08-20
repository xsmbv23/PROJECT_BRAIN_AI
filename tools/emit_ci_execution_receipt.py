"""Emit an explicit repository-execution receipt for GitHub Actions.

This receipt proves only that the repository workflow reached this step.
It never asserts external runtime truth, independent observation, admission,
or promotion.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def build_receipt(env: dict[str, str]) -> dict[str, object]:
    return {
        "evidence_kind": "REPOSITORY_WORKFLOW_EXECUTION",
        "repository_execution": "PROVEN_AT_THIS_STEP",
        "external_runtime_truth": "NOT_PROVEN",
        "independent_external_observation": False,
        "commit_sha": env.get("GITHUB_SHA", ""),
        "workflow_run_id": env.get("GITHUB_RUN_ID", ""),
        "workflow_run_attempt": env.get("GITHUB_RUN_ATTEMPT", ""),
        "workflow_started_at": env.get("GITHUB_RUN_STARTED_AT", ""),
        "receipt_generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "ci_execution_receipt.json")
    receipt = build_receipt(dict(os.environ))
    if not receipt["commit_sha"] or not receipt["workflow_run_id"]:
        raise SystemExit("required GitHub execution identity is missing")
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
