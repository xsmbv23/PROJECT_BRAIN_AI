# QUANT-N005 — Forensic Semantics Freeze

## Trigger

Successor review identified a subtle risk: readiness values could be mistaken for soft forensic evidence and accidentally become a second admission FSM.

## Decision

Freeze the following invariant:

```text
READINESS ∉ FORENSIC_CHAIN
```

Readiness is observability only. It has zero promotion authority and must not alter execution.

## Authoritative model

There is exactly one forensic admission FSM.

```text
Observability / Readiness
          |
          v
One Authoritative Admission FSM
          |
          v
Execution / Room
```

No readiness FSM. No rehearsal admission FSM. No hidden execution admission FSM.

## Database admission semantics

```text
DB_EXISTENCE -> DB_BINDING -> DB_TLS -> DB_ROUND_TRIP -> PROMOTION
```

PASS does not inherit to the next gate. Each gate requires its own evidence.

## Data semantics

```text
SOURCE -> RAW -> BUFFER/QUARANTINE -> ADMISSION -> IMMUTABLE CANONICAL -> ENGINE
```

The hard boundaries remain:

- BUFFER != ENGINE INPUT
- PARTIAL != TRUTH
- COLLECTION != ADMISSION

## N006 contract

The next acquisition milestone is not merely "crawl data". It is:

```text
SOURCE -> RAW -> BUFFER -> PROVENANCE HARDENING
```

with exact raw SHA-256, complete provenance, day-level isolation, independent-source quorum, append-only quarantine, and drift detection.

## Anti-loop rule

The project must not enter an endless hardening loop. A gate is hardened only when the proposed change closes a concrete invariant or produces missing evidence. No cosmetic refactor, duplicate gate, or readiness metric may create a new admission layer.

The next action must move the system toward real-source acquisition while preserving the frozen semantics.
