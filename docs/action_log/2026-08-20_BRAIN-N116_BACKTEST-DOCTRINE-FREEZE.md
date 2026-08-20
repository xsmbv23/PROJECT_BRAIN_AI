# BRAIN-N116 — Backtest Doctrine Freeze

## Scope

A permanent Backtest admission contract was added to the Forensic foundation. This action does not unlock runtime action admission, Room 02, or the staircase.

## Frozen invariants

1. Prediction for result day `T` uses only information available at or before `T-1`.
2. Model and prediction are frozen before result `T` is known.
3. Prediction Receipt SHA-256 must exist before 18:15 for `T`.
4. Missing/late/replayed/unverifiable receipt invalidates the forensic prediction and corresponding P&L/ROI verdict.
5. Historical source truth is mandatory; synthetic historical data is forbidden.
6. Source truth, derived data, hypothesis, evidence, and edge remain distinct classes.
7. `HYPOTHESIS != EVIDENCE`, `EVIDENCE != EDGE`, and `NO_EDGE != NOT_PROVEN`.
8. EV `< 0`, `UNKNOWN`, `NaN`, and `Inf` hard-deny at Pair, Set, Strategy, Day, and Portfolio levels.
9. Backtest evaluation includes OOS, robustness, stability/drift, multiple testing, cost, payout, P&L, and ROI; hit-rate alone is insufficient.
10. `BACKTEST_PASS != EDGE_PASS != EV_PASS != P&L_PASS != PROMOTION != ACTION`.
11. Noncanonical thresholds must not be invented by successor Bots.

## Immutable architecture rule

There remains exactly ONE Forensic FSM. The Backtest doctrine is a gate contract inside that FSM, not a second Forensic system.

## Files

- `docs/forensic/BACKTEST_ADMISSION_DOCTRINE.md`
- `docs/forensic/BACKTEST_ADMISSION_DOCTRINE.json`

## Promotion effect

```text
ACTION_SPACE = 0
PROMOTION = DENY
ROOM_01 = ACTIVE
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

## Successor instruction

A successor Bot must read the Backtest doctrine before implementing any historical replay, feature generation, prediction, Edge, EV, P&L, ROI, or promotion logic. No local PASS may be inherited by another gate.
