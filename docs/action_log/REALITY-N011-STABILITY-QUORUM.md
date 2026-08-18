# REALITY-N011-STABILITY-QUORUM

## Current disposition

`WAIT_EXTERNAL_EVENT` / `ACTIVE_HOLD`.

This is a valid terminal state for the current phase. It is not an idle state and it is not a failure.

## Mandatory rule

If `REAL_GITHUB_WORKFLOW_DISPATCH` has not occurred and no fresh runtime receipt exists, the correct action is **NO-OP**.

The system MUST NOT manufacture, simulate, infer, replay, or substitute the missing external event.

## Frozen forensic semantics

```text
ONE_FORENSIC_FSM
PASS_IS_LOCAL_TO_GATE
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
FAIL_IS_EVIDENCE
RETRY_IS_A_NEW_EVENT
NO_HISTORICAL_RECEIPT_OVERWRITE
LOCAL_PASS != RENDER_PASS
DATABASE_EXISTS != SERVICE_BOUND
SERVICE_BOUND != TLS_ADMITTED
TLS_ADMITTED != DURABLE_ROUND_TRIP
DURABLE_ROUND_TRIP != PROMOTION
```

## Required external event

```text
.github/workflows/reality_n011_runtime_receipt.yml
trigger = workflow_dispatch
runtime_identity = github_actions
source = https://ketqua16.net/
```

The missing event must be a real GitHub Actions runtime execution with a fresh receipt anchored to its actual commit/run identity.

## Forbidden while blocked

- HTML parsing
- 27-field extraction
- normalization
- domain mapping
- canonical schema changes
- business-date inference
- cross-source merge
- domain truth claims
- browser observation used as a substitute for Actions runtime evidence
- self-triggering merely to bypass the external-event boundary
- cosmetic hardening performed only because the system is waiting
- inventing external events
- alternate paths around a blocked transition
- reusing historical receipts as current evidence
- inheriting PASS from another gate or another run

## Layer state

```text
FOUNDATION = preserved
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

## Successor instruction

The next Bot MUST first check `state/next_action.json` and this action log. If the required external event is still absent, it MUST perform NO-OP and preserve the exact state. Only a fresh real external receipt may justify a new transition.
