# Forensic Admission Chain — Immutable Successor Rule

## Purpose

This document is a mandatory architectural handoff for every future Bot AI.
It prevents the database admission chain from being misunderstood as multiple
independent forensic systems and prevents Quant Engine from recreating Brain.

## One chain, not multiple forensic systems

The database state is ONE Forensic finite-state machine with sequential gates:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

A gate PASS is only a prerequisite for evaluating the next gate. PASS never
inherits forward as permission.

```text
DB_EXISTS = PASS
    != DB_BOUND = PASS
DB_BOUND = PASS
    != SECRET_RESOLUTION = PASS
SECRET_RESOLUTION = PASS
    != TLS_ADMISSION = PASS
TLS_ADMISSION = PASS
    != NETWORK_ORIGIN_PROOF = PASS
NETWORK_ORIGIN_PROOF = PASS
    != ROUND_TRIP = PASS
```

Only a real temporal compact-metadata write/read followed by SHA-256 equality
may satisfy the round-trip gate. Promotion remains DENY until that evidence
exists.

## Reachability rule

The chain is strictly sequential. On the first FAIL or UNKNOWN:

```text
current gate = TERMINAL DENY
later gates = UNREACHED
```

Later raw flags MUST NOT be interpreted as PASS, and a retry MUST NOT erase the
previous event. Failure is persisted as an immutable reason-coded event.

## Boundary distinction

These are three different facts:

1. **Existence** — the database resource exists.
2. **Authorization/binding** — the service has a valid secret-backed binding and
   TLS admission.
3. **Capability/evidence** — the exact runtime can perform the real compact
   write/read/hash-match round trip.

Do not collapse them into a single `DATABASE_PASS` state.

## Real external-event trigger rule

Some gates depend on events that must originate outside the Brain process.
Brain, Bot, and chat are allowed to prepare a workflow, inspect its result,
verify a receipt, and record the resulting state. They are NOT allowed to
manufacture the external event or its evidence in order to unlock themselves.

For a real GitHub Actions admission/dispatch, admissible origins are:

1. a real manual workflow dispatch;
2. a real source-code push/commit event;
3. a real authorized external API dispatch.

The resulting runner execution must be observable and fresh. A copied historical
receipt, synthetic fixture, invented Run ID, invented dispatch claim, or chat
message is not external-world evidence.

```text
REAL EXTERNAL EVENT
        |
        v
GITHUB ACTIONS RUNNER
        |
        +--> real execution identity
        +--> real receipt / artifact
        |
        v
FORENSIC FSM
        |
        +--> verify fresh evidence
        +--> authorize exact transition
        |
        v
NEXT ACTION SPACE
```

`WAIT_EXTERNAL_EVENT` is a valid state. Waiting is not a failure.

This is analogous to the protected-room rule:

```text
corridor key -> room key -> inner latch -> doorbell/external event -> admission
```

Correct route and correct keys do not manufacture the person inside opening the
door.

## Brain versus Quant Engine

`Project_Brain_AI` is the frozen Governance Control Plane.

`Quant_Engine` is the active execution layer.

Brain owns:

- immutable governance rules;
- admission decisions;
- capability/security policy;
- forensic state semantics;
- successor handoff authority.

Quant Engine owns:

- input adapter consumption from canonical data;
- calculation;
- signal generation;
- scoring/ranking;
- measurable output.

### Mandatory anti-duplication rule

> **Room in Quant Engine is a function boundary, not a second security boundary.**

Quant Engine MUST NOT recreate Brain's corridor locks, permission graph,
forensic admission FSM, or another governance system.

A Quant Engine room may have local input/output contracts and validation, but
security authority remains in Brain.

## QUANT-N001 minimum execution frame

The first Layer 1 implementation must prove:

```text
CANONICAL DATA
     |
     v
INPUT ADAPTER
     |
     v
ROOM 01 / SIGNAL FUNCTION
     |
     v
SCORING
     |
     v
OUTPUT
```

Success criterion:

```text
RUN -> OUTPUT -> MEASURABLE RESULT
```

Do not create multi-room orchestration, heavy corridor abstraction, duplicate
permission systems, or duplicate forensic layers before the first real
end-to-end signal pipeline exists.

## Why this rule is immutable

The foundation previously reached a terminal `DENY` because the exact Render
runtime was not bound to PostgreSQL. This was an external boundary limitation,
not a reason to weaken controls or fabricate evidence.

Layer 1 must therefore move forward without reopening the frozen foundation.
Only an explicitly authorized external binding may reopen a previously denied
foundation gate, and the old DENY event must remain immutable in history.
