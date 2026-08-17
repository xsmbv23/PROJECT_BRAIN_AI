# Forensic Database Admission Chain

## Canonical rule

The database admission states are **not independent Forensic systems**. They are sequential gates in one `FORENSIC DATABASE ADMISSION CHAIN`.

A PASS at an earlier gate is only a prerequisite for evaluating the next gate. **PASS is never inherited by inference.**

> UNKNOWN_IS_NOT_PASS
> DEFAULT_DENY
> NO_INFERENCE_ACROSS_GATES

## Chain

```text
FORENSIC DATABASE ADMISSION CHAIN
            |
            +--> DB_EXISTENCE
            |      "Does the database actually exist?"
            |          |
            |        PASS
            |          v
            +--> DB_BINDING
            |      "Does the service possess an explicit binding?"
            |          |
            |        PASS
            |          v
            +--> DB_TLS_ADMISSION
            |      "Does the binding satisfy TLS policy?"
            |          |
            |        BOUND_TLS
            |          v
            +--> DB_ROUND_TRIP
            |      "Can the service write/read a compact evidence envelope
            |       and verify SHA-256 equality?"
            |          |
            |        MATCH
            |          v
            +--> PROMOTION
```

Any failure or unknown state terminates the chain with `DENY`.

## Critical distinctions

```text
DATABASE EXISTS
    !=
SERVICE IS BOUND
    !=
SERVICE IS TLS-ADMITTED
    !=
DURABLE ROUND-TRIP IS PROVEN
    !=
PROMOTION IS ALLOWED
```

These are observations about different security/admission questions, not contradictory states.

## Gate semantics

- `DB_EXISTENCE`: proves the PostgreSQL resource exists and is available. It does not grant service access.
- `DB_BINDING`: proves the service possesses an explicit binding (`DATABASE_URL`). It does not prove safe communication.
- `DB_TLS_ADMISSION`: proves the binding satisfies the accepted TLS policy (`require`, `verify-ca`, `verify-full`). It does not prove a real database round-trip.
- `DB_ROUND_TRIP`: proves a real compact metadata envelope was written, read back, and SHA-256 verified as identical. The payload must contain no credentials and no bulk/source data.
- `PROMOTION`: may pass only after all required preceding gates have independently produced their evidence.

## Door/key analogy

- `DB_EXISTENCE`: the room exists.
- `DB_BINDING`: the service has the room's key.
- `DB_TLS_ADMISSION`: the key is accepted for protected communication.
- `DB_ROUND_TRIP`: the door actually opened and the forensic interaction was proven.
- `PROMOTION`: only after the full chain succeeds may durable DB evidence be promoted.

A service must never infer a later gate from an earlier PASS.

## Forbidden transitions

```text
DB_EXISTENCE = PASS
    -> DB_BINDING = PASS          FORBIDDEN BY INFERENCE

DB_BINDING = PASS
    -> DB_TLS_ADMISSION = PASS   FORBIDDEN BY INFERENCE

DB_TLS_ADMISSION = BOUND_TLS
    -> DB_ROUND_TRIP = MATCH      FORBIDDEN BY INFERENCE
```

Each transition requires its own observable evidence.

## Forensic invariants

1. `UNKNOWN_IS_NOT_PASS`.
2. `DEFAULT_DENY`.
3. No credential is stored in GitHub.
4. No credential is emitted in logs or evidence envelopes.
5. `psycopg` remains outside Brain `core/`.
6. Compact metadata only for admission probes.
7. Real write/read/hash evidence is required for durable round-trip PASS.
8. Layer 1 remains locked until the foundation promotion gate is explicitly satisfied.
9. The successor action log is authoritative for continuation.
10. A database resource's existence is never treated as an authorization grant.
11. A successful binding is never treated as proof of TLS admission.
12. TLS admission is never treated as proof of durable evidence persistence.

## Successor instruction

Never collapse the chain into a single boolean such as `DATABASE_PASS`.

If a future Bot sees:

```text
DB_EXISTENCE = PASS
DB_BINDING = NOT_BOUND
```

the correct interpretation is **database exists but service has no admitted access**. It is not an inconsistency.

If:

```text
DB_BINDING = PASS
DB_TLS_ADMISSION = DENY_TLS
```

the correct interpretation is **binding exists but is not admitted for protected communication**.

If:

```text
DB_TLS_ADMISSION = BOUND_TLS
DB_ROUND_TRIP = NOT_PROVEN
```

the correct interpretation is **the door/key path is admitted, but durable forensic interaction has not been proven**.

Only a verified `DB_ROUND_TRIP = MATCH` may reach `PROMOTION`.
