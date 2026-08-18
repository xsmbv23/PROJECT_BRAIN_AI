"""Verify the machine-readable Forensic admission FSM.

This verifier is deliberately independent from the External Event Path. It
checks contract integrity only; it cannot manufacture an external receipt and
cannot unlock Room 02.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "brain_admission_fsm_v1.json"
REQUIRED_STATES = {
    "STATE_DISPATCH_EXECUTION",
    "STATE_FRESH_ARTIFACT_VERIFY",
    "STATE_CANONICAL_INPUT_ADMISSION",
    "STATE_QUANT_EXECUTION_ADMISSION",
    "STATE_PROMOTION",
}


def verify() -> dict[str, object]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    imm = data["immutability"]
    assert imm["pass_locality"] is True
    assert imm["pass_is_prerequisite_only"] is True
    assert imm["no_pass_inheritance"] is True
    assert imm["unknown_is_not_pass"] is True
    assert imm["fail_is_evidence"] is True
    assert imm["default_deny"] is True

    edge = data["edge_policy"]
    assert edge["source_required"] is True
    assert edge["target_required"] is True
    assert edge["observable_evidence_required"] is True
    assert edge["unknown_edge"] == "DENY"
    assert edge["broken_edge"] == "DENY"
    assert edge["cross_layer_edge_without_contract"] == "DENY"

    states = {state["state_id"]: state for state in data["states"]}
    assert REQUIRED_STATES == set(states)
    assert states["STATE_DISPATCH_EXECUTION"]["external_dependency"] == "REAL_GITHUB_WORKFLOW_DISPATCH"
    assert states["STATE_DISPATCH_EXECUTION"]["default_action"] == "NO_OP"
    assert "STATE_PROMOTION" in states["STATE_DISPATCH_EXECUTION"]["forbidden_transitions"]
    assert "STATE_QUANT_EXECUTION" in states["STATE_DISPATCH_EXECUTION"]["forbidden_transitions"]

    external = data["paths"]["external_event_path"]
    assert external["authority"] == "REAL_EXTERNAL_EVENT_ONLY"
    assert external["when_event_absent"]["action_space"] == 0
    assert external["when_event_absent"]["action"] == "MANDATORY_NO_OP"
    assert external["self_manufactured_event"] == "FORBIDDEN"
    assert external["alternate_path"] == "FORBIDDEN"

    foundation = data["paths"]["foundation_path"]
    assert foundation["may_advance_without_external_event"] is True
    assert foundation["may_change_external_event_state"] is False
    assert foundation["may_unlock_room_02"] is False

    ev = data["ev_policy"]
    assert ev["owner"] == "QUANT_ENGINE"
    assert ev["brain_role"] == "ADMIT_OR_DENY"
    assert ev["ev_lt_0"] == "HARD_DENY"
    assert ev["ev_unknown"] == "DENY_ACTION"
    assert ev["ev_nan"] == "DENY_ACTION"
    assert ev["ev_infinite"] == "DENY_ACTION"
    assert ev["ev_zero"] == "NOT_SUFFICIENT_FOR_PASS"

    assert data["lineage"] == ["RAW_SOURCE", "ARTIFACT_HASH", "EVIDENCE", "ADMISSION", "ACTION"]
    assert data["room_policy"]["room_02"] == "LOCKED"
    assert data["room_policy"]["inner_release_required"] is True
    assert data["room_policy"]["no_staircase_unlock_from_foundation_pass"] is True

    return {
        "verifier": "verify_admission_fsm",
        "status": "PASS",
        "states": len(states),
        "external_event_path": "ISOLATED",
        "foundation_path": "ADVANCE_ALLOWED_EXTERNAL_STATE_UNCHANGED",
        "room_02": "LOCKED",
        "promotion": "DENY_UNTIL_FRESH_EVIDENCE",
    }


if __name__ == "__main__":
    print(verify())
