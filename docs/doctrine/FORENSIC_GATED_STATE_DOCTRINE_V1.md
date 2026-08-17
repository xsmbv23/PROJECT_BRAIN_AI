# FORENSIC GATED STATE DOCTRINE V1

## Purpose

This document is a successor-bot authority document for the XSMB_FORENSIC Brain foundation. It defines how forensic database admission states interact without allowing implicit progress.

## One state machine, not multiple forensic systems

Database admission is ONE FORENSIC FSM. The gates are sequential evidence gates inside the same state machine:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

A gate's PASS is local to that gate.

```text
PASS(Gn)
   => permits evaluation of Gn+1
   != PASS(Gn+1)
```

There is no `ASSUME_PASS`, `CHAIN_PASS`, `IMPLICIT_PASS`, or inherited PASS.

## Evidence semantics

Each transition requires evidence appropriate to that exact transition.

```text
REALITY_EVENT
    -> EVIDENCE
    -> STATE
    -> ACTION
```

No real external event may be manufactured by Brain, a test, a simulator, a chat message, or a successor bot.

No evidence may be synthesized from understanding, expectation, previous PASS, database existence, or silence.

## Current sealed state

```text
STATE                = WAIT_EXTERNAL_EVENT
MODE                 = GUARDED_STATE
REALITY_EVENT        = 0
EVIDENCE             = 0
TRANSITION_AUTHORITY = 0
ACTION_SPACE         = 0
ACTION               = NO-OP
PROMOTION            = DENY
LAYER_1              = LOCKED
STAIRCASE            = LOCKED
FORENSIC             = INVARIANT
```

`WAIT_EXTERNAL_EVENT` is not an ordinary pause. It is an actively protected terminal state for the current phase.

The system must prevent invalid transitions while waiting.

## GUARDED_STATE rules

While `GUARDED_STATE` is active, Brain must:

- OBSERVE
- VERIFY
- WAIT
- preserve state immutability
- reject fabricated events
- reject synthesized evidence
- reject PASS inheritance
- reject gate shortcuts
- reject pre-execution
- reject simulated progress
- reject optimization that changes state

Brain must NOT:

- PREPARE a future action as if authorized
- OPTIMIZE toward an anticipated transition
- SIMULATE a transition and treat it as real
- PRE-EXECUTE any protected action
- manufacture an external event

## Database gate semantics

```text
Database exists?
      |
      +-- NO  -> DENY
      |
      +-- YES -> evaluate binding

Binding exists?
      |
      +-- NO  -> NOT_BOUND / DENY
      |
      +-- YES -> evaluate TLS

TLS admissible?
      |
      +-- NO  -> DENY
      |
      +-- YES -> BOUND_TLS; evaluate round-trip

Round-trip:
compact metadata WRITE
      -> READ
      -> SHA-256 MATCH?

      +-- NO  -> DENY
      +-- YES -> durable evidence admission may PASS
```

Important:

```text
DATABASE EXISTS != DATABASE ACCESS
DATABASE ACCESS != TLS ADMISSION
TLS ADMISSION != ROUND-TRIP PROOF
ROUND-TRIP PROOF != arbitrary permission
```

Every transition is independently evidenced.

## Authority hierarchy

The chat window is not the authority for state.

```text
Repository state + persistent forensic evidence
                    |
                    v
              Brain governance
                    |
                    v
              communication UI
```

A successor bot must read persistent state and action history before interpreting the chat conversation.

## Immutability

The successor must never rewrite history to make the current state appear cleaner. Corrections are append-only action records or explicit state transitions with evidence.

A failed or DENIED gate remains historically true even after a later gate passes.

## Successor rule

When a successor bot starts:

1. Read `state/current_state.json`.
2. Read `state/next_action.json`.
3. Read the latest action log.
4. Verify the state hash/commit context where available.
5. Determine whether a REAL external event exists.
6. If no real event exists, execute NO-OP and do not create progress.
7. If an event exists, create evidence for that event before any state transition.
8. Never infer PASS from prior PASS.
9. Never unlock Layer 1 or the staircase merely because the foundation is understood.

## Non-negotiable invariant

```text
UNDERSTANDING -> ACTION     = FORBIDDEN

REAL EVENT -> EVIDENCE
EVIDENCE -> STATE
STATE -> AUTHORIZED ACTION
```

The purpose is not to make the system appear active. The purpose is to prevent an incorrect transition from ever becoming historical truth.
