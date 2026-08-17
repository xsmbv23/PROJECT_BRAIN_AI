# Forensic Database Admission Chain

## Canonical rule

The database admission states are **not independent Forensic systems**. They are sequential gates in one `FORENSIC DATABASE ADMISSION CHAIN`.

A PASS at an earlier gate is only a prerequisite for evaluating the next gate. **PASS is never inherited by inference.**

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

## Door/key analogy

- `DB_EXISTENCE`: the room exists.
- `DB_BINDING`: the service has the room's key.
- `DB_TLS_ADMISSION`: the key is the correct protected key.
- `DB_ROUND_TRIP`: the door actually opened and the forensic interaction was proven.
- `PROMOTION`: only after the full chain succeeds may durable DB evidence be promoted.

A service must never infer a later gate from an earlier PASS.

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
