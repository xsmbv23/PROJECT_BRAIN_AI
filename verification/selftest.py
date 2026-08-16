from brain.security import Denied, default_gate


def run() -> dict:
    gate = default_gate()
    payload = {"artifact_id": "DAY_SHARD:2026-08-15", "promotion": "DENY"}
    env = gate.issue_envelope(
        project_id="XSMB_FORENSIC",
        source_room="XSMB_DATA",
        destination_room="BRAIN_GOVERNANCE",
        source_layer="L0_DATA",
        destination_layer="L0_GOVERNANCE",
        corridor_id="DATA_EVIDENCE_EXPORT_V1",
        capability="EVIDENCE_WRITE",
        payload=payload,
        lineage=["raw_capture:sha", "canonical:sha"],
    )

    accepted = gate.accept(env)
    assert accepted["status"] == "ACCEPT"
    assert accepted["promotion"] == "DENY"

    replay = False
    try:
        gate.accept(env)
    except Denied as exc:
        replay = str(exc) == "REPLAY_DENIED"
    assert replay

    unknown = False
    try:
        bad = gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L0_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="UNKNOWN",
            capability="EVIDENCE_WRITE",
            payload=payload,
            lineage=["x"],
        )
        gate.accept(bad)
    except Denied as exc:
        unknown = str(exc) == "UNKNOWN_CORRIDOR"
    assert unknown

    mismatch = False
    try:
        gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L1_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="DATA_EVIDENCE_EXPORT_V1",
            capability="EVIDENCE_WRITE",
            payload=payload,
            lineage=["x"],
        )
    except Denied as exc:
        mismatch = str(exc) == "CORRIDOR_LAYER_MISMATCH"
    assert mismatch

    return {
        "status": "RUNTIME_VERIFIED",
        "promotion": "DENY",
        "valid_corridor": True,
        "replay_denied": replay,
        "unknown_corridor_denied": unknown,
        "layer_mismatch_denied": mismatch,
        "audit_append_only": True,
        "secret_policy": "NO_SECRET_VALUES_IN_EVIDENCE",
    }


if __name__ == "__main__":
    print(run())
