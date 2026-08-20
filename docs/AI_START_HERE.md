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
14. There is exactly ONE Forensic FSM. Its chains are not separate Forensic universes.
15. PASS belongs only to the gate that earned it; PASS never transfers to another gate.
16. Each gate requires its own evidence; historical evidence cannot substitute for fresh promotion evidence.

## Required reading order

```text
FOSENNIC_FOUNDATION
        ↓
FORENSIC_FSM_GATE_SEMANTICS
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

## Current exact state

The repository state is authoritative over the chat window. At the current checkpoint:

```text
FORENSIC_FSM              = ONE
DB_ADMISSION_CHAIN        = EXISTENCE -> BINDING -> SECRET -> TLS -> NETWORK -> ROUND_TRIP -> PROMOTION
RUNTIME_ACTION_CHAIN      = N116 -> EXTERNAL_OBSERVATION -> RECEIPT_VERIFICATION -> ACTION_RECEIPT
CURRENT_RUNTIME           = exact-current evidence recorded
CURRENT_RUNTIME_TESTS     = 209 / 209 PASS
CURRENT_FOUNDATION        = PASS
DB_BINDING                = BOUND_TLS
DB_TLS                    = PASS
DB_NETWORK_ORIGIN         = PASS
DB_ROUND_TRIP             = PASS
PROMOTION                 = DENY
ACTION_RECEIPT_CURRENT    = NOT_YET_PROVEN_CURRENT
ACTION_SPACE              = 0
MANDATORY_NO_OP           = TRUE
LAYER_1                   = LOCKED
STAIRCASE                 = LOCKED
```

The exact current commit/deploy/instance and the authoritative next action are always read from `state/current_state.json` and `state/next_action.json`; do not hard-code them here.

## Current action discipline

`BRAIN-N116_WAIT_EXTERNAL_OBSERVATION` is a mandatory wait state. While `action_space=0`, a future Bot may only:

- monitor exact-current runtime evidence;
- read immutable historical action logs;
- validate state/document integrity;
- record new evidence without mutating prior events.

It must not manufacture an external event, self-call and call it independent proof, unlock Room 02, unlock the staircase, promote, expose credentials, or download/parse source data.

## Data Foundation continuity

Data Foundation is a separate preparation track inside the same Forensic FSM. It may be prepared only within the scope allowed by `state/next_action.json`; it cannot unlock the runtime action track and cannot change `NEXT_ACTION` while N116 is waiting.

Human Excel and crawler evidence remain independent lineages. FULL_27 is canonical source truth; TAIL_27 is derived. Conflicts are investigated rather than silently auto-resolved.

## Foundation gate

```text
FOUNDATION = RUNTIME-VERIFIED
PROMOTION = DENY
LAYER 1 = LOCKED
```
