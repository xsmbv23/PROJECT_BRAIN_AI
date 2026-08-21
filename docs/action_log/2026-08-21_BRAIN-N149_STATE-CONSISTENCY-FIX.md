# BRAIN-N149 — Canonical State Consistency Fix

## Peer read

Before this action, Bot 1 read the current Quant Engine state. Quant remains `QUANT-N010 / WORKFLOW_TRIGGERED_BY_PUSH`; its completion gate still requires independently observable workflow execution evidence and does not authorize Brain promotion.

## Local finding

`tools/check_state_consistency.py` requires `ci_status` in `state/current_state.json`, but canonical current state did not contain that required field. The state checker would therefore fail closed on its own canonical state artifact.

## Fix

Added:

`ci_status = UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN`

This matches the existing N125 observation semantics and does not convert UNKNOWN to PASS.

## Scope

This is a canonical state-integrity repair only. It does not alter:

- `BRAIN-N125_WAIT_EXTERNAL`
- `ACTION_SPACE = 0`
- `MANDATORY_NO_OP`
- `PROMOTION = DENY`
- Room 02 lock
- Staircase lock
- external observation requirements

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
EXTERNAL_EVIDENCE = UNKNOWN
PROMOTED = NO

## Core Mission link

A broken state-consistency checker is a real governance/reliability blocker because the system cannot reliably distinguish canonical state from malformed state. Fixing it improves the evidence/control foundation without becoming a new objective.

## Next action

Re-read current peer state and latest peer work, then continue the highest-value safe Brain-side blocker audit. Do not create additional legacy/continuity documents unless they are required by an active dependency.
