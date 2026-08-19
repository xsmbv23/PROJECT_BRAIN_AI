# FORENSIC FSM STATE/HISTORY STANDARD V1

## Purpose

This document is a permanent successor handoff contract for the Brain Forensic control plane.
It formalizes the distinction between the current mutable state and the immutable append-only history.

## 1. Canonical model

```text
                    FORENSIC SYSTEM
                         │
             ┌───────────┴───────────┐
             │                       │
       CURRENT STATE            HISTORY
        (MUTABLE)             (IMMUTABLE)
             │                       │
     State Convergence        Append-Only
    (Hội tụ theo Evidence)   (Không sửa/Xóa)
             │                       │
             └──────────┬────────────┘
                        │
             EPISTEMIC INTEGRITY
```

There is ONE Forensic FSM. It has two complementary representations:

- `CURRENT STATE`: mutable operational projection that converges only from exact evidence.
- `HISTORY`: immutable append-only record of prior states, actions, denials, receipts, and handoffs.

They are not competing truths and must never be treated as two independent forensic systems.

## 2. Epistemic Integrity

The current state may converge when new exact evidence supersedes an earlier observation.
The historical record must not be rewritten to make the new state look as if it was always true.

Therefore:

```text
EXACT EVIDENCE
     │
     ├──────────────► CURRENT STATE CONVERGENCE
     │
     └──────────────► IMMUTABLE HISTORY APPEND
```

A state transition must preserve both facts:

1. what is true now;
2. what was previously believed/proven/denied and why.

## 3. Diamond Rule — Epistemic Non-Inference

Every edge in a forensic evidence chain requires its own Atomic Evidence Artifact.

Never infer one gate from another merely because the sequence appears logical.

```text
Container Exists
      X
      │
      ╲  NOT PROVEN
       ╲
Container Running
      X
      │
Shell Active
      X
      │
Probe Executed
      X
      │
Receipt Proven
```

More precisely:

```text
Container Exists
    ≠ Container Running
    ≠ Shell Active
    ≠ Probe Executed
    ≠ Receipt Proven
```

The same rule applies to database, network, source, execution, deployment, and promotion gates.

## 4. Diamond Rule — Strict Unproven Enforcement

```text
NO RECEIPT
    ↓
NOT_PROVEN
    ↓
HARD_DENY
```

No repository write, database mutation, execution claim, transport claim, or promotion claim may be recorded as proven without a direct receipt from the relevant Tool Boundary or exact runtime evidence source.

Connector silence is not success.

A tool returning metadata is not proof that a mutation happened.

A repository being reachable is not proof that a file was written.

A database existing is not proof that the service is bound to it.

## 5. Gate semantics

Each gate owns its own evidence.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
```

A PASS on gate N means only:

> gate N is proven and the next gate may be evaluated.

It does NOT mean:

> gate N+1 is proven.

## 6. Database admission chain

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
```

Semantics:

- `DB_EXISTENCE=PASS`: the database resource exists and is observable.
- `DB_BINDING=PASS`: the exact runtime has an authorized binding.
- `DB_TLS_ADMISSION=PASS`: the binding meets explicit TLS requirements.
- `DB_ROUND_TRIP=PASS`: a compact metadata envelope was actually written, read back, and SHA-256 verified.
- `PROMOTION=PASS`: only then may durable evidence promotion occur.

No stage inherits PASS from another stage.

## 7. Source admission chain

```text
SOURCE_INDEPENDENCE
    ↓
NETWORK_ORIGIN_PROOF
    ↓
RESULT_TRANSPORT
    ↓
OFFICIAL_RESULT_PANEL
    ↓
CANDIDATE
    ↓
EXCEL_VS_WEB_MATCH
    ↓
CANONICAL_QUORUM
    ↓
TRUTH_ADMISSION
```

The source chain has the same non-implication semantics as the DB chain.

Primary source target currently designated:

- `ketqua16.net`

Identity/secondary source currently designated:

- `xsmb.com.vn`

Advertisements are classified as non-truth content and must never enter the source-truth channel.

## 8. Mutable state and immutable history interaction

When exact evidence changes a state:

```text
OLD CURRENT STATE
       │
       │  new exact evidence
       ▼
NEW CURRENT STATE
       │
       └────────────► APPEND NEW HISTORY EVENT
```

The old history entry remains unchanged.

The current state is allowed to change.

The historical evidence is not allowed to change.

This is the required convergence model.

## 9. Forensic control-plane matrix

| Dimension | Current-state meaning | Historical meaning |
|---|---|---|
| Exact live runtime | current exact identity/evidence | previous exact identities preserved |
| Mutable state | converges from evidence | transition itself is preserved |
| Deployment identity | current deployment | prior deployments remain recorded |
| Transport execution | current proven state | every previous attempt/deny preserved |
| Transport receipt | current receipt if proven | previous receipts/absence preserved |
| DB binding | current admission state | historical binding decisions preserved |
| Promotion | current authorization state | previous promotions/denials preserved |
| Layer 1 | current lock state | every lock/unlock decision preserved |
| Staircase | current lock state | every lock/unlock decision preserved |

## 10. Forbidden shortcuts

- No synthetic production data.
- No proxy evidence.
- No local curl substitution for an exact Render runtime proof.
- No source modification solely to force a probe to PASS.
- No credential storage in GitHub.
- No hidden PASS inference.
- No rewriting of immutable history.
- No deleting prior DENY/BLOCKED records.

## 11. Successor protocol

A future Bot must read this document before changing any forensic gate.

It must then read:

1. `state/current_state.json`
2. `state/next_action.json`
3. latest `docs/action_log/*`
4. gate-specific contract documents
5. exact runtime evidence when available

The successor must continue from `next_action_id`, not restart from an assumption.

## 12. Current terminal condition

The current foundation remains blocked at the exact runtime execution primitive boundary.

```text
TRANSPORT PROBE       = LOCKED_READY
TRANSPORT IMPLEMENTED = PROVEN_FROM_SOURCE
TRANSPORT EXECUTION   = NOT_EXECUTED
TRANSPORT RECEIPT     = NOT_PROVEN
PROMOTION             = DENY
LAYER_1               = LOCKED
STAIRCASE             = LOCKED
```

The correct next action is to obtain the missing auditable execution primitive, not to manufacture a substitute receipt.
