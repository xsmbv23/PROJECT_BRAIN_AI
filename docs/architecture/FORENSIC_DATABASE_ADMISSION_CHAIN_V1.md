# FORENSIC DATABASE ADMISSION CHAIN V1

## Purpose

This document is a canonical architectural rule for successor AI agents.

There are NOT multiple independent forensic states or multiple forensic systems.
There is one `FORENSIC_STATE`, containing a sequential admission chain.

A PASS at one gate is evidence for that gate only. It is a prerequisite for
reaching the next gate, never permission to infer a deeper PASS.

## Admission chain

```text
FORENSIC_STATE
     |
     +--> GATE 1: DB_EXISTENCE
     |       |
     |       +-- NO  --> DENY / stop deeper DB admission
     |       |
     |       +-- YES --> GATE 2
     |
     +--> GATE 2: DB_BINDING
     |       |
     |       +-- NOT_BOUND --> DENY / stop deeper DB admission
     |       |
     |       +-- BOUND --> GATE 3
     |
     +--> GATE 3: DB_TLS_ADMISSION
     |       |
     |       +-- TLS invalid/unknown --> DENY / stop deeper DB admission
     |       |
     |       +-- BOUND_TLS --> GATE 4
     |
     +--> GATE 4: DB_ROUND_TRIP
             |
             +-- write compact metadata
             +-- read exact metadata
             +-- recompute SHA-256
             |
             +-- MISMATCH/ERROR/UNKNOWN --> DENY
             |
             +-- MATCH --> PROMOTION_GATE
```

## Non-inheritance rule

These transitions are forbidden:

```text
DB_EXISTS=PASS
    => DB_BINDING=PASS             FORBIDDEN

DB_BINDING=PASS
    => DB_TLS_ADMISSION=PASS       FORBIDDEN

DB_TLS_ADMISSION=BOUND_TLS
    => DB_ROUND_TRIP=PASS          FORBIDDEN

LOCAL_ROUND_TRIP=PASS
    => RENDER_ROUND_TRIP=PASS      FORBIDDEN
```

Only the evidence belonging to a gate may establish that gate.

## Stop-on-first-failure rule

If a gate fails, all later gates are `UNREACHED`, not `PASS` and not inferred.

Example:

```text
DB_EXISTENCE       = PASS
DB_BINDING         = NOT_BOUND
DB_TLS_ADMISSION   = UNREACHED
DB_ROUND_TRIP      = UNREACHED
PROMOTION          = DENY
```

Do not execute deeper gates merely to manufacture evidence after a known
blocking failure unless a separate diagnostic action explicitly permits it.
Such diagnostics must not change the admission state.

## Failure immutability

Every blocking failure must retain an immutable event containing at least:

- action id
- gate id
- reason code
- runtime anchor commit
- observation timestamp
- evidence hash/reference

A later successful attempt does not erase the previous failure history.

## Local versus Render evidence

```text
LOCAL PASS != RENDER PASS
```

A local test can prove implementation behavior only. A Render deployment can
prove deployed-runtime behavior only when its exact commit/runtime anchor is
known.

## Credential rule

Credentials are never evidence payloads.

`DATABASE_URL` may exist only as a Render Secret Environment binding. Its value
must never be copied into:

- GitHub
- source code
- action logs
- forensic receipts
- chat messages
- error messages

Only non-secret classification is admissible:

```text
NOT_BOUND
DENY_SCHEME
DENY_TLS
BOUND_TLS
```

## Round-trip rule

`BOUND_TLS` is still not durable-evidence PASS.

The final DB gate requires a compact temporal nonce A/B metadata transaction:

```text
nonce_A -> write -> read -> SHA256(A) match
nonce_B -> write -> read -> SHA256(B) match
```

The payload must contain no source dataset and no credentials.

## Promotion rule

Only this chain may reach promotion:

```text
DB_EXISTENCE=PASS
    AND DB_BINDING=BOUND
    AND DB_TLS_ADMISSION=BOUND_TLS
    AND DB_ROUND_TRIP=SHA256_MATCH
        |
        +--> PROMOTION=PASS
```

Anything else is `DENY`.

## Architectural analogy

The database is a secured room.

1. The corridor key proves the agent is on the correct corridor.
2. The room key proves it is authorized for that room.
3. The inner latch may still refuse entry for protected rooms.
4. Entry does not prove that evidence was successfully persisted.
5. The write/read/hash match proves the actual durable evidence path.

Therefore:

> **Existence is not authorization. Authorization is not TLS admission. TLS admission is not durable persistence. Persistence is not promotion until the exact forensic round-trip is proven.**

This rule is part of the foundation and must be read before any successor AI
changes the database boundary or opens Layer 1.
