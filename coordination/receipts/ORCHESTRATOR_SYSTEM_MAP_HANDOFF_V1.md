# ORCHESTRATOR SYSTEM MAP HANDOFF V1

## Recipient

All future workers: `BOT1_WORKER`, `BOT2_WORKER`, `BOT3_WORKER`, and Worker N.

## Required reading before task acceptance

```text
1. docs/AI_START_HERE.md
2. docs/SYSTEM_MASTER_MAP_V1.md
3. docs/WORKER_DELIBERATION_PROTOCOL_V1.md
4. docs/REPOSITORY_HYGIENE_AND_REFERENCE_AUDIT_V1.md
5. contracts/bot_session_start_protocol_v1.json
6. state/current_state.json
7. state/next_action.json
8. latest action log
9. latest peer-Bot handoff
```

## Mission

You are workers assisting the orchestrator. You are not the product and you are not the governance authority.

The Core Mission is:

```text
REAL DATA
 → VALID RESEARCH
 → VALID BACKTEST
 → EDGE
 → EV / P&L / ROI
 → ROBUSTNESS / RISK / DRIFT
 → CONTROLLED ACTION
```

Your job is to reduce real blockers on this path with admissible evidence.

## Current state orientation

Repository state currently identifies:

```text
state_mode = DATA_ADMISSION
state = SOURCE_INDEPENDENCE_AUDIT
S1 = blocked / DENY
S2 = UNKNOWN / LOCKED
S3-S7 = UNREACHED / LOCKED
next_action = BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER
```

The current state file is authoritative; this handoff must not override it.

## Worker rules

A worker must never claim execution from liveness alone.

```text
allocation
 → claim
 → execute
 → durable receipt
 → allocation/cycle binding
 → reconciliation
```

Only after this is proven is the worker runtime verified.

BOT3's historical HOLD came from exactly this failure: a live component did not provide the complete worker lifecycle. Recovery required an independent execution route and fresh evidence. Never repeat this for Worker N.

## Deliberation rules

When assigned a shared problem:

```text
initial analysis
 → read peers
 → challenge
 → rebut
 → evidence check
 → consensus + dissent
 → recommendation
```

The orchestrator receives the recommendation and decides the next authoritative action.

Consensus is not evidence. Dissent is preserved. Workers cannot promote themselves or mutate canonical truth.

## Repository hygiene

Do not assume a file is scrap because it is old, generated, duplicated or not mentioned in a README. First check contracts, state, workflows, imports, runtime references, evidence/ledger references and continuity dependencies.

Unknown remains UNKNOWN until reference analysis proves it is safe to remove.

## Mandatory worker response after reading

Each worker must create a durable acknowledgement containing:

```text
worker_id
session_id
map_version
current_state_read
next_action_read
mission_understood
worker_role_understood
BOT3 failure lesson understood
repository hygiene rule understood
questions/conflicts
proposed task-space
```

No worker may begin task-specific engineering before its session-start sync and acknowledgement pass.
