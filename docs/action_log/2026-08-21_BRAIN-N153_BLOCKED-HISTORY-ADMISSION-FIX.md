# BRAIN-N153 — Blocked-history admission hardening

## Peer synchronization

Bot 2 remains at QUANT-N010. Its completion gate still requires independently observable workflow execution evidence; no Brain promotion authority is delegated to Quant.

## Blocker found

`check_gate_invariant()` previously validated only the declared dependencies. A caller could provide history containing a later FAIL/UNKNOWN/UNREACHED result while the current gate depended on an earlier PASS, and the function could still return ADMITTED.

That violates the Forensic rule that a FAIL/UNKNOWN blocks reachability and later gates remain UNREACHED. A locked/failed portion of the chain must not be bypassed by selecting an earlier PASS dependency.

## Fix

`tools/gate_invariant.py` now fails closed whenever any recorded history result is not PASS before evaluating the current gate:

`BLOCKED_HISTORY:<gate_id>:<status>`

This keeps the dependency graph local while preventing a caller from bypassing a blocked history record.

## Tests

Added regression coverage in `tests/test_gate_invariant.py` for UNKNOWN dependency/history blocking.

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
EXTERNAL_EVIDENCE = UNKNOWN
PROMOTED = NO

## Gate state

BRAIN-N125_WAIT_EXTERNAL remains unchanged.
ACTION_SPACE = 0.
PROMOTION = DENY.
ROOM_02 = LOCKED.
STAIRCASE = LOCKED.

## Core Mission link

This is a real admission-integrity blocker. Fixing it prevents false reachability claims and protects the path toward valid data/research/backtest evidence without opening any gated action.

## Own next action

Re-read peer state and latest peer work, then continue the highest-value safe Brain-side blocker audit.

## Peer required next action

Quant Bot should continue QUANT-N010 execution evidence and provide exact run/attempt/commit/result when independently observable; it should not reinterpret this Brain-side fix as Quant promotion evidence.
