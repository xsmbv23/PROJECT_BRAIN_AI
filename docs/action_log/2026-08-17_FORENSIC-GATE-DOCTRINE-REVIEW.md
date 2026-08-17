# Forensic Gate Doctrine Review — 2026-08-17

## Decision

The proposed interpretation was reviewed and normalized into the existing frozen Forensic Gate Semantics document.

The architecture has **ONE_FORENSIC_FSM**, not multiple independent Forensic systems.

The database admission chain is:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Each gate has local truth only.

```text
PASS(G1) != PASS(G2)
PASS(G1) is only a prerequisite for evaluating G2
```

## Important distinction

The following are different evidence classes inside the same FSM:

- existence evidence: resource exists;
- binding evidence: service has an explicit runtime binding;
- TLS admission evidence: binding satisfies security contract;
- round-trip evidence: actual compact write/read/hash-match occurred;
- promotion evidence: the resulting evidence is authorized for the next architectural state.

None may silently inherit PASS from another.

## Immutability

A later observation never rewrites an earlier observation. A later `BOUND_TLS` observation is a new event, not an edit of an earlier `NOT_BOUND` event.

## Seal decision

A proposal to immediately declare `FOUNDATION SEALED — STAIRCASE OPENED` was **REJECTED as premature** for the current state.

Reason: the repository's current next action is `REALITY-N011-STABILITY-QUORUM`. The system still requires an independent GitHub Actions transport receipt before the stability/source-quorum gate can be evaluated. Opening the staircase now would violate the current Forensic progression.

The correct state remains:

```text
ONE_FORENSIC_FSM       = FROZEN
GATE_SEMANTICS         = FROZEN
NO_PASS_INHERITANCE    = ENFORCED
DB_ROUND_TRIP          = NOT_PROVEN
N011_EXECUTION         = WAITING
PROMOTION              = DENY
LAYER_1                = LOCKED
STAIRCASE              = LOCKED
```

## Successor instruction

Read `docs/architecture/FORENSIC_GATE_SEMANTICS.md` before modifying any admission state. Do not collapse the chain into `DATABASE_PASS`. Do not open Layer 1 or the staircase until the current successor gate says it is eligible.
