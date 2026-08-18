# BRAIN-N066 — Governed Wait Audit

## Purpose

Record the current external-event boundary without manufacturing a test event.

## Current FSM

```text
Gate A evidence
    -> PASS(A)
    -> unlock RIGHT TO CHECK Gate B
    -> Gate B requires FRESH evidence

PASS(A) does NOT become PASS(B).
```

This is the permanent database-admission doctrine:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Every gate requires fresh evidence. PASS is local to its gate. No PASS inheritance exists.

## External event currently observed

The latest observed Quant Engine workflow is:

- repository: `xsmbv23/Quant_Engine`
- run: `32096349433`
- event: `workflow_dispatch`
- workflow: `Quant Engine Layer 1 Verification`
- commit: `2620b72e93c0e1f2c885727124445eda8afed3a3`
- conclusion: `success`

This event is **runtime admission evidence**, not the independent `Quant Engine Tests` receipt required by `BRAIN-N066`.

The required test workflow is `.github/workflows/quant-engine-tests.yml`; its contract runs the bounded Python unit suite on push/pull_request to `main`.

## Decision

Do NOT:

- rerun or manufacture the required event merely to obtain a receipt;
- reuse the runtime admission receipt as a test receipt;
- infer domain truth from the runtime event;
- unlock the staircase;
- promote Layer 1;
- promote the database.

The correct state is:

```text
BRAIN-N066 = WAIT_EXTERNAL_EVENT
MODE       = ACTIVE_HOLD
PROMOTION  = DENY
STAIRCASE  = LOCKED
```

## Why waiting is a valid action

In a Forensic FSM, absence of the required fresh evidence is itself a state condition. The correct next action is therefore **no execution against the protected gate** until the independent test event exists.

A retry would be a new external event and cannot be substituted for the missing event by Brain.

## Successor rule

When a real `Quant Engine Tests` workflow run appears for the exact current Room 01 commit, Brain may consume that receipt, classify it independently, persist it, and then evaluate only the current gate.

Until then, remain governed hold.
