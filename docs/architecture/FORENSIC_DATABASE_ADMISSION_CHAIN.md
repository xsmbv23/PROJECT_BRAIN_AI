# Forensic Database Admission Chain

## Purpose

This document is normative foundation architecture. It prevents a successor Bot AI from confusing resource existence, authorization, TLS admission, and durable evidence proof.

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
   - Does NOT prove TLS or usable database access.

3. `DB_TLS_ADMISSION`
   - Evidence: PostgreSQL binding uses an accepted TLS mode: `require`, `verify-ca`, or `verify-full`.
   - Meaning: the key is valid for the required secure corridor.
   - Does NOT prove a real round-trip.

4. `DB_ROUND_TRIP`
   - Evidence: one compact, non-secret metadata envelope is written, read back, and its SHA-256 digest matches exactly.
   - Payload must contain no source dataset, credential, password, token, or bulk data.
   - Meaning: the service actually entered the room, used the authorized path, and preserved evidence integrity.

5. `PROMOTION`
   - Only the successful `DB_ROUND_TRIP` gate may promote durable evidence capability.

## Deny transitions

Any of the following is an immediate DENY and must not be silently converted:

```text
DB_EXISTS = false
DATABASE_URL missing
wrong URL scheme
TLS mode absent/invalid
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
DB_TLS_ADMISSION
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
corridor_key + room_key + TLS admission + inner proof
```

Knowing that a room exists is not possessing its key. Possessing a key is not proof that the secure door opened. Opening the door is not proof that the forensic evidence survived a write/read cycle.

## Immutability rules

- Never fabricate credentials.
- Never store credentials in GitHub.
- Never expose credentials in logs, health endpoints, action logs, or evidence envelopes.
- Never import PostgreSQL client dependencies into Brain governance core.
- Never promote on silence or inference.
- Never overwrite a prior forensic state; append a new action record.
- Every successor action must update `state/current_state.json` and `state/next_action.json`.
- Every action must have a durable action log containing result, evidence, deny/pass decision, and next action.

## Current foundation state

As of N062:

```text
DB_EXISTENCE       = PASS
DB_BINDING         = NOT_BOUND
DB_TLS_ADMISSION   = NOT_PROVEN
DB_ROUND_TRIP      = NOT_PROVEN
PROMOTION          = DENY
LAYER_1            = LOCKED
STAIRCASE          = LOCKED
```

The exact-current runtime records `NOT_BOUND` directly through the non-secret binding probe; the successor must not infer it from missing logs.

## OOM constraint

Render Free has a hard 512 MB boundary. Foundation runtime keeps a 320 MiB conservative guard. Database round-trip tests must remain compact and must never load source datasets or bulk evidence into memory.
