import json
from pathlib import Path


SCHEMA_PATH = Path(__file__).parents[1] / "contracts" / "multi_bot_deliberation.schema.json"


def test_deliberation_v2_separates_outcomes_and_preserves_dissent():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    decision = schema["$defs"]["decision"]["properties"]
    assert decision["scope"]["const"] == "DELIBERATION_ONLY"
    assert decision["outcome"]["enum"] == ["ACCEPTED", "REJECTED", "HOLD", "ESCALATE", "UNRESOLVED"]
    assert decision["gate_outcome"]["const"] == "UNCHANGED"
    assert decision["quant_outcome"]["const"] == "UNCHANGED"
    assert decision["execution_outcome"]["const"] == "UNCHANGED"

    dissent = schema["$defs"]["dissent"]["required"]
    assert dissent == ["bot", "claim", "reason", "evidence_refs", "resolved"]


def test_deliberation_v2_requires_lifecycle_and_immutable_rounds():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    rounds = schema["properties"]["rounds"]
    assert rounds["minItems"] == 4
    assert schema["protocol"]["minimum_lifecycle"] == [
        "PROPOSAL", "CHALLENGE", "REBUTTAL", "ARBITRATION"
    ]
    assert schema["protocol"]["arbitration_requires_prior_challenge"] is True
    assert schema["protocol"]["rounds_are_append_only"] is True
    assert schema["protocol"]["revision_requires_new_record"] is True


def test_deliberation_v2_evidence_refs_are_structured():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    ref = schema["$defs"]["evidenceRef"]["required"]
    assert ref == [
        "evidence_id", "record_ref", "record_sha256", "gate_owner", "execution_id", "status"
    ]
    assert schema["protocol"]["evidence_refs_must_resolve_to_persistent_records"] is True


def test_deliberation_v2_forbids_pass_like_decision_outcomes():
    forbidden = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["forbidden_patterns"]
    assert "decision.outcome = PASS" in forbidden
    assert "decision.outcome = DENY" in forbidden
    assert "consensus_inherits_gate_status" in forbidden
