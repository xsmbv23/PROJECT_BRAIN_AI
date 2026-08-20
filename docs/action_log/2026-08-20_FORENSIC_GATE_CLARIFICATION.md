# Forensic Gate Clarification — Successor Contract

## Permanent rule

There is **ONE Forensic FSM**.

Statements such as `DB_EXISTS=PASS` and `DB_BINDING=PASS` are not two separate Forensic states/universes. They are local states of two sequential gates inside the same admission chain.

The canonical database chain is:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> SECRET_RESOLUTION
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

## Interaction semantics

A PASS at gate N has exactly one meaning:

> Gate N has satisfied its own evidence predicate.

It has three effects only:

1. it records an immutable local evidence result;
2. it may permit evaluation of gate N+1;
3. it may never manufacture, inherit, or imply PASS at gate N+1.

Therefore:

```text
DB_EXISTS=PASS
    != DB_ACCESS=PASS
    != DB_TLS=PASS
    != DB_ROUND_TRIP=PASS
    != PROMOTION=PASS
```

Likewise, `BOUND_TLS` is not durable-evidence admission. A real compact write/read/hash-match receipt is still required.

## Security model

Use the building metaphor literally:

```text
corridor key
    +
room key
    +
room-specific admission condition
    +
inner latch for protected rooms
    =
actual admission
```

Knowing that a room exists does not provide its key.

Possessing a key does not prove the lock was opened.

Opening the lock does not prove the protected room released its inner latch.

Entering the room does not prove the requested forensic operation succeeded.

Only the evidence owned by the final gate can promote the operation.

## Immutable successor rule

Future Bots MUST NOT collapse these gates into one boolean such as `DATABASE_PASS`.

Future Bots MUST NOT infer a later PASS from an earlier PASS.

Future Bots MUST read:

- `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`
- `state/current_state.json`
- `state/next_action.json`

before taking action.

The current runtime/action track remains authoritative; this document is a clarification artifact only and does not unlock any room, staircase, promotion gate, or action space.

## Current N116 boundary

At the time this clarification was recorded, the canonical state remained:

```text
DB_BINDING      = BOUND_TLS
DB_TLS          = PASS
NETWORK_ORIGIN  = PASS
DB_ROUND_TRIP   = PASS
PROMOTION       = DENY
ACTION_RECEIPT  = NOT_YET_PROVEN_CURRENT
ACTION_SPACE    = 0
MANDATORY_NO_OP = TRUE
```

This clarification does **not** alter those states. It only makes their semantics explicit for successor Bots.
