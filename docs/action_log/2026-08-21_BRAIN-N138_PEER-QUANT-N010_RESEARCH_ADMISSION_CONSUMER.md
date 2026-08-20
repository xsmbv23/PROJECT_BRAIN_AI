# BRAIN-N138 — Peer QUANT-N010 research-admission consumer boundary

## Pre-action peer read

Read `Quant_Engine/state/next_action.json` before acting. Peer remains QUANT-N010 and explicitly queues `RESEARCH_DATASET_ADMISSION` after workflow evidence. The peer scope requires real-source-only data, no synthetic history, no lookahead, no PASS inheritance, Room 02 and promotion locked.

## Finding

The Quant Engine already has a research-dataset admission primitive, but Brain needs an independent consumer-side validator so a future research-admission receipt cannot silently become canonical truth, edge proof, EV/P&L proof, or action authorization.

## Action

Added `tools/research_dataset_admission_validator.py` and corresponding tests.

The consumer requires dataset identity, provenance, canonical input reference, dates, coverage, contiguity, train/test counts, temporal policy, and code version. It denies gaps, insufficient history, invalid temporal policy, and missing fields.

A valid receipt is explicitly scoped to:

`RESEARCH_ELIGIBILITY_ONLY`

and returns:

- canonical promotion = NOT_PROVEN
- edge = NOT_PROVEN
- EV/P&L = NOT_PROVEN
- action = NOT_AUTHORIZED

## Verification status

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
EXTERNAL_OBSERVATION = UNKNOWN
PROMOTED = NO

No gate was unlocked and no Brain state was promoted.

## Peer handoff

Quant Engine must provide an exact research-admission receipt once its own N010/workflow dependency permits the pivot. Brain will validate that receipt independently. A valid receipt only permits consideration by research; it does not establish canonical promotion, edge, EV/P&L, robustness, or action.
