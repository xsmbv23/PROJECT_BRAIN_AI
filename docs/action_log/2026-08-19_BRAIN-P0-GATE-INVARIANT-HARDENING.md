# BRAIN-P0 — State Integrity / PASS-Local Gate Hardening

## Decision

The database admission chain is one Forensic FSM, not multiple independent Forensic states.
Each gate owns its own evidence. A PASS is local to that gate and is only a prerequisite for reaching dependent gates.

## Machine invariants

```text
PASS_IS_LOCAL_TO_GATE       = true
PASS_IS_PREREQUISITE_ONLY   = true
NO_PASS_INHERITANCE         = true
IMPLEMENTED != ADMITTED     = true
ADMITTED != EXECUTABLE      = true
UNKNOWN_IS_NOT_PASS         = true
DEFAULT_DENY                = true
EVIDENCE_MUST_BE_FRESH      = true
EVIDENCE_TTL                = 300 seconds
EVIDENCE_UNIQUE_PER_GATE    = true
CYCLE_ID_REQUIRED           = true
DIRECT_EVALUATE              = FORBIDDEN
AUTHORIZED_RUNNER            = GateRunner.run_gate
```

## Gate chain

```text
DB_EXISTENCE
   ↓ prerequisite only
DB_BINDING
   ↓ prerequisite only
DB_TLS_ADMISSION
   ↓ prerequisite only
DB_ROUND_TRIP
   ↓ prerequisite only
PROMOTION
```

Round-trip itself is:

```text
WRITE → READ → REHASH → MATCH
```

No predecessor evidence hash may be reused as proof for a successor gate.

## Implementation

Added:

- `tools/gate_invariant.py`
- `tools/gate_runner.py`
- `tools/verify_gate_invariant.py`
- `tests/test_gate_invariant.py`
- `contracts/forensic_gate_invariant_v1.json`

Integrated `tools/verify_gate_invariant.py` into `tools/runtime_boot_gate.py`.

## Security boundary

The direct-call bypass identified during design is explicitly denied by the contract. Gate implementations use `_evaluate`; admission is performed by `GateRunner.run_gate`.

Evidence is bound to a reconciliation `cycle_id` and has a finite TTL. Stale, missing, duplicate, or mismatched evidence is not promoted to PASS.

## Architectural consequence

The old wording “two forensic states” is retired. The canonical term is:

`FORENSIC DATABASE ADMISSION CHAIN`

It is a single state machine containing multiple local gates.

## Current status

```text
P0 invariant contract       = IMPLEMENTED
P0 boot enforcement         = IMPLEMENTED
Layer 1                     = LOCKED
Staircase                   = LOCKED
Promotion                   = DENY
Network origin proof        = NOT_PROVEN
Database round-trip         = NOT_PROVEN
```

## Successor handoff

After P0, resume the already-authorized next action:

`BRAIN-N101_ORIGIN_METADATA_PROBE`

N101 must remain metadata-only, bounded, non-secret, and must not reinterpret redirect identity or hostname difference as canonicality/independence proof.
