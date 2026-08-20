# Foundation Documentation Event — Forensic Gate Interaction + Temporal Replay

## Event type

ARCHITECTURE_DOCUMENTATION_ONLY

No operational gate was promoted and no Layer 1 unlock was performed.

## Source-derived rule

The Quant specification requires explicit separation between:

```text
CAN_I_KNOW?
CAN_I_PREDICT?
IS_THERE_EDGE?
IS_EV_POSITIVE?
WOULD_I_BET?
WHAT_ACTUALLY_HAPPENED?
```

and requires historical replay to reconstruct the information available at the historical `as_of` boundary. `FULL27(T)` and `TAIL27(T)` remain future information until prediction T is frozen. fileciteturn756file0L934-L990

## Forensic interpretation preserved for successors

There is one Forensic FSM, not multiple independent Forensic systems. Database admission gates and Quant admission gates use the same non-inheritance law:

```text
PASS(N) = reachability to N+1
PASS(N) != PASS(N+1)
```

The repository's existing canonical admission-chain document already codifies this as one FSM and explicitly requires the first FAIL/UNKNOWN to stop downstream reachability. fileciteturn757file0L2-L2

## Durable Quant rule

A backtest must not be treated as valid merely because it produces P&L. Temporal validity is a prerequisite to all later interpretation.

For target T:

```text
inputs <= T-1
prediction frozen
reveal T
score
update
advance T+1
```

A prediction with `max_input_date >= target_date` or `training_cutoff >= target_date` is `TEMPORAL_LEAKAGE` and therefore invalid regardless of ROI.

## Zero-bet rule

`BET_RATE = 0%` is a valid scientific result. It must be decomposed by gate before anyone changes a contract. No component may relax an admission rule merely to manufacture bets or improve displayed ROI.

## Implementation consequence

The temporal doctrine has been persisted in:

```text
 docs/architecture/TEMPORAL_WALK_FORWARD_REPLAY_DOCTRINE.md
```

This event does NOT change the current execution successor. The current `state/next_action.json` remains authoritative; the current action must still be completed before this Quant replay engine is promoted into implementation.

## Next-action preservation

The successor Bot must read the current `state/next_action.json` rather than inventing a new action from this documentation event.
