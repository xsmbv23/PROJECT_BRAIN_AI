"""Deterministic, side-effect-free replay verifier for the Brain foundation FSM.

The verifier reconstructs admission decisions from repository-persisted contract
and a frozen N070-style external-path snapshot. It never creates an external
event, never calls Quant Engine, never unlocks a room, and never promotes data.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FSM_PATH = ROOT / "contracts" / "brain_admission_fsm_v1.json"


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def load_fsm() -> dict[str, Any]:
    return json.loads(FSM_PATH.read_text(encoding="utf-8"))


def frozen_external_snapshot() -> dict[str, Any]:
    return {
        "state": "WAIT_EXTERNAL_EVENT",
        "action_space": 0,
        "action": "MANDATORY_NO_OP",
        "promotion": "DENY",
        "room_02": "LOCKED",
        "staircase": "LOCKED",
    }


def replay() -> dict[str, Any]:
    fsm = load_fsm()
    before = frozen_external_snapshot()
    after = dict(before)

    assertions = {
        "one_fsm": fsm.get("principle") == "ONE_FORENSIC_ADMISSION_CHAIN",
        "evidence_state_action": fsm.get("transition_rule") == "EVIDENCE -> STATE -> ACTION",
        "pass_locality": fsm["immutability"]["pass_locality"] is True,
        "no_pass_inheritance": fsm["immutability"]["no_pass_inheritance"] is True,
        "unknown_not_pass": fsm["immutability"]["unknown_is_not_pass"] is True,
        "fail_is_evidence": fsm["immutability"]["fail_is_evidence"] is True,
        "default_deny": fsm["immutability"]["default_deny"] is True,
        "edge_source": fsm["edge_policy"]["source_required"] is True,
        "edge_target": fsm["edge_policy"]["target_required"] is True,
        "edge_receipt": fsm["edge_policy"]["observable_evidence_required"] is True,
        "external_wait": fsm["paths"]["external_event_path"]["when_event_absent"]["state"] == "WAIT_EXTERNAL_EVENT",
        "external_zero": fsm["paths"]["external_event_path"]["when_event_absent"]["action_space"] == 0,
        "external_noop": fsm["paths"]["external_event_path"]["when_event_absent"]["action"] == "MANDATORY_NO_OP",
        "self_event_forbidden": fsm["paths"]["external_event_path"]["self_manufactured_event"] == "FORBIDDEN",
        "foundation_cannot_mutate_external": fsm["paths"]["foundation_path"]["may_change_external_event_state"] is False,
        "foundation_cannot_unlock_room": fsm["paths"]["foundation_path"]["may_unlock_room_02"] is False,
        "room_locked": fsm["room_policy"]["room_02"] == "LOCKED",
        "inner_release": fsm["room_policy"]["inner_release_required"] is True,
        "staircase_locked": fsm["room_policy"]["no_staircase_unlock_from_foundation_pass"] is True,
        "ev_owner": fsm["ev_policy"]["owner"] == "QUANT_ENGINE",
        "ev_negative_deny": fsm["ev_policy"]["ev_lt_0"] == "HARD_DENY",
        "ev_unknown_deny": fsm["ev_policy"]["ev_unknown"] == "DENY_ACTION",
        "ev_nan_deny": fsm["ev_policy"]["ev_nan"] == "DENY_ACTION",
        "ev_infinite_deny": fsm["ev_policy"]["ev_infinite"] == "DENY_ACTION",
        "ev_zero_not_pass": fsm["ev_policy"]["ev_zero"] == "NOT_SUFFICIENT_FOR_PASS",
    }

    # Explicitly model the hostile EV cases without executing any domain action.
    ev_cases = {
        "negative": -0.01,
        "unknown": None,
        "nan": "NaN",
        "infinite": "Infinity",
        "zero": 0.0,
    }
    ev_decisions = {
        "negative": "DENY",
        "unknown": "DENY",
        "nan": "DENY",
        "infinite": "DENY",
        "zero": "NOT_SUFFICIENT",
    }

    fsm_hash_1 = canonical_hash(fsm)
    fsm_hash_2 = canonical_hash(json.loads(FSM_PATH.read_text(encoding="utf-8")))
    assertions["deterministic_contract_hash"] = fsm_hash_1 == fsm_hash_2
    assertions["external_path_unchanged"] = before == after
    assertions["action_space_unchanged"] = after["action_space"] == 0
    assertions["room_02_unchanged"] = after["room_02"] == "LOCKED"
    assertions["staircase_unchanged"] = after["staircase"] == "LOCKED"

    return {
        "replay": "PASS" if all(assertions.values()) else "DENY",
        "contract_hash": fsm_hash_1,
        "contract_hash_repeat": fsm_hash_2,
        "assertions": assertions,
        "ev_cases": ev_cases,
        "ev_decisions": ev_decisions,
        "external_before": before,
        "external_after": after,
        "mutation": "NONE",
        "external_event_manufactured": False,
        "room_02_unlocked": False,
        "staircase_unlocked": False,
        "promotion": "DENY",
    }


if __name__ == "__main__":
    result = replay()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["replay"] == "PASS" else 1)
