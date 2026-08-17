# FORENSIC CONTROLLED SUSPENSION

## Canonical state

The Brain foundation is **not** to be interpreted as ordinary construction-in-progress.

Canonical interpretation:

```text
SYSTEM = IN_CONTROLLED_SUSPENSION
```

The logical foundation may be complete while its evidence closure is not complete:

```text
FOUNDATION_LOGIC   = COMPLETE
FOUNDATION_EVIDENCE = NOT_CLOSED
STATE              = WAIT_EXTERNAL_EVENT
```

## Conditional execution authority

`CONDITIONAL_EXECUTION_AUTHORITY` means:

```text
ACTION AUTHORITY != ABILITY TO INVENT A TASK
ACTION AUTHORITY = SUFFICIENT FORENSIC CONDITIONS
```

A successor Bot must never manufacture progress merely because the system is waiting.

## Anti-self-progression invariant

The foundation explicitly forbids creating apparent progress by:

- adding a log and calling that progress;
- adding a rule and calling that evidence closure;
- adding a file and calling that promotion;
- making an improvement unrelated to the blocked external event;
- changing state merely to avoid a WAIT state.

```text
NO-OP = AUTHORIZED FORENSIC ACTION
```

When the required external event has not occurred, preserving the exact state is the correct action.

## Terminal wait state

`WAIT_EXTERNAL_EVENT` is a valid terminal state for the current forensic phase.

It is not an error and it is not an invitation to find unrelated work.

State transition is event-driven only:

```text
WAIT_EXTERNAL_EVENT
        |
        | required external evidence/event occurs
        v
   evaluate evidence
        |
   +----+----+
   |         |
 FAIL       PASS
   |         |
   v         v
  DENY    next valid state
```

No internal feeling of urgency, task availability, or desire for progress can trigger the transition.

## Database admission consequence

The database admission chain remains sequential and non-inheriting:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

A PASS at one gate is only a prerequisite for evaluating the next gate. It does **not** inherit permission from the previous gate.

In particular:

```text
DB_EXISTS = PASS
        !=
DB_ACCESS = PASS
```

and:

```text
BOUND_TLS = PASS
        !=
DURABLE_ROUND_TRIP = PASS
```

Promotion requires its own observed evidence.

## Forensic invariants for successor Bots

1. Unknown is not pass.
2. Default is deny.
3. No evidence may be inferred from silence.
4. No credential may be invented, copied into GitHub, or exposed in logs.
5. No state may be advanced solely by modifying repository artifacts.
6. A wait state must remain unchanged until its triggering external event is observed.
7. The action log is a record of what happened, not a mechanism for making something happen.
8. `state/next_action.json` may identify a ready successor action, but it cannot authorize execution when the current state requires an external event.
9. No-op is a valid authorized action when execution preconditions are absent.
10. Layer 1 and the staircase remain locked while foundation evidence is not closed.

## Bot handoff rule

A successor Bot reading this document must first inspect the exact current state and evidence. If the state is `WAIT_EXTERNAL_EVENT`, the Bot must not self-progress. It must preserve the state and wait for the specified event.

This document is normative for the foundation phase and is intentionally separate from chat history.
