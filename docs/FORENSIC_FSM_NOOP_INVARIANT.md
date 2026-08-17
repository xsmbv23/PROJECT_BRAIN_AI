# FORENSIC FSM — NO-OP / ACTIVE-HOLD INVARIANT

## Canonical checkpoint

FOUNDATION = FROZEN
STATE = WAIT_EXTERNAL_EVENT
MODE = ACTIVE_HOLD
ACTION = NO_OP
AUTHORITY = DENY
PROMOTION = DENY

This is a valid state, not an incomplete workflow. Internal authority is exhausted; the system must not manufacture a transition.

## Causal law

REALITY -> EVIDENCE -> STATE -> TRANSITION -> ACTION

Forbidden reverse causality:

ACTION -> STATE
STATE -> EVIDENCE
BRAIN -> REALITY

Brain may observe, validate, classify and prepare. Brain may not create the external event that would justify its own next state.

## Capability versus authority

CAPABILITY != AUTHORITY

Technical ability never creates permission. Implementation convenience must never convert capability into authority.

## FSM gate rule

PASS(Gn) only opens evaluation rights for Gn+1. It never means PASS(Gn+1).

Forbidden: PASS chaining, PASS inference, PASS assumption, PASS by silence, PASS by capability, PASS by historical success.

Every gate requires its own evidence.

## ACTIVE_HOLD

ACTIVE_HOLD = NO TRANSITION AUTHORITY + NO STRUCTURAL CHANGE + FULL READINESS FOR A REAL EXTERNAL EVENT

ACTIVE_HOLD is not sleep, timeout, missing work, or permission for opportunistic improvement. Preserve the last proven valid state until Reality supplies a new admissible event and evidence.

## Database example

DB_EXISTS=PASS -> evaluate DB_BINDING -> evaluate TLS -> evaluate WRITE/READ/SHA256 MATCH -> evaluate PROMOTION.

No earlier PASS can promote a later gate.

## External-event boundary

NO REAL EVENT -> NO EVIDENCE -> NO TRANSITION -> NO ACTION -> NO-OP

NO-OP is the correct forensic outcome.

## Successor rule

A successor Bot AI must read this document plus state/current_state.json and state/next_action.json before structural action. If canonical state is WAIT_EXTERNAL_EVENT + ACTIVE_HOLD + DENY, do not invent work merely to change state. Act only when a new external event produces admissible evidence and the FSM permits the transition.
