# Temporal Walk-Forward Replay Doctrine

## Status

This is a successor design doctrine captured from the Quant/Forensic specification. It does not by itself prove runtime execution. It must not be used as a substitute for exact-live evidence.

## Primary law

Backtest is not merely a P&L calculator. It must first answer:

> If the system had been alive at historical time T, with exactly the information available at that time, could it have produced a valid prediction?

Therefore the canonical causal sequence is:

```text
CAN_I_KNOW?
    -> CAN_I_PREDICT?
        -> IS_THERE_EDGE?
            -> IS_EV_POSITIVE?
                -> WOULD_I_BET?
                    -> WHAT_ACTUALLY_HAPPENED?
```

## Temporal firewall

For a target date `T`, prediction inputs are strictly bounded:

```text
available information <= T-1
prediction frozen at T-1
actual result at T remains hidden
reveal T only after prediction is immutable
score T
update model/history
advance to T+1
```

A feature, training record, model fit, normalization statistic, calibration artifact, threshold, or derived quantity that was produced using information from `T` or later is future leakage for a prediction targeting `T`.

## Walk-forward replay

Canonical loop:

```text
HISTORICAL CANONICAL DATA
          |
          v
       AS_OF T-1
          |
          v
RECONSTRUCT AVAILABLE WORLD
          |
          v
     BUILD FEATURES
          |
          v
       TRAIN <= T-1
          |
          v
       PREDICT T
          |
          v
   FREEZE PREDICTION LEDGER
          |
          v
      REVEAL RESULT T
          |
          v
        SCORE
          |
          v
   UPDATE MODEL / HISTORY
          |
          v
        T + 1
```

The replay engine must behave as though it does not know the future.

## Three evaluation layers

### A — Historical Replay

`T-1 -> Prediction(T) -> Reveal(T)`

Purpose: prove causal reconstruction and replayability.

### B — Walk-Forward OOS

```text
Train[1..T-1]
    -> Predict[T]
    -> Reveal[T]
    -> Train[1..T]
    -> Predict[T+1]
```

Purpose: evaluate Edge without allowing future training contamination.

### C — Strict Holdout

Research/development and final holdout must be separated. Once the holdout specification is frozen, the holdout results cannot be used to repeatedly tune the specification.

## Prediction ledger

Every prediction must be accompanied by a compact immutable receipt containing at least:

```text
prediction_id
target_date
as_of
min_input_date
max_input_date
training_cutoff
feature_snapshot_sha
prediction_input_sha
model_version
model_sha
prediction_sha
replay_status
```

The temporal auditor must prove:

```text
max_input_date < target_date
training_cutoff < target_date
```

Violation:

```text
TEMPORAL_LEAKAGE
    -> PREDICTION_INVALID
    -> BACKTEST_INVALID
```

ROI must not be used to rescue a temporally invalid prediction.

## XSMB-specific rule

For a prediction targeting date `T`, `FULL27(T)` is future information until the prediction is frozen. It may be revealed only after the prediction ledger is immutable.

`TAIL27(T)` is derived from `FULL27(T)` and therefore follows the same temporal barrier.

No current-day result may be allowed into a feature window for a prediction targeting that same day.

## Zero-bet doctrine

A result of zero approved bets is valid.

The system must not relax admission rules merely to produce activity or attractive ROI.

However, `BET_RATE = 0%` must be forensically decomposed by gate:

```text
ALL_DAYS
 -> DATA_VALID
 -> FEATURE_VALID
 -> HYPOTHESIS_TESTABLE
 -> EDGE_CANDIDATE
 -> EDGE_ADMITTED
 -> P_CALIBRATED
 -> EV_COMPUTABLE
 -> EV > 0
 -> BET
```

The audit must identify the first gate at which opportunities disappear.

Possible conclusions include:

- genuinely no Edge;
- Edge exists but EV is negative;
- Edge exists but evidence/calibration/OOS stability is insufficient;
- previous Edge disappeared after leakage removal;
- admission contract is incorrectly restrictive.

Only the last case justifies changing the contract, and the change itself requires forensic documentation.

## Opportunity rate vs Bet rate

Report separately:

```text
OPPORTUNITY_RATE = admitted opportunities / evaluated days
BET_RATE         = approved bets / evaluated days
```

A low or zero Bet Rate is not automatically a defect.

## Forensic interaction rule

The temporal replay chain follows the same single-FSM principle used by the database admission chain:

```text
PASS at gate N
    = permission to reach gate N+1
    != PASS at gate N+1
```

For example:

```text
DATA_VALID = PASS
    != FEATURE_VALID = PASS

FEATURE_VALID = PASS
    != EDGE = PASS

EDGE = PASS
    != EV_POSITIVE = PASS

EV_POSITIVE = PASS
    != BET = PASS
```

Every gate requires evidence belonging to that gate.

## Successor implementation mandate

Do not build a generic backtest that first loads all history, fits all features/models, and then rewinds the clock. That architecture can leak future information without an obvious `future_date` comparison.

The implementation must make the temporal boundary explicit in the API and data flow, ideally with an immutable `as_of`/`training_cutoff` context passed through every feature/model adapter.

The replay engine should be the next Quant-side architecture after the current foundation/data-admission gates are complete. It must remain separate from Brain governance and must not unlock Layer 1 merely because local replay tests pass.
