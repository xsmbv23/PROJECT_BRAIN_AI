# Worker Orchestration V1

## Purpose

Detach worker execution from ChatGPT browser sessions while preserving the Forensic Brain governance model.

The browser/chat remains a communication interface. Persistent state remains authoritative. Workers consume explicit task envelopes and emit append-only result records.

## Authority boundary

```text
BOT1 / Brain
  -> deliberation synthesis
  -> task allocation
  -> lease creation
  -> reconciliation
  -> canonical next_action

BOT2/BOT3/BOT4 workers
  -> execute allocated work
  -> produce evidence/results
  -> report PASS/FAIL/UNKNOWN/HOLD/CONFLICT
  -> propose next_action
  -> NEVER promote
  -> NEVER open a forensic gate
  -> NEVER rewrite canonical history
```

Worker execution is therefore **not** a second FSM. It is an execution layer above ONE FORENSIC FSM.

## Persistent loop

```text
state/current_state.json
        +
state/next_action.json
        +
current deliberation cycle
        |
        v
BOT1 allocation
        |
        v
worker task envelope
        |
        v
lease / claim
        |
        v
BOT2 / BOT3 / BOT4 worker
        |
        v
append-only result/evidence
        |
        v
BOT1 reconciliation
        |
        +--> CONFLICT/HOLD/ESCALATE
        |
        v
new canonical next_action
```

## Lease and race protection

A worker never directly owns `state/next_action.json`.

Each task has a unique `task_id` and `lease_id`. A worker may only mutate its branch-local task/result scope. Canonical state mutation is reserved for Bot 1 reconciliation.

A stale or duplicate lease is rejected. A worker retry creates a new attempt record rather than rewriting the previous attempt.

## Browser independence

The orchestration layer supports two execution modes:

1. `render_worker`: deterministic/runtime workers hosted on Render.
2. `external_worker`: an externally hosted worker endpoint authenticated by deployment secrets.

The orchestration layer does **not** claim that a normal ChatGPT browser session can continue reasoning after its browser is closed. That requires a real worker runtime/API. This contract is the bridge that allows those workers to be introduced without changing governance.

## Worker hierarchy

```text
BOT1 — Chief Forensic Architect
  |
  +-- BOT2 — Quant & Data Research
  |     +-- future BOT2.x workers
  |
  +-- BOT3 — Engineering & Runtime
  |     +-- future BOT3.x workers
  |
  +-- BOT4 — Independent Execution / Reality Challenge
        +-- future BOT4.x workers
```

Department workers inherit task scope, not forensic authority.

## Safety invariants

- `DELIBERATION != EVIDENCE`
- `CONSENSUS != PASS`
- `UNKNOWN != PASS`
- `WORKER_RESULT != FORENSIC_PASS`
- `BOT_ACCEPTED != PROMOTION`
- no PASS inheritance
- no canonical-state race between workers
- no credential/secrets in task/result records
- evidence references must be durable and independently observable
- historical records are append-only

## Rollout

V1 deliberately starts with orchestration primitives and deterministic worker dispatch. LLM reasoning is not silently assumed to exist in a background worker. A future LLM worker must have an explicit provider/API credential, resource budget, timeout, retry policy, and evidence contract before it is admitted.
