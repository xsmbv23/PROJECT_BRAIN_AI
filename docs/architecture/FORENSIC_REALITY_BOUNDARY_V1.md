# FORENSIC REALITY BOUNDARY V1

## Purpose

This document is a hard architectural invariant for successor Bots.

The Brain must never convert absence of an external event into an invented event,
receipt, transition, or action.

## HARD FSM

```text
NO REAL EVENT
    |
    v
NO EVIDENCE
    |
    v
NO TRANSITION
    |
    v
NO ACTION
    |
    v
WAIT_EXTERNAL_EVENT
    |
    +--> remains here while reality remains unchanged
```

`WAIT_EXTERNAL_EVENT` is an ACTIVE HOLD, not idle, stuck, timeout, or permission to
"try something else".

## Active Hold Invariants

While `WAIT_EXTERNAL_EVENT` is active:

- no synthetic event may be fabricated;
- no historical receipt may be reused as current evidence;
- no workflow may be triggered merely to manufacture an observation;
- no alternate path may be created merely to bypass the blocked transition;
- no PASS state may be inherited from an earlier gate or earlier run;
- no action may be taken unless a new real external event is observed.

## Gate Semantics

For every forensic admission chain:

```text
GATE_N = PASS
```

means only:

```text
GATE_N+1 MAY BE EVALUATED
```

It does NOT mean:

```text
GATE_N+1 = PASS
```

and it never grants authority by inheritance.

## Database Admission Example

```text
DB_EXISTENCE
    |
    +-- PASS --> evaluate DB_BINDING
    |
    +-- FAIL --> DENY

DB_BINDING
    |
    +-- PASS --> evaluate DB_TLS_ADMISSION
    |
    +-- NOT_BOUND --> DENY

DB_TLS_ADMISSION
    |
    +-- PASS --> evaluate DB_ROUND_TRIP
    |
    +-- FAIL/UNKNOWN --> DENY

DB_ROUND_TRIP
    |
    +-- WRITE -> READ -> SHA256 MATCH --> promotion may be evaluated
    +-- otherwise --> DENY
```

A PASS at `DB_EXISTENCE` is never a PASS at `DB_BINDING`.
A PASS at `DB_BINDING` is never a PASS at `DB_ROUND_TRIP`.

## Authority Rule

```text
REALITY
  -> OBSERVATION
  -> EVIDENCE
  -> STATE TRANSITION
  -> ACTION
```

Never:

```text
BRAIN
  -> fabricate REALITY
```

The Brain is the governance/control plane. It can observe, validate, deny,
classify, record, and authorize transitions. It cannot manufacture the external
event required to justify a transition.

## Successor Bot Rule

If the successor sees:

```text
WAIT_EXTERNAL_EVENT
ACTION = NO-OP
```

it MUST preserve the state unless a new real external event is available.

The successor MUST NOT interpret this as a request to search for a workaround.

## Canonical Phrase

> The system is not stuck. Reality has not supplied the event required for the next transition.
> ACTIVE HOLD is therefore the correct action.
