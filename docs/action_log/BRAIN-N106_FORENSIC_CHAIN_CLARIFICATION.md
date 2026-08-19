# BRAIN-N106 — Forensic Gate Non-Inheritance Clarification

## Purpose

This action permanently records a critical clarification raised during successor handoff.

There are **not multiple independent Forensic systems** for database state.

There is exactly **ONE FORENSIC FSM** containing ordered admission gates.

## Canonical chain

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

## Meaning of each PASS

`DB_EXISTENCE = PASS` proves only that the database resource exists.

`DB_BINDING = PASS` proves only that the service has an authorized binding.

`DB_TLS_ADMISSION = PASS` proves only that the binding satisfies the accepted TLS policy.

`DB_ROUND_TRIP = PASS` proves that the real service performed the compact metadata write/read/hash-match operation.

`PROMOTION = PASS` requires the complete chain plus every other foundation invariant.

## Non-inheritance rule

A PASS is LOCAL.

A PASS is a PREREQUISITE for evaluating the next gate.

A PASS is NOT inherited by the next gate.

```text
PASS(Gate_n) -> evaluate(Gate_n+1)
```

Never:

```text
PASS(Gate_n) -> PASS(Gate_n+1)
```

Therefore:

```text
DATABASE EXISTS
    !=
DATABASE ACCESS AUTHORIZED
    !=
DATABASE TLS ADMITTED
    !=
DURABLE EVIDENCE PROVEN
    !=
PROMOTION
```

These are ordered facts inside one FSM, not separate Forensic universes.

## Why this matters

A successor Bot must never see `DB_EXISTS=PASS` and infer that Brain can access the database.

It must never see `DB_BOUND_TLS=PASS` and infer that durable evidence is proven.

It must never see a readiness score and convert it into admission.

Only evidence produced by the corresponding gate can produce that gate's PASS.

## Current boundary

The current Brain foundation remains governed by:

```text
PASS_IS_LOCAL        = true
PASS_IS_PREREQUISITE = true
NO_PASS_INHERITANCE  = true
UNKNOWN_IS_NOT_PASS  = true
DEFAULT_DENY         = true
NO_RECEIPT_HARD_DENY = true
ONE_FORENSIC_FSM     = true
IMMUTABLE_HISTORY    = append-only
```

## Successor instruction

This clarification is normative. Read it together with:

`docs/doctrine/FORENSIC_ADMISSION_CHAIN.md`

before changing any admission gate, database boundary, transport gate, or promotion logic.
