# FORENSIC TERMINAL BOUNDARY — CURRENT FOUNDATION PHASE

## Authority

`REALITY AUTHORITY > BRAIN AUTHORITY`

Brain is the governance/control plane. The chat window is only a communication interface. Persistent repository state and persistent evidence are authoritative.

## Terminal semantics

When the current phase has no real external event that can legitimately advance state:

```text
CAPABILITY = COMPLETE
AUTHORITY  = ZERO
CONTROL    = PRESERVED
STATE      = CLOSED
```

Canonical state:

```text
WAIT_EXTERNAL_EVENT
```

This is a valid terminal state for the current phase. It is NOT equivalent to `pending`, `incomplete`, or `blocked`.

The only valid action while the required external event is absent is:

```text
NO REAL EVENT
    ↓
NO EVIDENCE
    ↓
NO STATE CHANGE
    ↓
NO ACTION
    ↓
NO-OP
```

The system MUST NOT create work merely because it is idle.

## One Forensic FSM

The database admission chain is one forensic finite-state machine, not multiple independent forensic systems:

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

Each gate owns only its own evidence.

### Non-inheritance rule

```text
PASS(Gn) NEVER IMPLIES PASS(Gn+1)
```

A PASS is local to its gate and is only a prerequisite for evaluating the next gate. No state may be promoted by inference.

Examples:

```text
DB_EXISTS = PASS
≠
DB_BINDING = PASS
```

```text
DB_BINDING = PASS
≠
DB_TLS_ADMISSION = PASS
```

```text
DB_TLS_ADMISSION = PASS
≠
DB_ROUND_TRIP = PASS
```

Only an actual compact metadata write/read with SHA-256 match may prove the round-trip gate. Only the completed admission chain can permit promotion.

## Evidence transition rule

```text
EVIDENCE → STATE → ACTION
```

Never:

```text
INTENT → STATE
INTENT → EVIDENCE
IDLE → ACTION
```

External events cannot be manufactured by Brain, by chat, by a retry, or by a cosmetic code change.

## Immutability

- Existing forensic receipts are never overwritten.
- A retry is a new event and must produce a new receipt.
- `FAIL` is evidence; it is not permission to erase or reinterpret history.
- `UNKNOWN` is not PASS.
- Default is DENY.
- Promotion remains DENY unless the exact required evidence exists.

## Current foundation boundary

```text
FORENSIC = INVARIANT
FOUNDATION = FROZEN
STATE = WAIT_EXTERNAL_EVENT
ACTION = NO-OP
PROMOTION = DENY
LAYER 1 = LOCKED
STAIRCASE = LOCKED
```

The next action may be defined in persistent state for a future external event, but it MUST NOT execute until that event actually occurs.
