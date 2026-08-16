# AI START HERE — MANDATORY

This file is the first file a future Bot must read.

## Mission

Preserve the Fosennic architecture while continuing work without architectural drift.

## Non-negotiable boundaries

1. Brain governs; it does not invent XSMB truth.
2. Every cross-room communication crosses a registered corridor.
3. Every corridor is layer-aware and capability-authorized.
4. Default is DENY.
5. Missing lineage, stale/replayed nonce, unknown corridor or scope mismatch => DENY.
6. Evidence is not promotion.
7. Static verification is not runtime verification.
8. Candidate artifacts remain `PROMOTION=DENY`.
9. Canonical FULL_27 remains the only truth representation; TAIL_27 is derived.
10. The Render UI remains a presentation boundary; it must not execute heavy crawl/backtest work.
11. Brain receives compact evidence envelopes, never the complete XSMB database.
12. Never log secrets.
13. Never erase action history to make the current state look clean.

## Required reading order

```text
FOSENNIC_FOUNDATION
        ↓
COMMUNICATION_SECURITY
        ↓
EVIDENCE_PROTOCOL
        ↓
ACTION_LEDGER_PROTOCOL
        ↓
state/current_state.json
        ↓
state/next_action.json
        ↓
action_log/* newest first
```

## Required action discipline

Before action:

- identify current state;
- identify exact next action;
- identify affected layer/corridor/capability;
- identify whether the action is static or runtime;
- preserve DENY until evidence proves otherwise.

After action:

- record action id;
- files changed;
- commit SHA;
- static result;
- runtime result;
- evidence references/hashes;
- failure/unknowns;
- governance decision;
- new current state;
- exact next action.

## Current foundation gate

```text
BRAIN FOUNDATION = IMPLEMENTED / NOT YET RUNTIME VERIFIED
LAYER 1 = LOCKED
PROMOTION = DENY
```
