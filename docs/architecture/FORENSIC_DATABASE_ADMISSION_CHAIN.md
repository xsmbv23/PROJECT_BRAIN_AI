# Forensic Database Admission Chain

## Purpose

This document is normative foundation architecture. It prevents a successor Bot AI from confusing resource existence, authorization, TLS admission, runtime secret resolution, network origin, and durable evidence proof.

## Core rule

**A PASS at one gate is only a prerequisite for the next gate. It is never permission to infer PASS at a deeper gate.**

There is one Forensic system and one database-admission chain. The states below are sequential gates, not independent Forensic systems.

## Gates

1. `DB_EXISTENCE`
   - Evidence: the configured Render PostgreSQL resource exists and is available.
   - Meaning: the room exists.
   - Does NOT grant access.

2. `DB_BINDING`
   - Evidence: the running service has the explicitly required `DATABASE_URL` binding.
   - Credential source must be Render Secret Environment only.
   - Meaning: the service has a candidate key to the room.
   - Does NOT prove secret resolution, TLS, or usable database access.

3. `SECRET_RESOLUTION`
   - Evidence: the exact runtime has a non-empty `DATABASE_URL` sourced from the approved Render Secret Environment boundary, is not a known placeholder, and is not overridden by an unapproved source.
   - Only non-secret classification may be emitted.
   - The raw secret must never be logged, returned, hashed as a standalone value, committed, or placed in an action receipt.
   - Does NOT prove network origin or database round-trip.

4. `DB_TLS_ADMISSION`
   - Evidence: PostgreSQL binding uses an accepted TLS mode: `require`, `verify-ca`, or `verify-full`.
   - Meaning: the key is valid for the required secure corridor.
   - Does NOT prove a real round-trip.

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
DB_EXISTENCE
     |
     | PASS only
     v
DB_BINDING
     |
     | PASS only
     v
SECRET_RESOLUTION
     |
     | PASS only
     v
DB_TLS_ADMISSION
     |
     | PASS only
     v
NETWORK_ORIGIN_PROOF
     |
     | PASS only
     v
DB_ROUND_TRIP
     |
     | SHA256 MATCH only
     v
PROMOTION
```

A failure at any stage stops the chain. A later gate cannot repair an earlier missing prerequisite.

## Security analogy

The database is a secured room.

```text
corridor_key + room_key + secret-resolution + TLS admission + origin proof + inner proof
```

Knowing that a room exists is not possessing its key. Possessing a key is not proof that the runtime resolved it. Resolving a key is not proof that the secure corridor was used. A secure connection is not proof of origin. Opening the door is not proof that the forensic evidence survived a write/read cycle.

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

The exact runtime anchor and exact-current deployment evidence are mandatory for production claims.

## Temporal round-trip

The final durable evidence gate requires a real temporal nonce A/B protocol, not a static self-check:

```text
A: generate compact nonce + metadata envelope
B: write to durable PostgreSQL through TLS
C: read back
D: verify nonce / envelope identity
E: SHA-256 match
F: persist receipt without secrets
```

A documented target is not a completed round-trip.

## Current foundation state

As of N070/N071 design handoff:

```text
DB_EXISTENCE       = PASS
DB_BINDING         = NOT_BOUND
SECRET_RESOLUTION  = UNREACHED
DB_TLS_ADMISSION   = UNREACHED
NETWORK_ORIGIN     = UNREACHED
DB_ROUND_TRIP      = UNREACHED
PROMOTION          = DENY
LAYER_1            = LOCKED
STAIRCASE          = LOCKED
```

The exact-current runtime records `NOT_BOUND` directly through the non-secret binding probe; the successor must not infer it from missing logs.

## OOM constraint

Render Free has a hard 512 MB boundary. Foundation runtime keeps a 320 MiB conservative guard. Database round-trip tests must remain compact and must never load source datasets or bulk evidence into memory.
