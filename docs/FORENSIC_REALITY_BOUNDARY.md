# FORENSIC REALITY BOUNDARY

## Status

**FROZEN FOUNDATION RULE**

This document is normative for every successor Bot AI working on `Project_Brain_AI`.

## 1. Core principle

The system must never create a fact merely because a fact would unblock progress.

```text
REALITY -> OBSERVATION -> EVIDENCE -> ADMISSION
```

Never:

```text
DESIRED RESULT -> SYNTHETIC RECEIPT -> PASS
```

## 2. Three states that must never be conflated

Every operation must distinguish:

```text
CAN_DO
CANNOT_DO
MUST_NOT_FAKE
```

`CANNOT_DO + MUST_NOT_FAKE` is a **valid system state**.

Therefore:

```text
WAIT_EXTERNAL_EVENT = VALID
```

It is not automatically an error, defect, or unfinished implementation.

## 3. Forensic admission chain

There is exactly **one** forensic FSM. It contains multiple gates. The gates are not independent forensic systems.

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

The same model applies to external-source reality validation.

### Critical invariant

> PASS IS LOCAL TO A GATE.
>
> PASS IS ONLY A PREREQUISITE FOR THE NEXT GATE.
>
> PASS NEVER INHERITS.

Examples:

```text
DB_EXISTS = PASS
!= DB_AUTHORIZED

DB_BOUND_TLS = PASS
!= DB_ROUND_TRIP

ROUNDTRIP_VALID = PASS
!= DOMAIN_TRUE
```

A successor must never collapse these into a single `PASS` flag.

## 4. Reality boundary

The system is an admission system, not a truth generator.

```text
SYSTEM DOES NOT CREATE TRUTH
SYSTEM ONLY ADMITS EVIDENCE
```

The system may observe:

- HTTP status
- raw byte count
- SHA-256
- runtime identity
- transport success/failure
- structural validity
- round-trip validity

But it must not silently infer domain truth from any single observation.

## 5. External event rule

If progress requires an event outside the available control surface, the absence of that event is a valid state.

```text
EXTERNAL_EVENT_REQUIRED
        |
        +-- event observed -> continue
        |
        +-- event absent -> WAIT_EXTERNAL_EVENT
```

Forbidden workarounds:

- browser substitution for runtime evidence
- synthetic receipt
- copied HTML presented as runtime receipt
- fabricated SHA
- alternate runtime substitution that changes the declared source identity
- modifying workflow semantics merely to manufacture the missing event

## 6. Runtime identity

A source is not identified only by URL.

```text
SOURCE_IDENTITY = (SOURCE_URL, EXECUTION_RUNTIME)
```

The same URL retrieved by two different runtimes is two distinct observations unless an explicit equivalence rule exists.

Do not silently merge them.

## 7. Receipt law

Before parsing, capture:

```text
HTTP_STATUS
RAW_BYTE_COUNT
SHA256
RUNTIME_IDENTITY
```

If capture fails:

```text
FAILURE_RECEIPT = FROZEN EVIDENCE
```

No raw bytes means no fabricated hash.

## 8. Classification

New receipt classifications:

```text
ROUNDTRIP_VALID
STRUCTURALLY_VALID
PARTIAL
CONFLICT
DRIFT_DETECTED
```

`STRUCTURALLY_VALID` does not mean domain truth.

`ROUNDTRIP_VALID` does not mean domain understanding.

## 9. Quorum

Canonicalization cannot be reached from one observation.

```text
receipts < 2 -> CANONICAL_UNREACHED
preferred minimum < 3 -> CANONICAL_UNREACHED
```

The current foundation deliberately preserves this boundary.

## 10. Readiness is not authority

Readiness/health/observability may report status but has:

```text
ZERO_PROMOTION_AUTHORITY
ZERO_ADMISSION_AUTHORITY
ZERO_EXECUTION_AUTHORITY
ZERO_COLLECTION_AUTHORITY
```

Likewise execution must remain deterministic and readiness-blind.

## 11. Anti-loop law

Do not create cosmetic hardening loops.

Every next action must do at least one of:

1. close a named invariant; or
2. produce missing evidence.

If neither occurs, stop.

## 12. Successor instruction

When the system reaches:

```text
WAIT_EXTERNAL_EVENT
```

record it as a successful preservation of the reality boundary.

Do not “fix” the wait state merely to make the dashboard green.

The correct next action is to identify the exact external event required and wait for real evidence.
