# BOT1 Multi-Bot Operating Model V1

Status: CANONICAL OPERATING DOCTRINE
Owner: BOT1_LEAD
Scope: BOT2 / BOT3 / BOT4 headless coordination

## 1. Purpose

This document freezes the agreed operating model for the three worker departments under BOT1. It defines how they deliberate, challenge one another, receive work, execute without collision, return evidence, and feed the next E2E action.

## 2. Authority boundary

BOT1_LEAD is the canonical allocator, synthesis authority, coordination authority, reconciliation authority, and controller of canonical next action.

BOT2 / BOT3 / BOT4 have execution responsibility and advisory/review authority only within their allocations. They do not own canonical state, cannot mutate `state/current_state.json` or `state/next_action.json`, and cannot perform forensic promotion.

Core invariants:

```text
DELIBERATION != EVIDENCE
CONSENSUS != TRUTH
CONSENSUS != FORENSIC PASS
PROPOSAL != EVIDENCE
WORKER RESULT != PROMOTION
ARBITRATION != FORENSIC AUTHORITY
UNKNOWN != PASS
MISSING EVIDENCE != PASS
CONFLICT != PASS
PASS != INHERITANCE
```

## 3. Deliberation cycle

Each substantive cycle follows:

```text
BOT1 PROPOSAL
  -> BOT2 CHALLENGE
  -> BOT3 INDEPENDENT REALITY/SOURCE REVIEW
  -> BOT4 INDEPENDENT EXECUTION/OPERATIONS REVIEW
  -> REBUTTAL / RESPONSE
  -> BOT1 SYNTHESIS
  -> ALLOCATION
  -> WORKER EXECUTION
  -> RECEIPTS
  -> RECONCILIATION
  -> LOCAL FORENSIC GATE
  -> NEXT ACTION
```

Workers must challenge rather than merely agree. Blocking challenges and minority opinions are persistent records and may not be deleted because a later consensus forms.

A consensus may select an implementation strategy, but never constitutes evidence for a forensic gate.

## 4. Worker roles

### BOT2_QUANT

Primary focus: quantitative/data/adversarial review.

Expected challenges include data gaps, statistical gaps, hidden assumptions, counterexamples, coverage errors, inconsistencies, and invalid inference.

### BOT3_REALITY

Primary focus: independent source/reality/provenance review.

Expected challenges include unsupported claims, provenance gaps, source mismatch, reproducibility problems, and assumptions that are not grounded in persistent evidence.

### BOT4_EXECUTION

Primary focus: independent execution/reality/deployment/operations review.

Expected challenges include non-runnable plans, deployment failures, runtime mismatch, stale workers, operational dead paths, and reproducibility failures.

## 5. Allocation protocol

After deliberation, BOT1 issues one canonical allocation containing at minimum:

```text
allocation_id
cycle_id
worker_id
objective
task_id
input evidence / references
required output
evidence requirements
write scope
lease / attempt
authority boundary
```

Each worker receives a disjoint write scope whenever practical. Worker output must be written to its own persistent result area. Workers must not edit canonical state directly.

A worker may not silently expand its write scope or authority.

## 6. Collision avoidance

Workers coordinate through the persistent allocation/bus, not through browser/chat sessions.

The collision-control rules are:

1. One canonical allocation per cycle.
2. Every task is bound to an exact `allocation_id`, `cycle_id`, and `task_id`.
3. Worker claims are lease-bound.
4. Worker result paths are worker-scoped.
5. Canonical state mutation is BOT1-controlled only.
6. Forensic promotion is local-gate controlled only.
7. Stale-cycle results are rejected from current-cycle reconciliation.
8. Duplicate receipts are not treated as new execution.

## 7. Rebuttal and conflict handling

A blocking disagreement is never resolved by majority vote alone.

Example:

```text
BOT2 PASS
BOT3 PASS
BOT4 BLOCKED
```

means the cycle is `HOLD` or requires a resolution allocation. It does not mean `PASS` because 2/3 agree.

Likewise:

```text
BOT2 PASS
BOT3 CONFLICT
BOT4 PASS
```

preserves BOT3's conflict and prevents silent promotion.

If a conflict remains after the configured deliberation budget, BOT1 allocates a resolution task or escalates. It does not rewrite the minority record.

## 8. Execution receipts

A worker `PASS` means only that the worker completed its assigned execution/check. It does not mean the target forensic gate passed.

Fresh receipts must identify the allocation/cycle/task and preserve:

```text
status
worker_id
allocation_id / cycle_id / task_id
evidence_refs
execution timestamp
authority boundary
canonical_mutation = FORBIDDEN
promotion = DENY
```

## 9. Reconciliation

BOT1 reconciles all worker receipts against the exact current allocation and current cycle.

BOT1 checks freshness, identity, completeness, conflicts, minority opinions, evidence references, and authority boundaries.

Only after reconciliation does BOT1 select the next action.

## 10. Autonomous continuation

When a cycle completes, BOT1 must read the canonical next action and continue without waiting for ordinary human approval.

```text
VERIFY RESULT
-> READ NEXT ACTION
-> EXECUTE
-> VERIFY
-> RECEIPT
-> RECONCILE
-> NEXT ACTION
```

If blocked:

```text
HOLD / DENY / ESCALATE
+ reason
+ evidence gap
+ persistent next action
```

The system must not stop merely because one approach failed; it should seek an alternative execution path when within BOT1 authority.

## 11. Forensic separation

Deliberation can determine *what to try*. Execution can produce evidence. Neither deliberation nor worker consensus can open a forensic gate. Each gate requires its own local evidence and its own admission conditions.

Therefore:

```text
THREE WORKERS PASS
      !=
TARGET GATE PASS
```

## 12. Canonical mental model

```text
                 BOT1_LEAD
                     |
              PROPOSAL / GOVERNANCE
                     |
       +-------------+-------------+
       |             |             |
      BOT2          BOT3          BOT4
     QUANT         REALITY        EXEC
       |             |             |
       +------ CHALLENGE ----------+
                     |
                 REBUTTAL
                     |
                 SYNTHESIS
                     |
              BOT1 ALLOCATION
                     |
       +-------------+-------------+
       |             |             |
      TASK2         TASK3         TASK4
       |             |             |
       +---------- RECEIPTS -------+
                     |
                RECONCILIATION
                     |
                LOCAL GATE
                     |
             PASS / HOLD / DENY
                     |
                 NEXT ACTION
```

This model is canonical for successor BOT1 sessions unless superseded by a later versioned doctrine.
