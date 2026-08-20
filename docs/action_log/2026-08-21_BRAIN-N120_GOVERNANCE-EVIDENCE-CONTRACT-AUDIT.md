# BRAIN-N120 — Governance Evidence Contract Audit

## Mandatory pre-action reads

Read:

- `contracts/dual_bot_coordination_v1.json`
- `state/current_state.json`
- `state/next_action.json`
- latest available Quant Engine state/action evidence
- `docs/action_log/2026-08-21_BRAIN-N119_CONTRACT-LIFECYCLE-INDEX.md`
- `contracts/exact_runtime_execution_primitive_v1.json`
- `contracts/contract_lifecycle_index_v1.json`

## Current authority

```text
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

N120 is parallel-safe contract engineering and does not alter Runtime Action Admission.

## Objective

Eliminate ambiguity around what can count as the independent exact-current `/governance` observation required by the frozen runtime gate.

## Findings

1. The exact-runtime primitive correctly rejects local curl, local execution, proxy execution, historical receipts and synthetic receipts, but its runtime identity is tied to a historical deployment.
2. Canonical state currently requires an independent exact-current `/governance` observation and explicitly rejects self-generated evidence.
3. Human input may carry evidence but cannot grant PASS or state authority.
4. Startup logs alone are not equivalent to an independently observable HTTP receipt.

## Repair

Created:

`contracts/governance_observation_admission_v1.json`

The contract now explicitly requires:

```text
EXTERNAL OBSERVER
+ /governance
+ exact current repository/commit/deployment/instance
+ fresh timestamp
+ nonce or unique request identity
+ observable receipt
+ verifiable provenance
```

and explicitly rejects:

```text
Brain self-call
Brain-generated receipt claimed as external
startup-log substitution
historical receipt
unverifiable screenshot
human assertion of PASS
chat request as authority
```

The contract defines evidence requirements only. It cannot grant action_space or promotion.

## Verification level

`FIXED` — governance evidence ambiguity is now explicitly contracted.

`RUNTIME_VERIFIED` — NOT CLAIMED.

`EXTERNAL_EVIDENCE` — NOT PRESENT.

No gate was opened.

## Bot 2 handoff

Bot 2 remains responsible for `QUANT-N007`: CI observation plus source-specific semantic extraction for `ketqua16.net` and `xsmb.com.vn`. It must read this log before its next action, keep raw-byte and semantic hashes distinct, and preserve canonical promotion DENY.

## Unresolved blockers

- Independent exact-current `/governance` observation is still absent.
- Render monitoring remains unavailable in this session until a workspace is selected; no inference about service health is made from that tooling limitation.
- Quant Engine semantic extraction/CI evidence remains pending.

## Own next action

`BRAIN-N121_CROSS_REPO_ADMISSION_CONTRACT_AUDIT`

Audit the Brain/Data/Quant cross-repository contracts for directionality violations, implicit trust edges, and any path where derived data or local computation could silently become source truth or governance authority.

## Completion gate

N120 complete at `FIXED` level when the new contract is recorded and no runtime gate is changed. N121 is the next parallel-safe action.
