# Forensic Database Admission Chain

## Purpose

This document is normative foundation architecture. It prevents a successor Bot AI from confusing resource existence, authorization, TLS admission, runtime secret resolution, network origin, and durable evidence proof.

## Core rule

**A PASS at one gate is only a prerequisite for the next gate. It is never permission to infer PASS at a deeper gate.**

There is one Forensic system and one database-admission chain / one FSM. The gates below are sequential and local, not independent Forensic systems.

## Canonical chain

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

## Gates

1. `DB_EXISTENCE`
   - Evidence: the configured Render PostgreSQL resource exists and is available.
   - Meaning: the room exists.
   - Does NOT grant access.

2. `DB_BINDING`
   - Evidence: the running service has the explicitly required `DATABASE_URL` binding.
   - Credential source must be Render Secret Environment only.
   - Meaning: the service has a candidate key to the room.
   - Does NOT prove secret resolution, TLS, network origin, or usable database access.

3. `SECRET_RESOLUTION`
   - Evidence: the exact runtime has a non-empty `DATABASE_URL` sourced from the approved Render Secret Environment boundary, is not a known placeholder, and is not overridden by an unapproved source.
   - Only non-secret classification may be emitted.
   - The raw secret must never be logged, returned, hashed as a standalone value, committed, or placed in an action receipt.
   - Does NOT prove network origin or database round-trip.

4. `DB_TLS_ADMISSION`
   - Evidence: PostgreSQL binding uses an accepted TLS mode: `require`, `verify-ca`, or `verify-full`.
   - Meaning: the key is valid for the required secure corridor.
   - Does NOT prove network origin or round-trip.

5. `NETWORK_ORIGIN_PROOF`
   - Evidence: the final database interaction can be attributed to the exact Render runtime, using exact runtime/database-side evidence or an equivalent challenge-response mechanism.
   - A successful local connection is NOT proof of Render origin.
   - Cached, tunneled, proxy-substituted, or otherwise ambiguous connections are not accepted as origin proof.
   - Does NOT by itself prove evidence integrity.

6. `DB_ROUND_TRIP`
   - Evidence: one compact temporal nonce A/B metadata envelope is written, read back, and its SHA-256 digest matches exactly.
   - Payload must contain no source dataset, credential, password, token, or bulk data.
   - Meaning: the service actually entered the room through the authorized runtime path and preserved evidence integrity.

7. `PROMOTION`
   - Only a successful `DB_ROUND_TRIP` on the exact runtime may satisfy the durable-evidence promotion gate.

## Non-inheritance law

These are NOT valid deductions:

```text
DB_EXISTENCE = PASS
    != DB_BINDING = PASS

DB_BINDING = BOUND_TLS
    != SECRET_RESOLUTION = PASS

DB_TLS_ADMISSION = PASS
    != NETWORK_ORIGIN_PROOF = PASS

NETWORK_ORIGIN_PROOF = PASS
    != DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
    != automatic downstream authority
```

A gate may only be marked PASS by evidence belonging to that gate.

## Gate interaction semantics — one FSM, not multiple Forensic states

The system has **one Forensic FSM**. Terms such as `DB_EXISTS`, `BOUND_TLS`, and `ROUND_TRIP_MATCH` are local observations/states of sequential gates inside that one FSM. They are not separate Forensic systems and must never be treated as peer permissions.

```text
                         ONE FORENSIC FSM
                               |
                       DB_EXISTENCE PASS?
                               |
                         prerequisite only
                               v
                        DB_BINDING PASS?
                               |
                         prerequisite only
                               v
                      SECRET + TLS ADMISSION
                               |
                         prerequisite only
                               v
                       NETWORK ORIGIN PROOF
                               |
                         prerequisite only
                               v
                        DB_ROUND_TRIP MATCH
                               |
                               v
                           PROMOTION
```

For any evaluation, the first `FAIL` or `UNKNOWN` stops downstream reachability. Later gates are `UNREACHED`; they are not silently converted to `FAIL`, and never to `PASS`.

### Three meanings that must remain distinct

```text
RESOURCE EXISTENCE
= the secured room actually exists

SERVICE AUTHORIZATION / BINDING
= the service has a candidate key and is admitted through the required corridor

ROUND-TRIP PROOF
= the exact runtime demonstrably entered the room and preserved evidence integrity
```

Therefore:

```text
DATABASE EXISTS
    !=
SERVICE IS AUTHORIZED

SERVICE IS AUTHORIZED
    !=
DURABLE EVIDENCE ROUND-TRIP IS PROVEN
```

This is a **single chain of evidence**, not two or more independent Forensic state machines.

### No PASS inheritance

A successor Bot must never perform inference such as:

```text
DB_EXISTS = PASS
    -> "therefore DB_ACCESS = PASS"       INVALID

DB_BINDING = PASS
    -> "therefore DB_ROUND_TRIP = PASS"   INVALID

ROUND_TRIP = PASS
    -> "therefore every downstream room is open" INVALID
```

A PASS grants exactly one thing: **reachability to the next declared gate**.

## Deny transitions

Any of the following is an immediate DENY and later gates become `UNREACHED` for that evaluation:

```text
DB_EXISTS = false
DATABASE_URL missing
wrong URL scheme
SECRET_RESOLUTION failed
placeholder or unauthorized override
TLS mode absent/invalid
NETWORK_ORIGIN_PROOF failed or ambiguous
round-trip write failed
round-trip read failed
SHA-256 mismatch
unknown evidence
```

`UNKNOWN_IS_NOT_PASS` is mandatory.

## State interaction

```text
                    ONE FORENSIC FSM
                          |
                    Evidence arrives
                          |
                          v
                    local gate check
                          |
                 +--------+--------+
                 |                 |
                PASS             FAIL/UNKNOWN
                 |                 |
                 v                 v
           next gate          DENY / UNREACHED
                 |
                 v
             next gate
```

A PASS is local to its gate. It is a prerequisite edge, not a state inheritance mechanism.

## Mandatory no-op interaction

When a required external event is not observable, the FSM enters:

```text
WAIT_EXTERNAL_EVENT
ACTION_SPACE = 0
ACTION = MANDATORY_NO_OP
PROMOTION = DENY
```

This is an **active safety state**, not an idle/error state.

The Foundation may:

- read exact-current runtime evidence;
- monitor the declared external event;
- append non-mutating forensic documentation;
- validate documentation integrity.

It may NOT manufacture the external event or mutate downstream state to escape the wait.

## Current exact-current state

The current exact-current runtime evidence is anchored by commit `eae5fc2c09c54cc2b13902cdf8d92843d4ca0097` and deploy `dep-da22s4lbedkc73d89kq0`.

Observed:

```text
DB_BINDING             = BOUND_TLS
DB_TLS_ADMISSION       = PASS
NETWORK_ORIGIN_PROOF   = NOT_PROVEN
DB_ROUND_TRIP          = NOT_PROVEN
PROMOTION              = DENY
FOUNDATION             = FROZEN
ACTION_SPACE           = 0
ACTION                 = MANDATORY_NO_OP
LAYER_1                = LOCKED
STAIRCASE              = LOCKED
```

The observed reason for the current network gate is `NETWORK_ORIGIN_PROBE_FAILED:OperationalError`.

Therefore the current successor action is:

```text
BRAIN-N086_WAIT_NETWORK_ORIGIN_PROOF
```

**No operational mutation is permitted while this mandatory wait remains active.**

## Security analogy

The database is a secured room.

```text
corridor_key
    +
room_key
    +
secret-resolution
    +
TLS admission
    +
network-origin proof
    +
inner proof where required
    =
permission to advance ONE edge
```

A key to one corridor/room never becomes a key to another room. A PASS for one gate never becomes a PASS for another gate.

## Immutability rules

- Never fabricate credentials.
- Never store credentials in GitHub.
- Never expose credentials in logs, health endpoints, action logs, or evidence envelopes.
- Never import PostgreSQL client dependencies into Brain governance core.
- Never promote on silence or inference.
- Never overwrite a prior forensic state; append a new action record.
- Every successor action must update `state/current_state.json` and `state/next_action.json`.
- Every action must have a durable action log containing result, evidence, deny/pass decision, and next action.
- A later retry creates a new event; it must not mutate the meaning of a historical FAIL/UNKNOWN event.

## Design truth vs execution truth

Contracts, diagrams, schemas, tests, and local results are design/local evidence. They do not prove Render execution.

```text
LOCAL PASS != RENDER PASS
DOCUMENTED TARGET != EXECUTED PROOF
```
