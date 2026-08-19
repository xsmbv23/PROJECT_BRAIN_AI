# BRAIN-N104 — State Artifact Transport-Envelope Drift Repair

## Incident

Render built commit `5840204b4d601c22ca682d90274cc8a71c79a3b8` successfully, but the exact-current runtime failed at `FOUNDATION_BOOT_GATE_DENY` during `state_consistency`.

Runtime evidence reported missing state keys and invalid `ci_status` even though the GitHub-visible state files appeared to contain those values.

## Root cause

`state/current_state.json` and `state/next_action.json` were stored as connector transport envelopes containing:

- `content`
- `encoding`
- `sha`
- display metadata

The boot verifier intentionally rejects transport envelopes and requires direct JSON state artifacts.

This was a genuine **state artifact representation drift**, not a Render build failure.

## Why this matters

The system must distinguish:

```text
CONNECTOR TRANSPORT REPRESENTATION
        !=
FORENSIC STATE ARTIFACT
```

A transport wrapper may be useful to the connector, but it is not allowed to become the persisted FSM artifact consumed by the runtime.

## Repair

Both state artifacts were rewritten as direct JSON objects.

`check_state_consistency.py` remains fail-closed and continues to reject transport envelopes.

No FSM rule was weakened.

No PASS was inferred.

No credential was touched.

## Exact evidence

Before repair:

```text
FOUNDATION_BOOT_GATE_DENY
failed = state_consistency
```

After repair, the expected exact-current boot gate is:

```text
state artifact = direct JSON
state_consistency = PASS
```

The new GitHub commits are:

```text
70cabd39f16f858b0d55065d7c78156a802a6759  current_state.json repair
dc638ef4ed284dde009bf69085a0bd1ed025d30c  next_action.json repair
```

## Forensic rule promoted to permanent doctrine

```text
STATE_ARTIFACT = DIRECT_JSON_ONLY
TRANSPORT_ENVELOPE = NOT_STATE
UNKNOWN = NOT_PASS
BUILD_SUCCESS != RUNTIME_SUCCESS
RUNTIME_SUCCESS != STATE_CONSISTENCY_SUCCESS
```

## Domain rule retained

Database and source admission remain parallel chains:

```text
DB_EXISTENCE -> DB_BINDING -> DB_TLS_ADMISSION -> DB_ROUND_TRIP -> PROMOTION

SOURCE_INDEPENDENCE -> NETWORK_ORIGIN_PROOF -> EXCEL_VS_WEB_MATCH -> CANONICAL_QUORUM -> TRUTH_ADMISSION
```

PASS is local to each gate and never crosses domains.

## Next action

Wait for Render auto-deploy of the repaired direct-JSON state. Do not trigger a manual deploy. Exact-current runtime boot must prove `state_consistency = PASS` before executing `BRAIN-N104A_SOURCE_EVIDENCE_ADAPTER`.
