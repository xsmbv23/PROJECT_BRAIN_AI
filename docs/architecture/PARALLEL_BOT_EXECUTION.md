# Parallel Bot Execution Contract

## Purpose

Multiple AI/Bot workers may operate concurrently. Concurrency must never create a second Forensic state machine and must never allow one worker to self-promote another worker's evidence.

## Canonical model

```text
                         ONE FORENSIC FSM
                               |
              +----------------+----------------+
              |                                 |
        BRAIN FOUNDATION                   QUANT ENGINE
        governance/control                calculation/engine
              |                                 |
        exact-current gates              local prerequisites
              |                                 |
        promotion authority               candidate evidence
              |                                 |
              +------------ NO PASS INHERITANCE -+
```

## Parallel work rule

A worker may proceed in parallel only when its work is a **non-dependent local prerequisite** and does not unlock a Brain gate.

Allowed:

- repository-local validation
- deterministic unit tests
- schema/contract validation
- static analysis
- memory-budget checks
- documentation and successor handoff records
- Quant Engine local workflow verification when explicitly marked `LOCAL_PREREQUISITE_ONLY`

Not allowed to be promoted by parallel work:

- exact-current Render runtime state
- independently observed external execution
- production database admission
- Forensic promotion
- Layer 1 unlock
- staircase unlock

## Evidence ownership

Every gate owns its own evidence.

```text
PASS(A) != PASS(B)
PASS(A) -> prerequisite_for(B)
PASS(A) -X-> PASS(B)
```

A parallel worker may emit evidence, but the receiving gate must classify it by scope. Repository execution evidence cannot become exact-current external runtime evidence merely because it is green.

## Current hard boundary

The current state has:

- `action_space = 0`
- `promotion = DENY`
- `next_action = BRAIN-N125_WAIT_EXTERNAL`
- `parallel_safe_engineering = QUANT-N007`

Therefore this contract explicitly forbids a parallel worker from changing Brain promotion state while the Brain gate is waiting for independent exact-current CI/runtime observation.

## Successor instruction

When a later Bot starts, it must read:

1. `state/current_state.json`
2. `state/next_action.json`
3. this contract
4. the latest action receipt/log

Then it must continue from the recorded successor action. It must not infer that a previous Bot's green local tests equal an external production receipt.

## Forensic invariant

> Parallelism may increase throughput; it may never increase authority.
