# Forensic Gate Semantics V1

## Purpose

This document freezes the database-admission and general Forensic gate semantics for all successor Bots.

The system has **one Forensic state machine**, not multiple independent Forensic systems.

The individual PASS / UNKNOWN / FAIL values below are **gate-local evidence states**, not separate Forensic state machines.

## One Forensic FSM

The database admission chain is one ordered chain of independent evidence gates:

```text
DB_EXISTENCE
    -> DB_BINDING
        -> SECRET_RESOLUTION
            -> DB_TLS_ADMISSION
                -> NETWORK_ORIGIN_PROOF
                    -> DB_ROUND_TRIP
                        -> PROMOTION
```

These gates interact directionally. A successful gate makes the next gate reachable; it never passes the next gate automatically.

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

## Gate ownership

Each gate owns exactly one narrow question and its own evidence.

```text
DB_EXISTENCE          = resource existence evidence
DB_BINDING            = service binding evidence
SECRET_RESOLUTION     = authorized secret-boundary evidence
DB_TLS_ADMISSION      = TLS-policy evidence
NETWORK_ORIGIN_PROOF  = authorized-runtime-origin evidence
DB_ROUND_TRIP          = real write/read/hash evidence
PROMOTION              = explicit authority decision
```

A gate may not borrow another gate's evidence merely because the evidence appears related.

## Evidence hierarchy

```text
resource existence
      |
      v
service binding
      |
      v
secret resolution
      |
      v
TLS admission
      |
      v
network origin
      |
      v
real write/read/hash verification
      |
      v
promotion authority
```

Every transition requires fresh evidence belonging to that transition.

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
RULE                  != AUTHORITY
ARTIFACT              != PROGRESS
SIMULATION             != EVIDENCE
```

## Room / door interpretation

The room metaphor maps onto the same FSM:

```text
corridor key
    -> reach the corridor
room key
    -> reach the room door
inner latch / host approval
    -> protected-room admission
own gate evidence
    -> prove what actually happened inside
promotion
    -> authority to use the result downstream
```

`DB_EXISTENCE=PASS` means the room exists. It does not mean the visitor has the corridor key, room key, inner release, or proof of a valid transaction.

## Quant Engine boundary

`xsmbv23/Quant_Engine` is Layer 1 research/execution infrastructure. It may prepare local prerequisites, source adapters, feature calculations, replay contracts, and compact evidence.

It may **not** reopen a Brain gate, reinterpret Brain evidence, promote itself into Brain authority, or convert a candidate edge into trade authorization.

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
5. If the event is absent, perform NO-OP on the blocked gate.
6. Continue only explicitly allowed parallel prerequisite work.
7. Never infer a later gate from an earlier PASS.
8. Never convert observability/readiness into authority.
9. Never manufacture evidence to advance the FSM.
10. Record every completed action and its evidence before changing `next_action.json`.
11. Keep Layer 1 and the staircase locked until their explicit promotion gates are proven.

## Current frozen position

```text
FOUNDATION = FROZEN
REALITY_BOUNDARY = FROZEN
DB_PROMOTION = DENY
LAYER_1 = ROOM_01_DATA_ADMISSION
ROOM_02 = LOCKED_FOR_PROMOTION
STAIRCASE = LOCKED
BRAIN_ACTION_SPACE = 0
PARALLEL_QUANT_WORK = LOCAL_PREREQUISITE_ONLY
```
