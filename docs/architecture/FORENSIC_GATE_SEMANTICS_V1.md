# Forensic Gate Semantics V1

## Purpose

This document freezes the database-admission and general Forensic gate semantics for all successor Bots.

The system has **one Forensic state machine**, not multiple independent Forensic systems.

The database admission chain is one ordered chain of independent evidence gates:

```text
DB_EXISTENCE
    -> DB_BINDING
        -> DB_TLS_ADMISSION
            -> DB_ROUND_TRIP
                -> PROMOTION
```

## Core law

> `PASS(N) != PASS(N+1)`

A PASS is local to the gate that produced it. It is only a prerequisite for evaluating the next gate. It never becomes inherited permission.

Therefore:

```text
DB_EXISTS = PASS
```

means only:

> The database resource exists.

It does **not** mean:

```text
SERVICE_AUTHORIZED = PASS
DATABASE_ACCESS = PASS
DB_TLS = PASS
DB_ROUND_TRIP = PASS
PROMOTION = PASS
```

Likewise:

```text
BOUND_TLS = PASS
```

does not imply a durable evidence round-trip.

Only a real compact metadata write -> read -> SHA-256 match can satisfy the round-trip gate.

## Evidence hierarchy

```text
resource existence
      |
      v
service binding
      |
      v
TLS admission
      |
      v
real write/read/hash verification
      |
      v
promotion authority
```

Every transition requires evidence belonging to that transition.

## Hard boundaries

The following equivalences are forbidden:

```text
DB_EXISTENCE          != DB_AUTHORIZATION
DB_AUTHORIZATION      != DB_TLS_ADMISSION
DB_TLS_ADMISSION      != DB_ROUND_TRIP
DB_ROUND_TRIP         != DOMAIN_TRUTH
STRUCTURALLY_VALID    != DOMAIN_TRUE
ROUNDTRIP_VALID       != DOMAIN_UNDERSTANDING
READINESS             != AUTHORITY
LOG                   != EVIDENCE
RULE                   != AUTHORITY
ARTIFACT               != PROGRESS
SIMULATION             != EVIDENCE
```

## External-event law

The system cannot manufacture the event required to advance a waiting state.

```text
NO EXTERNAL EVENT
        |
        v
NO TRANSITION
        |
        v
NO ACTION
```

`NO-OP` is therefore a valid Forensic outcome, not a failure.

## Single-observation law

A single receipt proves only the property represented by that receipt.

```text
ONE_RECEIPT != DOMAIN_UNDERSTANDING
```

Multiple observations from the same URL but different runtime identities remain distinct observations and must not be silently merged.

Runtime source identity is:

```text
SOURCE_IDENTITY = (SOURCE_URL, EXECUTION_RUNTIME)
```

## Failure semantics

Failure is evidence.

A failed retrieval must be frozen as a failure receipt with no fabricated bytes, hashes, parsed fields, or inferred truth.

Retrying is a new event and must never overwrite the historical receipt.

## Successor Bot instruction

Before taking any action, a successor Bot MUST:

1. Read `state/current_state.json`.
2. Read `state/next_action.json`.
3. Treat the current state as authoritative persistent state, not the chat transcript.
4. Determine whether the next action requires an external event.
5. If the event is absent, perform NO-OP.
6. Never infer a later gate from an earlier PASS.
7. Never convert observability/readiness into authority.
8. Never manufacture evidence to advance the FSM.
9. Record every completed action and its evidence before changing `next_action.json`.
10. Keep Layer 1 and the staircase locked until their explicit promotion gates are proven.

## Current frozen position

At the time this contract was written:

```text
FOUNDATION = FROZEN
REALITY_BOUNDARY = FROZEN
DB_PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
NEXT = REALITY-N011-STABILITY-QUORUM
NEXT_STATUS = WAIT_EXTERNAL_EVENT
```
