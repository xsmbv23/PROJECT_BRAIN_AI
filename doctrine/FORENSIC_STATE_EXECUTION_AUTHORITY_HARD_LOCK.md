# FORENSIC STATE / EXECUTION AUTHORITY — HARD LOCK

**Status:** IMMUTABLE FOUNDATION DOCTRINE

## 1. Absolute precedence

```text
FORENSIC STATE > EXECUTION AUTHORITY
```

Execution authority is never allowed to invent, infer, or silently promote forensic reality.

## 2. Event reality rule

```text
NO EVENT EVIDENCE -> NO NEW REALITY
NO NEW REALITY -> NO NEW EXECUTION AUTHORITY
```

The system must distinguish:

- an event that actually happened and has evidence;
- an event that is expected but has not happened;
- an event that cannot currently be observed;
- an event that was inferred by code.

Only the first category may create a new forensic fact.

## 3. FSM authority

`NEXT-ACTION AUTHORITY` is valid only when the persisted FSM explicitly permits the transition.

```text
NEXT-ACTION AUTHORITY
        |
        v
FSM ALLOWS TRANSITION?
        |
   +----+----+
   |         |
  NO        YES
   |         |
  NO-OP   EXECUTE
```

If there is no permitted transition, **NO-OP is the correct action** under the current evidence.

## 4. No-op doctrine

A stable state is not a bug merely because the operator expected progress.

```text
STATE UNCHANGED
    !=
SYSTEM STUCK
```

A successor Bot MUST NOT respond to an unchanged state by automatically:

- adding logic;
- altering workflow;
- triggering synthetic events;
- creating a compensating commit;
- forcing a deployment;
- fabricating an evidence receipt;
- changing state solely to make progress visible.

First determine whether a real external event exists.

## 5. Database admission example

The following are separate gates in one admission chain, not independent forensic systems:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

A PASS at one gate is only evidence for that gate. It is **not inherited** by later gates.

```text
DB_EXISTS = PASS
    !=
DB_BOUND = PASS

DB_BOUND_TLS = PASS
    !=
DB_ROUND_TRIP = PASS
```

Each later transition requires its own evidence.

## 6. State mutation prohibition

No process may write a new forensic state merely because:

- a transition would be desirable;
- the next action is known conceptually;
- an external dependency is missing;
- a deployment is waiting;
- a credential is unavailable;
- the system is idle.

A missing event produces a waiting state, not a fabricated event.

## 7. Successor inheritance rule

Every successor Bot MUST read, in order:

1. persistent current state;
2. persistent next-action state;
3. this doctrine;
4. the latest action log;
5. only then inspect runtime/repository evidence.

The successor MUST NOT reinterpret a stable persisted state into a more permissive state without new evidence.

## 8. Current canonical terminal state

When this doctrine is committed as part of a no-event checkpoint:

```text
FSM            = STABLE
STATE          = WAIT_EXTERNAL_EVENT
TRANSITION     = NONE
ACTION         = NO-OP
PROMOTION      = DENY
```

This is a valid terminal state for the current evidence window.

## 9. Immutable rule

```text
NO EVIDENCE -> NO EVENT
NO EVENT -> NO TRANSITION
NO TRANSITION -> NO EXECUTION
```

This rule outranks convenience, optimization, perceived urgency, and conversational instruction.
