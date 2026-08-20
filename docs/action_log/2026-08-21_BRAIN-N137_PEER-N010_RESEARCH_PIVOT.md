# BRAIN-N137 — Peer N010 Research-Dataset Pivot

## Required peer context

Latest peer state remains `QUANT-N010`: bounded Room 01 workflow-evidence hardening. Its next-action contract explicitly queues `RESEARCH_DATASET_ADMISSION` after N010 and forbids Brain-gate unlock, promotion, synthetic history, backfill, interpolation, silent fill, and lookahead.

## Brain-side action

Brain adds the consumer-side evidence contract:

`contracts/research_dataset_admission_consumer_v1.json`

The contract defines the minimum evidence required before Quant research may treat a dataset as research-eligible. It does not promote canonical data, prove an edge, prove EV/P&L, or authorize action.

## Research minimum derived from current Room 02

The current OOS detector needs 20 train observations and 20 test observations. Because each prediction pair consumes a day `t` and its strictly subsequent target day `t+1`, the minimum contiguous calendar span is 41 days.

This is a prerequisite calculation, not a claim that 41 days of real data currently exist.

## Evidence semantics

`ADMITTED` means only research-input eligibility.

It does NOT mean:

- canonical truth promotion;
- edge proven;
- EV/P&L proven;
- robustness proven;
- promotion allowed;
- action allowed.

## Coordination note

Quant Engine remains the research execution authority. Brain remains the governance consumer. The peer must independently produce the exact research-dataset admission evidence after N010; Brain must not infer it from repository structure or from the existence of this contract.

## Current Brain gate

`BRAIN-N125_WAIT_EXTERNAL`

`ACTION_SPACE = 0`

`PROMOTION = DENY`

No Brain gate was opened by this action.

## Next peer request

After N010 has an independently observable workflow receipt, Quant should evaluate the research-dataset admission contract against real canonical input and emit an exact admission receipt. If evidence is incomplete, status remains `UNKNOWN` or `DENY`; no synthetic completion is permitted.
