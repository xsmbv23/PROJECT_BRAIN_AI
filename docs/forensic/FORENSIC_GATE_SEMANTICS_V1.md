# FORENSIC GATE SEMANTICS V1

## Purpose

This document is an immutable architectural rule for all future Brain/Quant bots.
It defines how forensic states interact. There is **ONE FORENSIC FSM**, not multiple independent forensic systems.

## Core law

A `PASS` belongs only to the gate that produced the evidence.

```text
GATE_A_PASS != GATE_B_PASS
```

A PASS is a **local prerequisite**, never an inherited authorization.

```text
PASS(GATE_A)
    !=
PASS(GATE_B)
```

The next gate must execute its own evidence-producing check.

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

Meaning:

- `DB_EXISTENCE=PASS`: the database exists.
- `DB_BINDING=PASS`: the service has an actual runtime binding.
- `DB_TLS_ADMISSION=PASS`: that binding satisfies the accepted TLS policy.
- `DB_ROUND_TRIP=PASS`: the exact runtime performed the real write/read/hash verification.
- `PROMOTION=PASS`: and only then may durable evidence promotion occur.

None of these PASS values may automatically create another PASS.

## Source admission chain

```text
SOURCE_INDEPENDENCE
    |
    v
NETWORK_ORIGIN_PROOF
    |
    v
RESULT_TRANSPORT
    |
    v
OFFICIAL_RESULT_PANEL
    |
    v
CANDIDATE
    |
    v
EXCEL_VS_WEB_MATCH
    |
    v
CANONICAL_QUORUM
    |
    v
TRUTH_ADMISSION
```

A successful network request does not prove the result is official.
A parsed candidate does not prove truth.
A source match does not prove quorum.
A quorum does not erase the requirement for the next gate's own evidence.

## Hard denial rules

```text
UNKNOWN       -> DENY
NOT_AVAILABLE -> DENY
NOT_EXECUTED  -> DENY
MISSING       -> DENY
MISMATCH      -> DENY
```

No fallback, proxy, local substitution, synthetic receipt, or inference may convert one of these states into PASS.

## Exact-runtime rule

These are never equivalent:

```text
CODE_EXISTS
CODE_EXECUTED

DEPLOYMENT_IDENTITY
RUNTIME_RECEIPT

LOCAL_CURL
EXACT_RUNTIME_EVIDENCE
```

A receipt is valid only when produced by the exact runtime being audited and cryptographically bound to its runtime identity.

## Security interaction model

The Brain security model remains:

```text
corridor key
    +
room key
    +
(optional protected-room inner release)
    +
local gate evidence
    =
permission to continue
```

Keys authorize access to a room; they do not manufacture forensic evidence.
Forensic evidence authorizes state transitions; it does not bypass room security.

## Current consequence

`BRAIN-N104C.1D-INFRA` is legitimately BLOCKED because the exact-runtime execution primitive is unavailable.

This is not a defect to be hidden. It is a valid forensic state.

The correct next action is an infrastructure task to obtain an auditable exact-runtime execution primitive. Until then:

```text
TRANSPORT_RECEIPT = NOT_PROVEN
TRANSPORT_GATE    = DENY
CANONICAL_TRUTH   = DENY
LAYER_1           = LOCKED
STAIRCASE         = LOCKED
```

## Successor instruction

Future bots **must not** resume the blocked gate by using local curl, a proxy, sidecar evidence, fabricated receipts, source mutation, or any other substitute for exact-runtime execution.
