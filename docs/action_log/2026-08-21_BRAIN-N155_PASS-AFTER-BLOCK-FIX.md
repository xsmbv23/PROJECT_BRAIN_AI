# BRAIN-N155 — Blocked-chain resume integrity fix

## Session type

Safe Brain-side blocker audit while `BRAIN-N125_WAIT_EXTERNAL` remains authoritative.

## Peer read

Bot 1 read the latest Brain state and the Quant-N010 action/state before acting. Quant-N010 remains a local prerequisite only; independent CI evidence is still not observable. The Quant state explicitly keeps Brain as transition authority and its own state as a read-only projection.

## Blocker found

The recorded-chain validator enforced uniqueness, freshness, cycle consistency, and ordering, but it did not explicitly reject a later `PASS` after an earlier `FAIL`, `UNKNOWN`, or `UNREACHED` result in the same recorded chain.

That creates an admission-integrity ambiguity: a blocked chain could appear to resume without a fresh reconciliation boundary.

## Fix

`tools/gate_invariant.py` now tracks `blocked_seen` during `gate_chain_is_valid()`.

Once a non-PASS result appears, a later PASS is rejected as:

`PASS_AFTER_BLOCK:<gate_id>`

The rule is deliberately local to the recorded chain and does not alter promotion authority.

## Test status

The corresponding test update was attempted, but the test file changed concurrently and the repository rejected the stale SHA update. Therefore **TESTED = UNKNOWN** for this specific new rule until the current test file is re-read and the test is successfully persisted/executed.

No claim of test PASS is made.

## Gate state

```text
BRAIN-N125_WAIT_EXTERNAL = UNCHANGED
ACTION_SPACE = 0
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

## Peer coordination

Decision: `AGREE` with Quant-N010's separation of repository workflow evidence from external runtime truth.

Peer next action: continue N010 only with independently observable workflow evidence; do not self-attest CI.

## Own next action

Re-read the concurrently changing gate tests and persist a matching test for `PASS_AFTER_BLOCK` only when the current file version can be updated safely. Then continue blocker-first audit without touching promotion or Layer 1.

## Verification level

`FIXED` for source code.
`TESTED = UNKNOWN`.
`RUNTIME_VERIFIED = UNKNOWN`.
`EXTERNAL_EVIDENCE = UNKNOWN`.
`PROMOTED = NO`.
