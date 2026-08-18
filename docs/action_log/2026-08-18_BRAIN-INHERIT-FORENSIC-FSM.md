# BRAIN-INHERIT — Forensic FSM inheritance rule

This is a documentation-only successor handoff. It does not change runtime state or unlock any gate.

## Non-negotiable inheritance

A future Bot AI must understand that there is **one Forensic FSM**, not multiple independent Forensic systems.

The database admission chain is:

`DB_EXISTENCE → DB_BINDING → SECRET_RESOLUTION → DB_TLS_ADMISSION → NETWORK_ORIGIN_PROOF → DB_ROUND_TRIP → PROMOTION`

Each PASS is local to its own gate.

```text
PASS(A) → may evaluate B
PASS(A) → does NOT equal PASS(B)
PASS(A) → does NOT authorize downstream action
```

Every downstream gate needs its own observable evidence.

## Current handoff

The exact-current state is frozen at `MANDATORY_NO_OP` because `NETWORK_ORIGIN_PROOF = NOT_PROVEN`.

No action may be invented to create this missing external event.

The next permitted transition is only the externally evidenced transition:

`NETWORK_ORIGIN_PROOF: NOT_PROVEN → PASS`

After that, and only after that, the successor may evaluate `DB_ROUND_TRIP`.

## Forensic safety

- UNKNOWN is not PASS.
- DEFAULT is DENY.
- Old deployment descriptions do not outrank exact-current evidence.
- Reports do not authorize actions.
- Predictions do not execute actions.
- EV evidence does not authorize actions.
- Layer 1 remains LOCKED.
- Staircase remains LOCKED.
- Credentials remain forbidden in GitHub and forensic evidence.

This record exists so the next Bot does not repeat the previously identified planning error of jumping directly to Promotion.
