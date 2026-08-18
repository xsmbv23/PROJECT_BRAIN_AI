# FORENSIC FSM — ADMISSION SEMANTICS V1

## Purpose

This document is a durable inheritance contract for every future Brain AI successor.
It prevents a successor from treating separate evidence gates as independent Forensic systems or from inheriting PASS from one gate into another.

## One Forensic FSM only

There is exactly **one** Forensic admission state machine for durable database admission:

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
SECRET_RESOLUTION
    ↓
DB_TLS_ADMISSION
    ↓
NETWORK_ORIGIN_PROOF
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
    ↓
DATA_ADMISSION
    ↓
RESEARCH_ADMISSION
    ↓
EDGE / EVIDENCE ANALYSIS
    ↓
REPORTING
```

These are sequential gates in one chain. They are not separate Forensic state machines.

## Local PASS rule

A PASS belongs only to the gate that produced it.

```text
PASS(A)
  ↓
permits evaluation of B
  ↓
B must obtain its own evidence
  ↓
PASS(B)
```

Therefore:

```text
PASS(A) ≠ PASS(B)
PASS(A) does not inherit
PASS(A) does not authorize downstream action
```

A previous PASS is a **prerequisite**, never a downstream PASS.

## Unknown and deny

```text
UNKNOWN = NOT PASS
DEFAULT  = DENY
```

Absence of an error is not evidence of PASS.
An old deployment description cannot override exact-current runtime evidence.
A hypothesis cannot satisfy a gate.

## Evidence → State → Action

Every transition must follow:

```text
OBSERVABLE EVIDENCE
        ↓
FORENSIC STATE
        ↓
ALLOWED ACTION SPACE
```

Never:

```text
DESIRED ACTION → assume state → manufacture evidence
```

## Database admission meanings

### DB_EXISTENCE
Confirms that the database resource exists and is available as an infrastructure object.

It does **not** imply service access.

### DB_BINDING
Confirms that the service has a binding/key path to the database.

It does **not** imply successful network access.

### SECRET_RESOLUTION
Confirms the secret is resolved through the approved runtime secret mechanism.

Credentials must never be stored in GitHub, source files, action logs, or forensic evidence.

### DB_TLS_ADMISSION
Confirms the resolved PostgreSQL connection uses an explicitly accepted TLS mode.

Accepted modes are contract-defined; anything else is DENY.

### NETWORK_ORIGIN_PROOF
Confirms the actual service-to-database network path/origin is proven by exact-current runtime evidence.

This is the current blocking gate in the frozen foundation state.

No synthetic probe, workaround, alternate route, or guessed network event may satisfy it.

### DB_ROUND_TRIP
Requires a real compact metadata envelope:

```text
WRITE → READ → SHA-256 MATCH
```

An in-memory round-trip is not durable PostgreSQL evidence.

### PROMOTION
Only the successful DB_ROUND_TRIP may satisfy the durable evidence promotion condition.

## Reporting boundary

```text
REPORTING ≠ AUTHORIZATION
PREDICTION ≠ EXECUTION
EV EVIDENCE ≠ ACTION AUTHORIZATION
```

The reporting layer can describe state/evidence but can never promote itself or authorize upstream/downstream actions.

## Edge rule

Every transition/edge must identify:

- source state
- target state
- observable evidence supporting the transition
- exact current evidence timestamp/identity where applicable

Unknown edge = DENY.

## Current frozen state

At the time this contract was written:

```text
FOUNDATION             = FROZEN
STATE                  = WAIT_EXTERNAL_EVENT
ACTION_SPACE           = 0
ACTION                 = MANDATORY_NO_OP
NETWORK_ORIGIN_PROOF   = NOT_PROVEN
DB_ROUND_TRIP           = NOT_PROVEN
PROMOTION              = DENY
DATA_ADMISSION         = LOCKED
RESEARCH_ADMISSION     = LOCKED
EVIDENCE_ANALYSIS      = LOCKED
REPORTING              = LOCKED
LAYER_1                = LOCKED
STAIRCASE              = LOCKED
```

The exact-current repository state remains authoritative. Do not advance the FSM merely because this document exists.

## Mandatory successor behavior

When the FSM is `MANDATORY_NO_OP`:

1. observe exact-current evidence;
2. wait for the required external event;
3. update forensic documentation if needed;
4. do not create the missing external event;
5. do not bypass the gate;
6. do not open Layer 1 or the staircase;
7. do not reinterpret an infrastructure PASS as an authorization PASS.

**The correct action while waiting is intentional no-op.**
