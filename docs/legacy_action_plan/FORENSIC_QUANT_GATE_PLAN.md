# Forensic Quant Gate Plan — Preserved Roadmap

This document preserves the supplied Quant/XSMB gate plan as a successor-readable roadmap. It does **not** override the current canonical runtime state.

## Non-negotiable architecture

- Brain AI is the governance/control plane and holds authority.
- Quant Engine is execution/calculation infrastructure and must never bypass Brain room locks.
- Chat is communication only; persistent state and action history live in repositories/evidence.
- PASS is local to its gate. PASS never inherits to another gate.
- UNKNOWN is not PASS.
- DEFAULT DENY.
- Implemented is not admitted; admitted is not executable.
- No credentials in GitHub or forensic evidence.
- Render Free 512 MB / 1 CPU is a hard boundary; retain the 320 MiB guard.
- Do not alter signal logic merely to manufacture a positive result.
- Every completed action must update durable state and a successor-readable action log before promotion.

## Proposed work sequence

### P0 — State Integrity Reconciliation

Reconcile Brain authority and Quant Engine state. Quant Engine must reject execution when Brain says a room is locked or when the state/evidence cycle does not match.

### P1 — Canonical Input Boundary

Remove unsafe implicit sorting from the canonical time-index contract. Room 02 must accept only an explicit `ADMITTED_INPUT_ENVELOPE` produced by the upstream admission gate.

### P2 — Feature Semantics and Calibration Repair

Repair feature semantics, including `_imbalance()`. Remove constant/dummy outputs. Add calibration (Isotonic or Platt) and multiple-testing correction. Calibration is a downstream statistical gate, not permission to change source truth.

### P3–P6 — EV Engine Guard

Hard deny any EV calculation when EV is negative, NaN, Inf, or Unknown. Never coerce invalid values to zero or a positive score. The EV gate is downstream of valid admitted inputs.

For the supplied XSMB example only, the stated arithmetic is:

`EV = P(hit) × payout - cost`

with cost 27,000 VND and payout 99,000 VND, giving a nominal break-even probability of approximately 27.27%. Any statistical claim above that threshold must be supported by the actual calibration/evidence protocol; it must not be inferred from the threshold alone.

### P7–P8 — Prediction Receipt and Daily Audit

Freeze prediction receipt before 18:15, hash it, and make the receipt immutable. Daily audit must report N predictions, K hits, exact hit/miss pairs, total stake, payout, net P/L, realized ROI, pair-level EV, edge source, and explicit EV-denied pairs.

## Interaction with current foundation

The current canonical state is already in `ROOM_01_DATA_ADMISSION` and currently has `BRAIN-N101_ORIGIN_METADATA_PROBE` as the next action. Therefore this roadmap must not cause a jump directly to Room 02 or statistical signal work.

Correct execution order is:

`current data-admission foundation → origin proof → durable evidence → promotion → P0/P1 boundary work → P2 statistical repair → P3–P6 EV guard → P7–P8 receipts/reporting → only then higher research rooms`

## Forensic gate rule

No downstream roadmap item may be marked PASS merely because an upstream item is PASS. Each gate requires fresh evidence, its own cycle identity, and its own admission receipt.
