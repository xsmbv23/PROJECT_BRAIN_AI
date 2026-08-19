# FORENSIC GATE SEMANTICS — SUCCESSOR HANDOFF

This document is a permanent successor instruction. The machine-readable contract is the semantic authority:

`docs/forensic/FORENSIC_GATE_SEMANTICS_V1.json`

## Core law

A PASS belongs only to the gate that produced the evidence.

```text
PASS_IS_LOCAL = TRUE
PASS_IS_PREREQUISITE_ONLY = TRUE
PASS_INHERITANCE = FORBIDDEN
UNKNOWN_IS_NOT_PASS = TRUE
DEFAULT_DENY = TRUE
```

Therefore:

```text
DB_EXISTENCE(PASS)  !=> DB_BINDING(PASS)
DB_BINDING(PASS)    !=> DB_ROUND_TRIP(PASS)
DB_ROUND_TRIP(PASS) !=> PROMOTION(PASS)
```

These are not independent forensic systems. They are ordered admission gates inside ONE canonical Forensic FSM.

## Blocked is valid

`BLOCKED`, `PAUSED`, and `ARMED` are valid stable forensic states.

A successor bot MUST NOT:

- invent a workaround merely to remove BLOCKED;
- replace exact-runtime evidence with local curl;
- replace runtime receipt with proxy/sidecar evidence;
- treat code existence as execution evidence;
- treat deployment identity as runtime receipt;
- treat an old PASS as a current PASS;
- fabricate a TransportReceipt;
- mutate the state only to make progress appear.

The correct action when the exact primitive is unavailable is:

```text
PRESERVE STATE
    -> PRESERVE DENY
    -> PRESERVE IMMUTABILITY
    -> WAIT FOR EXACT PRIMITIVE
```

## Memory hierarchy

Chat is only the communication interface.

Canonical operational truth is held by:

1. `state/current_state.json`
2. `state/next_action.json`
3. machine-readable forensic contracts
4. immutable append-only action logs

Old documentation and chat history are references, never permission to override current evidence.

## Current foundation boundary

`BRAIN-N104C.1D-INFRA` remains `BLOCKED_ON_EXECUTION_PRIMITIVE`.

Layer 1 and the staircase remain LOCKED.

The only legitimate resume condition is an auditable exact-runtime execution primitive that runs the unchanged transport probe and emits the required compact `TransportReceipt` bound to the exact runtime identity.
