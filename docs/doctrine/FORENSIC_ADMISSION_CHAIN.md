# Forensic Admission Chain — Permanent Doctrine

## Purpose

This document is a successor-authoritative doctrine for every future Brain AI instance. It prevents a successor from confusing resource existence, authorization, transport security, evidence integrity, and promotion.

## Core rule

A PASS at one gate is **only a prerequisite for evaluating the next gate**. It is never permission to infer or inherit PASS at a deeper gate.

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

## Gate meanings

### 1. DB_EXISTENCE

Question: does the database resource actually exist and report an acceptable service state?

`DB_EXISTS = PASS` means only that the room exists.

It does NOT mean:

- the service has credentials;
- the service can connect;
- TLS is valid;
- evidence can be written;
- evidence can be read back;
- promotion is allowed.

### 2. DB_BINDING

Question: has the service received the required database binding through an authorized secret mechanism?

Required binding name:

`DATABASE_URL`

Credential policy:

- Render Secret Environment only;
- never GitHub;
- never repository files;
- never source code;
- never logs;
- never forensic snapshots.

`NOT_BOUND` is an explicit observed state, not an error to hide.

### 3. DB_TLS_ADMISSION

Question: does the binding use an accepted PostgreSQL scheme and TLS mode?

Accepted TLS modes:

- `require`
- `verify-ca`
- `verify-full`

Any other state is DENY.

### 4. DB_ROUND_TRIP

Question: can the authorized service actually perform a minimal real durable-evidence transaction?

Required proof:

```text
compact metadata envelope
        -> WRITE
        -> READ
        -> SHA-256 recomputation
        -> exact MATCH
```

The payload must not contain source bulk data, credentials, or secrets.

A successful binding without a successful round-trip is NOT promotion evidence.

### 5. PROMOTION

Only the complete chain can authorize promotion:

```text
DB_EXISTS
AND DB_BOUND
AND TLS_ADMITTED
AND ROUND_TRIP_HASH_MATCH
AND all other foundation invariants PASS
```

Anything else is DENY.

## Non-inheritance invariant

Never implement logic equivalent to:

```text
if DB_EXISTS:
    DB_ACCESS = PASS
```

or:

```text
if DB_BOUND_TLS:
    PROMOTION = PASS
```

Those are forensic violations.

Correct model:

```text
PASS(Gate_n) -> evaluate(Gate_n+1)
```

not:

```text
PASS(Gate_n) -> inherit(PASS)
```

## Continuous evidence doctrine

The system must produce valid evidence even while admission fails.

N005 and successors must treat the pipeline as:

```text
COLLECT(real)
  -> APPEND-ONLY BUFFER
  -> READINESS OBSERVATION
  -> DRY-RUN
  -> ADMISSION CHECK
  -> FORENSIC SNAPSHOT
  -> SLEEP / NEXT BOUNDED CYCLE
```

Readiness is observational only.

Permanent invariant:

`READINESS_SCORE MUST NOT TRIGGER ADMISSION.`

A readiness value of `0.92` is not a PASS.

## Drift invariant

If a raw evidence item changes after being recorded:

```text
DRIFT_DETECTED
    -> DENY
    -> FREEZE OLD SEGMENT
    -> CREATE VERSIONED NEW SEGMENT
```

Never overwrite historical raw evidence.

Example:

```text
data_buffer/2026-08-12/v1/
data_buffer/2026-08-12/v2/
```

## Admission attempt invariant

Every admission attempt must be append-only and contain at least:

- attempt_id
- timestamp
- dataset_hash
- admission_result
- reason
- missing_days
- conflicts
- readiness_score
- trace_hash
- input_hash
- dataset_state_hash

This allows successors to see previous DENY decisions rather than resetting history.

## Dead-pipeline invariant

A pipeline that does not crash can still be dead.

If `collected_days == 0` for the configured consecutive observation window, emit:

`DEAD_PIPELINE`

This is a forensic failure state, not a successful empty run.

## Memory/environment invariant

For Render Free:

```text
hard boundary = 512 MiB
operational guard = 320 MiB
```

Every continuous cycle must remain bounded. The continuous evidence loop is **not** an infinite uncontrolled process.

Each cycle must have:

- bounded input;
- bounded memory;
- bounded execution time;
- bounded evidence output;
- explicit sleep/termination condition.

Memory evidence should include compact RSS/peak observations and buffer disk usage without loading the complete dataset into RAM.

## Brain role

Brain remains the governance/control plane.

It does not become:

- the source-of-truth data engine;
- the calculation engine;
- the bulk scraper;
- the sensor engine;
- the database owner.

The chat window is only a communication interface. Persistent doctrine, state, evidence, action history, and successor instructions live outside the chat.

## Security analogy

The permanent house model is:

```text
corridor key + room key
```

A protected room may additionally require an inner release/doorbell. Possessing the corridor key and room key does not bypass an inner latch.

The DB admission chain follows the same rule:

```text
resource exists
-> authorized binding
-> transport admitted
-> actual room entry proven
-> evidence integrity proven
-> promotion
```

## Permanent sentence

> A fast system is not one that reaches PASS quickly, but one that produces valid evidence continuously—even while still failing.

## Successor instruction

Read this doctrine before modifying any foundation gate. If a proposed optimization makes a deeper PASS inferable from a shallower PASS, rejects evidence because it is DENY instead of preserving it, overwrites raw evidence, or uses readiness as admission, reject the change.
