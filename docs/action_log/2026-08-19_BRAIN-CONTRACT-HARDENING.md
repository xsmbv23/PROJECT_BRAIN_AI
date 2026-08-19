# BRAIN-CONTRACT-HARDENING — Successor Safety Upgrade

## Why this action exists

A roadmap document can describe intent but cannot grant execution permission. A report template can describe receipts but cannot create forensic evidence. An origin probe name without explicit admission criteria allows a successor bot to invent its own meaning.

These gaps are closed before N101 execution.

## Contracts added

- `contracts/quant_roadmap_activation_v1.json`
- `contracts/receipt_immutability_v1.json`
- `contracts/forensic_transition_invariants_v1.json`
- `docs/forensic/ORIGIN_METADATA_PROBE_V1.md`

## Critical invariant

```text
PASS(Gate A)
   != PASS(Gate B)
   != PROMOTION
```

A PASS is local to the gate that produced it. It only authorizes evaluation of the next gate. No state may be inferred from prose, chat, stale evidence, or another gate's PASS.

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

Round-trip itself is ordered:

```text
WRITE -> READ -> REHASH -> MATCH
```

## Broader data chain

```text
NETWORK_ORIGIN_PROOF
    -> DURABLE_ROUND_TRIP
    -> PROMOTION
    -> DATA_ADMISSION
    -> RESEARCH_ADMISSION
    -> EVIDENCE_ANALYSIS
    -> REPORTING
```

## Origin probe admission

`ORIGIN_METADATA_PROBE` is now defined as a bounded, non-secret, HTTPS-only provenance observation. Canonicality and independence are explicit evidence fields. Different hostnames alone never prove independence.

## Anti-loop rule

A failed transition may not automatically retry itself. A retry requires:

1. new action id;
2. new evidence;
3. explicit successor authorization.

After repeated failure without new evidence, the system HALTs and records the denial rather than looping.

## Receipt rule

Future prediction reporting must create an immutable, content-addressed `PREDICTION_RECEIPT` before any `RESULT_RECEIPT`. A report without the persisted prediction receipt is not a valid forensic prediction report.

## Current decision

These contracts harden the foundation but do not change promotion status.

```text
PROMOTION = DENY
LAYER_1   = LOCKED
STAIRCASE = LOCKED
N101      = READY
```

The next execution remains the explicitly named `BRAIN-N101_ORIGIN_METADATA_PROBE`, now with machine-readable admission constraints.
