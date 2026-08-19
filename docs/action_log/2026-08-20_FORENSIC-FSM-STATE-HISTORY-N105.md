# BRAIN-N105 — Forensic FSM State/History Standard

## Trigger

Successor handoff required clarification of the relationship between mutable current state and immutable forensic history.

## Decision

There is **ONE FORENSIC FSM**.

It is represented by:

1. a mutable current-state projection that may converge from exact evidence;
2. an immutable append-only history that records every prior action/state/deny/receipt/handoff.

These two representations jointly establish epistemic integrity.

## Critical rules

### Rule A — State convergence is allowed

When new exact evidence proves that the current state changed, the current-state projection may be updated.

### Rule B — History convergence is forbidden

Historical records must never be rewritten, deleted, or retroactively normalized to make the new state appear older than it is.

### Rule C — Epistemic non-inference

Every edge in an evidence chain requires its own Atomic Evidence Artifact.

```text
Container Exists
≠ Container Running
≠ Shell Active
≠ Probe Executed
≠ Receipt Proven
```

### Rule D — Strict unproven enforcement

```text
NO RECEIPT → NOT_PROVEN → HARD_DENY
```

Connector silence is not success.

## Gate rule

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
```

A gate PASS only authorizes evaluation of the next gate. It cannot set the next gate PASS.

## DB chain

```text
DB_EXISTENCE
→ DB_BINDING
→ DB_TLS_ADMISSION
→ DB_ROUND_TRIP
→ PROMOTION
```

## Source chain

```text
SOURCE_INDEPENDENCE
→ NETWORK_ORIGIN_PROOF
→ RESULT_TRANSPORT
→ OFFICIAL_RESULT_PANEL
→ CANDIDATE
→ EXCEL_VS_WEB_MATCH
→ CANONICAL_QUORUM
→ TRUTH_ADMISSION
```

## Forensic immutability

Prior `DENY`, `BLOCKED`, `NOT_PROVEN`, and failed execution events are historical facts and must remain append-only.

## Current boundary

At the time of this handoff:

```text
EXACT RUNTIME              = PROVEN
CURRENT STATE              = CONVERGED
HISTORY                    = APPEND_ONLY
DB ROUND_TRIP              = PASS
DB PROMOTION               = LOCAL_PASS
SOURCE PROMOTION           = DENY
TRANSPORT EXECUTION        = NOT_EXECUTED
TRANSPORT RECEIPT          = NOT_PROVEN
PROMOTION                  = DENY
LAYER 1                    = LOCKED
STAIRCASE                  = LOCKED
```

## Successor instruction

The next Bot must preserve this distinction before performing any action. It must never “upgrade” a gate from a previous gate's PASS and must never rewrite the historical record.

Read this document before reading or modifying `state/current_state.json` or `state/next_action.json`.

## Next action

Resume from the existing `next_action_id` and acquire the missing exact-runtime execution primitive. If no auditable execution primitive is available, remain `NOT_PROVEN/HARD_DENY` and append the observation.
