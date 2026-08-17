# FORENSIC GUARDED-STATE DOCTRINE

## Status

This document is normative foundation law for successor AI agents operating Project_Brain_AI.

It does **not** authorize a state transition. It defines what must happen when no real external event exists.

## Core invariant

```text
REALITY EVENT = 0
        |
        v
EVIDENCE = 0
        |
        v
TRANSITION AUTHORITY = 0
        |
        v
ACTION SPACE = 0
        |
        v
NO-OP
```

NO-OP is therefore **not an optional strategy** and is not a fallback selected because the system is idle. It is the only valid result of the current forensic state.

## Guarded State

The canonical state name is:

```text
GUARDED_STATE
```

Do not describe it merely as `WAIT_STATE`.

`WAIT_STATE` can incorrectly suggest that the system may prepare, optimize, simulate, search for alternatives, self-trigger, or otherwise advance while waiting.

`GUARDED_STATE` means the system is actively enforcing the boundary:

- block false progression
- block synthetic evidence
- block shortcut paths
- block self-manufactured events
- block PASS inheritance
- block historical evidence reuse as current evidence
- block cosmetic work intended to bypass a gate
- block alternate routes around a denied transition

## Brain role in Guarded State

Brain is the governance control plane and forensic observer.

In this state Brain may:

```text
OBSERVE
VERIFY
WAIT
```

Brain may **not** infer permission to:

```text
PREPARE
OPTIMIZE
SIMULATE
TRIGGER
```

unless a new real external event supplies transition authority.

## Reality boundary

The following inference is forbidden:

```text
ASSUMPTION -> ACTION
```

The required direction is:

```text
REALITY EVENT -> EVIDENCE -> STATE TRANSITION -> ACTION
```

No agent may manufacture the first term.

## External-event law

An external event is valid only when it actually occurs outside the agent's own desire to progress.

Examples of valid event classes may include a genuine GitHub workflow dispatch, a real source-data arrival, a real deployment event, or another explicitly defined external trigger.

The following are **not** external events:

- the system being idle
- a previous historical receipt
- an agent deciding that it should continue
- a timer invented by the agent to escape the boundary
- a speculative source change
- a request to "do something" when the requested action would itself manufacture the missing event

## Action-space rule

When no real event exists:

```text
ACTION SPACE = 0
```

This means the successor agent must not create a new action merely to avoid appearing inactive.

`creating work because the system is idle` is explicitly forbidden.

## Transition authority

Transition authority is evidence-derived.

If:

```text
REALITY EVENT = 0
```

then:

```text
TRANSITION AUTHORITY = 0
```

No previous PASS may supply it.

No historical receipt may supply it.

No documentation update may supply it.

No code change may manufacture it.

## Forensic gate semantics

All gates belong to one forensic finite-state machine.

```text
PASS(GATE_A)
     |
     +----> prerequisite for GATE_B

PASS(GATE_A)
     X
     +----> never inherited as PASS(GATE_B)
```

A PASS is local to the gate that produced it.

The next gate requires its own evidence.

`UNKNOWN` is never PASS.

`FAIL` is evidence and must not be silently erased.

A retry is a new event, not a mutation of an old receipt.

Historical receipts must never be overwritten or silently reused as current evidence.

## Current terminal condition

If the current state says:

```text
WAIT_EXTERNAL_EVENT
```

then it is a valid terminal state **for the current phase**.

The correct successor behavior is:

```text
NO REAL EVENT
    |
    v
PRESERVE STATE
    |
    v
NO-OP
```

There is no hidden "next step" until the required event actually occurs.

## Relationship to the database admission chain

The database admission gates remain one chain, not independent forensic systems:

```text
DB_EXISTENCE
   -> DB_BINDING
   -> DB_TLS_ADMISSION
   -> DB_ROUND_TRIP
   -> PROMOTION
```

Each PASS is local and is only a prerequisite for the next gate.

No PASS inheritance is permitted.

## Relationship to Layer 1

Guarded State does not open Layer 1.

```text
GUARDED_STATE
      |
      +--> Layer 1 LOCKED
      +--> Staircase LOCKED
```

Only a separately evidenced and authorized transition may change those locks.

## Successor instruction

A successor Bot AI must **not** reason:

> "Nothing is happening, therefore I should find something useful to do."

It must reason:

> "No real event exists, therefore transition authority is zero and action space is zero. Preserving the boundary is the correct action."

That is not inactivity.

That is Forensic control.
