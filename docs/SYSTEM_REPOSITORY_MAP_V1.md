# SYSTEM REPOSITORY MAP V1

## Status

**CANONICAL SYSTEM MAP — FOUNDATION / FORENSIC**

This document defines the repository boundaries for successor AI agents. The three repositories are NOT one codebase and MUST NOT be collapsed into one implementation boundary.

## Canonical repositories

| Repository | Layer / Role | Authority |
|---|---|---|
| `xsmbv23/Project_Brain_AI` | Brain / Governance / Forensic Control Plane | governance, admission, locks, promotion gates, successor state |
| `xsmbv23/xsmb-quant` | XSMB Data / Ingestion / Source Foundation / Runtime | source truth, ingestion, reconciliation, raw artifacts, data contracts, runtime data foundation |
| `xsmbv23/Quant_Engine` | Quant / Calculation / Research Engine | calculations, factors, signals, research/backtest logic |

## Non-negotiable boundary

```text
                    PROJECT_BRAIN_AI
             Governance / Forensic Control
                         │
             explicit capability/admission
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        xsmb-quant              Quant_Engine
     Source/Data Truth        Calculation/Research
             │                       │
             └──────── evidence ─────┘
                         │
                         ▼
                  Brain admission
```

Brain governs. Data owns source truth. Quant calculates. Neither Data nor Quant may silently redefine Brain governance. Brain must not become a data-ingestion engine or calculation engine.

## Authority matrix

### 1. Source truth

Owner: `xsmbv23/xsmb-quant`

Examples already present in the data repository include:

- raw artifact handling;
- data contracts;
- calendar ledger/state;
- reconciliation;
- source-truth handoff documentation;
- data foundation runbook/blueprint;
- data-side security corridor/capability/audit/self-test.

Evidence in the current repository includes `docs/STATE_AUTHORITY_HANDOFF.md`, `data/contracts/README.md`, `storage/raw_artifacts.py`, `data/reconciliation/legacy_reconcile.py`, and the AI progress/action ledgers. fileciteturn764file0L1-L5 fileciteturn764file5L26-L30 fileciteturn764file14L71-L75 fileciteturn764file22L111-L115

### 2. Calculation / research

Owner: `xsmbv23/Quant_Engine`

The repository is deliberately isolated from Brain governance and XSMB source-truth ownership. Calculation code must consume explicit, admissible inputs and must not mutate source truth.

Current repository metadata confirms `Quant_Engine` is a public `main`-branch repository owned by `xsmbv23`.

### 3. Governance / Forensic control

Owner: `xsmbv23/Project_Brain_AI`

Brain owns:

- governance FSM;
- corridor admission;
- corridor-key + room-key separation;
- per-room locks;
- protected-room inner release;
- capability admission;
- immutable forensic state;
- promotion gates;
- successor action log / next-action handoff;
- compact evidence policy;
- Render OOM safety boundary.

Brain is a control plane, not the system's source-data owner.

## Data flow

```text
SOURCE WEB / EXCEL / RAW INPUT
          │
          ▼
      xsmb-quant
          │
          ├── raw artifact
          ├── source validation
          ├── reconciliation
          ├── canonical data state
          │
          ▼
   explicit admissible dataset
          │
          ▼
     Quant_Engine
          │
          ├── calculation
          ├── factor/signal logic
          ├── research/backtest
          │
          ▼
      derived result
          │
          ▼
     Project_Brain_AI
          │
          ├── admission
          ├── forensic validation
          ├── security policy
          ├── promotion decision
          └── compact evidence
```

A derived Quant result is NEVER allowed to overwrite source truth. Brain can deny admission even when Quant produces a mathematically valid result.

## Evidence flow

```text
xsmb-quant
   │
   │ source evidence + provenance
   ▼
Quant_Engine
   │
   │ derived calculation evidence
   ▼
Project_Brain_AI
   │
   ├── validate provenance
   ├── validate capability
   ├── validate security corridor
   ├── validate immutable state transition
   └── decide PROMOTE / DENY
```

## Forensic database admission chain

A database's existence is NOT equivalent to service authorization, and authorization is NOT equivalent to durable evidence promotion.

```text
DB_EXISTENCE
    │
    │ prerequisite only
    ▼
DB_BINDING
    │
    ▼
DB_TLS_ADMISSION
    │
    ▼
DB_ROUND_TRIP
    │  write → read → SHA-256 match
    ▼
PROMOTION
```

**Critical invariant:** PASS at an earlier gate never automatically promotes a later gate. Every state requires its own evidence.

Therefore:

```text
DB_EXISTS = PASS
       !=
DB_BOUND = PASS
       !=
DB_ROUND_TRIP = PASS
       !=
PROMOTION = PASS
```

Unknown is never Pass. Default is Deny.

## Security corridor

Every cross-repository communication is treated as movement through a secured corridor:

```text
source layer
   │
   ▼
CORRIDOR KEY
   │
   ▼
ROOM KEY
   │
   ▼
ROOM POLICY
   │
   ├── normal room → explicit capability admission
   │
   └── protected room → inner-release / human-equivalent latch
```

The existence of a valid route does not imply permission to enter the destination room.

## Layer direction

Repository boundaries are directional. The map is NOT a closed circle.

Allowed conceptual direction:

```text
DATA → explicit admissible input → QUANT → derived evidence → BRAIN admission
```

Brain may govern or deny the transaction. It must not silently become the owner of Data or Quant internals.

No automatic reverse mutation is implied by an admission decision.

## Render boundary

`Project_Brain_AI` runs under a strict Render Free memory boundary. The Brain runtime is dataset-free and must remain lightweight.

Rules:

- do not load bulk historical datasets into Brain;
- do not perform large backtests inside Brain;
- do not duplicate source data into Brain memory;
- prefer compact evidence envelopes;
- branch heavy computation to `xsmb-quant` or `Quant_Engine`;
- preserve a conservative 320 MiB guard against the 512 MB Render Free ceiling;
- one CPU / one instance remains the safe baseline unless explicitly revalidated.

## Human/UI boundary

The chat/UI is only a communication interface. It is NOT the persistent memory authority and is NOT the forensic source of truth.

Persistent state must live in repository state/contracts/action logs and durable evidence systems, subject to the Forensic admission chain.

## Successor rule

Every AI agent inheriting this system MUST read this document before modifying any repository.

The successor MUST NOT:

1. merge the three repositories;
2. move source-truth authority into Brain;
3. move calculation authority into Brain;
4. treat DB existence as DB authorization;
5. infer PASS from missing evidence;
6. bypass corridor/room locks;
7. promote unknown state;
8. store secrets in GitHub;
9. load bulk data into Brain runtime;
10. unlock Layer 1 or the staircase merely because the foundation runtime is healthy.

Every action MUST create/update the successor action ledger before declaring the action complete.

## Current foundation status

```text
THREE-REPOSITORY MAP       = ESTABLISHED
DATA AUTHORITY             = xsmb-quant
CALCULATION AUTHORITY      = Quant_Engine
GOVERNANCE AUTHORITY       = Project_Brain_AI
DB EXISTENCE               = PASS
DB BINDING                 = NOT_BOUND
DB TLS ROUND-TRIP          = NOT_PROVEN
PROMOTION                  = DENY
LAYER 1                    = LOCKED
STAIRCASE                  = LOCKED
```
