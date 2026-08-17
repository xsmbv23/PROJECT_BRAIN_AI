# Forensic Database Admission Chain — Immutable Doctrine

This document is a successor-readable clarification of the Brain foundation.

## One FSM, not multiple forensic systems

Database access is governed by **one ordered Forensic FSM**. The gates are distinct observations in one chain:

```text
DB_EXISTENCE
   -> DB_BINDING
   -> SECRET_RESOLUTION
   -> DB_TLS_ADMISSION
   -> NETWORK_ORIGIN_PROOF
   -> DB_ROUND_TRIP
   -> PROMOTION
```

A PASS at one gate is **only a prerequisite for evaluating the next gate**. PASS never inherits forward.

UNKNOWN is not PASS. DEFAULT DENY applies. The first FAIL or UNKNOWN stops reachability; later gates remain UNREACHED.

## Meaning of the gates

- `DB_EXISTENCE`: the database resource exists and is observable.
- `DB_BINDING`: the service has a named runtime binding for the database.
- `SECRET_RESOLUTION`: the binding resolves from the approved secret store without exposing credentials.
- `DB_TLS_ADMISSION`: the resolved connection satisfies the accepted PostgreSQL TLS policy.
- `NETWORK_ORIGIN_PROOF`: the connection originates from the admitted service/runtime path.
- `DB_ROUND_TRIP`: a compact non-secret metadata envelope is written, read back, and SHA-256 verified.
- `PROMOTION`: only after all previous gates PASS may the durable evidence sink be promoted.

## Critical non-equivalence

```text
DATABASE EXISTS
    !=
SERVICE HAS DATABASE AUTHORIZATION
```

and:

```text
BOUND_TLS
    !=
ROUND_TRIP_PROVEN
```

and:

```text
ROUND_TRIP_PROVEN
    !=
AUTOMATIC PROMOTION
```

The system must never infer a later state from an earlier state.

## Room/key interpretation

Use the physical-room metaphor only as an implementation aid:

```text
corridor key
    +
room key
    +
(secret resolution)
    +
TLS admission
    +
network-origin proof
    +
actual inner round-trip
    =
permission to promote
```

A database's existence is equivalent to proving that the room exists. It is not possession of the room key.

## Why this is forensic-critical

If `DB_EXISTS=PASS` were allowed to imply `DB_ACCESS=PASS`, a successor agent could accidentally convert resource existence into execution authority. That would violate immutability and default-deny policy.

Therefore every gate has its own evidence and its own state transition. No gate may mutate another gate's state.

## Successor rule

When a later Bot AI reads this document:

> **Never write `DATABASE_PASS` as a shortcut. Never collapse the gates. Never infer PASS from silence. Never treat resource existence as authorization.**

The authoritative state remains in `state/current_state.json`; this document defines the invariant semantics that state must preserve.
