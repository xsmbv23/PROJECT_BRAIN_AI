# BRAIN-N119 — Contract Lifecycle Index

## Mandatory pre-action reads

Read before action:

- `contracts/dual_bot_coordination_v1.json`
- `state/current_state.json`
- `state/next_action.json`
- latest available Quant Engine state/log evidence
- `docs/action_log/2026-08-21_BRAIN-N118_PROACTIVE_CROSS_REPO_AUDIT.md`
- `contracts/exact_runtime_execution_primitive_v1.json`
- `contracts/contract_lifecycle_index_v1.json`

## Current state

Canonical gated runtime authority remains:

```text
ACTION_RECEIPT_NOT_YET_PROVEN_CURRENT
ACTION_SPACE = 0
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

This action is parallel-safe foundation engineering. It does not request or grant runtime action admission.

## Objective

Prevent historical runtime contracts from being mistaken for exact-current runtime evidence while preserving immutable history.

## Finding

`contracts/exact_runtime_execution_primitive_v1.json` binds an earlier runtime commit/deployment. The canonical current runtime anchor is different. Therefore the older contract is historical evidence, not current runtime authority.

The contract is intentionally preserved unchanged. The lifecycle classification is maintained separately in `contracts/contract_lifecycle_index_v1.json`.

## Repair

Created `contracts/contract_lifecycle_index_v1.json` with explicit classifications:

```text
CURRENT_AUTHORITY
HISTORICAL_EVIDENCE
SUPERSEDED
PROPOSAL
UNKNOWN
```

Current-runtime evidence now has an explicit required tuple:

```text
exact current runtime identity
+ exact runtime commit
+ exact deployment identity
+ fresh evidence
+ own-gate admission
```

Historical evidence remains immutable and cannot become current merely by reference.

## Verification level

`FIXED` for the contract-lifecycle ambiguity.

`RUNTIME_VERIFIED = NOT APPLICABLE` to this documentation-only repair.

No promotion effect.

## Bot 2 coordination

Quant Engine remains an independent workstream. Its canonical state is still Room 01, compute locked, promotion DENY, next action `QUANT-N007`, with CI observation and source-specific semantic extraction as its current dependency. Bot 2 must read this log before its next action and must not inherit any PASS from Brain.

## Unresolved blockers

1. Exact-current independent `/governance` observation remains unavailable; this continues to block Runtime Action Admission.
2. Render workspace monitoring cannot be performed from this session until a Render workspace is selected; this is an infrastructure/tooling boundary, not evidence of service failure.
3. Quant Engine CI/source semantic extraction remains pending in Bot 2's workstream.

## Own next action

`BRAIN-N120_GOVERNANCE_EVIDENCE_CONTRACT_AUDIT`

Audit the governance/evidence contracts for three failure modes:

1. stale runtime identity,
2. evidence freshness ambiguity,
3. self-attestation paths that could masquerade as independent observation.

The audit must produce only safe contract/code changes that do not manufacture external evidence or alter the frozen action gate.

## Other bot required next action

`QUANT-N007`

Continue CI observation and source-specific semantic extraction for `ketqua16.net` and `xsmb.com.vn`; preserve raw-byte receipts separately from semantic hashes; keep canonical admission and Room 02 locked.

## Completion gate

N119 is complete at `FIXED` level for contract lifecycle ambiguity. The next safe parallel action is N120. Canonical runtime action authority remains unchanged.
