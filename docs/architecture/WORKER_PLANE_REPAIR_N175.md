# Worker Plane Repair — N175

## Purpose

Repair the canonical headless worker path without changing forensic promotion state.

## Repairs applied

1. `orchestration/dispatch_workers.py` now consumes `coordination/worker_allocation_v2.json`, not stale v1 allocation.
2. `orchestration/worker_reconcile.py` now treats `BOT2_QUANT`, `BOT3_EXECUTION`, and `BOT4_EXECUTION` as the default E2E worker set.
3. Reconciliation now records `workers_expected`, `workers_observed`, and `missing_workers`; a missing worker receipt forces `HOLD`.
4. Worker authority remains execution-only: canonical state mutation is forbidden and forensic promotion remains denied.

## Current allocation

`ALLOC-N175-TRIPLE-WORKER-REACTIVATION-001`

Cycle: `BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER`

The allocation requires all three workers to return fresh persistent receipts bound to the exact allocation and cycle. This is an execution completion rule, not a forensic promotion rule.

## Remaining architecture risks

- Render deployment/build failures prevent independent runtime verification for some workers.
- Existing worker implementations can still produce advisory PASS from context/allocation checks; this must not be confused with substantive S1 evidence.
- Deliberation schema/version drift remains to be repaired separately and must be versioned rather than rewriting historical records.

## Forensic status

S1 remains HOLD/DENY. No downstream gate is opened by these repairs.

## Verification requirement

A repair is complete only after the canonical dispatcher produces current-cycle outbox tasks and the reconciler observes fresh receipts from all three workers. Code existence alone is insufficient.
