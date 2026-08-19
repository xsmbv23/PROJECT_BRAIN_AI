"""Fail-closed reconciliation of Brain authority against runtime evidence.

Deployment IDs are operational evidence and may change without a code/state
change. The immutable runtime identity used for reconciliation is the deployed
commit SHA. This verifier never mutates logical state.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "current_state.json"
CONTRACT_PATH = ROOT / "contracts" / "state_authority_chain_v1.json"


def _read_wrapped(path: Path) -> dict:
    outer = json.loads(path.read_text(encoding="utf-8"))
    content = outer.get("content")
    if isinstance(content, str):
        return json.loads(content)
    return outer


def reconcile(runtime_commit: str | None = None, deployment_id: str | None = None) -> dict:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    state_outer = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state = _read_wrapped(STATE_PATH)

    authority_ok = (
        contract["authority"]["repository"] == "xsmbv23/Project_Brain_AI"
        and contract["authority"]["path"] == "state/current_state.json"
        and contract["authority"]["role"] == "SINGLE_SOURCE_OF_LOGICAL_STATE_TRUTH"
    )

    expected_runtime = state.get("last_verified_runtime_commit") or state.get("promotion_runtime_commit")
    observed_runtime = runtime_commit or os.environ.get("RENDER_GIT_COMMIT", "")
    runtime_known = bool(observed_runtime and observed_runtime != "UNKNOWN")
    runtime_match = bool(expected_runtime and runtime_known and observed_runtime == expected_runtime)

    # Deployment IDs are not immutable identity: a redeploy can legitimately
    # create a new ID while running the same commit. Keep them as evidence only.
    observed_deploy = deployment_id or os.environ.get("RENDER_DEPLOY_ID", "")
    expected_deploy = state.get("last_verified_deploy") or state.get("promotion_runtime_deploy")
    deploy_evidence = {
        "known": bool(observed_deploy),
        "expected": expected_deploy or "UNKNOWN",
        "observed": observed_deploy or "UNKNOWN",
        "identity_rule": "DEPLOYMENT_ID_IS_EVIDENCE_ONLY",
    }

    state_mode = state.get("state_mode") or state.get("state")
    promotion = state.get("promotion")

    consistent = authority_ok and runtime_match
    status = "VERIFIED" if consistent else "HARD_DENY"

    return {
        "state_consistency": status,
        "authority": "BRAIN_CURRENT_STATE_ONLY" if authority_ok else "DENY",
        "state_mode": state_mode,
        "promotion": promotion,
        "runtime_commit_known": runtime_known,
        "runtime_commit_match": runtime_match,
        "deployment_evidence": deploy_evidence,
        "runtime_is_authority": False,
        "downstream_override_allowed": False,
        "unknown_is_not_pass": True,
        "default_deny": True,
        "brain_state_blob_sha": state_outer.get("sha", "UNKNOWN"),
    }


if __name__ == "__main__":
    result = reconcile()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["state_consistency"] == "VERIFIED" else 1)
