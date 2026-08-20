# CORE MISSION FREEZE — 2026-08-16

## Purpose

The system's objective is now explicitly frozen as a **real system progression**, not FSM aesthetics.

```text
REAL DATA
  -> VALID RESEARCH
  -> VALID BACKTEST
  -> EV / P&L
  -> ROBUSTNESS / RISK
  -> CONTROLLED ACTION
```

## Important distinction

The Forensic FSM is an admission/control mechanism. It exists to prevent invalid transitions and preserve evidence. It is not the product objective.

Therefore:

```text
FSM PASS != SYSTEM SUCCESS
DOCUMENTATION != SYSTEM PROGRESS
HEALTHY RUNTIME != VALID QUANT RESULT
DB ACCESS != DATA TRUTH
DATA INGEST != VALID RESEARCH
BACKTEST != PROFIT
POSITIVE EV CLAIM != CONTROLLED ACTION
```

Every stage must produce its own evidence.

## Current state impact

No admission state is changed by this document.

The official current next action remains:

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
```

The repository's existing Forensic doctrine already establishes that there is exactly one Forensic FSM and that PASS is local to the gate that earned it. This mission document adds the priority rule for selecting work: prefer changes that move the actual system toward real data, valid research/backtest, EV/P&L, robustness/risk, and controlled action.

## Decision rule for future work

For every candidate change:

1. Identify the missing capability on the mission path.
2. Identify its owner repository/service.
3. Define its evidence.
4. Define its admission gates.
5. Verify security, immutability, architecture, and 320 MiB Render guard.
6. Implement the smallest real increment.
7. Measure it.
8. Record evidence.
9. Do not promote merely because another gate is green.
