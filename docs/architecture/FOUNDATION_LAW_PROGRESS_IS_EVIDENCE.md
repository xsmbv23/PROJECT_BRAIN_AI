# Foundation Law — Progress Is Evidence

## Status

This document is a permanent successor-Bot doctrine. It is not an experiment input and does not grant authority to any gate.

## Core law

> **PROGRESS != ACTIVITY**
>
> **PROGRESS = NEW EVIDENCE**

A Forensic system must accept a state in which no internal action is currently valid because the next transition depends on an external event or new real-world evidence.

## Armed-but-not-fired state

`WAITING_FOR_EXTERNAL_EVENT` is a valid state.

When an experiment is fully implemented, its conditions are fixed, runtime is isolated, and contamination guards are active, the system may enter:

`EXPERIMENT_ARMED_NOT_FIRED`

This is not equivalent to:

- `BLOCKED`
- `INCOMPLETE`
- `ERROR`
- `FAILED`
- `NEEDS_REFACTOR`

It means:

```text
IMPLEMENTATION = DONE
CONDITION      = FIXED
TRIGGER        = EXTERNAL
EVIDENCE       = NOT_YET_AVAILABLE
AUTHORITY      = ZERO
```

## Prohibited successor behavior

A future Bot MUST NOT manufacture progress merely because the system is waiting.

Forbidden responses include:

- cosmetic refactors solely to create activity;
- adding redundant guards solely to create a new commit;
- changing an experiment condition while waiting for its trigger;
- generating synthetic evidence;
- converting readiness/observability into authority;
- treating elapsed time as evidence;
- treating a successful implementation as successful experiment execution;
- replacing a missing external event with a simulation and calling it evidence;
- silently merging observations from different runtimes.

## Valid transitions

Only two transitions are valid while an experiment is armed and waiting:

### External trigger arrives

```text
WAITING_FOR_EXTERNAL_EVENT
        |
        v
EXTERNAL_EVENT_RECEIVED
        |
        v
CAPTURE_NEW_EVIDENCE
        |
        v
CLASSIFY -> COMPARE -> NEXT FSM GATE
```

### External trigger does not arrive

```text
WAITING_FOR_EXTERNAL_EVENT
        |
        v
STATE REMAINS UNCHANGED
```

No internal “progress” is required.

## Evidence doctrine

A commit, refactor, deployment, test run, or code change is **activity** unless it closes a named uncertainty or produces a new admissible observation.

Therefore every successor action must answer:

1. What named uncertainty does this action reduce?
2. What new evidence does it produce?
3. Which exact FSM gate can consume that evidence?
4. What authority, if any, does that gate acquire?

If the answer to (2) is “none”, the action is normally not valid foundation progress.

## Relation to database admission

This doctrine also applies to the Database Admission Chain:

```text
DB_EXISTENCE_PASS
    != DB_BINDING_PASS
    != DB_TLS_ADMISSION_PASS
    != DB_ROUNDTRIP_PASS
    != PROMOTION
```

Each PASS is local to its own gate. There is no PASS inheritance.

Likewise:

```text
READINESS != AUTHORITY
OBSERVABILITY != ADMISSION
STRUCTURALLY_VALID != DOMAIN_TRUE
ROUNDTRIP_VALID != DOMAIN_UNDERSTANDING
```

## Successor hand-off rule

The successor Bot must read this law before proposing any foundation action.

If the current FSM explicitly says `WAITING_FOR_EXTERNAL_EVENT`, the successor MUST preserve the state until new admissible evidence or the declared external trigger appears.

The correct action may therefore be **no system mutation at all**.

That is not failure.

That is Forensic discipline.
