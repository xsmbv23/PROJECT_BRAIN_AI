# Forensic DB Admission Chain — Canonical Invariant

## Purpose

This document is canonical successor guidance for the database admission model.

There is **ONE** Forensic state machine (FSM), not multiple independent Forensic systems.
Database existence, service binding, TLS admission, and durable round-trip are sequential gates inside the same FSM.

## Core invariant

```text
PASS_IS_LOCAL_TO_GATE
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
```

A PASS at Gate N never becomes PASS at Gate N+1.
It only authorizes evaluation of Gate N+1.

## Admission chain

```text
DB_EXISTENCE
    |
    | PASS only proves the database resource exists
    v
DB_BINDING
    |
    | PASS only proves the service has an explicit binding
    v
DB_TLS_ADMISSION
    |
    | PASS only proves the binding satisfies TLS policy
    v
DB_ROUND_TRIP
    |
    | PASS requires real compact metadata WRITE -> READ -> SHA-256 MATCH
    v
PROMOTION
```

At every edge:

```text
FAIL / UNKNOWN -> DENY
```

## Important distinction

These are **not two Forensic states**:

```text
DATABASE_EXISTS
SERVICE_BOUND
```

They are two gates in one Forensic FSM.

`DATABASE_EXISTS=PASS` means:

> The secured room exists.

It does **not** mean:

> The service possesses the key.

`SERVICE_BOUND=PASS` means the service has an explicit binding, but it still does not prove that TLS admission or a durable evidence round-trip succeeds.

## Interaction with the security metaphor

```text
corridor_key
    -> permits reaching the room

room_key
    -> permits presenting credentials for the room

inner_latch / protected-room release
    -> permits high-security entry

DB_EXISTENCE
    -> confirms the room actually exists

DB_BINDING
    -> confirms the service has the room's key

DB_TLS_ADMISSION
    -> confirms the key is being used through an accepted secure channel

DB_ROUND_TRIP
    -> confirms actual controlled entry and evidence integrity
```

The security layers must never be collapsed.

## State transition law

The global Brain law remains:

```text
EVIDENCE -> STATE -> ACTION
```

Never:

```text
STATE -> ACTION
```

Therefore:

```text
DB_EXISTS=PASS
    != DB_BINDING=PASS
    != DB_TLS=PASS
    != DB_ROUND_TRIP=PASS
    != PROMOTION=PASS
```

## External-event boundary

The current system is frozen at:

```text
STATE        = WAIT_EXTERNAL_EVENT
MODE         = ACTIVE_HOLD
EVIDENCE     = NONE
TRANSITION   = NONE
AUTHORITY    = NONE
ACTION_SPACE = 0
ACTION       = NO-OP
```

A successor bot MUST NOT create a workaround, retry, synthetic event, alternate path, or cosmetic change merely because the system is waiting.

Only:

```text
REAL_GITHUB_WORKFLOW_DISPATCH
    -> fresh runtime receipt
    -> EVIDENCE > 0
    -> transition authority
```

can change the state.

## Immutability rule

Historical receipts are immutable.
A new execution is a new event and must create a new receipt.
No historical receipt may be overwritten and no PASS may be inherited from a previous run.

## Promotion rule

Even a real GitHub Actions receipt does not itself prove domain truth.
It proves only the transport/runtime gate covered by that receipt.
Domain truth and Layer 1 promotion remain separately gated.

## Successor instruction

Read this file before modifying any database admission code.
If a proposed change weakens any of the invariants above, reject the change.
