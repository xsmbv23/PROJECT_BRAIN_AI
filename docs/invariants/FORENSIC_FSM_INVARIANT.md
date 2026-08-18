# FORENSIC FSM INVARIANT — SEALED

## Canonical rule

`ONE_FORENSIC_FSM = TRUE`

There is one canonical Forensic state machine. Database admission gates are not separate Forensic machines.

## Gate locality

`PASS_IS_LOCAL_TO_GATE`

A PASS belongs only to the gate that produced the evidence.

`NO_PASS_INHERITANCE`

A PASS from gate N never becomes a PASS for gate N+1 by implication.

`UNKNOWN_IS_NOT_PASS`

Missing, silent, unavailable, or ambiguous evidence is not PASS.

`DEFAULT = DENY`

Any unproven transition is denied.

## Database admission chain

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
```

The arrows mean **prerequisite ordering**, not state inheritance.

Forbidden:

```text
PASS(Gn) → PASS(Gn+1)
```

Required:

```text
Evidence(Gn+1) → PASS(Gn+1)
```

## External event authority

The runtime may not manufacture an external event.

```text
REAL_GITHUB_WORKFLOW_DISPATCH
        ↓
fresh runtime receipt
        ↓
EVIDENCE > 0
        ↓
TRANSITION AUTHORITY
```

Until that real event is observed:

```text
STATE        = WAIT_EXTERNAL_EVENT
MODE         = ACTIVE_HOLD
REAL_EVENT   = NOT_OBSERVED
EVIDENCE     = NONE
TRANSITION   = NONE
AUTHORITY    = NONE
ACTION_SPACE = 0
ACTION       = NO-OP
```

## Forensic consequence

The system must not:

- invent evidence;
- infer a transition from silence;
- inherit PASS across gates;
- prepare an action merely because an action may be useful later;
- unlock Layer 1 or the staircase without the canonical transition authority.

## Immutable successor rule

A future Bot must read this document before modifying the foundation. If a proposed change contradicts this invariant, the proposed change is DENIED unless the invariant itself is explicitly and forensically superseded by a new sealed governance decision.
