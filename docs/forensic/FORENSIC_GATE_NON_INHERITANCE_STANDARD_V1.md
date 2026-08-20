# FORENSIC GATE NON-INHERITANCE STANDARD V1

## Purpose

This document is normative for the single Forensic FSM of `PROJECT_BRAIN_AI`.
It exists so successor Bots cannot reinterpret independent evidence gates as one
compound PASS state.

## Core rule

> PASS is local evidence for exactly one gate. PASS is only a prerequisite for
the next gate. PASS is never inherited, promoted, copied, or inferred into any
other gate.

Formally:

```text
PASS(G_i) != PASS(G_i+1)
PASS(G_i) => eligible_to_evaluate(G_i+1)
PASS(G_i) does not => PASS(G_i+1)
```

## Database admission chain

```text
DB_EXISTENCE
    |
    v
DB_BINDING
    |
    v
DB_TLS_ADMISSION
    |
    v
DB_ROUND_TRIP
    |
    v
PROMOTION
```

Each node owns its own evidence.

### DB_EXISTENCE

Question: does the PostgreSQL resource exist and is its authoritative identity
known?

PASS means only existence/identity is proven.
It grants no access permission.

### DB_BINDING

Question: is the live service bound to the required runtime secret binding?

Required binding name: `DATABASE_URL`.

PASS means the service-side binding is observed.
It does not prove TLS admission or connectivity.

### DB_TLS_ADMISSION

Question: does the observed binding use an accepted PostgreSQL scheme and an
accepted TLS mode?

Accepted TLS modes:

- `require`
- `verify-ca`
- `verify-full`

PASS means TLS policy is satisfied.
It does not prove a real database round-trip.

### DB_ROUND_TRIP

Question: can the exact authorized runtime perform a bounded compact metadata
write/read operation and verify the returned evidence hash?

Required evidence:

```text
WRITE -> READ -> SHA-256 MATCH
```

The payload must contain no source dataset, credentials, or bulk data.

PASS means the round-trip is proven for that exact runtime.
It does not unlock unrelated rooms or Layer 1.

### PROMOTION

Question: may durable evidence be treated as an admitted sink for the next
Forensic gate?

Promotion requires the preceding database admission chain to have independently
passed. No promotion may be inferred from database existence, binding, or TLS
alone.

## Source provenance chain

The same rule applies to source provenance:

```text
SOURCE_INDEPENDENCE
    -> NETWORK_ORIGIN_PROOF
    -> RESULT_TRANSPORT
    -> OFFICIAL_RESULT_PANEL
    -> CANDIDATE
    -> EXCEL_VS_WEB_MATCH
    -> CANONICAL_QUORUM
    -> TRUTH_ADMISSION
```

A PASS at `RESULT_TRANSPORT` does not imply `OFFICIAL_RESULT_PANEL`.
A PASS at `OFFICIAL_RESULT_PANEL` does not imply `CANONICAL_QUORUM`.
A PASS at `CANONICAL_QUORUM` does not imply global Layer 1 unlock.

## Security interpretation

Treat every gate as a room with its own lock.

```text
corridor_key + room_key + gate_evidence
```

Possession of a corridor key does not open a room.
Possession of a room key does not satisfy the room's internal latch.
Passing one room does not grant access to another room.
A protected room may additionally require an inner-release action.

## State discipline

The canonical state is a mutable projection of exact current evidence.
Historical action logs are immutable append-only custody records.

Therefore:

```text
EXACT_CURRENT_RUNTIME_EVIDENCE
    > PERSISTED_STATE
    > IMMUTABLE_ACTION_HISTORY
    > OLD_DOCUMENTATION
    > HYPOTHESIS
```

A historical PASS cannot overwrite a current NOT_PROVEN/DENY state.

## Forbidden shortcuts

- no pass inheritance
- no aggregate `DATABASE_PASS`
- no proxy evidence
- no local curl substitution for exact runtime execution
- no synthetic data
- no credential in GitHub
- no credential in receipts
- no source modification solely to force a probe PASS
- no general Layer 1 unlock from a local gate PASS
- no staircase unlock from a Room 01 PASS

## Current implication

At the current foundation state, the transport receipt is still `NOT_PROVEN`
because the unchanged probe has not been executed inside the exact live Render
runtime. The execution primitive exists in source, but source existence is not
runtime execution evidence.

This distinction is mandatory for all successor Bots.
