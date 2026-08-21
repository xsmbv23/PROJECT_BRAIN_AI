# BRAIN-N174 — Multi-Bot Governance Rollout

## Decision

Adopt the three-bot operating model:

- Bot 1 = Lead / governance / forensic reviewer / E2E orchestrator
- Bot 2 = Quant / data / research / backtest worker
- Bot 3 = Execution / runtime / implementation worker

## Rollout evidence

- Multi-Bot Governance V1 contract added.
- Machine-readable handoff schema added.
- Fail-closed handoff validator added.
- Regression tests added for owner, segment, evidence, and challenge status.
- Bot 3 onboarding contract added.

## E2E state

Current gate remains:

`S1_REAL_DATA = BLOCKED`

`S2_VALID_RESEARCH = LOCKED`

`S3..S7 = UNREACHED/LOCKED`

`PROMOTION = DENY`

This rollout changes execution topology only. It does not promote any gate and does not weaken forensic admission requirements.

## Operating rule

Parallelism is the default for safe local work. Governance is centralized at Bot 1. Shared-state mutations remain ownership-scoped and version-aware.
