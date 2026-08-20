# BACKTEST ADMISSION DOCTRINE — Canonical Forensic Contract

## Status

PERMANENT FOUNDATION CONTRACT.

This document freezes the Backtest semantics for successor Bots. It is part of the ONE Forensic FSM and does not create a second Forensic universe.

## Core temporal law

For a prediction made for result day `T`, the model may use only information that was actually available at `T-1` or earlier.

```text
AVAILABLE INFORMATION <= T-1
        |
        v
MODEL FREEZE
        |
        v
PREDICTION FREEZE
        |
        v
PREDICTION RECEIPT
        |
        v
RESULT T
        |
        v
SETTLE
        |
        v
RECORD
        |
        v
OOS / ROBUSTNESS / DRIFT / MULTIPLE TESTING / COST / PAYOUT / P&L / ROI
```

The result for `T` must never participate in constructing the prediction for `T`.

No future leakage, lookahead, synthetic historical data, or retroactive feature repair is permitted.

## Prediction receipt invariant

A prediction is not forensic evidence until its immutable Prediction Receipt exists.

The canonical timing rule is:

```text
Prediction Receipt SHA-256 MUST EXIST BEFORE 18:15 FOR RESULT DAY T
```

If the receipt is missing, late, unverifiable, replayed, or inconsistent with the prediction payload:

```text
FORENSIC PREDICTION = INVALID
P&L / ROI FORENSIC VERDICT = DENY
```

A verifier must never manufacture the receipt it is trying to verify.

## Source and lineage law

The following categories are distinct and must never be silently collapsed:

```text
SOURCE_TRUTH
DERIVED_DATA
HYPOTHESIS
EVIDENCE
EDGE
```

Historical Backtest input must originate from real source truth. Synthetic historical data is forbidden in production.

A crawler cannot silently repair Human Reference data. Human Reference cannot silently repair crawler evidence. Conflicts remain conflicts until independently investigated.

## Hypothesis / Edge semantics

```text
HYPOTHESIS != EVIDENCE
EVIDENCE   != EDGE
```

Also:

```text
NO_EDGE    != NOT_PROVEN
```

`NO_EDGE` means the evidence supports rejection of an edge claim. `NOT_PROVEN` means the evidence is insufficient to establish the claim. Successor Bots must not convert either state into the other merely for reporting convenience.

## EV hard-deny law

`EV < 0`, `UNKNOWN`, `NaN`, and `Inf` are hard-deny conditions at every aggregation level.

```text
Pair
  -> Set
  -> Strategy
  -> Day
  -> Portfolio
```

A denied lower-level value may not be promoted upward to rescue an aggregate result.

Required semantics by layer:

```text
DATA LEVEL
  domain/cardinality violation -> HARD_DENY

RESEARCH LEVEL
  EV < 0 / NaN / Inf / UNKNOWN -> EDGE_CANDIDATE = FALSE

REPORTING LEVEL
  EV < 0 / NaN / Inf / UNKNOWN -> warning only; no prediction report

ACTION LEVEL
  EV < 0 / NaN / Inf / UNKNOWN -> ACTION_SPACE = 0
```

## Backtest evaluation law

Backtest evaluation is not hit-rate alone. A valid forensic evaluation must preserve separate gates for:

```text
OOS
ROBUSTNESS
STABILITY / DRIFT
MULTIPLE TESTING
COST
PAYOUT
P&L
ROI
```

A good result on one dataset does not automatically prove Edge.

## No automatic promotion

These are distinct states:

```text
BACKTEST_PASS
    != EDGE_PASS
    != EV_PASS
    != P&L_PASS
    != PROMOTION
    != ACTION
```

A PASS from one gate is local to that gate. It may only unlock evaluation of the next gate; it cannot donate its PASS to the next gate.

## Parameters deliberately NOT canonical yet

The following values have not been supplied as canonical project invariants and therefore must not be invented by successor Bots:

- train/test split percentage
- exact walk-forward window
- OOS minimum sample size
- minimum overall sample size
- overlap rule
- transaction cost
- slippage
- confidence interval
- drawdown threshold
- robustness threshold
- P&L threshold
- promotion threshold

Bots may propose these as research hypotheses, but may not silently promote them into project policy.

## Successor rule

Before implementing or modifying any Backtest, successor Bots must read:

1. `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`
2. `state/next_action.json`
3. this document

The governing sentence is:

> Backtest must recreate the information boundary that existed at each historical prediction time; prediction must be frozen before result; immutable prediction evidence must exist before the deadline; and Edge, EV, OOS, P&L, promotion, and action are separate forensic gates.

This contract is immutable in meaning. Improvements may add stricter evidence, but may not weaken these invariants.
