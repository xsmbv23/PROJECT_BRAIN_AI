# BRAIN-N118 — Proactive Cross-Repository Audit

## Pre-action evidence read

- Canonical policy: `contracts/dual_bot_coordination_v1.json`
- Brain current state: `state/current_state.json`
- Brain next action: `state/next_action.json`
- Other-bot current state: `xsmbv23/Quant_Engine/state/current_state.json`
- Other-bot latest observed handoff: Quant Engine `QUANT-N007`, commit `e0d6dcab2aac37d97dd23fc8b663e1a5e114c811`
- Brain parallel continuation boundary: `docs/action_log/2026-08-21_BRAIN-N117_PARALLEL_COORDINATION.md`

## Current authority

Brain remains:

```text
ACTION_RECEIPT_NOT_YET_PROVEN_CURRENT
ACTION_SPACE = 0
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

This audit does not alter that authority.

## Cross-repository observation

### Project_Brain_AI

Current exact runtime anchor in canonical state:

```text
commit  = e23a5baa645753306a1a829a2ffcf72015a8f07c
deploy  = dep-da38hngu01pc73854hh0
instance = srv-da0506u1egvs73ftsdng-7wgsv
```

Runtime tests are recorded as 209 PASS; DB binding, TLS, network-origin proof and DB round-trip are PASS locally to their respective gates. The action receipt remains NOT_YET_PROVEN_CURRENT.

### Quant_Engine

Other bot currently projects:

```text
action = QUANT-N006
next   = QUANT-N007
room   = ROOM_01_INPUT_ADAPTER
compute_surface = LOCKED
promotion = DENY
```

Its latest handoff explicitly requires observation of N006 CI evidence and source-specific semantic extraction contracts for `ketqua16.net` and `xsmb.com.vn`. The Quant Engine state also records Render service `quant-engine` as LIVE with an observed memory footprint of 28,221,440 bytes against the 320 MiB engineering guard.

## Finding 1 — historical exact-runtime primitive must not be confused with current authority

`contracts/exact_runtime_execution_primitive_v1.json` still describes an older runtime anchor:

```text
required_runtime_commit = 2d4415a875df3582aa26df4598f4f409c3c23027
required_deployment     = dep-da2tjk7qj5pc738ht64g
```

The contract itself is historical evidence of an earlier exact-runtime execution primitive. Current canonical state points to a different runtime commit/deployment and N116 explicitly forbids using stale runtime evidence as current evidence.

### Decision

Do NOT overwrite or delete the historical contract. Do NOT relabel it as current without evidence. The correct engineering action is to make the lifecycle distinction explicit in a future contract-registry/historical-contract index, preserving immutable history.

Verification level: FOUND

No promotion effect.

## Finding 2 — Bot 2 has a valid independent workstream

The other bot is not idle. Its current N007 scope is materially connected to Core Mission:

```text
REAL SOURCE
 -> source-specific semantic extraction
 -> validated 27-value domain
 -> semantic fingerprint
 -> two-source quorum
 -> canonical admission
```

Therefore Bot 1 must not duplicate or mutate Quant Engine implementation. Bot 1's immediate dependency is to ensure the governance side has an explicit, auditable handoff boundary for the semantic evidence that Quant Engine will produce.

Verification level: FOUND

## Finding 3 — current dual-bot contract is directionally correct

The coordination contract already requires every action to read canonical policy, own state, the other bot's latest log, relevant contracts and evidence state; it also requires declaration of the other bot's required next action and own next action.

No change to the coordination contract is required in this audit.

## Selected safe blocker

The highest-value safe blocker in Bot 1's domain is **contract lifecycle ambiguity between historical exact-runtime primitives and current runtime authority**. This can cause a future bot to select stale runtime identity as if it were current evidence.

## Repair plan

Create a machine-readable historical/current contract index without changing the historical contract or current FSM state. The index must classify contracts as:

- CURRENT_AUTHORITY
- HISTORICAL_EVIDENCE
- SUPERSEDED
- PROPOSAL
- UNKNOWN

and require an exact runtime anchor before any contract can be treated as current runtime evidence.

## Bot 2 handoff

Bot 2 must continue `QUANT-N007` and, before its next action, read this log. It should:

1. observe the latest CI evidence for N006;
2. inspect/define source-specific semantic parser contracts for both real sources;
3. preserve raw bytes and raw SHA-256 independently of semantic hashes;
4. keep canonical promotion denied;
5. report whether any parser/domain defect is a real blocker to Core Mission progress.

Bot 2 must not treat its local PASS/CI evidence as a Brain admission PASS.

## Bot 1 next action

`BRAIN-N119_CONTRACT_LIFECYCLE_INDEX`

Build the historical/current contract index described above, then re-audit for stale runtime references and cross-repo authority ambiguity.

## Completion gate

N118 is complete at FOUND level. No gated authority changed. The next safe action is contract-lifecycle hardening only.
