# BRAIN-N111 — Epistemic Separation + Prediction Lineage Contract

## Purpose

Freeze the distinction between what the system **knows as evidence**, what it
**currently projects as state**, what it **remembers as history**, what it
**believes as hypothesis**, and what it **must obey as doctrine**.

## Machine contract

`core/epistemic_contract.py` defines:

- DOCTRINE — invariant rule; never evidence
- EVIDENCE — concrete receipt/artifact; only admissible evidence type
- STATE — mutable projection; never evidence
- HISTORY — immutable action record; never evidence
- HYPOTHESIS — testable proposition; never evidence without a fresh evidence gate

`validate_evidence_claim()` hard-denies every non-EVIDENCE category.

## Gate semantics

A gate PASS is local:

```text
PASS(G1) != PASS(G2)
PASS(G2) != PROMOTION
```

PASS only makes the next gate eligible for evaluation. Every gate must own
fresh evidence. UNKNOWN is not PASS. DEFAULT DENY remains active.

## Prediction lineage

Frozen chain:

```text
PREDICTION_ID
   ↓
FEATURE_SNAPSHOT_SHA
   ↓
CANONICAL_SHA
   ↓
RAW_RECEIPT_SHA
```

A missing or malformed link returns:

```text
PREDICTION_STATUS = NOT_PROVEN
EXECUTION = CANCEL
```

The lineage validator never creates missing hashes and never mutates evidence.

## Temporal invariant

Prediction features are causal and must use only data available through T-1;
no result-of-T or future timestamp may enter the prediction feature snapshot.
The prediction receipt is frozen before result reveal.

## Architectural boundary

Brain remains the governance control plane. Quant Engine remains the execution
and calculation plane. Chat remains communication only. This action does not
open Layer 1 or the staircase.

## Next action

`BRAIN-N112` — integrate the epistemic and lineage validators into the exact
runtime admission gate, while preserving the current deployment as the sole
runtime authority and keeping source promotion denied until exact-live transport
evidence is independently proven.
