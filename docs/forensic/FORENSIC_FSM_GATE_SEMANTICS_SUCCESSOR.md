# Successor Doctrine — One Forensic FSM

This is a permanent handoff contract for every future Bot.

## Non-negotiable rule

> **A PASS belongs only to the gate that earned it. PASS only permits evaluation of the next gate. PASS never transfers, propagates, or inherits to another gate.**

There is exactly ONE Forensic FSM. Database admission, runtime action admission, and source/data admission are chains inside that FSM.

## State interaction

A gate transition is valid only when:

```text
CURRENT_GATE
   |
   | own evidence receipt
   v
PASS_LOCAL
   |
   | prerequisite only
   v
NEXT_GATE_EVALUATION
```

Never:

```text
Gate A PASS -> Gate B PASS
```

Instead:

```text
Gate A PASS
   -> permission to CHECK B
   -> B gathers B-owned evidence
   -> B decides its own state
```

## Database example

```text
DB_EXISTENCE=PASS
    != DB_BINDING=PASS
    != SECRET_RESOLUTION=PASS
    != DB_TLS_ADMISSION=PASS
    != NETWORK_ORIGIN_PROOF=PASS
    != DB_ROUND_TRIP=PASS
    != PROMOTION=PASS
```

Each is a separate admission gate in one FSM.

## Why this matters

A healthy database, healthy runtime, successful startup, historical receipt, or another subsystem's PASS can never be used as a substitute for the missing evidence of the current gate.

Historical evidence can prove what happened historically. It cannot by itself prove exact-current admission.

## Current runtime action track

When `state/next_action.json` says `READY_WAIT`, `ACTION_SPACE=0`, and `MANDATORY_NO_OP=true`, the Bot MUST NOT manufacture an observation to escape the wait state.

It may only perform the actions explicitly listed as allowed foundation actions. The next action must remain unchanged until the required independent external event exists.

## Successor boot order

Every future Bot MUST:

1. Read `state/current_state.json`.
2. Read `state/next_action.json`.
3. Read this document.
4. Read the canonical Forensic FSM document.
5. Treat repository state as authoritative for what has actually been proven.
6. Treat unknown/missing evidence as `NOT_PROVEN`, never as PASS.
7. Preserve historical receipts; never rewrite them to make a later decision green.
8. Do not unlock a room, staircase, Layer 1, or promotion gate without the exact evidence required by that gate.

## Current canonical baseline

At the time of this handoff:

```text
N116 = READY_WAIT
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
ACTION_RECEIPT = NOT_YET_PROVEN_CURRENT
```

The runtime has independently recorded:

```text
runtime_tests = 209
foundation = PASS
db_binding = BOUND_TLS
db_tls = PASS
network_origin = PASS
db_round_trip = PASS
promotion = DENY
```

But the exact-current external `/governance` action receipt remains unproven. Therefore the runtime action gate remains DENY.

## Absolute prohibition

No future Bot may say:

> "Another gate passed, therefore this gate is probably safe."

That sentence violates the Forensic foundation.

The only valid reasoning is:

> "The previous gate passed, therefore I am permitted to evaluate the next gate using that next gate's own evidence." 
