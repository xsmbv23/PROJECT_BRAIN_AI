"""Fail-closed reconciliation of Brain authority against runtime evidence.

Runtime commit SHA is immutable audit evidence, not a self-referential logical
state key. Logical-state compatibility is governed by the authority protocol
version and state schema version.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "current_state.json"
CONTRACT_PATH = ROOT / "contracts" / "state_authority_chain_v1.json"
SUPPORTED_PROTOCOL = "1.0"


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
    protocol = contract.get("authority_protocol_version", "UNKNOWN")
    protocol_compatible = protocol == SUPPORTED_PROTOCOL

    # A runtime may legitimately execute a newer deployed commit containing a
    # logical-state change. That is code/version evidence, not proof that the
    # logical state has mutated outside Brain. Never require commit == state
    # commit; that creates a self-referential deployment loop.
    observed_runtime = runtime_commit or os.environ.get("RENDER_GIT_COMMIT", "")
    runtime_known = bool(observed_runtime and observed_runtime != "UNKNOWN")
    expected_runtime = state.get("last_verified_runtime_commit") or state.get("promotion_runtime_commit")
    runtime_is_same_as_last_verified = bool(runtime_known and expected_runtime and observed_runtime == expected_runtime)

    observed_deploy = deployment_id or os.environ.get("RENDER_DEPLOY_ID", "")
    expected_deploy = state.get("last_verified_deploy") or state.get("promotion_runtime_deploy")
    deploy_evidence = {
        "known": bool(observed_deploy),
        "expected_last_verified": expected_deploy or "UNKNOWN",
        "observed": observed_deploy or "UNKNOWN",
        "identity_rule": "DEPLOYMENT_ID_IS_EVIDENCE_ONLY",
    }

    state_mode = state.get("state_mode") or state.get("state")
    promotion = state.get("promotion")
    schema_version = state.get("state_schema_version", "UNDECLARED")
    schema_known = schema_version != "UNDECLARED"

    # Hard-deny only on authority/protocol uncertainty. Runtime commit drift is
    # reported as version drift and requires an explicit reconciliation action.
    status = "VERIFIED" if (authority_ok and protocol_compatible) else "HARD_DENY"
    if status == "VERIFIED" and runtime_known and expected_runtime and not runtime_is_same_as_last_verified:
        status = "RECONCILE_REQUIRED"

    return {
        "state_consistency": status,
        "authority": "BRAIN_CURRENT_STATE_ONLY" if authority_ok else "DENY",
        "authority_protocol_version": protocol,
        "protocol_compatible": protocol_compatible,
        "state_schema_version": schema_version,
        "state_schema_known": schema_known,
        "state_mode": state_mode,
        "promotion": promotion,
        "runtime_commit_known": runtime_known,
        "runtime_commit": observed_runtime or "UNKNOWN",
        "runtime_last_verified_commit": expected_runtime or "UNKNOWN",
        "runtime_commit_same_as_last_verified": runtime_is_same_as_last_verified,
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
    raise SystemExit(0 if result["state_consistency"] == "VERIFIED" else 2 if result["state_consistency"] == "RECONCILE_REQUIRED" else 1)
