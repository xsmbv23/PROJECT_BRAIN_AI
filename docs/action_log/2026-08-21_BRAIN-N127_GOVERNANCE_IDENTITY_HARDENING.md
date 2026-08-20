# BRAIN-N127 — Governance Deployment Identity Hardening

## BOT_ID
BOT_1

## REPOSITORY
xsmbv23/Project_Brain_AI

## PRE-ACTION READS
- `contracts/dual_bot_coordination_v1.json` — read before action; mandatory policy requires other-bot latest log before next action.
- `state/current_state.json` — current canonical state remains `CI_OBSERVATION_UNKNOWN_CURRENT`, `ACTION_SPACE=0`, `MANDATORY_NO_OP`, `PROMOTION=DENY`.
- `contracts/governance_observation_admission_v1.json` — exact-current binding requires repository, commit, deployment, and instance as distinct fields.
- `Quant_Engine/docs/action_log/2026-08-21_QUANT-N006.md` — latest observable Bot 2 log at decision time; no newer N007 log was observable through the connector.

## CORE MISSION
REAL_DATA -> VALID_RESEARCH -> VALID_BACKTEST -> EDGE -> EV/P&L/ROI -> ROBUSTNESS/RISK/DRIFT -> CONTROLLED_ACTION

## OBJECTIVE
Continue proactive safe engineering in Bot 1 ownership while the runtime admission gate remains locked.

## OBSERVED BLOCKER
`brain/server.py` exposed deployment identity using a fallback from `RENDER_DEPLOY_ID` to `RENDER_INSTANCE_ID`. The governance admission contract requires `deployment` and `instance` to be separately verifiable runtime-identity fields. Treating instance identity as deployment identity weakens exact-current binding and can make an observation structurally ambiguous.

## SELECTED BLOCKER / WHY
High-value safe blocker at the governance observation boundary. Fixing the identity semantics improves the ability of an independent observer to bind an exact-current response without asserting that the gate has passed.

## ACTION TAKEN
Updated `_deployment_identity()` so `deployment` is populated only from `RENDER_DEPLOY_ID`. If that variable is unavailable, deployment remains `UNKNOWN` rather than silently substituting an instance identifier. `RENDER_INSTANCE_ID` remains independently exposed as `instance`.

Commit: `db0c89f30283d7197827ecf43c1c8f8d7e5b0861`

## VERIFICATION LEVEL
FIXED

No CI or external runtime evidence was observed through this action. The change is therefore not marked TESTED, RUNTIME_VERIFIED, EXTERNAL_EVIDENCE, or PROMOTED.

## UNRESOLVED BLOCKERS
- Exact-current external `/governance` observation remains absent.
- CI execution evidence remains UNKNOWN.
- Runtime must prove both deployment and instance identities on the exact-current deployment.
- Bot 2's semantic extraction work remains independent and must not inherit PASS from this change.

## OTHER BOT REQUIRED NEXT ACTION
BOT_2 must read this log and the shared coordination policy before its next action. Continue source-specific semantic extraction for `ketqua16.net` and `xsmb.com.vn`, keeping canonical 27-value semantics separate from raw artifacts and without changing source truth or promotion state.

## BOT 1 NEXT ACTION
Observe or audit the next available exact-current CI/runtime evidence for the governance boundary. If evidence remains unavailable, continue safe governance/security/architecture audit rather than self-attesting verification.

## DEPENDENCY
External CI/runtime observation is required to move this change beyond FIXED. It is not required for further independent safe engineering.

## FORBIDDEN
- No self-call claimed as independent observation.
- No fabricated receipt.
- No canonical state unlock.
- No Room 02/staircase unlock.
- No PASS inheritance.
- No secrets in GitHub or logs.
