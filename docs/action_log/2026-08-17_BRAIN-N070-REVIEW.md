# BRAIN-N070 — Successor Review and Foundation Invariants

## Input

A successor review identified two useful hardening requirements:

1. failure persistence must be immutable and reason-coded;
2. the durable round-trip proof should be temporal/nonced rather than a single optimistic echo.

It also correctly warned that Foundation work must not become an infinite infrastructure loop.

## Decision

Accept both hardening requirements as **foundation design invariants**, but do not falsely mark them implemented merely because the design has been documented.

### Failure persistence

Required future evidence event:

```text
 gate
 status=FAIL
 reason_code
 timestamp
 evidence_hash
 runtime_anchor
 immutable=true
```

A later successful retry creates a new event. It never deletes, overwrites, or rewrites the historical failure.

### Temporal round-trip

The target durable proof is:

```text
WRITE nonce A
READ nonce A
WRITE nonce B
READ nonce B
verify A != B
verify both values match their writes
hash compact A+B evidence
```

This is stronger than a single write/read echo, but it is still only a target until observed on the exact Render runtime against the intended PostgreSQL instance.

### Environment separation

A local database success is never Render evidence.

```text
LOCAL PASS != RENDER PASS
```

Only exact-current deployed runtime evidence may satisfy the Render gate.

## Important correction

The admission chain is one state machine, not two Forensic systems:

```text
DB_EXISTENCE
 -> DB_BINDING
 -> DB_TLS_ADMISSION
 -> DB_ROUND_TRIP
 -> PROMOTION
```

A gate PASS is only permission to attempt the next proof. It does not inherit trust.

After the first failure/unknown:

```text
later gates = UNREACHED
```

not PASS.

## Scope control

N070 must solve only the Render secret-only binding boundary and, if safely available, the real durable proof. It must not begin Quant Engine work and must not open Layer 1 merely because infrastructure is inconvenient.

If the Render control surface cannot safely establish the binding without exposing credentials, the correct result remains `NOT_BOUND` and the exact external operation is documented.

## Current foundation status

```text
Forensic state semantics       = CODIFIED
Failure persistence design     = REQUIRED / NOT YET OBSERVED
Temporal round-trip design     = REQUIRED / NOT YET OBSERVED
Render DB binding              = NOT_BOUND
Durable DB round-trip          = NOT_PROVEN
Promotion                      = DENY
Layer 1                        = LOCKED
Staircase                      = LOCKED
```
