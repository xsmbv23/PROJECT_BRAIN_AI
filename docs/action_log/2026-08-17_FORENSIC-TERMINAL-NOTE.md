# FORENSIC TERMINAL NOTE — 2026-08-17

This note is a durable successor instruction.

The current foundation is frozen and waiting for a real external event. The system is not incomplete merely because no action is available.

Canonical rule:

```text
NO REAL EVENT
→ NO EVIDENCE
→ NO STATE CHANGE
→ NO ACTION
→ NO-OP
```

Authority hierarchy:

```text
REALITY AUTHORITY > BRAIN AUTHORITY
```

Database admission is one Forensic FSM:

```text
DB_EXISTENCE → DB_BINDING → DB_TLS_ADMISSION → DB_ROUND_TRIP → PROMOTION
```

Critical invariant:

```text
PASS(Gn) NEVER IMPLIES PASS(Gn+1)
```

A gate PASS is local evidence only. It does not inherit into the next gate.

The Brain must never generate its own justification, manufacture an external event, overwrite historical evidence, or create work solely because the system is idle.

Current phase terminal state:

```text
CAPABILITY = COMPLETE
AUTHORITY = ZERO
CONTROL = PRESERVED
STATE = WAIT_EXTERNAL_EVENT
ACTION = NO-OP
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

Successor Bots must read this note together with `state/current_state.json` and `state/next_action.json` before taking any action.
