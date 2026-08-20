# BRAIN-N139 — Temporal Research Admission Hardening

## Peer synchronization

Before acting, Brain read the current Quant Engine `state/next_action.json`. Peer remains on `QUANT-N010`; its queued strategy is `RESEARCH_DATASET_ADMISSION`. Brain state remains `BRAIN-N125_WAIT_EXTERNAL`, `action_space=0`, `promotion=DENY`.

## Finding

The Brain-side research admission consumer checked that `contiguous=true` and `missing_days=[]` were claimed, but did not validate internal consistency between the claimed date range, actual day count, and OOS split. A claimant could therefore provide internally inconsistent temporal metadata and still reach the consumer's admission branch.

## Repair

Hardened the consumer to require:

- `required_days >= 41`;
- `required_days == train_observations + test_observations + 1`;
- valid ISO start/end dates;
- end date not before start date;
- `actual_days == inclusive calendar span`;
- existing contiguity, missing-day, no-lookahead, provenance, and 20/20 minimum checks remain mandatory.

Added regression tests for OOS-threshold inconsistency, date-span mismatch, and reversed ranges.

## Commits

- validator: `e4d766ea7f726a3f4859272ab53a7cb7da1c9e5c`
- tests: `432ead9568feb4cc7725a0d42710245f221f6849`

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO

No test execution or external runtime claim is made here.

## Peer handoff

Quant Engine must continue `QUANT-N010` and its research-admission work. Its admission implementation computes temporal gaps from actual `DayRecord` dates; Brain will consume only an exact receipt and validate it independently. If the peer receipt adds a stronger date-manifest/hash evidence field, Brain should adopt it rather than weakening this consumer boundary.

## Next action

Read the newest Quant Engine implementation and action log before further mutation. If its receipt semantics are weaker than this consumer contract, record an explicit objection/handoff and require stronger evidence. Otherwise continue with the highest-value safe blocker on REAL DATA -> RESEARCH -> BACKTEST without unlocking the external Brain gate.
