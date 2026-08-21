# BRAIN-N147 — Gate-chain record integrity hardening

## Peer synchronization

Bot 2 remains on QUANT-N010. Its completion gate is independent workflow execution evidence; Brain remains BRAIN-N125_WAIT_EXTERNAL with promotion DENY. No Brain gate is opened by this action.

## Active blocker found

`tools/gate_invariant.py::gate_chain_is_valid()` previously checked uniqueness/status/hash reuse but did not enforce the same freshness and cycle-integrity invariants used by live admission.

That created a semantic split:

- live gate admission rejected stale or cross-cycle evidence;
- recorded-chain validation could still report `CHAIN_RECORD_VALID` for stale or cross-cycle history.

A forensic system must not have two meanings of "valid chain".

## Change

`gate_chain_is_valid()` now rejects:

- invalid TTL;
- missing evidence identity;
- missing cycle identity;
- invalid status;
- evidence reuse;
- duplicate gate IDs;
- cross-cycle results;
- future-dated evidence;
- stale evidence outside the same TTL boundary used by live admission.

It deliberately does not invent dependency semantics because it receives `GateResult` values, not `GateDefinition` objects. Dependency admission remains the responsibility of `check_gate_invariant()` / `GateRunner`.

## Commit

`b217635b86cbb33a5c4e5466637bf028afc25801`

## Evidence status

IMPLEMENTED=YES
TESTED=UNKNOWN
RUNTIME_VERIFIED=UNKNOWN
PROMOTED=NO

No gate or promotion state was changed.
