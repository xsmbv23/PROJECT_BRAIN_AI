# BRAIN-N156 — End-to-End next-action binding

## Finding

The previous `state/next_action.json` represented the immediate safe step, but did not explicitly bind that step to the full Core Mission path. That creates a risk of locally correct work becoming an orphaned task.

## Fix

`state/next_action.json` now contains an explicit `core_mission_e2e` map:

`S1 REAL_DATA -> S2 VALID_RESEARCH -> S3 VALID_BACKTEST -> S4 EDGE -> S5 EV_PNL_ROI -> S6 ROBUSTNESS_RISK_DRIFT -> S7 CONTROLLED_ACTION`

Each segment has an owner, exit evidence, blocked downstream segments, and dependency semantics.

The next-action format now requires:

- `e2e_segment`
- `blocker`
- `immediate_action`
- `required_evidence`
- `exit_criteria`
- `downstream_impact`
- `peer_required_action`
- `safe_parallel_work`

## Rule

An immediate next action is a step inside the E2E Core Mission plan, never an orphan task. A local PASS never authorizes a downstream segment. Downstream work may be prepared safely, but PASS must be earned independently at each gate/segment.

## Current position

Current E2E segment: `S2_VALID_RESEARCH`.

Current parallel work: `QUANT-N010` workflow-evidence hardening.

Brain gate remains `BRAIN-N125_WAIT_EXTERNAL`, `ACTION_SPACE=0`, `PROMOTION=DENY`.

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO
