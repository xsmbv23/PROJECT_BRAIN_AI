# ACTIVE_HOLD_DOCTRINE — Forensic Invariant

## Authority

This document is a durable successor-facing doctrine. It records a semantic invariant, not an instruction to manufacture work.

## Core invariant

```text
BRAIN != REALITY GENERATOR
```

The Brain may observe reality, validate evidence, preserve state, and wait for a transition-authorizing external event. It must never manufacture the external event, evidence, cause, or justification for its own transition.

## ACTIVE_HOLD

```text
WAIT_EXTERNAL_EVENT = ACTIVE_HOLD
```

ACTIVE_HOLD is:

- not IDLE;
- not STUCK;
- not FAILED;
- not an unfinished internal task.

During ACTIVE_HOLD the system remains observable, state-valid, transition-ready, and prohibited from creating the cause of transition.

Therefore:

```text
NO TRANSITION AUTHORITY
        ->
NO STRUCTURAL CHANGE
```

Preparatory refactors, speculative hardening, cosmetic YAML changes, extra logging, or other internal work must not be performed merely because an external event has not happened yet.

## Forensic admission chain

Database admission is ONE forensic state machine composed of independent evidence gates:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Each gate proves only a local fact.

```text
PASS(Gn) = local evidence for Gn
PASS(Gn) != inherited permission for Gn+1
```

There is explicitly **NO PASS INHERITANCE**.

Examples:

```text
DB_EXISTS = PASS
    does not imply
DB_BINDING = PASS
```

```text
BOUND_TLS = PASS
    does not imply
DB_ROUND_TRIP = PASS
```

```text
DB_ROUND_TRIP = PASS
    is the evidence required before promotion may be considered
```

`UNKNOWN` is never `PASS`. The default is `DENY`.

## Transition law

```text
EVIDENCE -> STATE -> ACTION
```

Never:

```text
CAPABILITY -> ACTION -> EVIDENCE
```

because that would allow the system to manufacture evidence that validates its own action.

## Phase-terminal semantics

When the current phase reaches:

```text
WAIT_EXTERNAL_EVENT
```

that is a valid terminal state for the current phase.

There is no hidden internal `next step` to execute.

The only valid future transition authority is:

```text
EXTERNAL REALITY HAPPENS
```

or the system remains correct and waiting.

## Successor-Bot prohibition

A successor Bot must not interpret these as reasons to continue modifying the system:

- "we should harden more";
- "we should refactor first";
- "we should optimize YAML";
- "we should add logging just in case";
- "we should create a workaround";
- "we should make the gate green".

If no transition-authorizing evidence exists, such activity is drift.

## Current sealed state

```text
foundation = FROZEN
state = WAIT_EXTERNAL_EVENT
action = NO-OP
promotion = DENY
layer_1 = LOCKED
staircase = LOCKED
forensic = INVARIANT
next_action = NONE_UNTIL_EXTERNAL_EVENT
sealed = true
```

The current persistent state is authoritative. This document does not override it; it explains why it must remain unchanged until reality supplies the required event/evidence.
