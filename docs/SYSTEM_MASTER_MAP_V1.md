# SYSTEM MASTER MAP V1 — ORCHESTRATOR + WORKER CONTINUITY

> Canonical orientation document for future Bot/Worker sessions.
>
> Purpose: preserve the complete system-level understanding before any new worker task is allocated. This document is an orientation map, not a replacement for the underlying contracts, state files, action ledger, evidence receipts, or source code.

## 0. Mission in one sentence

Build an XSMB prediction system that advances from **real data → valid research → valid backtest → demonstrable edge → EV/P&L/ROI → robustness/risk/drift → controlled action**, while the Forensic FSM prevents fabricated evidence, invalid inference, lookahead, provenance loss, stale evidence, and unauthorized promotion.

## 1. Core Mission flow

```text
REAL DATA
    |
    v
VALID RESEARCH
    |
    v
VALID BACKTEST
    |
    v
EDGE
    |
    v
EV / P&L / ROI
    |
    v
ROBUSTNESS / RISK / DRIFT
    |
    v
CONTROLLED ACTION
```

The Forensic FSM is the **control/admission mechanism**, not the product goal.

## 2. System layers

```text
                         +---------------------------+
                         |       ORCHESTRATOR         |
                         | Brain / governance plane   |
                         +-------------+-------------+
                                       |
                              task / allocation
                                       |
             +-------------------------+-------------------------+
             |                         |                         |
             v                         v                         v
       WORKER 1                   WORKER 2                  WORKER 3
       coordination               Quant/data                reality/runtime
             |                         |                         |
             +-------------------------+-------------------------+
                                       |
                           worker deliberation
                                       |
                           consensus + dissent
                                       |
                                       v
                              recommendation
                                       |
                                       v
                              ORCHESTRATOR
                                       |
                                NEXT ACTION
```

Workers are employees/helpers for the orchestrator. They are not the product and do not own canonical governance.

## 3. Governance / control plane

```text
SESSION_START_SYNC
        |
        v
CURRENT_STATE + NEXT_ACTION
        |
        v
POLICY / CONTRACTS
        |
        v
ACTION LEDGER + PEER HANDOFF
        |
        v
FORENSIC FSM
        |
        v
OWN-GATE EVIDENCE
        |
        v
PASS / UNKNOWN / DENY
```

Non-negotiable semantics:

- one Forensic FSM;
- PASS is local to the gate that earned it;
- PASS is only a prerequisite, never automatic promotion;
- no PASS inheritance;
- UNKNOWN is not PASS;
- default DENY;
- every gate owns its evidence;
- fresh evidence is required for promotion;
- historical evidence cannot substitute for current promotion evidence;
- workers cannot mutate canonical truth or promote themselves.

## 4. Data foundation branch

```text
REAL SOURCES
   |
   v
SOURCE INDEPENDENCE
   |
   v
NETWORK / RESULT TRANSPORT
   |
   v
OFFICIAL RESULT PANEL
   |
   v
CANDIDATE CAPTURE
   |
   v
EXCEL-vs-WEB MATCH
   |
   v
CANONICAL QUORUM
   |
   v
TRUTH ADMISSION
   |
   v
FROZEN CANONICAL ARTIFACT
```

Canonical representation:

```text
FULL_27 = only canonical truth representation
TAIL_27 = derived representation
```

Do not reverse-engineer FULL_27 from TAIL_27. Do not turn synthetic or legacy tail-only data into production truth.

Required S1 canonical evidence includes:

```text
real-source provenance
acquisition channel
acquisition reference
aquisition timestamp
raw-byte SHA-256
consecutive real-date coverage
coverage_ratio = 1.0
zero unresolved conflicts
real admission receipt
frozen canonical hash
admitted canonical artifact
```

Current state says S1 remains blocked until those predicates are independently evidenced.

## 5. Research branch

```text
CANONICAL REAL DATA
       |
       v
DATE-ALIGNED RESEARCH DATASET
       |
       v
NO-LOOKAHEAD VALIDATION
       |
       v
REPRODUCIBLE BASELINE RESEARCH
       |
       v
BOUNDED EXPERIMENTS
```

Research dataset admission must establish timestamp boundaries, feature availability, reproducibility, missing-data policy, provenance, and no-lookahead behavior.

## 6. Backtest / Quant branch

```text
ADMITTED RESEARCH DATASET
       |
       v
FEATURE / MODEL CONFIG
       |
       v
WALK-FORWARD / TRAIN-TEST
       |
       v
EXECUTION ASSUMPTIONS
       |
       v
COST / SLIPPAGE / LIMITS
       |
       v
LOOKAHEAD AUDIT
       |
       v
BASELINE COMPARISON
       |
       v
P&L / EV
       |
       v
MULTIPLE-TESTING / ROBUSTNESS
```

A working backtest is not automatically valid. A statistically significant-looking result is not automatically an edge.

## 7. Edge / EV branch

```text
VALID BACKTEST
     |
     v
OUT-OF-SAMPLE EDGE
     |
     v
EV > 0 under explicit assumptions
     |
     v
P&L / ROI
     |
     v
ROBUSTNESS
     |
     v
RISK / DRIFT
     |
     v
CONTROLLED ACTION
```

The terminal product criterion is not “model runs”. It is demonstrable real edge with positive expected value and sufficient robustness to survive reasonable alternative assumptions.

## 8. Runtime / infrastructure branch

```text
CODE
 |
v
GITHUB ACTIONS / EXECUTION PLANE
 |
v
WORKER PROCESS
 |
v
RUNTIME EVIDENCE
 |
v
DURABLE RECEIPT
 |
v
RECONCILIATION
```

Render is infrastructure/presentation/runtime support. Render UI must not become the heavy crawl/backtest execution plane merely because it is convenient.

Current runtime authority is exact-current runtime evidence, not a historical deployment screenshot or a static repository claim.

## 9. Worker lifecycle — mandatory for Worker N

```text
IDENTITY
  |
  v
SESSION_START_SYNC
  |
  v
CURRENT ALLOCATION
  |
  v
CLAIM
  |
  v
PROCESS EXECUTION
  |
  v
DURABLE RECEIPT
  |
  v
ALLOCATION + CYCLE BINDING
  |
  v
RECONCILIATION
  |
  v
WORKER RUNTIME VERIFIED
```

Service liveness is not sufficient:

```text
HTTP 200 / port open / process alive
                 !=
worker execution verified
```

### BOT3 historical failure

BOT3 was initially treated as healthy because its HTTP/source-independence component was alive. The actual allocation consumer / claim / execute / receipt chain was incomplete. This created a HOLD.

Recovery succeeded only after changing the execution route so BOT3 could be executed through an independent GitHub Actions E2E path and proving fresh receipts against the current allocation/cycle.

Permanent rule:

> Never onboard Worker N from liveness alone. Prove allocation → claim → execute → receipt → reconcile on the current execution boundary.

## 10. Worker deliberation branch

Deliberation itself must be real execution, not orchestrator prose.

```text
COMMON TASK
    |
    +--> WORKER 1 initial analysis
    +--> WORKER 2 initial analysis
    +--> WORKER 3 initial analysis
             |
             v
         CROSS-READ
             |
             v
      CHALLENGE / CRITIQUE
             |
             v
         REBUTTAL
             |
             v
        EVIDENCE CHECK
             |
             +------> DISSENT
             |
             v
         CONSENSUS
             |
             v
      RECOMMENDATION
             |
             v
       ORCHESTRATOR
             |
             v
        NEXT ACTION
```

Required deliberation artifact:

```text
session_id
allocation_id
cycle_id
worker identities
execution boundary
initial positions
peer challenges
peer rebuttals
evidence references
agreements
disagreements
minority position
consensus
recommended_next_action
unresolved risks
```

Consensus is a recommendation, not proof. Dissent must be preserved.

## 11. Communication branch

```text
WORKER
  |
  v
REGISTERED CORRIDOR
  |
  v
IDENTITY + PROJECT + LAYER
  |
  v
CAPABILITY AUTHORIZATION
  |
  v
NONCE / FRESHNESS / REPLAY PROTECTION
  |
  v
LINEAGE + PAYLOAD HASH
  |
  v
POLICY CHECK
  |
  v
POST-VERIFICATION
  |
  v
AUDIT APPEND
```

No credentials, tokens, cookies, database URLs, or private capability material in worker messages.

## 12. State / continuation branch

The repository is authoritative over chat memory.

```text
state/current_state.json
        |
        v
state/next_action.json
        |
        v
latest action log
        |
        v
latest peer handoff
        |
        v
SESSION_START_RECORD
```

Current observed state (read from repository):

```text
project            = XSMB_FORENSIC
brain_role         = GOVERNANCE_CONTROL_PLANE
chat_role          = COMMUNICATION_INTERFACE_ONLY
forensic_fsm       = ONE_FORENSIC_FSM
state_mode         = DATA_ADMISSION
state              = SOURCE_INDEPENDENCE_AUDIT
S1                 = BLOCKED / DENY
S2                 = UNKNOWN / LOCKED
S3                 = UNREACHED / LOCKED
S4                 = UNREACHED / LOCKED
S5                 = UNREACHED / LOCKED
S6                 = UNREACHED / LOCKED
S7                 = UNREACHED / LOCKED
```

The current state file identifies `BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER` as the authoritative next-action chain, with fresh evidence required for every missing S1 predicate.

## 13. N-series continuation model

N numbers are continuity/action units, not separate products.

```text
N116 ... N174
       |
       v
N175
       |
       v
N176
       |
       v
...
       |
       v
N_FINAL
```

A later N must read current state and latest action/peer handoff rather than assuming a historical N status is still current.

N175 E2E triple-worker PASS proves a runtime/execution segment. It does not itself promote S1 canonical data or unlock S2.

## 14. File/system classification

### AUTHORITATIVE / LIVE

Treat these as high-priority system sources:

```text
state/current_state.json
state/next_action.json
contracts/*
.github/workflows/*
docs/AI_START_HERE.md
docs/architecture/*
docs/forensic/*
docs/communication_security* / related communication contracts
docs/evidence/* / evidence protocol
docs/*ACTION* / action-ledger material
orchestration/*
workers/*
Quant_Engine/*
```

### RUNTIME / RECEIPT EVIDENCE

```text
coordination/receipts/*
coordination/reconciliation/*
state/action logs / durable action records
```

These are evidence/history, not automatically current authority.

### DERIVED / SECONDARY

```text
TAIL_27
reports
summaries
rendered UI artifacts
human-readable snapshots
```

Use for interpretation only when their derivation and freshness are established.

### HISTORICAL / IMMUTABLE

Old action logs, old receipts and forensic records must not be deleted just to make the repository look clean. They remain historical evidence.

### POTENTIAL SCRAP / UNKNOWN

Files that are duplicates, abandoned experiments, obsolete one-off probes, generated artifacts, stale scratch notes, or superseded implementations must **not** be deleted by assumption. They first need a repository audit and reference check.

The cleanup objective is:

```text
file
 |
 +--> referenced by live contract/code/workflow/state?
 |          |
 |         YES --> LIVE/AUTHORITATIVE
 |
 +--> evidence/history referenced by ledger?
 |          |
 |         YES --> HISTORICAL/IMMUTABLE
 |
 +--> generated/derived but reproducibly rebuildable?
 |          |
 |         YES --> DERIVED
 |
 +--> unreferenced + obsolete + safe to remove?
            |
           YES --> SCRAP CANDIDATE
```

No deletion occurs until the reference graph is checked.

## 15. What workers are for

Workers exist to accelerate the Core Mission, not to become a second governance system.

Good worker assignments are concrete blocker-reduction tasks such as:

- source/provenance audit;
- dataset admission verification;
- research methodology review;
- no-lookahead audit;
- baseline model construction;
- bounded backtest design;
- EV/P&L analysis;
- robustness/drift analysis;
- runtime verification;
- code/test hardening;
- communication/receipt verification;
- repository cleanup after reference analysis.

Bad worker assignments are vague tasks such as “make the system better” without a current blocker, evidence target, or exit criterion.

## 16. Orchestrator rule before every task allocation

```text
READ CURRENT STATE
      |
      v
READ NEXT ACTION
      |
      v
READ LATEST ACTION LOG
      |
      v
READ LATEST PEER HANDOFF
      |
      v
IDENTIFY CORE-MISSION BLOCKER
      |
      v
IDENTIFY AFFECTED LAYER / CORRIDOR / GATE
      |
      v
CHECK STATIC vs RUNTIME EVIDENCE
      |
      v
ALLOCATE HIGHEST-VALUE SAFE WORK
      |
      v
WORKERS DELIBERATE
      |
      v
ORCHESTRATOR CHOOSES NEXT ACTION
```

## 17. Permanent anti-drift rules

1. Do not confuse infrastructure completion with product completion.
2. Do not confuse worker execution with XSMB model edge.
3. Do not confuse E2E PASS with data admission.
4. Do not confuse data admission with valid research.
5. Do not confuse valid research with valid backtest.
6. Do not confuse backtest profit with real edge.
7. Do not confuse edge with positive EV under realistic costs.
8. Do not confuse positive EV with robustness.
9. Do not confuse consensus with evidence.
10. Do not confuse historical evidence with fresh evidence.
11. Do not confuse service liveness with worker execution.
12. Do not use Render UI as a heavy-compute shortcut.
13. Do not delete historical evidence.
14. Do not promote because a worker or orchestrator “feels” the gate is complete.
15. Always continue from repository state, not chat memory.

## 18. Immediate orientation for the next Bot generation

Before accepting any work, the successor must:

```text
AI_START_HERE
   ↓
SYSTEM_MASTER_MAP_V1
   ↓
WORKER_DELIBERATION_PROTOCOL_V1
   ↓
FOSENNIC / FORENSIC / COMMUNICATION / EVIDENCE / ACTION contracts
   ↓
CURRENT_STATE
   ↓
NEXT_ACTION
   ↓
LATEST ACTION LOG
   ↓
LATEST PEER HANDOFF
   ↓
ONLY THEN: task-specific files/code
```

The successor must compare this map against repository reality and report discrepancies before modifying architecture.
