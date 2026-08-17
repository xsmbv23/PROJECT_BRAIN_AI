# REALITY-BOUNDARY-FREEZE

## Action

`REALITY-BOUNDARY-FREEZE`

## Purpose

Preserve the system rule that a missing external event is a valid forensic state and must not be converted into a synthetic success.

## Frozen invariants

```text
FSM = SINGLE / LOCKED
PASS = LOCAL_TO_GATE
PASS_INHERITANCE = FORBIDDEN
UNKNOWN = NOT_PASS
DEFAULT = DENY
EXTERNAL_EVENT_CANNOT_BE_MANUFACTURED
WAIT_EXTERNAL_EVENT = VALID
READINESS = OBSERVABILITY_ONLY
READINESS != AUTHORITY
ROUNDTRIP_VALID != DOMAIN_TRUE
STRUCTURALLY_VALID != DOMAIN_TRUE
SINGLE_RECEIPT != DOMAIN_UNDERSTANDING
```

## Gate chain

```text
EXISTENCE
  -> BINDING
  -> TLS_ADMISSION
  -> ROUND_TRIP
  -> PROMOTION
```

Each gate emits its own evidence. A PASS at one gate only authorizes evaluation of the next gate. A PASS never inherits permission from an earlier gate.

## Next-action authority

The standing permission to take the next action is **CONDITIONAL_EXECUTION_AUTHORITY**.

It is NOT:

`ALWAYS_DO_SOMETHING`.

An automatic action is authorized only when it:

1. closes a named invariant with evidence;
2. obtains real missing evidence through an allowed control surface; or
3. restores an already-defined invariant after a detected violation.

Every action must name the gate or invariant it affects.

## NO-OP rule

If no authorized action exists for the current evidence set, the correct outcome is:

`NO-OP`

`NO ACTION = CORRECT`.

NO-OP is not laziness and is not failure. It is a valid terminal state for the current evidence boundary.

## External-event boundary

Do not interpret a WAIT state as a bug simply because no more automatic work is possible.

Do not:

- fabricate a receipt;
- manufacture a workflow_dispatch event;
- substitute browser data for runtime data;
- silently switch execution runtime while keeping the same source identity;
- weaken a gate to obtain PASS;
- invent a cosmetic hardening task merely to create activity;
- unlock Layer 1 because the system has been waiting for a long time.

Correct transition:

`WAIT_EXTERNAL_EVENT`
→ `BLOCK SYSTEM ADVANCEMENT`
→ `PRESERVE INTEGRITY`

## Current implication

The system may be fully implemented up to the available reality boundary while remaining `WAIT_EXTERNAL_EVENT`.

That is a correct terminal state until the required external evidence exists.

## Successor warning

The next action record must explicitly contain either:

- an authorized concrete action, or
- `WAIT_EXTERNAL_EVENT`, or
- `NO-OP`.

A successor must never treat an empty queue as permission to invent work.
