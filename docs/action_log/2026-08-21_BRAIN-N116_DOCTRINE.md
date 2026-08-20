# BRAIN-N116 — Core Mission / Forensic Priority Freeze

## Decision

The system must never confuse the Forensic FSM with the Core Mission.

### Core Mission

```text
REAL DATA
 -> VALID RESEARCH
 -> VALID BACKTEST
 -> EDGE
 -> EV / P&L / ROI
 -> ROBUSTNESS / RISK / DRIFT
 -> CONTROLLED ACTION
```

### Forensic role

There is exactly ONE Forensic FSM. It controls admission between mission stages. It is not the mission itself.

## Frozen invariants

- PASS is local to its own gate.
- PASS is only a prerequisite for evaluating the next gate.
- PASS never inherits across gates.
- Every gate owns its own evidence.
- Promotion requires fresh evidence.
- UNKNOWN is not PASS.
- Default deny remains the safe state.
- Historical evidence is immutable.
- No manufactured receipt.
- No self-attestation as independent evidence.
- No synthetic production history, fake candles, future leakage, or lookahead.
- Source truth, derived data, and model output remain distinct.
- `EV < 0`, `EV = NaN`, or `EV = Inf` forces `EDGE_CANDIDATE=FALSE`, no prediction report, and `ACTION_SPACE=0`.
- Aggregate levels cannot rescue a lower-level failed/unknown evidence item.
- Backtest PASS is not Edge PASS; Edge PASS is not EV PASS; EV PASS is not P&L PASS; P&L PASS is not Promotion; Promotion is not Action.
- Brain remains governance/control plane.
- `xsmb-quant` remains source/data truth.
- `Quant_Engine` remains calculation/research.
- Render 512 MB remains a hard boundary; 320 MiB remains the conservative guard.

## Priority

Engineering priority must follow real mission progress. FSM/documentation work is supporting work unless it removes a real blocker to real data, valid research, valid backtest, Edge, EV/P&L, robustness/risk/drift, or controlled action.

## Current admission state

N116 remains `WAIT_EXTERNAL_OBSERVATION` with `ACTION_SPACE=0`.

This doctrine freeze does not unlock N116, does not manufacture external observation, and does not alter the canonical next action.

## Successor instruction

Read this file before modifying mission priorities. Read the full gate semantics and `state/next_action.json` before taking action.
