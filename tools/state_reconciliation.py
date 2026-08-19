"""Fail-closed reconciliation of Brain authority against runtime evidence.

A gate PASS is local evidence only. It is never inherited by the next gate.
Logical state is authoritative in state/current_state.json; runtime commit and
deployment identifiers are evidence, never logical-state authorities.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "current_state.json"
CONTRACT_PATH = ROOT / "contracts" / "state_authority_chain_v1.json"
SUPPORTED_PROTOCOL = "1.0"
SUPPORTED_STATE_MODES = {"FOUNDATION_LOCKED", "DATA_ADMISSION"}


def _read_wrapped(path: Path) -> dict:
    outer = json.loads(path.read_text(encoding="utf-8"))
    content = outer.get("content")
    if isinstance(content, str):
        return json.loads(content)
    return outer


def _semantic_errors(state: dict) -> list[str]:
    errors: list[str] = []
    mode = state.get("state_mode")
    if mode not in SUPPORTED_STATE_MODES:
        errors.append(f"unknown state_mode: {mode}")
        return errors
    if state.get("pass_inheritance") is not False:
        errors.append("pass_inheritance must be false")
    if state.get("unknown_is_not_pass") is not True:
        errors.append("unknown_is_not_pass must be true")
    if state.get("default_deny") is not True:
        errors.append("default_deny must be true")
    if state.get("database_admission_chain") != "ONE_FORENSIC_FSM":
        errors.append("database admission chain must be ONE_FORENSIC_FSM")
    if state.get("database_gate_noninheritance") is not True:
        errors.append("database gate noninheritance must be true")
    if state.get("database_promotion_requires_fresh_evidence") is not True:
        errors.append("database promotion must require fresh evidence")
    if mode == "DATA_ADMISSION":
        if state.get("action_space") != 1:
            errors.append("DATA_ADMISSION requires action_space=1")
        if state.get("action") != "RUNTIME_PROVENANCE_EXECUTION":
            errors.append("DATA_ADMISSION requires runtime provenance action")
        if state.get("layer_1") != "ROOM_01_DATA_ADMISSION":
            errors.append("DATA_ADMISSION requires Room 01 only")
        if state.get("staircase") != "LOCKED":
            errors.append("DATA_ADMISSION requires staircase LOCKED")
        if state.get("promotion") != "PASS_TO_ROOM_01_ONLY;CANONICAL_QUORUM_DENY":
            errors.append("DATA_ADMISSION promotion scope is invalid")
    return errors


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
    semantic_errors = _semantic_errors(state)

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

    schema_version = state.get("state_schema_version", "UNDECLARED")
    schema_known = schema_version != "UNDECLARED"
    status = "VERIFIED" if (authority_ok and protocol_compatible and not semantic_errors) else "HARD_DENY"
    if status == "VERIFIED" and runtime_known and expected_runtime and not runtime_is_same_as_last_verified:
        status = "RECONCILE_REQUIRED"

    return {
        "state_consistency": status,
        "authority": "BRAIN_CURRENT_STATE_ONLY" if authority_ok else "DENY",
        "authority_protocol_version": protocol,
        "protocol_compatible": protocol_compatible,
        "state_schema_version": schema_version,
        "state_schema_known": schema_known,
        "state_mode": state.get("state_mode"),
        "state": state.get("state"),
        "promotion": state.get("promotion"),
        "action_space": state.get("action_space"),
        "action": state.get("action"),
        "semantic_errors": semantic_errors,
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
