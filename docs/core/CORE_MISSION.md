# XSMB FORENSIC — CORE MISSION

## Mission

The objective is **not to make the Forensic FSM look beautiful**.

The objective is to move the current system toward a real XSMB research and controlled-action system:

```text
REAL DATA
  -> VALID RESEARCH
  -> VALID BACKTEST
  -> EV / P&L
  -> ROBUSTNESS / RISK
  -> CONTROLLED ACTION
```

Every transition must have real evidence and must preserve the architecture.

## Non-negotiable invariants

- Forensic evidence is real and traceable.
- A state reflects reality; it is never painted green for convenience.
- Every gate owns its own evidence.
- PASS never transfers between gates.
- UNKNOWN is not PASS.
- DEFAULT DENY applies to unresolved admission.
- Source truth and crawler evidence have independent lineages.
- No synthetic production data.
- No lookahead bias.
- Backtests must use frozen temporal information and valid out-of-sample evaluation.
- EV/P&L must be measured, not inferred.
- If EV is negative, NaN, Inf, or required conditions are missing, `ACTION_SPACE=0`.
- Brain, Data, Quant Engine, and UI remain separate responsibilities.
- Brain is the governance/control plane, not the calculator or source-data owner.
- Render Free 512 MB is a hard resource boundary; the 320 MiB guard is mandatory.
- Credentials never enter GitHub, source-control logs, or ordinary evidence receipts.
- TLS is mandatory for durable database access.

## Correct use of FSM

The Forensic FSM is an admission/control mechanism, not the product objective.

A beautiful FSM with no real data, no valid research, no valid backtest, no measured EV/P&L, and no controlled action is an unsuccessful system.

FSM correctness exists to prevent the system from taking an invalid shortcut while progressing toward the mission.

## Priority rule for next actions

When selecting the next action, ask in this order:

1. What real capability is missing from the mission path?
2. What evidence is required to prove that capability?
3. Which repository/service owns the change?
4. Which gates must be satisfied before it can be used?
5. Can it be implemented without weakening Forensic, immutability, security, or the Render memory boundary?
6. What is the smallest verifiable increment that moves the system toward REAL DATA -> RESEARCH -> BACKTEST -> EV/P&L -> CONTROLLED ACTION?

Documentation is required when it protects architecture or enables reproducibility, but documentation itself is never treated as progress unless it accompanies a real system improvement or a required forensic record.
