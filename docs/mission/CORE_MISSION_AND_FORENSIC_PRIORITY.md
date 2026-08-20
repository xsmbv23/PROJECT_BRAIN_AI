# CORE MISSION + FORENSIC CONTROL DOCTRINE

## Status

Permanent successor-facing doctrine. This document defines **what the system is trying to achieve** and **how Forensic controls the route**.

## 1. Core mission

The Core Mission is the objective, not the Forensic FSM itself:

```text
REAL DATA
  -> VALID RESEARCH
  -> VALID BACKTEST
  -> EDGE
  -> EV / P&L / ROI
  -> ROBUSTNESS / RISK / DRIFT
  -> CONTROLLED ACTION
```

Every engineering decision must be judged against one question:

> Does this move the system materially closer to real XSMB data, valid research, valid backtest, measurable Edge, EV/P&L, robustness/risk, and ultimately controlled action?

Forensic work exists to make each transition valid. Documentation, contracts, FSM refinement, and action logs are supporting work unless they remove a real blocker on that path.

## 2. One Forensic FSM

There is exactly **ONE Forensic FSM**.

Database admission, runtime action admission, source admission, research admission, and promotion are gate chains inside that FSM. They are not independent permission universes.

The immutable semantics are:

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
```

A PASS at Gate A only permits evaluation of Gate B. It never donates PASS to Gate B.

## 3. Forensic evidence

Every material conclusion requires evidence that is traceable to source, time, runtime/commit, and the relevant context.

Rules:

- no evidence -> no conclusion;
- absence of an observed error is not evidence of success;
- historical evidence is immutable;
- a stale receipt cannot prove a current observation;
- no manufactured receipts;
- no self-attestation presented as independent evidence;
- mutation requires lineage and evidence;
- canonical state must not be changed merely because a conversation wants progress.

## 4. Data truth boundary

```text
SOURCE TRUTH != DERIVED DATA != MODEL OUTPUT
```

Production forbids synthetic historical data, fake candles, future data, lookahead, future leakage, and unlabelled mixing of source and derived data.

Invalid domain/cardinality/schema evidence is HARD DENY.

Human Reference and crawler output are separate evidence lineages. Neither may silently repair the other.

## 5. Research/backtest admission

The minimum temporal discipline is:

```text
T-1 INFORMATION SET
  -> MODEL FREEZE
  -> PREDICTION FREEZE
  -> SHA256 RECEIPT
  -> RESULT T
  -> SETTLE
  -> RECORD
  -> OOS
  -> ROBUSTNESS
  -> DRIFT
  -> MULTIPLE TESTING
  -> COST / PAYOUT
  -> P&L / ROI
```

Prediction must be frozen before the result is known.

`BACKTEST_PASS`, `EDGE_PASS`, `EV_PASS`, `P&L_PASS`, `PROMOTION`, and `ACTION` are distinct gates. A good backtest does not authorize action.

Thresholds such as sample-size rules, split percentages, walk-forward windows, slippage, confidence intervals, and drawdown thresholds are not canonical until explicitly admitted.

## 6. EV < 0 cross-level invariant

Negative, NaN, or infinite EV is not merely a reporting issue.

```text
EV < 0 / NaN / Inf
  -> EDGE_CANDIDATE = FALSE
  -> no prediction report
  -> ACTION_SPACE = 0
```

This invariant applies across aggregation levels. A parent aggregate may not use valid siblings to rescue a child evidence item that is `UNKNOWN`, `NaN`, `Inf`, or `EV < 0`.

No aggregate may silently convert a failed or unknown lower-level evidence item into PASS.

## 7. P&L is a real outcome gate

P&L/ROI evaluation must include payout, cost, risk/drawdown, robustness, drift, OOS behavior, and multiple-testing effects. A visually attractive metric is not sufficient evidence of an edge.

## 8. Architecture boundary

```text
Project_Brain_AI = Governance / Forensic Control
xsmb-quant       = Source / Data Truth
Quant_Engine     = Calculation / Research
```

Forbidden architectural transfers:

```text
Brain -> Data Engine authority
Brain -> Quant Engine authority
Quant Engine -> mutate Source Truth
Data -> self-grant Brain admission
```

Brain controls admission/governance. It is not the source-data authority and not the calculation engine.

## 9. Resource/security boundary

Render Free's 512 MB is a hard boundary. The 320 MiB guard is conservative policy. Large datasets must not be loaded into the Brain runtime.

Secrets must never be committed to GitHub. Database access must not be fabricated, mocked as a substitute for real round-trip evidence, or made insecure by disabling TLS.

## 10. Action boundary

When required evidence is absent or unknown:

```text
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
```

This is a valid controlled state, not an error to be bypassed.

## 11. Work-priority rule

Priority order:

```text
REAL DATA
  -> DATA VALIDATION
  -> RESEARCH
  -> VALID BACKTEST
  -> EDGE
  -> EV
  -> P&L / ROI
  -> ROBUSTNESS / RISK / DRIFT
  -> CONTROLLED ACTION
```

Forensic controls intervene to prevent invalid transitions.

A task is **material progress** if it:

- admits real data;
- strengthens data admission;
- enables valid research;
- enables lineage-preserving backtest;
- measures Edge/EV/P&L;
- tests robustness/risk/drift;
- enables controlled action;
- or removes a concrete blocker to one of those outcomes.

Otherwise it is supporting work and must not consume priority merely because it makes the FSM more elaborate.

## 12. Successor rule

A future Bot must read this document, `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`, and `state/next_action.json` before acting.

The permanent principle is:

> **The Core Mission is to move from real data to valid research/backtest, measurable EV/P&L, robustness/risk, and controlled action. Forensic is the control mechanism that guarantees every transition is evidenced and valid. A PASS belongs only to the gate that earned it.**
