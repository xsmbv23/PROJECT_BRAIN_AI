# BRAIN-N105 — Forensic Gate Independence Doctrine

## Trigger

A critical architectural clarification was identified and must survive every successor Bot:
there is **one Forensic FSM**, but it contains multiple admission chains. These chains are not separate Forensic systems and their PASS states are not globally interchangeable.

## Canonical rule

```text
PASS IS LOCAL TO THE GATE.
PASS IS A PREREQUISITE, NOT GLOBAL AUTHORIZATION.
NO PASS INHERITANCE.
NO CROSS-DOMAIN PASS INHERITANCE.
UNKNOWN IS NOT PASS.
DEFAULT DENY.
```

## Database chain

```text
DB_EXISTENCE
  -> DB_BINDING
  -> DB_TLS_ADMISSION
  -> DB_ROUND_TRIP
  -> PROMOTION
```

A database being present does not mean the service has a key.
A valid binding does not prove TLS admission.
TLS admission does not prove a real durable round trip.
Only independent evidence for every DB gate can satisfy promotion.

## Source chain

```text
SOURCE_INDEPENDENCE
  -> NETWORK_ORIGIN_PROOF
  -> EXCEL_VS_WEB_MATCH
  -> CANONICAL_QUORUM
  -> TRUTH_ADMISSION
```

A network-origin proof is source-domain evidence only.
Excel/web reconciliation is a local content gate only.
A local source PASS never becomes canonical truth by inheritance.

## Domain separation

```text
DATABASE PASS  -X-> SOURCE PASS
SOURCE PASS    -X-> DATABASE PASS
```

The same Forensic FSM enforces both domains, but each proposition requires its own evidence receipt.

## Security analogy

```text
CORRIDOR_KEY -> ROOM_KEY -> INNER_RELEASE_WHEN_PROTECTED
```

Correct corridor access does not grant room access.
Correct room key does not bypass an inner latch.
This is the same rule as gate-local evidence.

## Code changes

Added:

- `docs/architecture/FORENSIC_GATE_INDEPENDENCE_DOCTRINE_V1.md`
- `tests/test_forensic_gate_independence.py`

Updated:

- `state/current_state.json` — doctrine and regression test references persisted.
- `state/next_action.json` — N104A now requires reading the doctrine and running the regression suite before promotion.

## Current state

```text
FOUNDATION      = PROMOTED_TO_DATA_ADMISSION
ROOM_01         = ACTIVE / ADMISSION ONLY
CANONICAL       = DENY_INDEPENDENCE
LAYER_1         = LOCKED
STAIRCASE       = LOCKED
```

The next action remains `BRAIN-N104A_SOURCE_EVIDENCE_ADAPTER`.

## Non-goals

This action does not open canonical quorum.
It does not grant DB promotion.
It does not collect source data.
It does not modify source truth.

It only makes the Forensic invariant explicit, executable, and inheritable.
