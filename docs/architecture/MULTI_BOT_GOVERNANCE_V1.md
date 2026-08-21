# Multi-Bot Governance V1

## Purpose

Run Bot 2 and Bot 3 in parallel while keeping one governance authority and one end-to-end mission state.

## Roles

| Role | Authority | Primary responsibility | May mutate | May promote |
|---|---|---|---|---|
| Bot 1 | Governance / Lead | architecture, forensic review, blocker selection, E2E coordination, challenge | Brain governance repo/state | Yes, only when gate evidence satisfies contract |
| Bot 2 | Quant / Research | data/quant/research/backtest implementation and evidence | Quant repo and owned runtime | No |
| Bot 3 | Execution / Runtime | implementation, tests, CI, Render/runtime integration | Execution-owned repo/runtime | No |

## Authority boundaries

1. Chat is communication only. Persistent state, contracts, receipts and evidence are authoritative.
2. Bot 2 and Bot 3 may execute safe local actions without waiting for Bot 1.
3. Bot 1 is required for governance mutations, gate changes, promotion, or any action that crosses an ownership boundary.
4. A green test suite, deployment, workflow, or implementation result never becomes a governance PASS by itself.
5. UNKNOWN is not PASS. UNREACHED is not PASS. PASS never inherits downstream.
6. Parallel work must not create shared mutation ownership.

## E2E requirement

Every action must declare its E2E segment and downstream impact.

Core mission:

`REAL_DATA -> VALID_RESEARCH -> VALID_BACKTEST -> EDGE -> EV_P&L&ROI -> ROBUSTNESS_RISK_DRIFT -> CONTROLLED_ACTION`

An action is not considered complete merely because a file changed. It is complete only when its local exit evidence exists and the next E2E state is explicitly recorded.

## Handoff protocol

Every Bot 2 or Bot 3 handoff must persist:

- `owner`
- `action_id`
- `e2e_segment`
- `blocker`
- `action`
- `evidence_refs`
- `result`
- `next_action`
- `peer_impact`
- `challenge_status`

Allowed `challenge_status` values:

- `ACK`
- `AGREE`
- `CHALLENGE`
- `UNKNOWN`
- `BLOCKED`

## Bot 1 review protocol

For every material peer handoff Bot 1 records one of:

- ACK: evidence and scope are accepted locally.
- AGREE: position is consistent with current contract.
- CHALLENGE: a concrete contradiction, missing evidence, or unsafe assumption exists.
- UNKNOWN: evidence is insufficient to agree or challenge.
- BLOCKED: action cannot safely continue until a stated dependency is satisfied.

A peer acknowledgement is coordination evidence only; it is never gate evidence.

## Bottleneck prevention

Bot 1 must not become a serial approval queue.

Safe local work continues in parallel. Bot 1 review is mandatory only for:

- governance state changes;
- admission/promotion decisions;
- cross-repo ownership changes;
- unsafe or ambiguous mutations;
- evidence that can unlock a downstream gate.

## Race handling

When two Bots mutate related state concurrently:

1. Never force-overwrite an unknown newer version.
2. Read the latest persistent version.
3. Compare action lineage and successor pointers.
4. Reconcile forward from the newer valid state.
5. Persist a reason-coded reconciliation event.

## Promotion rule

Only the exact gate-local evidence contract can open a gate. Bot 1 is the final governance authority, but it may not manufacture evidence or infer PASS from implementation, tests, runtime liveness, or peer agreement.
