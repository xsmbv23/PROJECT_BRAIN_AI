# BRAIN-N116 — Forensic Gate Doctrine Handoff

## Purpose

This action freezes the interpretation of the Forensic state machine for all successor Bots.

## Canonical rule

**ONE FORENSIC FSM. EACH GATE OWNS ITS OWN EVIDENCE. PASS IS LOCAL. PASS IS A PREREQUISITE ONLY. NO PASS INHERITANCE. UNKNOWN IS NOT PASS. DEFAULT DENY. PROMOTION REQUIRES FRESH EXACT-CURRENT EVIDENCE.**

## Current state

```text
N116 = READY_WAIT
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
ACTION_RECEIPT = NOT_YET_PROVEN_CURRENT
```

The canonical repository state already records these values. This document does not alter the runtime action space and does not create an external observation.

## Important interpretation

Database existence, service binding, TLS admission, network origin, round-trip, and promotion are not separate Forensic systems. They are sequential gates in one FSM.

A PASS on one gate never becomes PASS on another gate. It only permits the next gate to be evaluated.

Example:

```text
DB_EXISTENCE PASS
    -> allowed to check DB_BINDING
DB_BINDING PASS
    -> allowed to check SECRET_RESOLUTION
SECRET_RESOLUTION PASS
    -> allowed to check DB_TLS_ADMISSION
...
DB_ROUND_TRIP PASS
    -> allowed to evaluate PROMOTION
```

At every arrow, the next gate must gather its own evidence.

## Runtime action track

N116 is waiting for an independently observable exact-current `/governance` receipt. The verifier must never generate its own request and then treat that request as independent proof.

Until the external event is independently observable, the correct action is **NO-OP** and promotion remains denied.

## Successor boot instruction

Before any action, future Bots must read:

1. `state/current_state.json`
2. `state/next_action.json`
3. `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`
4. `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS_SUCCESSOR.md`
5. the latest action log

They must not use chat history as the system's memory authority.

## Integrity principle

The repository state and immutable evidence history are the durable handoff. Chat is only the communication interface.

No historical receipt may be edited to manufacture a PASS.
