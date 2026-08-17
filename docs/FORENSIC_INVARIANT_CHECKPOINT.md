# FORENSIC INVARIANT CHECKPOINT

## Authority
This document is a durable successor-AI checkpoint. It is not chat memory. Future Bots MUST read and preserve it before taking foundation actions.

## Brain role

```text
BRAIN = OBSERVER + VERIFIER + EXECUTOR
```

Brain is **NOT** a reality generator.

```text
BRAIN != REALITY GENERATOR
```

The chat window is only the communication interface. Persistent repository state, action logs, contracts, and forensic evidence are the durable authority.

## Canonical causal chain

```text
REALITY → EVIDENCE → STATE → TRANSITION → ACTION
```

Each arrow is a gated transition. No successor may collapse these stages into one inferred state.

## Forbidden shortcut

```text
BRAIN ✗ → EVENT
BRAIN ✗ → EVIDENCE
BRAIN ✗ → STATE CHANGE
```

Brain may observe, verify, and execute an already-authorized action. It may not manufacture the underlying event, evidence, or state transition.

## No-event invariant

```text
NO REAL EVENT
      ↓
NO EVIDENCE
      ↓
NO TRANSITION
      ↓
NO ACTION
      ↓
NO-OP (REQUIRED)
```

No trigger, no simulation presented as reality, no synthetic event, no inference used as substitute for missing evidence.

## Forensic database admission chain

Database existence, service binding, TLS admission, and durable round-trip are NOT interchangeable states.

```text
DB_EXISTENCE
    ↓ prerequisite only
DB_BINDING
    ↓ prerequisite only
DB_TLS_ADMISSION
    ↓ prerequisite only
DB_ROUND_TRIP
    ↓ prerequisite for promotion
PROMOTION
```

`PASS` at one gate NEVER implies `PASS` at the next gate.

Specifically:

```text
DATABASE EXISTS
    !=
SERVICE IS AUTHORIZED/BINDED
```

and:

```text
BOUND_TLS
    !=
DURABLE_EVIDENCE_PASS
```

The only promotion-grade database evidence is a real compact metadata-envelope write, read-back, and SHA-256 match observed through the authorized runtime path.

## Security analogy / corridor model

Every protected room has:

```text
CORRIDOR_KEY + ROOM_KEY
```

A protected/high-security room additionally requires an inner release:

```text
CORRECT CORRIDOR
    ↓
CORRECT ROOM KEY
    ↓
DOOR STILL LATCHED FROM INSIDE
    ↓
REQUEST / BELL
    ↓
INNER RELEASE
    ↓
ENTRY
```

Possessing a key never grants an implicit bypass of the inner latch.

## Invariant state at this checkpoint

```text
FOUNDATION = FROZEN
STATE      = WAIT_EXTERNAL_EVENT
ACTION     = NO-OP
FORENSIC   = INVARIANT
PROMOTION  = DENY
LAYER_1    = LOCKED
STAIRCASE  = LOCKED
```

## Successor rule

A successor Bot MUST:

1. Read this checkpoint and `state/current_state.json`.
2. Read `state/next_action.json`.
3. Continue from the recorded action ID, never from chat recollection alone.
4. Treat `UNKNOWN`, `NOT_PROVEN`, and missing evidence as **not PASS**.
5. Preserve the causal chain `REALITY → EVIDENCE → STATE → TRANSITION → ACTION`.
6. Preserve default-deny and no-op behavior when no real event exists.
7. Never fabricate credentials, events, evidence, source truth, or state changes.
8. Record every material action and its evidence before handing off to the next Bot.

## Final principle

> Brain may react to Reality. Brain must never replace Reality.
