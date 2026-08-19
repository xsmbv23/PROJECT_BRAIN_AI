# STATE AUTHORITY CHAIN — V1

## Purpose

Prevent drift between Brain, Quant, data-plane repositories, Render runtime, and historical action logs.

The system has **one logical state authority**:

```text
xsmbv23/Project_Brain_AI/state/current_state.json
```

Everything else is evidence, projection, or history.

## Authority hierarchy

```text
                    ┌──────────────────────────────┐
                    │ BRAIN CURRENT_STATE.JSON     │
                    │ SINGLE LOGICAL STATE         │
                    │ AUTHORITY                    │
                    └──────────────┬───────────────┘
                                   │
                     Evidence -> State -> Action
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
   Quant Engine              xsmb-quant                 Render
   projection               data-plane                runtime
   READ ONLY                projection                 EVIDENCE
          │                        │                        │
          └────────────────────────┴────────────────────────┘
                                   │
                                   ▼
                              RECONCILIATION
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                 MATCH                         MISMATCH
                    │                             │
                    ▼                             ▼
                VERIFIED                    HARD DENY
```

## Critical semantics

### 1. PASS is local to a gate

A gate's PASS means only that gate's condition was proven.

```text
DB_EXISTENCE = PASS
```

does **not** imply:

```text
DB_BINDING = PASS
DB_TLS = PASS
DB_ROUND_TRIP = PASS
PROMOTION = PASS
```

### 2. No PASS inheritance

```text
PASS(Gate A) != PASS(Gate B)
```

Each downstream gate requires its own evidence.

### 3. Runtime is evidence, not authority

Render can prove what code is actually running. It cannot rewrite logical state merely because the running code says something different.

### 4. Deployment ID is evidence, not immutable identity

A new Render deployment may legitimately have a new deployment ID while executing the same commit. Immutable runtime identity is the deployed commit SHA.

### 5. Historical action logs are immutable history

Action logs explain what happened. They do not override `current_state.json`.

### 6. Quant Engine is not a second Brain

`Quant_Engine/state/current_state.json` is a read-only projection. If it conflicts with Brain authority, it must stop/deny rather than choose its own interpretation.

### 7. Data plane cannot self-promote

Collectors, receipts, semantic quorum, canonical candidates, and derived data can produce evidence. They cannot promote themselves into a higher logical state.

## State reconciliation rule

For a runtime reconciliation:

```text
1. Load Brain current_state.json.
2. Verify authority contract.
3. Obtain exact current runtime commit SHA.
4. Compare runtime commit to Brain's last verified runtime commit.
5. If equal -> VERIFIED.
6. If different/unknown -> HARD DENY.
```

Deployment ID is recorded as supplemental evidence only.

## Why this does not create a second FSM

The database admission chain remains one forensic FSM:

```text
DB_EXISTENCE
   -> DB_BINDING
   -> DB_TLS_ADMISSION
   -> NETWORK_ORIGIN_PROOF
   -> DB_ROUND_TRIP
   -> PROMOTION
```

The State Authority Chain is **governance over that FSM**, not another competing FSM.

## Successor rule

A future Bot must never infer state from:

- chat history
- an old action log
- Quant's local state
- Render deployment status alone
- a green test alone
- a downstream PASS
- an implementation claim

It must read Brain `state/current_state.json`, then reconcile exact-current runtime evidence.

If the evidence conflicts with Brain authority:

```text
DO NOT GUESS
DO NOT AUTO-PROMOTE
DO NOT REPAIR BY OVERWRITING HISTORY
HARD DENY
CREATE A NEW FORENSIC ACTION LOG
```

## Layer status

```text
FOUNDATION       = ACTIVE
STATE AUTHORITY  = SINGLE SOURCE
DATA ADMISSION   = CURRENT BRAIN STATE
LAYER 1          = LOCKED EXCEPT CURRENTLY ADMITTED ROOM
STAIRCASE        = LOCKED
```
