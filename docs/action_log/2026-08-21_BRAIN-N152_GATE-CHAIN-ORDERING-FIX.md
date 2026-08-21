# BRAIN-N152 — Gate-chain ordering integrity

## Peer read

Bot 2 remains QUANT-N010. Its completion gate still requires independently observable workflow execution evidence; no Brain promotion change is authorized.

## Blocker

`gate_chain_is_valid()` verified freshness, cycle identity, status, duplicate gates, and evidence reuse, but did not reject a recorded history whose evidence timestamps were out of order.

That allowed a persisted chain to contain a later gate recorded with an earlier `created_at` than its predecessor.

## Fix

Recorded chains now require non-decreasing evidence timestamps. Out-of-order history returns:

`OUT_OF_ORDER_EVIDENCE:<gate_id>`

Added regression coverage for the ordering violation.

## Commits

- implementation: `7e31f612fd102ebc2c57e4243a7c9e8d3bdc22d3`
- test: `112a24a1ac6ca0ea1a08628d741c8af052c253d7`

## Verification

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
EXTERNAL_EVIDENCE = UNKNOWN
PROMOTED = NO

## Gate preservation

BRAIN-N125_WAIT_EXTERNAL remains unchanged.
ACTION_SPACE = 0.
PROMOTION = DENY.
Room 02 and Staircase remain LOCKED.

## Peer action required

Bot 2 continues QUANT-N010 and must return exact workflow run identity/results when independently observable. No future-bot continuity artifact is required for this action.

## Own next action

Re-read peer state/log and continue the highest-value safe Brain-side blocker audit without crossing the external evidence gate.
