from brain.security import Denied, default_gate
from tools.evidence_lineage_validator import validate_evidence


def expect_denied(fn, expected: str) -> bool:
    try:
        fn()
    except Denied as exc:
        return str(exc) == expected
    return False


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
    valid_corridor = accepted.get("status") == "ACCEPT" and accepted.get("promotion") == "DENY"

    replay_denied = expect_denied(lambda: gate.accept(env), "REPLAY_DENIED")

    unknown_corridor_denied = expect_denied(
        lambda: gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L0_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="UNKNOWN",
            capability="EVIDENCE_WRITE",
            payload=payload,
            lineage=["x"],
        ),
        "UNKNOWN_CORRIDOR",
    )

    layer_mismatch_denied = expect_denied(
        lambda: gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L1_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="DATA_EVIDENCE_EXPORT_V1",
            capability="EVIDENCE_WRITE",
            payload=payload,
            lineage=["x"],
        ),
        "CORRIDOR_LAYER_MISMATCH",
    )

    lineage_denied = expect_denied(
        lambda: gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L0_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="DATA_EVIDENCE_EXPORT_V1",
            capability="EVIDENCE_WRITE",
            payload=payload,
            lineage=[],
        ),
        "MISSING_LINEAGE",
    )

    capability_denied = expect_denied(
        lambda: gate.issue_envelope(
            project_id="XSMB_FORENSIC",
            source_room="XSMB_DATA",
            destination_room="BRAIN_GOVERNANCE",
            source_layer="L0_DATA",
            destination_layer="L0_GOVERNANCE",
            corridor_id="DATA_EVIDENCE_EXPORT_V1",
            capability="PROMOTION_WRITE",
            payload=payload,
            lineage=["x"],
        ),
        "CAPABILITY_SCOPE_MISMATCH",
    )

    lineage_source = {
        "source_identity": "ketqua16.net",
        "observation_timestamp": "2026-08-21T00:00:00Z",
        "observation_origin": "external_source",
    }
    lineage_source_pass = validate_evidence(lineage_source)["status"] == "PASS"
    lineage_derived_denied = validate_evidence(lineage_source | {"derived": True})["status"] == "DENY"
    lineage_hashes_distinct = validate_evidence(
        lineage_source | {
            "raw_artifact_sha256": "raw",
            "semantic_fingerprint": "meaning",
            "semantic_quorum": True,
        }
    )["status"] == "PASS"

    result = {
        "status": "RUNTIME_VERIFIED",
        "promotion": "DENY",
        "valid_corridor": valid_corridor,
        "replay_denied": replay_denied,
        "unknown_corridor_denied": unknown_corridor_denied,
        "layer_mismatch_denied": layer_mismatch_denied,
        "missing_lineage_denied": lineage_denied,
        "capability_scope_denied": capability_denied,
        "lineage_source_pass": lineage_source_pass,
        "lineage_derived_denied": lineage_derived_denied,
        "lineage_hashes_distinct": lineage_hashes_distinct,
        "audit_append_only": isinstance(gate.audit, list) and len(gate.audit) >= 2,
        "secret_policy": "NO_SECRET_VALUES_IN_EVIDENCE",
    }

    failures = [key for key, value in result.items() if key not in {"status", "promotion", "secret_policy"} and value is not True]
    if failures:
        raise AssertionError(f"FOUNDATION_SECURITY_SELFTEST_FAILED: {failures}")
    print(result, flush=True)
    return result


if __name__ == "__main__":
    run()
