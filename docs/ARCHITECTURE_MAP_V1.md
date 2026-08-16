# PROJECT BRAIN AI — ARCHITECTURE MAP V1

## 0. Critical correction

The ChatGPT/Bot chat window is **only a communication interface**.

It is NOT:

- the system memory;
- the source of truth;
- the governance registry;
- the action ledger;
- the architecture definition;
- the permission store;
- the Fosennic state machine.

A future Bot must be able to resume from repository state and evidence even with zero chat history.

## 1. Physical architecture

```text
                         COMMUNICATION INTERFACE
                         Chat / Bot conversation
                                  │
                                  │  NO AUTHORITY
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                 PROJECT_BRAIN_AI                             │
│                 GOVERNANCE / MEMORY PLANE                   │
│                                                              │
│  Persistent State   Action Ledger   Corridor Registry       │
│  Capability Policy  Evidence Index  Layer Map               │
│  Verification       Promotion Gate  Bot Handoff             │
└───────────────┬──────────────────────────────┬───────────────┘
                │ controlled corridor          │ controlled corridor
                ▼                              ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│ XSMB DATA / BUILD PLANE  │       │ XSMB RUNTIME / UI PLANE  │
│                          │       │                          │
│ raw sources              │       │ app.py / preserved UI    │
│ crawler                  │       │ lightweight projections  │
│ structural validator     │       │ audit/read interfaces    │
│ provenance               │       │                          │
│ canonicalizer            │       │ NO canonical mutation    │
│ day shards               │       │                          │
│ manifest                 │       │                          │
└──────────────────────────┘       └──────────────────────────┘
```

## 2. Room / corridor model

Every cross-component communication is treated as entering a different room through a corridor.

```text
source room
   │
   ├─ identity
   ├─ source layer
   ├─ corridor authorization
   ├─ capability
   ├─ nonce/freshness
   ├─ lineage
   └─ payload integrity
        │
        ▼
destination room
```

No implicit hallway exists.

No component may jump directly from a lower-level room into a protected room.

## 3. Layer model

```text
L0 FOUNDATION / GOVERNANCE
  ├─ Fosennic policy
  ├─ persistent memory
  ├─ security
  ├─ evidence
  ├─ action ledger
  └─ promotion gate

L0 DATA / BUILD
  ├─ source capture
  ├─ structural validation
  ├─ provenance
  ├─ canonicalization
  ├─ shards
  └─ immutable data contract

L0 RUNTIME / UI
  ├─ app.py interface
  ├─ read projections
  └─ user communication

L1 INTELLIGENCE
  ├─ forensic analysis
  ├─ research
  ├─ Quant engines
  └─ controlled model experimentation
```

**L1 remains LOCKED until the foundation/data gates are complete.**

The staircase to L1 is itself a governed artifact. It is not automatically available because code exists.

## 4. Data authority

The data architecture follows the existing forensic contract:

```text
SOURCE
  ↓
STRUCTURAL VALIDATION
  ↓
PROVENANCE
  ↓
CANONICALIZATION
  ↓
CANONICAL DB
  ↓
CONTRACT HASH
  ↓
FORENSIC MANIFEST
```

For XSMB:

```text
FULL_PRIZE source truth
        ↓
27 prize values
        ↓
last 2 digits of each prize
        ↓
canonical 27 tails
```

The source representation and Quant representation are different objects. FULL_PRIZE must never be reconstructed from TAIL_27.

Legacy 27-tail records remain `LEGACY_TAIL27`; they must never be relabeled as `FULL_PRIZE`.

Same-date replacement requires structural validation + provenance + quorum + contract update + forensic handling.

## 5. Memory authority

Persistent memory is distributed by responsibility:

```text
state/current_state.json
    current governed state

state/next_action.json
    exact resumable next action

action_log/
    immutable historical actions

docs/
    architecture + policies + contracts

evidence/
    compact evidence envelopes / indexes
```

The chat may summarize these objects, but it does not own them.

## 6. Bot continuity

A new Bot starts with:

```text
AI_START_HERE
    ↓
ARCHITECTURE_MAP
    ↓
FOSENNIC_FOUNDATION
    ↓
COMMUNICATION_SECURITY
    ↓
EVIDENCE_PROTOCOL
    ↓
ACTION_LEDGER_PROTOCOL
    ↓
CURRENT_STATE
    ↓
NEXT_ACTION
    ↓
NEWEST ACTION LOG
```

It then executes exactly the next governed action and appends its own result.

## 7. Runtime boundary

Heavy computation must not be placed in the lightweight Brain/UI process.

The Brain receives compact evidence envelopes, hashes, manifests, status and governance metadata.

The UI receives compact projections rather than rebuilding thousands of historical records in RAM.

This preserves the Render 512 MB constraint without sacrificing forensic lineage.

## 8. Promotion topology

```text
DATA VERIFIED
      ↓
EVIDENCE BOUND
      ↓
GOVERNANCE VERIFIED
      ↓
PROMOTION GATE
      ↓
PROMOTION OR DENY
```

Foundation default:

```text
PROMOTION = DENY
```

## 9. Foundation completion criterion

The foundation is complete only when:

1. persistent Brain state is authoritative outside chat;
2. action continuity is append-only;
3. corridor/layer/capability gates execute fail-closed;
4. evidence is compact and lineage-preserving;
5. XSMB data contract is connected without provenance loss;
6. Render runtime boundary is verified;
7. promotion remains DENY until explicitly justified;
8. the staircase to L1 is defined and itself auditable.

Only then may L1 be unlocked.
