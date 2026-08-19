# BRAIN-N098 — Gate Semantics Freeze

## Purpose

Before executing the N098 runtime provenance capture, freeze the semantic rule that prevents downstream escalation from unrelated PASS states.

## Frozen rule

`PASS_IS_LOCAL_TO_GATE`

A PASS proves exactly one gate proposition. It is a prerequisite for evaluating the next gate, not an inherited authorization.

## Current chain

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

## Consequences

```text
DB_EXISTENCE=PASS
  != DB_BINDING=PASS

DB_BINDING=PASS
  != SECRET_RESOLUTION=PASS

DB_TLS_ADMISSION=PASS
  != NETWORK_ORIGIN_PROOF=PASS

NETWORK_ORIGIN_PROOF=PASS
  != DB_ROUND_TRIP=PASS
```

No state field may copy or inherit another gate's PASS.

## Source provenance consequence

For N098:

```text
raw artifact capture
  -> provenance evidence
  -> source identity
  -> anti-ad collision boundary
  -> independence evidence
  -> deterministic FULL27 hash
  -> reconciliation
  -> canonical quorum
```

A successful HTTP request, parser execution, or runtime boot cannot substitute for the specific evidence required by any later gate.

## Current state

The repository's current state is already in `ROOM_01_DATA_ADMISSION`, while canonical quorum remains DENY because source provenance and independence are not proven. This is a coherent state in one FSM, not contradictory Forensic states. fileciteturn757file0L2-L2

## N098 execution rule

N098 must capture at least two registered sources for target date `2026-08-12`, retaining raw artifacts and compact receipts. Hard-deny conditions include missing raw artifact, unknown provenance, identity collision, date mismatch, FULL27 parse failure, synthetic/inferred data, hash missing, independence unproven, ambiguous canonicalization, and ambiguous advertising boundary. fileciteturn758file0L2-L2

If durable evidence cannot be retained safely, successful network observations remain non-canonical and promotion stays DENY.

## Successor instruction

Read:

1. `docs/doctrine/PASS_IS_LOCAL_TO_GATE.md`
2. `docs/doctrine/FORENSIC_GATE_SEMANTICS_V1.md`
3. `state/current_state.json`
4. `state/next_action.json`
5. this action log

Then continue N098 from the exact current gate. Do not restart the FSM, do not reinterpret historical PASS values, and do not unlock Layer 1 or the staircase prematurely.
