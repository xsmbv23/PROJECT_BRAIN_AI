# FORENSIC FSM — DATABASE ADMISSION CHAIN V1

## Canonical rule

There is ONE Forensic FSM. Database admission is one ordered chain inside that FSM; it is not a second forensic system.

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
```

## Gate semantics

`DB_EXISTENCE=PASS` means only that the database resource exists and is observable.
It does not prove that the service can access it.

`DB_BINDING=PASS` means only that the exact runtime has an authorized database binding.
It does not prove TLS admission or successful database I/O.

`DB_TLS_ADMISSION=PASS` means only that the binding satisfies the explicit TLS policy.
It does not prove a real round trip.

`DB_ROUND_TRIP=PASS` means a compact metadata envelope was actually written, read back, and its SHA-256 matched.
Only this gate may satisfy the durable evidence sink admission condition.

`PROMOTION=PASS` means durable evidence promotion is authorized after the prior gate has its own receipt.

## Non-inheritance invariant

```text
PASS(N) ≠ PASS(N+1)
```

Every gate requires its own Atomic Evidence Artifact. A PASS is local evidence and only a prerequisite for evaluating the next gate.

```text
DB EXISTS
   ≠
DB BOUND
   ≠
DB TLS ADMITTED
   ≠
DB ROUND-TRIP PROVEN
   ≠
PROMOTION AUTHORIZED
```

## Epistemic enforcement

```text
NO RECEIPT
   ↓
NOT_PROVEN
   ↓
HARD_DENY
```

The system must never infer authorization from resource existence, connector metadata, silence, historical state, or an earlier gate's PASS.

## Interaction with mutable state and immutable history

Exact current evidence may change the mutable state projection. The old state and the reason for the transition are appended to immutable history and are never rewritten.

```text
EXACT CURRENT EVIDENCE
        ├──────────────→ CURRENT STATE CONVERGENCE
        └──────────────→ IMMUTABLE HISTORY APPEND
```

## Security analogy

Database existence proves that the room exists.
Database binding proves that the service has the room key.
TLS admission proves that the key is acceptable under the security policy.
Round-trip proves that the door was actually opened and the evidence could be exchanged intact.
Promotion is the authority to treat that room as a durable forensic evidence sink.

Each stage is distinct because the evidence required to prove it is distinct.

## Prohibited shortcuts

- No PASS inheritance.
- No local substitution for exact runtime evidence.
- No proxy evidence.
- No fabricated DATABASE_URL.
- No credentials in GitHub.
- No disabling TLS to make the gate pass.
- No bulk source data in Brain runtime.
